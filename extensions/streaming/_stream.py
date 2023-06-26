from extensions.streaming._stream_pool import StreamPool
from vlc import Instance, VideoLogoOption, EventType, callbackmethod
from socket import gethostbyname
from threading import Thread
from gevent import sleep
import urllib.parse
import logging
import platform
import subprocess
import gc


class Stream:
    # stream name
    __name = ""
    # input parameters
    __resource = ""
    # output parameters
    __protocol = "http"
    __ip = "127.0.0.1"
    __port = 0
    # stream_type
    __stream_type = "standard"
    # vlc instance parameters
    __file_caching = 1000
    __m_iface = ""
    __loop = False
    __audio_track = 1
    # transcode stream type parameters
    __video_rate = 5000
    __video_codec = "mp2v"
    __width = 0
    __height = 0
    __scale = 0
    __audio_rate = 96
    __audio_codec = "mpga"
    __audio_channels = 2
    __audio_sample_rate = 44100
    __subtitles_codec = ""
    __subtitles_filter = ""
    # all stream types parameters
    __mux = "ts"
    # logo
    __logo_file = ""

    def __init__(self,
                 name, resource, protocol, ip, port, stream_type,
                 file_caching=1000, multicast_output_interface="", loop=True, audio_track=1,
                 video_rate=500, video_codec="mp2v", width=0, height=0, scale=0,
                 audio_rate=96, audio_codec="mpga", audio_channels=2, audio_sample_rate=44100,
                 subtitles_codec="", subtitles_filter="",
                 mux="ts", logo_file=""):

        self.__name = name
        self.__resource = resource
        self.__protocol = protocol
        self.__ip = ip
        self.__port = port
        self.__stream_type = stream_type
        self.__file_caching, self.__m_iface = file_caching, multicast_output_interface
        self.__loop, self.__audio_track = loop, audio_track
        self.__video_rate, self.__video_codec = video_rate, video_codec
        self.__width, self.__height, self.__scale = width, height, scale
        self.__audio_rate, self.__audio_codec = audio_rate, audio_codec
        self.__audio_channels, self.__audio_sample_rate = audio_channels, audio_sample_rate
        self.__subtitles_codec, self.__subtitles_filter = subtitles_codec, subtitles_filter
        self.__mux, self.__logo_file = mux, logo_file
        self.__restart_thread = None
        self.__active = True

        self.__vlc_instance_parameters = [
            '--quiet' if StreamPool.quiet() else None,
            '--file-caching=' + str(self.__file_caching),
            '--audio-track=' + str(self.__audio_track),
            '--miface=' + self.__m_iface if self.__m_iface != '' else None,
            '--no-video' if self.__stream_type == 'test' else None
        ]
        self.__vlc_instance = Instance(' '.join(filter(None, self.__vlc_instance_parameters)))
        self.__player = self.__vlc_instance.media_player_new()

        if self.__logo_file != '':
            self.__player.video_set_logo_int(VideoLogoOption.logo_enable, 1)
            self.__player.video_set_logo_string(VideoLogoOption.logo_file, self.__logo_file)

        if self.__stream_type == 'transcode':
            transcode_parameters = [
                'vcodec=' + self.__video_codec,
                'vb=' + str(self.__video_rate),
                'width=' + str(self.__width) if self.__width > 0 else None,
                'height=' + str(self.__height) if self.__height > 0 else None,
                'scale=' + str(self.__scale) if self.__scale > 0 else None,
                'acodec=' + self.__audio_codec,
                'ab=' + str(self.__audio_rate),
                'channels=' + str(self.__audio_channels),
                'samplerate=' + str(self.__audio_sample_rate),
                'scodec=' + self.__subtitles_codec if self.__subtitles_codec != '' else None,
                'sfilter=' + self.__subtitles_filter if self.__subtitles_filter != '' else None
            ]
            transcode = '{' + ','.join(filter(None, transcode_parameters)) + '}'

            if self.__protocol == 'http':
                address = ',dst=' + self.__ip + ':' + str(self.__port)
            else:
                address = ',dst=' + self.__ip + ',port=' + str(self.__port)

            out_name = f',name="{self.__name}"' if self.__name != '' else ''

            self.__sout = 'sout=#transcode' + transcode + ':' + self.__protocol + \
                          '{mux=' + self.__mux + address + ',sdp' + out_name + ',ttl=2}'

        elif self.__stream_type == 'standard':
            standard_parameters = [
                'access=' + self.__protocol,
                'mux=' + self.__mux,
                'dst=' + (self.__ip + ':' + str(self.__port) if self.__protocol == 'http' else self.__ip),
                'port=' + str(self.__port) if self.__protocol != 'http' else None,
                'name=' + self.__name if self.__name else ''
            ]
            standard = '{' + ','.join(filter(None, standard_parameters)) + '}'

            self.__sout = 'sout=#standard' + standard

        else:
            self.__sout = ''

    def __thread_tester(self, lock):
        with lock:
            if self.__active:
                tester = Stream("_", self.get_address(), 'none', 'test', 0, 'test', loop=False)
                tester.start()
                sleep(5)
                online = tester.online()
                tester.stop()
                if not online and self.__active:
                    self.restart()
                tester.release()

    def start_test(self, lock):
        if self.__loop:
            self.__restart_thread = Thread(target=self.__thread_tester, args=(lock, ), daemon=True)
            self.__restart_thread.start()

    @property
    def active(self):
        return self.__active

    @active.setter
    def active(self, value):
        self.__active = value

    @property
    def restart_thread_alive(self):
        if self.__restart_thread:
            return self.__restart_thread.is_alive()
        else:
            return None

    def get_name(self):
        return self.__name

    def get_resource(self):
        return self.__resource

    def get_address(self):
        return f'{self.__protocol + "://" + self.__ip + ":" + str(self.__port)}'

    def get_type(self):
        return self.__stream_type

    def get_info(self):
        data = {
            "name": self.__name, "resource": self.__resource,
            "protocol": self.__protocol, "ip": self.__ip, "port": self.__port,
            "stream_type": self.__stream_type,
            "file_caching": self.__file_caching, "multicast_output_interface": self.__m_iface,
            "loop": self.__loop, "audio_track": self.__audio_track,
            "mux": self.__mux, "logo_file": self.__logo_file
        }
        data.update({
                "video_rate": self.__video_rate, "video_codec": self.__video_codec,
                "width": self.__width, "height": self.__height, "scale": self.__scale,
                "audio_rate": self.__audio_rate, "audio_codec": self.__audio_codec,
                "audio_channels": self.__audio_channels, "audio_sample_rate": self.__audio_sample_rate,
                "subtitles_codec": self.__subtitles_codec, "subtitles_filter": self.__subtitles_filter,
            } if self.__stream_type == 'transcode' else {})
        return data

    def get_db_info(self):
        data = {
            "name": self.__name, "resource": self.__resource,
            "protocol": self.__protocol, "ip": self.__ip, "port": self.__port,
            "stream_type": self.__stream_type,
            "file_caching": self.__file_caching, "multicast_output_interface": self.__m_iface,
            "video_rate": self.__video_rate, "video_codec": self.__video_codec,
            "width": self.__width, "height": self.__height, "scale": self.__scale,
            "audio_rate": self.__audio_rate, "audio_codec": self.__audio_codec,
            "audio_channels": self.__audio_channels, "audio_sample_rate": self.__audio_sample_rate,
            "subtitles_codec": self.__subtitles_codec, "subtitles_filter": self.__subtitles_filter,
            "loop": self.__loop, "audio_track": self.__audio_track,
            "mux": self.__mux, "logo_file": self.__logo_file
        }
        return data

    def start(self):
        if not self.__player.is_playing():
            self.__player.set_media(self.__vlc_instance.media_new(self.__resource, self.__sout))
            self.__player.play()
            logging.warning(f'Start restream from {self.__resource} to {self.get_address()}')
            return True
        else:
            return False

    def stop(self):
        if self.__player.is_playing():
            self.__player.stop()
            logging.warning(f'Stop stream on {self.get_address()}')
            return True
        else:
            return False

    def release(self):
        self.__active = False
        self.__player.release()

    def recreate(self):
        if self.__player.is_playing():
            self.__player.stop()
        self.__player.release()
        self.__vlc_instance = Instance(' '.join(filter(None, self.__vlc_instance_parameters)))
        self.__player = self.__vlc_instance.media_player_new()
        if self.__logo_file != '':
            self.__player.video_set_logo_int(VideoLogoOption.logo_enable, 1)
            self.__player.video_set_logo_string(VideoLogoOption.logo_file, self.__logo_file)
        gc.collect()
    
    def restart(self):
        if self.__player.is_playing():
            self.__player.stop()
        if not self.__player.is_playing():
            self.__player.set_media(self.__vlc_instance.media_new(self.__resource, self.__sout))
            self.__player.play()
            logging.warning(f'Restart restream from {self.__resource} to {self.get_address()}')

    def ping(self):
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '1', gethostbyname(str(urllib.parse.urlparse(self.__resource).netloc.split(':')[0]))]
        return subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) == 0

    def online(self):
        playing = self.__player.is_playing()
        if not playing:
            logging.warning(f'Stream down detected on {self.get_address()}')
        return playing
