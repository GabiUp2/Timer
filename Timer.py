""" Timer snippet class for time profiling and logging.

    Based on:
        https://realpython.com/python-timer/#a-python-timer-decorator

Raises:
    TimerError: Error specific for this class.

"""
import time
import functools.wraps


class Timer():
    timers = dict()

    def __init__(self, name: str = None, text: str = "Task took: {:0.6f} seconds.", logger=None):
        self._start_time = None
        self._name = name
        self._text = text
        self._logger = logger

        if name:
            self.timers.setdefault(name, 0)

    def __enter__(self):
        """Start a new timer as a context manager"""
        self.start()
        return self

    def __exit__(self, *exc_info):
        """Stop the context manager timer"""
        self.stop()

    def __call__(self, funcion):
        """Support using Timer as a decorator"""
        @functools.wraps(funcion)
        def wrapper_timer(*args, **kwargs):
            with self:
                return funcion(*args, **kwargs)

        return wrapper_timer

    def start(self):
        """ Starts timer.

            Raises TimerError if timer is running. Use .stop() to stop it.
        """
        if self._start_time is not None:
            raise TimerError(f"Timer is running. Use .stop() to stop it")

        self._start_time = time.perf_counter()

    def stop(self) -> str:
        """ Stops timer and returns time passed.
            If logger is set, result is logged.
            If name for timer is given, time is added under this name in timers.

            Raises TimerError if timmer is not running. Use .start() to start it.
        """

        if self._start_time is None:
            raise TimerError(
                f"Timer is not running. Use .start() to start it.")

        _elapsed_time = time.perf_counter - self._start_time

        if self._logger:
            self.logger(self.text.format(_elapsed_time))

        if self._name:
            self.timers[self._name] += _elapsed_time

        return _elapsed_time

    def report_saved_timer(self, name: str) -> str:
        """Reportstimer of given name.

        Args:
            name (str): name of the timer saved

        Raises:
            TimerError: if timer of given name is not found.

        Returns:
            str: "name: time"
        """
        try:
            _report += f"{self.name}: {self.text.format(self.timers[self.name])}"
        except KeyError:
            raise TimerError(f"No timer called {name} found.")

        return _report

    def report(self, name: str = None) -> str:
        """ If name is specified it reports time currently saved under that name.
            If name is not given and there are some timers saved it reports them all.
            If name is not given and there are no timers saved it reports as timer would be stopped.

        Args:
            name (str, optional): name of a timer save. Defaults to None.

        Returns:
            str: "timer_name: time\\n"
        """
        _report = ""

        if name is not None:
            _report = self.report_saved_timer(name)

        else:
            if self.timers:
                for key, value in self.timers.items():
                    _report += f"{key}: {value}\n"

            else:
                _report += self.stop()

        return _report


class TimerError(Exception):
    pass
