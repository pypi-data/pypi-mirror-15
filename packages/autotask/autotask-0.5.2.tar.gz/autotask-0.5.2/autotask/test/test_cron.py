
import datetime
from datetime import datetime as dt
import pytest

from django.conf import settings
from django.utils.timezone import make_aware

from autotask.cron import (
    CronScheduler,
    get_next_value,
)


@pytest.mark.parametrize(
    'crontab, minutes, hours, dow, months, dom', [
        ('* * * * *', None, None, None, None, None),
        ('5 * * * *', [5], None, None, None, None),
        ('5,7 * * * *', [5, 7], None, None, None, None),
        ('5-7 * * * *', [5, 6, 7], None, None, None, None),
        ('5-8,12 * * * *', [5, 6, 7, 8, 12], None, None, None, None),
        ('1,5-8,12,14,20-22 * * * *', [1, 5, 6, 7, 8, 12, 14, 20, 21, 22], None, None, None, None),
        ('30 7 * * *', [30], [7], None, None, None),
        ('30 7-9 * * *', [30], [7, 8, 9], None, None, None),
        ('30 7 0 * *', [30], [7], [0], None, None),
        ('30 7 0 4,7 10-15', [30], [7], [0], [4, 7], [10, 11, 12, 13, 14, 15]),
    ])
def test_crontab(crontab, minutes, hours, dow, months, dom):
    cs = CronScheduler(crontab=crontab)
    assert cs.minutes == minutes
    assert cs.hours == hours
    assert cs.dow == dow
    assert cs.months == months
    assert cs.dom == dom


@pytest.mark.parametrize(
    'value, values, result', [
        (2, [5, 10, 15], 5),
        (5, [5, 10, 15], 10),
        (10, [5, 10, 15], 15),
        (15, [5, 10, 15], 5),
        (2, [7], 7),
        (7, [7], 7),
        (9, [7], 7),
    ])
def test_get_next_value(value, values, result):
    assert result == get_next_value(value, values)


@pytest.mark.parametrize(
    'crontab, minutes, minute, result', [
        (None, None, 10, 11),
        (None, None, 58, 59),
        (None, None, 59, 0),
        (None, [10, 30], 2, 10),
        (None, [10, 30], 10, 30),
        (None, [10, 30], 30, 10),
        (None, [10], 30, 10),
        (None, [10], 10, 10),
        (None, [10], 1, 10),
        ('* * * * *', None, 10, 11),
        ('5 * * * *', None, 10, 5),
        ('5,15 * * * *', None, 10, 15),
        ('5,15 * * * *', [12, 20], 10, 15),
        ('5,15 * * * *', [12, 20], 15, 5),
    ])
def test_get_next_minute(crontab, minutes, minute, result):
    last_schedule = datetime.datetime(2016, 4, 20, minute=minute)
    cs = CronScheduler(last_schedule=last_schedule, crontab=crontab, minutes=minutes)
    assert result == cs.get_next_minute(last_schedule)


@pytest.mark.parametrize(
    'crontab, hours, hour, result', [
        (None, None, 22, 23),
        (None, None, 23, 0),
        ('* * * * *', None, 10, 11),
        ('* 15 * * *', None, 10, 15),
        ('* 15 * * *', None, 15, 15),
        ('* 15 * * *', None, 17, 15),
    ])
def test_get_next_hour(crontab, hours, hour, result):
    last_schedule = datetime.datetime(2016, 4, 20, hour=hour)
    cs = CronScheduler(last_schedule=last_schedule, crontab=crontab, hours=hours)
    assert result == cs.get_next_hour(last_schedule)


@pytest.mark.parametrize(
    'crontab, last_schedule, result', [
        ('* * * * 3', dt(2016, 4, 1), dt(2016, 4, 3)),
        ('* * * * 3', dt(2016, 4, 3), dt(2016, 5, 3)),
        ('* * * * 3,20', dt(2016, 4, 3), dt(2016, 4, 20)),
        ('* * * * 3,20', dt(2016, 4, 20), dt(2016, 5, 3)),
    ])
def test_get_next_dom(crontab, last_schedule, result):
    cs = CronScheduler(last_schedule=last_schedule, crontab=crontab)
    assert result == cs.get_next_dom(last_schedule)


@pytest.mark.parametrize(
    'crontab, last_schedule, result', [
        ('* * 0 * *', dt(2016, 3, 1), dt(2016, 3, 7)),
        ('* * 0 * *', dt(2016, 3, 7), dt(2016, 3, 14)),
        ('* * 0 * *', dt(2016, 3, 28), dt(2016, 4, 4)),
        ('* * 0 * *', dt(2016, 2, 22), dt(2016, 2, 29)),  # leap year
        ('* * 2,4 * *', dt(2016, 4, 1), dt(2016, 4, 6)),
        ('* * 2,4 * *', dt(2016, 4, 6), dt(2016, 4, 8)),
        ('* * 2,4 * *', dt(2016, 4, 8), dt(2016, 4, 13)),
    ])
def test_get_next_dow(crontab, last_schedule, result):
    cs = CronScheduler(last_schedule=last_schedule, crontab=crontab)
    assert result == cs.get_next_dow(last_schedule)


@pytest.mark.parametrize(
    'crontab, schedule, result', [
        ('* * * * *', dt(2016, 4, 26), True),
        ('* * * 4 *', dt(2016, 4, 26), True),
        ('* * * 5 *', dt(2016, 4, 26), False),
        ('* * * 4,5 *', dt(2016, 4, 26), True),
        ('* * * 3-5 *', dt(2016, 4, 26), True),
    ])
def test_month_allowed(crontab, schedule, result):
    cs = CronScheduler(crontab=crontab)
    assert result == cs.month_allowed(schedule)


@pytest.mark.parametrize(
    'crontab, schedule, result', [
        ('* * * * *', dt(2016, 4, 26), True),
        ('* * 0 * *', dt(2016, 4, 26), False),
        ('* * 1 * *', dt(2016, 4, 26), True),
        ('* * * * 24', dt(2016, 4, 26), False),
        ('* * * * 24-27', dt(2016, 4, 26), True),
        ('* * 1 * 22', dt(2016, 4, 26), True),
        ('* * 2 * 22', dt(2016, 4, 26), False),
        ('* * 2 * 26', dt(2016, 4, 26), True),
        ('* * 1 * 26', dt(2016, 4, 26), True),
    ])
def test_day_allowed(crontab, schedule, result):
    cs = CronScheduler(crontab=crontab)
    assert result == cs.day_allowed(schedule)


@pytest.mark.parametrize(
    'crontab, schedule, result', [
        ('* * * 5 *', dt(2016, 4, 26), dt(2016, 5, 1)),
        ('* * * 4 *', dt(2016, 4, 26), dt(2017, 4, 1)),
        ('* * * 3-5 *', dt(2016, 2, 26), dt(2016, 3, 1)),
        ('* * * 3-5 *', dt(2016, 3, 26), dt(2016, 4, 1)),
        ('* * * 3-5 *', dt(2016, 4, 26), dt(2016, 5, 1)),
        ('* * * 3-5 *', dt(2016, 5, 26), dt(2017, 3, 1)),
    ])
def test_set_allowed_month(crontab, schedule, result):
    cs = CronScheduler(crontab=crontab)
    assert result == cs.set_allowed_month(schedule)


@pytest.mark.parametrize(
    'crontab, schedule, result', [
        ('* * * * *', dt(2016, 4, 26, 8, 58), dt(2016, 4, 26, 8, 59)),
        ('* * * * *', dt(2016, 4, 26, 8, 59), dt(2016, 4, 26, 9, 0)),
        ('15,30 * * * *', dt(2016, 4, 26, 8, 59), dt(2016, 4, 26, 9, 15)),
        ('15,30 * * * *', dt(2016, 4, 26, 9, 15), dt(2016, 4, 26, 9, 30)),
        ('15,30 * * * *', dt(2016, 4, 26, 9, 30), dt(2016, 4, 26, 10, 15)),
        ('30 7-8 * * *', dt(2016, 4, 26, 6, 30), dt(2016, 4, 26, 7, 30)),
        ('30 7-8 * * *', dt(2016, 4, 26, 7, 30), dt(2016, 4, 26, 8, 30)),
        ('30 7-8 * * *', dt(2016, 4, 26, 8, 30), dt(2016, 4, 27, 7, 30)),
        ('* 10 * * *', dt(2016, 4, 27, 7, 58), dt(2016, 4, 27, 10, 59)),
        ('* 10 * * *', dt(2016, 4, 27, 10, 59), dt(2016, 4, 28, 10, 0)),
        ('30 10 * 7 *', dt(2016, 4, 27, 10, 59), dt(2016, 7, 1, 10, 30)),
        ('30 10 * 7 *', dt(2016, 7, 1, 10, 30), dt(2016, 7, 2, 10, 30)),
        ('30 10 * 7 *', dt(2016, 7, 31, 10, 30), dt(2017, 7, 1, 10, 30)),
        ('30 10 1 * *', dt(2016, 4, 6, 11, 30), dt(2016, 4, 12, 10, 30)),
        ('30 10 1 * *', dt(2016, 4, 26, 11, 30), dt(2016, 5, 3, 10, 30)),
        ('0 8 * * 22,23', dt(2016, 4, 26, 11, 30), dt(2016, 5, 22, 8, 0)),
        ('0 8 * * 22,23', dt(2016, 5, 22, 8, 0), dt(2016, 5, 23, 8, 0)),
        ('0 8 * * 22,23', dt(2016, 5, 23, 8, 0), dt(2016, 6, 22, 8, 0)),
        ('0 8 0 * 22,23', dt(2016, 5, 23, 8, 0), dt(2016, 5, 30, 8, 0)),
        ('0 8 0 6 22,23', dt(2016, 5, 23, 8, 0), dt(2016, 6, 6, 8, 0)),
        ('0 8 0 6 22,23', dt(2016, 6, 6, 8, 0), dt(2016, 6, 13, 8, 0)),
        ('0 8 0 6 22,23', dt(2016, 6, 13, 8, 0), dt(2016, 6, 20, 8, 0)),
        ('0 8 0 6 22,23', dt(2016, 6, 20, 8, 0), dt(2016, 6, 22, 8, 0)),
        ('0 8 0 6 22,23', dt(2016, 6, 23, 8, 0), dt(2016, 6, 27, 8, 0)),
        ('0 8 0 6 22,23', dt(2016, 6, 27, 8, 0), dt(2017, 6, 5, 8, 0)),
    ])
def test_get_next_schedule(crontab, schedule, result):
    cs = CronScheduler(crontab=crontab, last_schedule=schedule)
    if settings.USE_TZ:
        result = make_aware(result)
    assert result == cs.get_next_schedule()
