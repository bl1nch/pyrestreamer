function hide_show_transcode() {
    var param = document.getElementById('stream_type').value;
    if (param == 'transcode') {
        document.getElementById("a_transcode").hidden = false;
        document.getElementById("v_transcode").hidden = false;
    }
    else {
        document.getElementById("a_transcode").hidden = true;
        document.getElementById("v_transcode").hidden = true;
    }
}

function create_stream(url) {
    var text = "?";
    var param = "";
    param = document.getElementById('stream_name').value;
    if (param)
        text += ("name=" + param + "&");
    param = document.getElementById('stream_resource').value;
    if (param)
        text += ("resource=" + param + "&");
    param = document.getElementById('stream_protocol').value;
    if (param)
        text += ("protocol=" + param + "&");
    param = document.getElementById('stream_ip').value;
    if (param)
        text += ("ip=" + param + "&");
    param = document.getElementById('stream_port').value;
    if (param)
        text += ("port=" + param + "&");
    param = document.getElementById('stream_type').value;
    if (param)
        text += ("stream_type=" + param + "&");

    param = document.getElementById('stream_file_caching').value;
    if (param)
        text += ("file_caching=" + param + "&");
    param = document.getElementById('stream_miface').value;
    if (param)
        text += ("multicast_output_interface=" + param + "&");
    param = document.getElementById('stream_loop').value;
    if (param)
        text += ("loop=" + param + "&");
    param = document.getElementById('stream_audio_track').value;
    if (param)
        text += ("audio_track=" + param + "&");
    param = document.getElementById('stream_mux').value;
    if (param)
        text += ("mux=" + param + "&");
    param = document.getElementById('stream_logo_file').value;
    if (param)
        text += ("logo_file=" + param + "&");
    if (document.getElementById('stream_type').value == 'transcode') {
    param = document.getElementById('stream_audio_rate').value;
    if (param)
        text += ("audio_rate=" + param + "&");
    param = document.getElementById('stream_audio_codec').value;
    if (param)
        text += ("audio_codec=" + param + "&");
    param = document.getElementById('stream_audio_channels').value;
    if (param)
        text += ("audio_channels=" + param + "&");
    param = document.getElementById('stream_audio_samplerate').value;
    if (param)
        text += ("audio_sample_rate=" + param + "&");
    param = document.getElementById('stream_subtitles_codec').value;
    if (param)
        text += ("subtitles_codec=" + param + "&");
    param = document.getElementById('stream_subtitles_filter').value;
    if (param)
        text += ("subtitles_filter=" + param + "&");
    param = document.getElementById('stream_video_rate').value;
    if (param)
        text += ("video_rate=" + param + "&");
    param = document.getElementById('stream_video_codec').value;
    if (param)
        text += ("video_codec=" + param + "&");
    param = document.getElementById('stream_width').value;
    if (param)
        text += ("width=" + param + "&");
    param = document.getElementById('stream_height').value;
    if (param)
        text += ("height=" + param + "&");
    param = document.getElementById('stream_scale').value;
    if (param)
        text += ("scale=" + param + "&");
    }
    if (text != "?")
        text = text.slice(0, -1);
    else
        text = "";
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", url + text, false );
    xmlHttp.onload = () => {
        if (xmlHttp.status == 200) {
            var obj = JSON.parse(xmlHttp.responseText);
            if (obj.done){
                window.location.replace("/");
            }
            else {
                alert(obj.info);
            }
        }
        else
            alert("Error. Please check your input");
    };
    xmlHttp.send( null );
}