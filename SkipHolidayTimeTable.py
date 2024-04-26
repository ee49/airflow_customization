from abc import ABC, abstractmethod
from datetime import timedelta
from airflow.timetables.base import DagRunInfo, TimeRestriction
from airflow.timetables.interval import CronTriggerTimetable

class HolidayTimetable(CronTriggerTimetable, ABC):
    @abstractmethod
    def is_holiday(self, date):
        pass

    def next_dagrun_info(
        self,
        *,
        last_automated_dagrun: Optional[pendulum.DateTime],
        restriction: TimeRestriction,
    ) -> Optional[DagRunInfo]:
        # Use the parent class's logic to get the next run date
        next_run_date = super().next_dagrun_info(
            last_automated_dagrun=last_automated_dagrun,
            restriction=restriction,
        )

        if next_run_date is None:
            return None

        # Check if the next run date is a holiday
        while self.is_holiday(next_run_date):
            # If it is, skip it and calculate the next run date
            next_run_date += timedelta(days=1)

        return DagRunInfo.interval(start_date=next_run_date, end_date=next_run_date)


from holidays import UnitedStates

class USHolidayTimetable(HolidayTimetable):
    def is_holiday(self, date):
        us_holidays = UnitedStates()
        return date in us_holidays



dag = DAG(
    dag_id='my_dag',
    timetable=USHolidayTimetable('* * * * *'),  # Use your cron expression
    # Other DAG parameters...
)


####################

#testcases:


