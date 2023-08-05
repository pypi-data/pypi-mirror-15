
import calendar
import datetime
from datetime import timedelta
import re

from django.conf import settings
from django.utils.timezone import (
    make_aware,
    now,
)


class CronScheduler(object):
    """
    Schedules a cron task.

    Usage:

    cs = CronScheduler()
    next_schedule = cs.get_next_schedule()
    """

    def __init__(self, last_schedule=None, minutes=None, hours=None,
                 dow=None, months=None, dom=None, crontab=None):
        """
        Inits the scheduler with values according the crontab-format.

        All arguments are optional. If no arguments are given the task
        is scheduled from now on every minute.

        last_schedule: last time the according tasks has run
        minutes: list of integers when a task should run in an hour [0-59]
        hours: list of integers when a task should run during a day [0-23]
        dow: list of integers for the days of week when a task should
        run [0-6] (0 for monday up to 6 for sunday).
        month: list of integers for the months a task should run [1-12]
        dom: list of intergs for the day in a month a task should run [1-31]
        """
        self.last_schedule = last_schedule or now()
        if crontab:
            self.parse_crontab(crontab)
        else:
            self.minutes = minutes
            self.hours = hours
            self.dow = dow
            self.months = months
            self.dom = dom

    def parse_crontab(self, crontab):
        """
        Parses a simple crontab-string with five patterns:

        Minute [0,59]
        Hour [0,23]
        Day of the month [1,31]
        Month of the year [1,12]
        Day of the week ([0,6] with 0=Monday)

        Each of these patterns can be either an asterisk (meaning all
        valid values), an element, or a list of elements separated by
        commas. An element shall be either a number or two numbers
        separated by a hyphen (meaning an inclusive range).

        A day-range for a month like 1-4,12,20-25 is also ok. But keep
        in mind that no spaces are allowed as spaces are the separators
        between the patterns.

        Some examples:

        * * * * *               runs every minute
        5 * * * *               runs every five minutes
        30 7 0 4,7 10-15        runs at 7:30 on mondays and also from the
                                10th to 15th of a month, but only in april
                                and july

        May raise errors if the crontab could not be parsed. The
        crontab-content is *not* checked for correctness).
        """
        if not crontab:
            return False
        outer = []
        for item in crontab.split():
            item = item.strip()
            if item == '*':
                outer.append(None)
                continue
            inner = []
            for element in item.split(','):
                mo = re.match(r'(\d+)-(\d+)', element)
                if mo:
                    inner.extend([i for i in range(
                        int(mo.group(1)), int(mo.group(2))+1)])
                else:
                    inner.append(int(element))
            outer.append(inner)
        self.minutes, self.hours, self.dow, self.months, self.dom = outer

    def get_next_schedule(self, last_schedule=None):
        """
        Returns the next schedule based on the current date as a
        datetime-object.
        """
        ls = last_schedule or self.last_schedule
        next_schedule = self.find_next_schedule(ls)
        if not self.month_allowed(next_schedule):
            schedule = self.set_allowed_month(next_schedule)
            return self.get_next_schedule(schedule)
        if settings.USE_TZ and not is_aware(next_schedule):
            next_schedule = make_aware(next_schedule)
        return next_schedule

    def set_allowed_month(self, schedule):
        """
        Modifies the schedule to the first day of the next allowed
        month and returns this new schedule.
        """
        month = get_next_value(schedule.month, self.months)
        if month > schedule.month:
            year = schedule.year
        else:
            year = schedule.year + 1
        return datetime.datetime(year, month, 1)

    def month_allowed(self, schedule):
        """
        Returns a boolean whether the scheduled month is allowed by the
        crontab data.
        """
        if not self.months:
            return True
        return schedule.month in self.months

    def day_allowed(self, schedule):
        """
        Returns a boolean whether the scheduled day is allowed by the
        crontab data.
        """
        if not self.dom and not self.dow:
            # every day is allowed
            return True
        if self.dom and schedule.day in self.dom:
            # day of month is allowed
            return True
        weekday = calendar.weekday(schedule.year, schedule.month, schedule.day)
        if self.dow and weekday in self.dow:
            # weekday is allowed
            return True
        return False

    def hour_allowed(self, schedule):
        """
        Returns a boolean whether the scheduled hour is allowed by the
        crontab data.
        """
        if not self.hours:
            return True
        return schedule.hour in self.hours

    def find_next_schedule(self, last_schedule):
        """
        Finds the next allowed day and time according to the crontab
        data. It has to be assumed that last_schedule may not be a valid
        schedule (may be initialized with now()).
        Returns a datetime-object.
        """
        # short cut
        ls = last_schedule
        next_minute = self.get_next_minute(ls)
        if next_minute > ls.minute:
            # same day, same hour
            delta = next_minute - ls.minute
            if self.hour_allowed(ls):
                return ls + timedelta(minutes=delta)
        next_hour = self.get_next_hour(ls)
        if next_hour > ls.hour:
            # same day
            if self.day_allowed(ls):
                delta_hours = next_hour - ls.hour
                delta_minutes = next_minute - ls.minute
                return ls + timedelta(hours=delta_hours, minutes=delta_minutes)
        if not self.dow and not self.dom:
            # next day
            schedule = self.get_next_day(ls)
        elif self.dom and not self.dow:
            # find next allowed day of month
            schedule = self.get_next_dom(ls)
        elif not self.dom and self.dow:
            # find next allowed weekday
            schedule = self.get_next_dow(ls)
        elif self.dom and self.dow:
            # find first next allowed day of month
            schedule_dom = self.get_next_dom(ls)
            schedule_dow = self.get_next_dow(ls)
            schedule = min(schedule_dom, schedule_dow)
        return schedule + timedelta(
            hours=next_hour-ls.hour,
            minutes=next_minute-ls.minute)

    def get_next_minute(self, last_schedule):
        """
        Returns the next minute a task should run according to
        last_schedule (a datetime object) and the content of
        self.minutes.
        """
        if self.minutes:
            minute = get_next_value(last_schedule.minute, self.minutes)
        else:
            minute = last_schedule.minute + 1
            if minute > 59:
                minute = 0
        return minute

    def get_next_hour(self, last_schedule):
        """
        Returns the next hour a task should run according to
        last_schedule ( a datetime object) and the content of
        self.hours.
        """
        if self.hours:
            hour = get_next_value(last_schedule.hour, self.hours)
        else:
            hour = last_schedule.hour + 1
            if hour > 23:
                hour = 0
        return hour

    @staticmethod
    def get_next_day(last_schedule):
        """
        Increments the day according to last_schedule (a
        datetime-object) and returns the new date as datetime-object.
        """
        return last_schedule + datetime.timedelta(days=1)

    def get_next_dom(self, last_schedule):
        """
        Calculates the next allowed day and returns the result as a
        datetime-object.
        """
        # method gets not called if self.dom is None or empty
        next_day = get_next_value(last_schedule.day, self.dom)
        day = last_schedule.day
        if next_day > day:
            delta = next_day - day
        else:
            _, max_days = calendar.monthrange(
                last_schedule.year, last_schedule.month)
            delta = max_days - day + next_day
        return last_schedule + datetime.timedelta(days=delta)

    def get_next_dow(self, last_schedule):
        """
        Calculates the next allowed weekday and returns the result as a
        datetime-object.
        """
        weekday = calendar.weekday(
            last_schedule.year, last_schedule.month, last_schedule.day)
        next_weekday = get_next_value(weekday, self.dow)
        if next_weekday > weekday:
            delta = next_weekday - weekday
        else:
            delta = 7 - weekday + next_weekday
        return last_schedule + datetime.timedelta(days=delta)


def get_next_value(value, values):
    """
    Returns the next value from values which is larger then value or the
    first item from the sequence values.
    """
    for item in values:
        if item > value:
            return item
    return values[0]
