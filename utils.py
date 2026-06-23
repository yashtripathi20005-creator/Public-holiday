"""
Utility functions for the Public Holiday Checker.
"""

from datetime import datetime, date
from typing import Optional
from prettytable import PrettyTable
from colorama import init, Fore, Style
import sys

# Initialize colorama for cross-platform colored output
init(autoreset=True)


def print_colored(text: str, color: str = 'white', bold: bool = False):
    """Print colored text to the console."""
    color_map = {
        'red': Fore.RED,
        'green': Fore.GREEN,
        'yellow': Fore.YELLOW,
        'blue': Fore.BLUE,
        'magenta': Fore.MAGENTA,
        'cyan': Fore.CYAN,
        'white': Fore.WHITE,
        'reset': Style.RESET_ALL
    }
    
    color_code = color_map.get(color, Fore.WHITE)
    style_code = Style.BRIGHT if bold else ''
    print(f"{style_code}{color_code}{text}{Style.RESET_ALL}")


def format_date(date_obj: date) -> str:
    """Format a date object as a string."""
    return date_obj.strftime('%Y-%m-%d')


def format_holiday_display(holiday_info: dict) -> str:
    """Format holiday information for display."""
    name = holiday_info.get('name', 'Unknown')
    holiday_type = holiday_info.get('type', 'unknown')
    date_obj = holiday_info.get('date')
    
    if date_obj:
        date_str = format_date(date_obj)
        day_of_week = date_obj.strftime('%A')
        return f"{name} ({holiday_type}) - {date_str} ({day_of_week})"
    return f"{name} ({holiday_type})"


def display_holidays_table(holidays: dict, title: str = None):
    """
    Display holidays in a formatted table.
    
    Args:
        holidays (dict): Dictionary of holidays
        title (str): Optional title for the table
    """
    if not holidays:
        print_colored("No holidays found.", 'yellow')
        return
    
    table = PrettyTable()
    table.field_names = ["Date", "Holiday", "Type", "Day"]
    table.align["Holiday"] = "l"
    
    for date_str, info in sorted(holidays.items()):
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        day_of_week = date_obj.strftime('%A')
        table.add_row([
            date_str,
            info['name'],
            info.get('type', 'unknown'),
            day_of_week
        ])
    
    if title:
        print_colored(f"\n{title}", 'cyan', bold=True)
    print(table)


def display_upcoming_holidays(holidays: list, title: str = None):
    """
    Display upcoming holidays in a formatted table.
    
    Args:
        holidays (list): List of upcoming holidays
        title (str): Optional title for the table
    """
    if not holidays:
        print_colored("No upcoming holidays found.", 'yellow')
        return
    
    table = PrettyTable()
    table.field_names = ["Date", "Holiday", "Type", "Days Until"]
    table.align["Holiday"] = "l"
    
    for holiday in holidays:
        table.add_row([
            format_date(holiday['date']),
            holiday['name'],
            holiday['type'],
            holiday['days_until']
        ])
    
    if title:
        print_colored(f"\n{title}", 'cyan', bold=True)
    print(table)


def validate_date(date_str: str) -> Optional[date]:
    """
    Validate and parse a date string.
    
    Args:
        date_str (str): Date string in YYYY-MM-DD format
    
    Returns:
        date: Parsed date object or None if invalid
    """
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return None


def validate_year(year_str: str) -> Optional[int]:
    """
    Validate and parse a year string.
    
    Args:
        year_str (str): Year string
    
    Returns:
        int: Parsed year or None if invalid
    """
    try:
        year = int(year_str)
        if 1900 <= year <= 2100:
            return year
        return None
    except ValueError:
        return None


def get_user_confirmation(prompt: str, default: bool = True) -> bool:
    """
    Get user confirmation for an action.
    
    Args:
        prompt (str): Prompt to display
        default (bool): Default choice (True for yes, False for no)
    
    Returns:
        bool: True if confirmed, False otherwise
    """
    default_str = "[Y/n]" if default else "[y/N]"
    response = input(f"{prompt} {default_str} ").strip().lower()
    
    if not response:
        return default
    
    return response in ['y', 'yes']


def print_error(message: str):
    """Print an error message in red."""
    print_colored(f"Error: {message}", 'red', bold=True)


def print_success(message: str):
    """Print a success message in green."""
    print_colored(f"Success: {message}", 'green', bold=True)


def print_info(message: str):
    """Print an informational message in blue."""
    print_colored(message, 'blue')


def print_warning(message: str):
    """Print a warning message in yellow."""
    print_colored(f"Warning: {message}", 'yellow', bold=True)


def create_holiday_summary(holidays: dict) -> str:
    """
    Create a summary string of holidays.
    
    Args:
        holidays (dict): Dictionary of holidays
    
    Returns:
        str: Summary string
    """
    if not holidays:
        return "No holidays found."
    
    summary = []
    for date_str, info in sorted(holidays.items()):
        summary.append(f"{date_str}: {info['name']}")
    
    return "\n".join(summary)
