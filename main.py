"""
Main entry point for the Public Holiday Checker.
"""

import argparse
import sys
from datetime import datetime, date
from holiday_checker import HolidayChecker
from utils import (
    print_colored, display_holidays_table, display_upcoming_holidays,
    validate_date, validate_year, print_error, print_success,
    print_info, format_date, get_user_confirmation
)


def check_holiday(args):
    """Check if a specific date is a holiday."""
    checker = HolidayChecker()
    
    # Parse date
    if args.date:
        check_date = validate_date(args.date)
        if not check_date:
            print_error(f"Invalid date format: {args.date}. Use YYYY-MM-DD")
            return
    else:
        check_date = date.today()
    
    country = args.country.upper() if args.country else 'US'
    
    try:
        is_holiday, holiday_name = checker.is_holiday(check_date, country)
        
        print_info(f"\nChecking: {format_date(check_date)} ({check_date.strftime('%A')})")
        print_info(f"Country: {country}")
        
        if is_holiday:
            print_success(f"✓ It's a public holiday! 🎉")
            print_colored(f"  Holiday: {holiday_name}", 'green')
        else:
            print_colored("✗ Not a public holiday.", 'yellow')
            
        # Show other holidays in the same month
        month_holidays = checker.get_holidays(check_date.year, country)
        month_holidays = {k: v for k, v in month_holidays.items() 
                         if k.startswith(f"{check_date.year}-{check_date.month:02d}")}
        
        if month_holidays:
            print_info(f"\nOther holidays in {check_date.strftime('%B')} {check_date.year}:")
            display_holidays_table(month_holidays)
            
    except ValueError as e:
        print_error(str(e))
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")


def list_holidays(args):
    """List all holidays for a given year."""
    checker = HolidayChecker()
    
    year = args.year or datetime.now().year
    country = args.country.upper() if args.country else 'US'
    
    # Validate year
    if not validate_year(str(year)):
        print_error(f"Invalid year: {year}. Must be between 1900 and 2100")
        return
    
    try:
        holidays = checker.get_holidays(year, country)
        
        title = f"Holidays in {country} - {year} (Total: {len(holidays)})"
        display_holidays_table(holidays, title)
        
        # Show holiday types
        types = checker.get_holiday_types(country)
        print_info(f"\nHoliday types: {', '.join(types)}")
        
    except ValueError as e:
        print_error(str(e))
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")


def upcoming_holidays(args):
    """Show upcoming holidays."""
    checker = HolidayChecker()
    
    days = args.days or 30
    country = args.country.upper() if args.country else 'US'
    
    try:
        holidays = checker.get_upcoming_holidays(country, days)
        
        title = f"Upcoming Holidays in {country} (Next {days} days)"
        display_upcoming_holidays(holidays, title)
        
        if not holidays:
            print_info("No holidays found in the next {days} days.")
            
    except ValueError as e:
        print_error(str(e))
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")


def search_holidays(args):
    """Search for holidays by name."""
    checker = HolidayChecker()
    
    query = args.query
    country = args.country.upper() if args.country else 'US'
    
    if not query:
        print_error("Please provide a search query")
        return
    
    try:
        results = checker.search_holidays(query, country)
        
        if results:
            print_info(f"\nFound {len(results)} matching holidays in {country}:")
            for i, holiday in enumerate(results, 1):
                print_colored(f"{i}. {holiday['name']}", 'cyan')
                print(f"   Type: {holiday.get('type', 'unknown')}")
                print(f"   Date: {holiday.get('month', 'N/A')}/{holiday.get('day', 'N/A')}")
                print()
        else:
            print_info(f"No holidays found matching '{query}' in {country}")
            
    except ValueError as e:
        print_error(str(e))
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")


def gui_mode():
    """Launch the GUI interface."""
    try:
        from gui import HolidayCheckerGUI
        app = HolidayCheckerGUI()
        app.run()
    except ImportError:
        print_error("GUI dependencies not installed. Please install: pip install tkinter")
        print_info("Or use the command-line interface instead.")
    except Exception as e:
        print_error(f"Failed to start GUI: {str(e)}")


def interactive_mode():
    """Run in interactive mode."""
    checker = HolidayChecker()
    
    print_colored("\n" + "=" * 50, 'cyan', bold=True)
    print_colored("   PUBLIC HOLIDAY CHECKER - Interactive Mode", 'cyan', bold=True)
    print_colored("=" * 50 + "\n", 'cyan', bold=True)
    
    while True:
        print_colored("\nOptions:", 'yellow', bold=True)
        print("1. Check if a date is a holiday")
        print("2. List all holidays for a year")
        print("3. View upcoming holidays")
        print("4. Search for holidays")
        print("5. Change country")
        print("6. Show supported countries")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == '1':
            # Check date
            while True:
                date_str = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
                if not date_str:
                    check_date = date.today()
                    break
                check_date = validate_date(date_str)
                if check_date:
                    break
                print_error("Invalid date format. Use YYYY-MM-DD")
            
            country = input("Enter country code (or press Enter for US): ").strip() or 'US'
            try:
                is_holiday, holiday_name = checker.is_holiday(check_date, country.upper())
                print_info(f"\n{format_date(check_date)} ({check_date.strftime('%A')})")
                if is_holiday:
                    print_success(f"✓ It's {holiday_name}! 🎉")
                else:
                    print_colored("✗ Not a public holiday.", 'yellow')
            except ValueError as e:
                print_error(str(e))
        
        elif choice == '2':
            # List holidays
            year_str = input("Enter year (or press Enter for current year): ").strip()
            year = int(year_str) if year_str else datetime.now().year
            country = input("Enter country code (or press Enter for US): ").strip() or 'US'
            try:
                holidays = checker.get_holidays(year, country.upper())
                title = f"Holidays in {country.upper()} - {year}"
                display_holidays_table(holidays, title)
            except ValueError as e:
                print_error(str(e))
        
        elif choice == '3':
            # Upcoming holidays
            days_str = input("Enter number of days to look ahead (or press Enter for 30): ").strip()
            days = int(days_str) if days_str else 30
            country = input("Enter country code (or press Enter for US): ").strip() or 'US'
            try:
                holidays = checker.get_upcoming_holidays(country.upper(), days)
                title = f"Upcoming Holidays in {country.upper()} (Next {days} days)"
                display_upcoming_holidays(holidays, title)
            except ValueError as e:
                print_error(str(e))
        
        elif choice == '4':
            # Search holidays
            query = input("Enter search query: ").strip()
            country = input("Enter country code (or press Enter for US): ").strip() or 'US'
            if query:
                try:
                    results = checker.search_holidays(query, country.upper())
                    if results:
                        print_info(f"\nFound {len(results)} matching holidays:")
                        for holiday in results:
                            print_colored(f"• {holiday['name']}", 'cyan')
                    else:
                        print_info(f"No holidays found matching '{query}'")
                except ValueError as e:
                    print_error(str(e))
            else:
                print_error("Please enter a search query")
        
        elif choice == '5':
            # Change country
            print_info("\nSupported countries:")
            for code, name in checker.get_supported_countries().items():
                print(f"  {code}: {name}")
            new_country = input("\nEnter new country code: ").strip().upper()
            if new_country in checker.supported_countries:
                print_success(f"Country changed to {new_country}")
            else:
                print_error(f"Country '{new_country}' not supported")
        
        elif choice == '6':
            # Show supported countries
            print_info("\nSupported countries:")
            for code, name in checker.get_supported_countries().items():
                print_colored(f"  {code}: {name}", 'green')
        
        elif choice == '7':
            print_info("\nGoodbye! 👋")
            break
        
        else:
            print_error("Invalid choice. Please enter 1-7")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Public Holiday Checker',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py check --date 2026-01-01 --country US
  python main.py list --year 2026 --country UK
  python main.py upcoming --days 30 --country CA
  python main.py search --query Christmas --country AU
  python main.py --interactive
  python main.py --gui
        """
    )
    
    parser.add_argument('--gui', action='store_true', help='Launch GUI interface')
    parser.add_argument('--interactive', '-i', action='store_true', help='Run in interactive mode')
    parser.add_argument('--country', help='Country code (US, UK, CA, AU, IN)', default='US')
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Check command
    check_parser = subparsers.add_parser('check', help='Check if a date is a holiday')
    check_parser.add_argument('--date', help='Date in YYYY-MM-DD format (default: today)')
    check_parser.add_argument('--country', help='Country code', default='US')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List all holidays for a year')
    list_parser.add_argument('--year', type=int, help='Year (default: current year)')
    list_parser.add_argument('--country', help='Country code', default='US')
    
    # Upcoming command
    upcoming_parser = subparsers.add_parser('upcoming', help='Show upcoming holidays')
    upcoming_parser.add_argument('--days', type=int, help='Number of days to look ahead', default=30)
    upcoming_parser.add_argument('--country', help='Country code', default='US')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search for holidays by name')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('--country', help='Country code', default='US')
    
    args = parser.parse_args()
    
    # Handle GUI mode
    if args.gui:
        gui_mode()
        return
    
    # Handle interactive mode
    if args.interactive:
        interactive_mode()
        return
    
    # Handle commands
    if args.command == 'check':
        check_holiday(args)
    elif args.command == 'list':
        list_holidays(args)
    elif args.command == 'upcoming':
        upcoming_holidays(args)
    elif args.command == 'search':
        search_holidays(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGoodbye! 👋")
        sys.exit(0)
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")
        sys.exit(1)
