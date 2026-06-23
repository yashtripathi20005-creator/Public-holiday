"""
Core holiday checking functionality.
"""

from datetime import datetime, date
from typing import Dict, List, Optional, Tuple
import json
import os
from holiday_data import get_holidays, HOLIDAY_DATA
from config import CACHE_FILE, CACHE_DURATION_DAYS


class HolidayCache:
    """Cache for holiday data to improve performance."""
    
    def __init__(self, cache_file=CACHE_FILE):
        self.cache_file = cache_file
        self.cache = self._load_cache()
    
    def _load_cache(self):
        """Load cache from file."""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
    
    def _save_cache(self):
        """Save cache to file."""
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(self.cache, f)
        except IOError:
            pass
    
    def get(self, country, year):
        """Get cached holidays for a country and year."""
        key = f"{country}_{year}"
        if key in self.cache:
            # Check if cache is still valid
            cache_date = self.cache[key].get('cached_date', '')
            if cache_date:
                cached_dt = datetime.strptime(cache_date, '%Y-%m-%d')
                if (datetime.now() - cached_dt).days < CACHE_DURATION_DAYS:
                    return self.cache[key].get('holidays', {})
        return None
    
    def set(self, country, year, holidays):
        """Cache holidays for a country and year."""
        key = f"{country}_{year}"
        self.cache[key] = {
            'holidays': holidays,
            'cached_date': datetime.now().strftime('%Y-%m-%d')
        }
        self._save_cache()


class HolidayChecker:
    """Main class for checking public holidays."""
    
    def __init__(self, cache_enabled=True):
        self.cache = HolidayCache() if cache_enabled else None
        self.supported_countries = list(HOLIDAY_DATA.keys())
    
    def get_holidays(self, year: int, country: str = 'US') -> Dict[str, Dict]:
        """
        Get all holidays for a given year and country.
        
        Args:
            year (int): The year
            country (str): Country code
        
        Returns:
            dict: Dictionary of holidays
        """
        country = country.upper()
        if country not in self.supported_countries:
            raise ValueError(f"Country '{country}' not supported. Supported: {self.supported_countries}")
        
        # Check cache first
        if self.cache:
            cached_holidays = self.cache.get(country, year)
            if cached_holidays:
                return cached_holidays
        
        # Get holidays from data
        holidays = get_holidays(year, country)
        
        # Cache the results
        if self.cache:
            self.cache.set(country, year, holidays)
        
        return holidays
    
    def is_holiday(self, check_date: date, country: str = 'US') -> Tuple[bool, Optional[str]]:
        """
        Check if a specific date is a public holiday.
        
        Args:
            check_date (date): The date to check
            country (str): Country code
        
        Returns:
            tuple: (is_holiday, holiday_name)
        """
        holidays = self.get_holidays(check_date.year, country)
        date_str = check_date.strftime('%Y-%m-%d')
        
        if date_str in holidays:
            return True, holidays[date_str]['name']
        return False, None
    
    def get_upcoming_holidays(self, country: str = 'US', days: int = 30) -> List[Dict]:
        """
        Get upcoming holidays within a specified number of days.
        
        Args:
            country (str): Country code
            days (int): Number of days to look ahead
        
        Returns:
            list: List of upcoming holidays
        """
        today = date.today()
        end_date = today + date.timedelta(days=days)
        
        # Get holidays for the current year and next year if needed
        holidays = []
        current_year = today.year
        next_year = end_date.year
        
        year_holidays = self.get_holidays(current_year, country)
        if next_year != current_year:
            next_year_holidays = self.get_holidays(next_year, country)
            year_holidays.update(next_year_holidays)
        
        # Filter holidays within the date range
        for date_str, holiday_info in year_holidays.items():
            holiday_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            if today <= holiday_date <= end_date:
                holidays.append({
                    'date': holiday_date,
                    'name': holiday_info['name'],
                    'type': holiday_info['type'],
                    'days_until': (holiday_date - today).days
                })
        
        # Sort by date
        holidays.sort(key=lambda x: x['date'])
        return holidays
    
    def get_holiday_types(self, country: str = 'US') -> List[str]:
        """
        Get available holiday types for a country.
        
        Args:
            country (str): Country code
        
        Returns:
            list: List of holiday types
        """
        country = country.upper()
        if country not in HOLIDAY_DATA:
            raise ValueError(f"Country '{country}' not supported")
        
        types = set()
        for holiday in HOLIDAY_DATA[country]:
            types.add(holiday.get('type', 'unknown'))
        return sorted(list(types))
    
    def search_holidays(self, query: str, country: str = 'US') -> List[Dict]:
        """
        Search for holidays by name.
        
        Args:
            query (str): Search query
            country (str): Country code
        
        Returns:
            list: List of matching holidays
        """
        country = country.upper()
        if country not in HOLIDAY_DATA:
            raise ValueError(f"Country '{country}' not supported")
        
        results = []
        query_lower = query.lower()
        
        for holiday in HOLIDAY_DATA[country]:
            if query_lower in holiday['name'].lower():
                results.append(holiday)
        
        return results
    
    def get_supported_countries(self) -> Dict[str, str]:
        """
        Get all supported countries with their full names.
        
        Returns:
            dict: Country code to full name mapping
        """
        from config import SUPPORTED_COUNTRIES
        return SUPPORTED_COUNTRIES
