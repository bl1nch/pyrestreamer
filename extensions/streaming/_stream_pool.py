from extensions.singleton import Singleton


class StreamPool(metaclass=Singleton):
    __quiet = False

    def __init__(self, scheduler, quiet=False):
        self.__class__.__quiet = quiet
        self.__data = {}

        @scheduler.scheduled_job('cron', id='scheduled_restarter_am', hour=1)
        def scheduled_restarter_am():
            self.restart()

        @scheduler.scheduled_job('cron', id='scheduled_restarter_pm', hour=13)
        def scheduled_restarter_pm():
            self.restart()

        @scheduler.scheduled_job('interval', id='check_and_restart', minutes=10)
        def check_and_restart():
            self.restart_crashed()

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

    def restart_crashed(self):
        for _, stream in self.__data.items():
            stream.start_test()

    def restart_if_down(self):
        for _, stream in self.__data.items():
            if not stream.online():
                stream.restart()
