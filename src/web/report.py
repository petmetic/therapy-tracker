import calendar
from datetime import datetime


def define_month():
    year = datetime.today().year
    month = datetime.today().month
    _, end_day = calendar.monthrange(year, month)
    last_day_str = datetime(year, month, end_day).strftime("%Y-%m-%d")
    first_day_str = datetime(year, month, 1).strftime("%Y-%m-%d")

    first_day = datetime(year, month, 1)
    last_day = datetime(year, month, end_day)

    return first_day_str, last_day_str, first_day, last_day
