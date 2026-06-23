"""
Configuration settings for the Public Holiday Checker.
"""

# Supported countries and their codes
SUPPORTED_COUNTRIES = {
    'US': 'United States',
    'UK': 'United Kingdom',
    'CA': 'Canada',
    'AU': 'Australia',
    'IN': 'India'
}

# Date format for input/output
DATE_FORMAT = '%Y-%m-%d'

# Default country if none specified
DEFAULT_COUNTRY = 'US'

# API endpoints (for future expansion)
HOLIDAY_API_URL = 'https://date.nager.at/api/v3'

# File paths
DATA_DIR = 'data'
CACHE_FILE = 'holiday_cache.json'

# Logging configuration
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# GUI settings
GUI_TITLE = 'Public Holiday Checker'
GUI_WIDTH = 800
GUI_HEIGHT = 600

# Cache settings
CACHE_DURATION_DAYS = 30
