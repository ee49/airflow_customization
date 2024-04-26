import pytest
from datetime import datetime
from pendulum import DateTime
from myapp.timetables import HolidayTimetable, USHolidayTimetable  # adjust this import according to your project structure

class TestHolidayTimetable:
    class TestHolidayTimetableSubclass(HolidayTimetable):
        def is_holiday(self, date):
            return date.day == 1  # For simplicity, let's say every 1st of the month is a holiday

    def test_is_holiday(self):
        timetable = self.TestHolidayTimetableSubclass('* * * * *')
        assert timetable.is_holiday(datetime(2022, 1, 1))
        assert not timetable.is_holiday(datetime(2022, 1, 2))

    def test_next_dagrun_info(self):
        timetable = self.TestHolidayTimetableSubclass('* * * * *')
        next_dagrun_info = timetable.next_dagrun_info(last_automated_dagrun=DateTime(2022, 1, 1), restriction=None)
        assert next_dagrun_info.start_date.day == 2  # The next run date should be January 2nd, because the 1st is a holiday

class TestUSHolidayTimetable:
    def test_is_holiday(self):
        timetable = USHolidayTimetable('* * * * *')
        assert timetable.is_holiday(datetime(2022, 7, 4))  # July 4th is a holiday
        assert not timetable.is_holiday(datetime(2022, 7, 5))  # July 5th is not a holiday

    def test_next_dagrun_info(self):
        timetable = USHolidayTimetable('* * * * *')
        next_dagrun_info = timetable.next_dagrun_info(last_automated_dagrun=DateTime(2022, 7, 3), restriction=None)
        assert next_dagrun_info.start_date.day == 5  # The next run date should be July 5th, because the 4th is a holiday
