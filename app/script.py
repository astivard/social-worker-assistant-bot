from calendar import monthcalendar
from datetime import datetime

from days_month_data import correct_week_day_names, correct_month_names, holidays


def get_number_days(week_days: list) -> int:
    number_of_visit_days = 0
    month = datetime.now().month
    for day in week_days:
        number_of_visit_days += len([1 for i in monthcalendar(datetime.now().year,
                                                              month) if
                                     i[correct_week_day_names[day]] != 0 and i[correct_week_day_names[day]] not in
                                     holidays[month - 1]])
    return number_of_visit_days


def get_total(is_privileged: bool, week_days: list) -> (float, int, float, str):
    month = correct_month_names[datetime.now().month]
    number_of_days = get_number_days(week_days)
    if is_privileged:
        coef = 0.78
        total = round(number_of_days * coef, 2)
    else:
        coef = 1.30
        total = round(number_of_days * coef, 2)
    return total, number_of_days, coef, month
