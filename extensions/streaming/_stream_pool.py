from extensions.singleton import Singleton
from gevent.threading import Lock
from gevent import sleep


class StreamPool(metaclass=Singleton):
    __quiet = False

    def __init__(self, scheduler, quiet=False):
        self.__class__.__quiet = quiet
        self.__sched_using = False
        self.__sched_lock = Lock()
        self.__data = {}

        @scheduler.scheduled_job('cron', id='scheduled_restarter_am_l', hour=1)
        def scheduled_restarter_am_l():
            self.__sched_using = True
            while self.__sched_lock.locked():
                sleep(5)
            self.recreate_and_start()
            self.__sched_using = False

        @scheduler.scheduled_job('cron', id='scheduled_restarter_am_h', hour=7)
        def scheduled_restarter_am_h():
            self.__sched_using = True
            while self.__sched_lock.locked():
                sleep(5)
            self.recreate_and_start()
            self.__sched_using = False

        @scheduler.scheduled_job('cron', id='scheduled_restarter_pm_l', hour=13)
        def scheduled_restarter_pm_l():
            self.__sched_using = True
            while self.__sched_lock.locked():
                sleep(5)
            self.recreate_and_start()
            self.__sched_using = False

        @scheduler.scheduled_job('cron', id='scheduled_restarter_pm_h', hour=19)
        def scheduled_restarter_pm_h():
            self.__sched_using = True
            while self.__sched_lock.locked():
                sleep(5)
            self.recreate_and_start()
            self.__sched_using = False

        @scheduler.scheduled_job('interval', id='check_and_restart', minutes=15)
        def check_and_restart():
            if not self.__sched_using:
                self.restart_crashed()
                gc.collect()

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

    def recreate_and_start(self):
        for _, stream in self.__data.items():
            stream.recreate()
            stream.start()
    
    def restart(self):
        for _, stream in self.__data.items():
            stream.restart()

    def restart_crashed(self):
        for _, stream in self.__data.items():
            stream.start_test(self.__sched_lock)

    def restart_if_down(self):
        for _, stream in self.__data.items():
            if not stream.online():
                stream.restart()
