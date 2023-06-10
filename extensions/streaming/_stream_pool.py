from extensions.singleton import Singleton


class StreamPool(metaclass=Singleton):
    __quiet = False
    __address = ''

    def __init__(self, address, scheduler, quiet=False):
        self.__class__.__address = address
        self.__class__.__quiet = quiet
        self.__data = {}

        @scheduler.task('cron', id='scheduler_1', day='*', hour=1)
        def scheduled_restarter():
            self.restart()

        @scheduler.task('cron', id='scheduler_12', day='*', hour=12)
        def scheduled_restarter():
            self.restart()

    @classmethod
    def address(cls):
        return cls.__address

    @classmethod
    def quiet(cls):
        return cls.__quiet

    def get(self, stream_name):
        return self.__data.get(stream_name)

    def add(self, stream):
        name = stream.get_name()
        if name not in self.__data:
            self.__data[name] = stream
            return True
        else:
            return False

    def remove(self, stream_name):
        if stream_name in self.__data:
            self.__data.pop(stream_name)
            return True
        else:
            return False

    def list(self):
        represent = []
        for name, stream in self.__data.items():
            represent.append({"name": name, "resource": stream.get_resource(), "address": stream.get_address()})
        return represent

    def start(self):
        for _, stream in self.__data.items():
            stream.start()

    def stop(self):
        for _, stream in self.__data.items():
            stream.stop()

    def restart(self):
        for _, stream in self.__data.items():
            stream.restart()

    def restart_if_down(self):
        for _, stream in self.__data.items():
            if not stream.online():
                stream.restart()
