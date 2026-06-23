"""
Unit tests for the Public Holiday Checker.
"""

import unittest
from datetime import date, datetime
from holiday_checker import HolidayChecker
from holiday_data import get_holidays, get_nth_weekday, calculate_easter


class TestHolidayData(unittest.TestCase):
    """Test holiday data functions."""
    
    def test_get_nth_weekday(self):
        """Test getting nth weekday of a month."""
        # Test Thanksgiving 2026 (4th Thursday in November)
        thanksgiving = get_nth_weekday(2026, 11, 3, 4)
        self.assertEqual(thanksgiving, date(2026, 11, 26))
        
        # Test last Monday in May 2026 (Memorial Day)
        memorial_day = get_nth_weekday(2026, 5, 0, -1)
        self.assertEqual(memorial_day, date(2026, 5, 25))
        
        # Test first Monday in September 2026 (Labor Day)
        labor_day = get_nth_weekday(2026, 9, 0, 1)
        self.assertEqual(labor_day, date(2026, 9, 7))
    
    def test_calculate_easter(self):
        """Test Easter calculation."""
        easter_2026 = calculate_easter(2026)
        self.assertEqual(easter_2026, date(2026, 4, 5))
        
        easter_2025 = calculate_easter(2025)
        self.assertEqual(easter_2025, date(2025, 4, 20))
        
        easter_2024 = calculate_easter(2024)
        self.assertEqual(easter_2024, date(2024, 3, 31))
    
    def test_get_holidays_us(self):
        """Test getting US holidays."""
        holidays = get_holidays(2026, 'US')
        
        # Check some fixed holidays
        self.assertIn('2026-01-01', holidays)
        self.assertEqual(holidays['2026-01-01']['name'], "New Year's Day")
        
        self.assertIn('2026-07-04', holidays)
        self.assertEqual(holidays['2026-07-04']['name'], "Independence Day")
        
        self.assertIn('2026-12-25', holidays)
        self.assertEqual(holidays['2026-12-25']['name'], "Christmas Day")
        
        # Check some variable holidays
        self.assertIn('2026-11-26', holidays)
        self.assertEqual(holidays['2026-11-26']['name'], "Thanksgiving Day")
    
    def test_get_holidays_invalid_country(self):
        """Test getting holidays for invalid country."""
        with self.assertRaises(ValueError):
            get_holidays(2026, 'XX')


class TestHolidayChecker(unittest.TestCase):
    """Test HolidayChecker class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.checker = HolidayChecker(cache_enabled=False)
    
    def test_is_holiday(self):
        """Test checking if a date is a holiday."""
        # Test a known holiday
        is_holiday, name = self.checker.is_holiday(date(2026, 1, 1), 'US')
        self.assertTrue(is_holiday)
        self.assertEqual(name, "New Year's Day")
        
        # Test a non-holiday
        is_holiday, name = self.checker.is_holiday(date(2026, 1, 2), 'US')
        self.assertFalse(is_holiday)
        self.assertIsNone(name)
        
        # Test a variable holiday
        is_holiday, name = self.checker.is_holiday(date(2026, 11, 26), 'US')
        self.assertTrue(is_holiday)
        self.assertEqual(name, "Thanksgiving Day")
    
    def test_get_holidays(self):
        """Test getting all holidays for a year."""
        holidays = self.checker.get_holidays(2026, 'US')
        self.assertIsInstance(holidays, dict)
        self.assertGreater(len(holidays), 5)
    
    def test_get_upcoming_holidays(self):
        """Test getting upcoming holidays."""
        # This test might need adjustment based on current date
        holidays = self.checker.get_upcoming_holidays('US', 365)
        self.assertIsInstance(holidays, list)
        
        # Should have at least some holidays
        self.assertGreater(len(holidays), 0)
        
        # Check that all holidays are in the future
        today = date.today()
        for holiday in holidays:
            self.assertGreaterEqual(holiday['date'], today)
    
    def test_get_supported_countries(self):
        """Test getting supported countries."""
        countries = self.checker.get_supported_countries()
        self.assertIsInstance(countries, dict)
        self.assertIn('US', countries)
        self.assertIn('UK', countries)
        self.assertIn('CA', countries)
        self.assertIn('AU', countries)
        self.assertIn('IN', countries)
    
    def test_search_holidays(self):
        """Test searching for holidays."""
        results = self.checker.search_holidays('Christmas', 'US')
        self.assertGreater(len(results), 0)
        self.assertTrue(any('Christmas' in h['name'] for h in results))
        
        results = self.checker.search_holidays('Nonexistent', 'US')
        self.assertEqual(len(results), 0)
    
    def test_get_holiday_types(self):
        """Test getting holiday types."""
        types = self.checker.get_holiday_types('US')
        self.assertIsInstance(types, list)
        self.assertIn('federal', types)
    
    def test_invalid_country(self):
        """Test invalid country handling."""
        with self.assertRaises(ValueError):
            self.checker.get_holidays(2026, 'XX')
        
        with self.assertRaises(ValueError):
            self.checker.is_holiday(date(2026, 1, 1), 'XX')
        
        with self.assertRaises(ValueError):
            self.checker.get_upcoming_holidays('XX', 30)


if __name__ == '__main__':
    unittest.main()
