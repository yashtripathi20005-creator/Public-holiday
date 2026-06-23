"""
Holiday data for various countries.
"""

from datetime import date, datetime

# Holiday data for different countries
# Each country has a list of holidays with name, date, and type
HOLIDAY_DATA = {
    'US': [
        {'name': 'New Year\'s Day', 'month': 1, 'day': 1, 'type': 'federal'},
        {'name': 'Martin Luther King Jr. Day', 'month': 1, 'day': None, 'weekday': 1, 'week': 3, 'type': 'federal'},
        {'name': 'Washington\'s Birthday', 'month': 2, 'day': None, 'weekday': 1, 'week': 3, 'type': 'federal'},
        {'name': 'Memorial Day', 'month': 5, 'day': None, 'weekday': 0, 'week': -1, 'type': 'federal'},
        {'name': 'Juneteenth', 'month': 6, 'day': 19, 'type': 'federal'},
        {'name': 'Independence Day', 'month': 7, 'day': 4, 'type': 'federal'},
        {'name': 'Labor Day', 'month': 9, 'day': None, 'weekday': 0, 'week': 1, 'type': 'federal'},
        {'name': 'Columbus Day', 'month': 10, 'day': None, 'weekday': 1, 'week': 2, 'type': 'federal'},
        {'name': 'Veterans Day', 'month': 11, 'day': 11, 'type': 'federal'},
        {'name': 'Thanksgiving Day', 'month': 11, 'day': None, 'weekday': 3, 'week': 4, 'type': 'federal'},
        {'name': 'Christmas Day', 'month': 12, 'day': 25, 'type': 'federal'},
    ],
    'UK': [
        {'name': 'New Year\'s Day', 'month': 1, 'day': 1, 'type': 'bank'},
        {'name': 'Good Friday', 'month': None, 'day': None, 'type': 'bank', 'dynamic': 'easter', 'offset': -2},
        {'name': 'Easter Monday', 'month': None, 'day': None, 'type': 'bank', 'dynamic': 'easter', 'offset': 1},
        {'name': 'Early May Bank Holiday', 'month': 5, 'day': None, 'weekday': 0, 'week': 1, 'type': 'bank'},
        {'name': 'Spring Bank Holiday', 'month': 5, 'day': None, 'weekday': 0, 'week': -1, 'type': 'bank'},
        {'name': 'Summer Bank Holiday', 'month': 8, 'day': None, 'weekday': 0, 'week': -1, 'type': 'bank'},
        {'name': 'Christmas Day', 'month': 12, 'day': 25, 'type': 'bank'},
        {'name': 'Boxing Day', 'month': 12, 'day': 26, 'type': 'bank'},
    ],
    'CA': [
        {'name': 'New Year\'s Day', 'month': 1, 'day': 1, 'type': 'federal'},
        {'name': 'Family Day', 'month': 2, 'day': None, 'weekday': 0, 'week': 3, 'type': 'provincial'},
        {'name': 'Good Friday', 'month': None, 'day': None, 'type': 'federal', 'dynamic': 'easter', 'offset': -2},
        {'name': 'Victoria Day', 'month': 5, 'day': None, 'weekday': 0, 'week': -1, 'type': 'federal'},
        {'name': 'Canada Day', 'month': 7, 'day': 1, 'type': 'federal'},
        {'name': 'Labour Day', 'month': 9, 'day': None, 'weekday': 0, 'week': 1, 'type': 'federal'},
        {'name': 'National Day for Truth and Reconciliation', 'month': 9, 'day': 30, 'type': 'federal'},
        {'name': 'Thanksgiving Day', 'month': 10, 'day': None, 'weekday': 0, 'week': 2, 'type': 'federal'},
        {'name': 'Remembrance Day', 'month': 11, 'day': 11, 'type': 'federal'},
        {'name': 'Christmas Day', 'month': 12, 'day': 25, 'type': 'federal'},
    ],
    'AU': [
        {'name': 'New Year\'s Day', 'month': 1, 'day': 1, 'type': 'national'},
        {'name': 'Australia Day', 'month': 1, 'day': 26, 'type': 'national'},
        {'name': 'Good Friday', 'month': None, 'day': None, 'type': 'national', 'dynamic': 'easter', 'offset': -2},
        {'name': 'Easter Saturday', 'month': None, 'day': None, 'type': 'national', 'dynamic': 'easter', 'offset': -1},
        {'name': 'Easter Sunday', 'month': None, 'day': None, 'type': 'national', 'dynamic': 'easter', 'offset': 0},
        {'name': 'Easter Monday', 'month': None, 'day': None, 'type': 'national', 'dynamic': 'easter', 'offset': 1},
        {'name': 'ANZAC Day', 'month': 4, 'day': 25, 'type': 'national'},
        {'name': 'King\'s Birthday', 'month': 6, 'day': None, 'weekday': 0, 'week': 2, 'type': 'national'},
        {'name': 'Labour Day', 'month': 10, 'day': None, 'weekday': 0, 'week': 1, 'type': 'national'},
        {'name': 'Christmas Day', 'month': 12, 'day': 25, 'type': 'national'},
        {'name': 'Boxing Day', 'month': 12, 'day': 26, 'type': 'national'},
    ],
    'IN': [
        {'name': 'Republic Day', 'month': 1, 'day': 26, 'type': 'national'},
        {'name': 'Holi', 'month': 3, 'day': None, 'type': 'national', 'dynamic': 'holi'},
        {'name': 'Good Friday', 'month': None, 'day': None, 'type': 'national', 'dynamic': 'easter', 'offset': -2},
        {'name': 'Independence Day', 'month': 8, 'day': 15, 'type': 'national'},
        {'name': 'Gandhi Jayanti', 'month': 10, 'day': 2, 'type': 'national'},
        {'name': 'Diwali', 'month': 10, 'day': None, 'type': 'national', 'dynamic': 'diwali'},
        {'name': 'Guru Nanak Jayanti', 'month': 11, 'day': None, 'type': 'national', 'dynamic': 'guru_nanak'},
        {'name': 'Christmas Day', 'month': 12, 'day': 25, 'type': 'national'},
    ]
}


def get_nth_weekday(year, month, weekday, week):
    """
    Get the date of the nth occurrence of a weekday in a month.
    
    Args:
        year (int): The year
        month (int): The month (1-12)
        weekday (int): 0=Monday, 6=Sunday
        week (int): Week number (1-5, or -1 for last week)
    
    Returns:
        datetime.date: The calculated date
    """
    from calendar import monthcalendar
    
    cal = monthcalendar(year, month)
    
    if week == -1:  # Last occurrence
        for week_num in range(len(cal) - 1, -1, -1):
            if cal[week_num][weekday] != 0:
                return date(year, month, cal[week_num][weekday])
    else:
        if len(cal) >= week and cal[week - 1][weekday] != 0:
            return date(year, month, cal[week - 1][weekday])
        elif len(cal) >= week and cal[week - 1][weekday] == 0:
            # If the day doesn't exist in that week, use the next week's occurrence
            for i in range(week - 1, len(cal)):
                if cal[i][weekday] != 0:
                    return date(year, month, cal[i][weekday])
    
    return None


def calculate_easter(year):
    """
    Calculate Easter Sunday date for a given year using the Computus algorithm.
    
    Args:
        year (int): The year
    
    Returns:
        datetime.date: Easter Sunday date
    """
    # Anonymous Gregorian algorithm
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    
    return date(year, month, day)


def get_holiday_date(year, holiday):
    """
    Get the actual date of a holiday for a given year.
    
    Args:
        year (int): The year
        holiday (dict): Holiday definition
    
    Returns:
        datetime.date: The calculated date, or None if not calculable
    """
    if 'dynamic' in holiday and holiday['dynamic']:
        if holiday['dynamic'] == 'easter':
            easter = calculate_easter(year)
            offset = holiday.get('offset', 0)
            from datetime import timedelta
            return easter + timedelta(days=offset)
        elif holiday['dynamic'] == 'holi':
            # Approximate Holi date (full moon in Phalguna)
            # This is a simplified approximation
            # In reality, Holi is calculated based on the Hindu lunar calendar
            from dateutil.relativedelta import relativedelta
            from dateutil.easter import easter as calc_easter
            easter_date = calc_easter(year)
            # Holi is roughly 2 weeks before Easter in most years
            holi_date = easter_date - relativedelta(days=14)
            return holi_date
        elif holiday['dynamic'] == 'diwali':
            # Approximate Diwali date (new moon in Kartika)
            # Simplified calculation
            from dateutil.relativedelta import relativedelta
            from dateutil.easter import easter as calc_easter
            easter_date = calc_easter(year)
            # Diwali is roughly 6 months after Easter
            diwali_date = easter_date + relativedelta(months=6, days=15)
            return diwali_date
        elif holiday['dynamic'] == 'guru_nanak':
            # Approximate Guru Nanak Jayanti (full moon in Kartika)
            from dateutil.relativedelta import relativedelta
            from dateutil.easter import easter as calc_easter
            easter_date = calc_easter(year)
            guru_date = easter_date + relativedelta(months=6, days=20)
            return guru_date
        else:
            return None
    elif 'weekday' in holiday:
        return get_nth_weekday(year, holiday['month'], holiday['weekday'], holiday['week'])
    else:
        return date(year, holiday['month'], holiday['day'])


def get_holidays(year, country='US'):
    """
    Get all holidays for a given year and country.
    
    Args:
        year (int): The year
        country (str): Country code (US, UK, CA, AU, IN)
    
    Returns:
        dict: Dictionary mapping date strings to holiday information
    """
    if country not in HOLIDAY_DATA:
        raise ValueError(f"Country '{country}' not supported")
    
    holidays = {}
    
    for holiday in HOLIDAY_DATA[country]:
        try:
            holiday_date = get_holiday_date(year, holiday)
            if holiday_date:
                date_str = holiday_date.strftime('%Y-%m-%d')
                holidays[date_str] = {
                    'name': holiday['name'],
                    'type': holiday.get('type', 'unknown'),
                    'date': holiday_date
                }
        except Exception:
            # Skip holidays that can't be calculated
            continue
    
    return holidays
