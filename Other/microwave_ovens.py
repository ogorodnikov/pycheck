from contextlib import suppress
from datetime import time
from re import match

TIME_PATTERNS = r'(\d{2}):(\d{2})', r'(\d+)m()', r'()(\d+)s'


class MicrowaveTime(time):

    def __add__(self, other):
        total_seconds = self.total_seconds + other.total_seconds
        total_seconds = min(90 * 60, total_seconds)
        return MicrowaveTime.from_seconds(total_seconds)

    def __sub__(self, other):
        total_seconds = self.total_seconds - other.total_seconds
        total_seconds = max(0, total_seconds)
        return MicrowaveTime.from_seconds(total_seconds)

    @property
    def total_seconds(self):
        return self.hour * 3600 + self.minute * 60 + self.second

    @classmethod
    def from_seconds(cls, total_seconds):
        return MicrowaveTime(*cls.seconds_to_hms(total_seconds))

    @staticmethod
    def seconds_to_hms(total_seconds):
        hours, seconds_remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(seconds_remainder, 60)
        return hours, minutes, seconds


class MicrowaveBase:
    _time = None
    _faulty_segment = None

    def __init__(self):
        self.set_time('00:00')

    @staticmethod
    def string_to_time(time_string):

        minutes = seconds = 0

        for pattern in TIME_PATTERNS:
            with suppress(AttributeError):
                minutes, seconds = (int(value) if value else 0
                                    for value in match(pattern, time_string).groups())

        total_seconds = 60 * minutes + seconds

        return MicrowaveTime.from_seconds(total_seconds)

    def set_time(self, time_string):
        self._time = self.string_to_time(time_string)

    def add_time(self, time_string):
        self._time += self.string_to_time(time_string)

    def del_time(self, time_string):
        self._time -= self.string_to_time(time_string)

    def show_time(self):
        minutes, seconds = divmod(self._time.total_seconds, 60)
        time_string = f'{minutes:02}:{seconds:02}'

        faulty_time_string = ''.join('_' if i == self._faulty_segment
                                     else letter
                                     for i, letter in enumerate(time_string))

        return faulty_time_string


class Microwave1(MicrowaveBase):
    _faulty_segment = 0


class Microwave2(MicrowaveBase):
    _faulty_segment = 4


class Microwave3(MicrowaveBase):
    _faulty_segment = None


class RemoteControl:
    _microwave = None

    def __init__(self, microwave):
        self._microwave = microwave

    def __getattr__(self, item):
        return getattr(self._microwave, item)

    def show_time(self):
        return self._microwave.show_time()


if __name__ == '__main__':
    microwave_1 = Microwave1()
    microwave_2 = Microwave2()
    microwave_3 = Microwave3()

    remote_control_1 = RemoteControl(microwave_1)
    remote_control_1.set_time("01:00")

    remote_control_2 = RemoteControl(microwave_2)
    remote_control_2.add_time("90s")

    remote_control_3 = RemoteControl(microwave_3)
    remote_control_3.del_time("300s")
    remote_control_3.add_time("100s")

    assert remote_control_1.show_time() == "_1:00"
    assert remote_control_2.show_time() == "01:3_"
    assert remote_control_3.show_time() == "01:40"

    # mission tests

    microwave_2 = Microwave2()
    rc_2 = RemoteControl(microwave_2)
    rc_2.set_time("89:00")
    rc_2.add_time("90s")
    rc_2.add_time("20m")
    assert rc_2.show_time() == "90:0_"
