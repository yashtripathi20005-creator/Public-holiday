"""
GUI interface for the Public Holiday Checker using tkinter.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime, date
from holiday_checker import HolidayChecker
from utils import format_date, display_holidays_table
import sys


class HolidayCheckerGUI:
    """Main GUI class for the Public Holiday Checker."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Public Holiday Checker")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Initialize holiday checker
        self.checker = HolidayChecker()
        
        # Setup UI
        self.setup_ui()
        
        # Current country
        self.current_country = tk.StringVar(value='US')
        
    def setup_ui(self):
        """Setup the user interface."""
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="Public Holiday Checker",
            font=('Helvetica', 18, 'bold')
        )
        title_label.grid(row=0, column=0, pady=(0, 10))
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create tabs
        self.create_check_tab()
        self.create_list_tab()
        self.create_upcoming_tab()
        self.create_search_tab()
        self.create_info_tab()
        
        # Status bar
        self.status_bar = ttk.Label(
            self.root,
            text="Ready",
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))
    
    def create_check_tab(self):
        """Create the 'Check Holiday' tab."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Check Holiday")
        
        # Country selection
        ttk.Label(tab, text="Country:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        country_var = tk.StringVar(value='US')
        country_combo = ttk.Combobox(
            tab,
            textvariable=country_var,
            values=sorted(self.checker.supported_countries),
            state='readonly',
            width=10
        )
        country_combo.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Date selection
        ttk.Label(tab, text="Date:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        date_var = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        date_entry = ttk.Entry(tab, textvariable=date_var, width=15)
        date_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Check button
        check_btn = ttk.Button(
            tab,
            text="Check Holiday",
            command=lambda: self.check_holiday(date_var.get(), country_var.get())
        )
        check_btn.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Result display
        self.check_result = scrolledtext.ScrolledText(
            tab,
            height=15,
            width=70,
            wrap=tk.WORD
        )
        self.check_result.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        # Configure grid weights
        tab.columnconfigure(0, weight=1)
        tab.columnconfigure(1, weight=1)
        tab.rowconfigure(3, weight=1)
    
    def create_list_tab(self):
        """Create the 'List Holidays' tab."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="List Holidays")
        
        # Country selection
        ttk.Label(tab, text="Country:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        country_var = tk.StringVar(value='US')
        country_combo = ttk.Combobox(
            tab,
            textvariable=country_var,
            values=sorted(self.checker.supported_countries),
            state='readonly',
            width=10
        )
        country_combo.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Year selection
        ttk.Label(tab, text="Year:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        year_var = tk.StringVar(value=str(datetime.now().year))
        year_entry = ttk.Entry(tab, textvariable=year_var, width=10)
        year_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
        # List button
        list_btn = ttk.Button(
            tab,
            text="List Holidays",
            command=lambda: self.list_holidays(year_var.get(), country_var.get())
        )
        list_btn.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Result display
        self.list_result = scrolledtext.ScrolledText(
            tab,
            height=15,
            width=70,
            wrap=tk.WORD
        )
        self.list_result.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        # Configure grid weights
        tab.columnconfigure(0, weight=1)
        tab.columnconfigure(1, weight=1)
        tab.rowconfigure(3, weight=1)
    
    def create_upcoming_tab(self):
        """Create the 'Upcoming Holidays' tab."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Upcoming Holidays")
        
        # Country selection
        ttk.Label(tab, text="Country:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        country_var = tk.StringVar(value='US')
        country_combo = ttk.Combobox(
            tab,
            textvariable=country_var,
            values=sorted(self.checker.supported_countries),
            state='readonly',
            width=10
        )
        country_combo.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Days selection
        ttk.Label(tab, text="Days ahead:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        days_var = tk.StringVar(value='30')
        days_entry = ttk.Entry(tab, textvariable=days_var, width=10)
        days_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Show button
        show_btn = ttk.Button(
            tab,
            text="Show Upcoming Holidays",
            command=lambda: self.show_upcoming(days_var.get(), country_var.get())
        )
        show_btn.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Result display
        self.upcoming_result = scrolledtext.ScrolledText(
            tab,
            height=15,
            width=70,
            wrap=tk.WORD
        )
        self.upcoming_result.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        # Configure grid weights
        tab.columnconfigure(0, weight=1)
        tab.columnconfigure(1, weight=1)
        tab.rowconfigure(3, weight=1)
    
    def create_search_tab(self):
        """Create the 'Search Holidays' tab."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Search Holidays")
        
        # Country selection
        ttk.Label(tab, text="Country:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        country_var = tk.StringVar(value='US')
        country_combo = ttk.Combobox(
            tab,
            textvariable=country_var,
            values=sorted(self.checker.supported_countries),
            state='readonly',
            width=10
        )
        country_combo.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Search query
        ttk.Label(tab, text="Search query:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        query_var = tk.StringVar()
        query_entry = ttk.Entry(tab, textvariable=query_var, width=30)
        query_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Search button
        search_btn = ttk.Button(
            tab,
            text="Search",
            command=lambda: self.search_holidays(query_var.get(), country_var.get())
        )
        search_btn.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Result display
        self.search_result = scrolledtext.ScrolledText(
            tab,
            height=15,
            width=70,
            wrap=tk.WORD
        )
        self.search_result.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        # Configure grid weights
        tab.columnconfigure(0, weight=1)
        tab.columnconfigure(1, weight=1)
        tab.rowconfigure(3, weight=1)
    
    def create_info_tab(self):
        """Create the 'Info' tab."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="About")
        
        info_text = """
Public Holiday Checker v1.0

A comprehensive application to check public holidays
for different countries around the world.

Features:
• Check if a specific date is a public holiday
• List all holidays for a given year
• View upcoming holidays
• Search for holidays by name
• Support for multiple countries

Supported Countries:
• United States (US)
• United Kingdom (UK)
• Canada (CA)
• Australia (AU)
• India (IN)

Data includes:
• Federal/National holidays
• Bank holidays
• Provincial holidays
• Cultural celebrations

Created with Python using:
• tkinter for GUI
• Custom holiday data
• Caching for performance

License: MIT
        """
        
        info_display = scrolledtext.ScrolledText(
            tab,
            height=20,
            width=70,
            wrap=tk.WORD
        )
        info_display.insert(tk.END, info_text)
        info_display.config(state=tk.DISABLED)
        info_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    
    def check_holiday(self, date_str, country):
        """Check if a date is a holiday."""
        try:
            check_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD")
            return
        
        self.check_result.delete(1.0, tk.END)
        self.status_bar.config(text="Checking holiday...")
        
        try:
            is_holiday, holiday_name = self.checker.is_holiday(check_date, country)
            
            self.check_result.insert(tk.END, f"Date: {format_date(check_date)} ({check_date.strftime('%A')})\n")
            self.check_result.insert(tk.END, f"Country: {country}\n")
            self.check_result.insert(tk.END, "-" * 40 + "\n\n")
            
            if is_holiday:
                self.check_result.insert(tk.END, "✓ It's a public holiday! 🎉\n\n", "holiday")
                self.check_result.insert(tk.END, f"Holiday: {holiday_name}\n")
                self.check_result.tag_config("holiday", foreground="green", font=('TkDefaultFont', 10, 'bold'))
            else:
                self.check_result.insert(tk.END, "✗ Not a public holiday.\n\n", "no_holiday")
                self.check_result.tag_config("no_holiday", foreground="orange", font=('TkDefaultFont', 10, 'bold'))
            
            # Show other holidays in the month
            holidays = self.checker.get_holidays(check_date.year, country)
            month_holidays = {k: v for k, v in holidays.items() 
                            if k.startswith(f"{check_date.year}-{check_date.month:02d}")}
            
            if month_holidays:
                self.check_result.insert(tk.END, f"\nOther holidays in {check_date.strftime('%B')} {check_date.year}:\n")
                for date_str, info in sorted(month_holidays.items()):
                    self.check_result.insert(tk.END, f"  • {date_str}: {info['name']}\n")
            
            self.status_bar.config(text=f"Checked date: {format_date(check_date)}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to check holiday: {str(e)}")
            self.status_bar.config(text="Error occurred")
    
    def list_holidays(self, year_str, country):
        """List all holidays for a year."""
        try:
            year = int(year_str)
            if year < 1900 or year > 2100:
                raise ValueError("Year must be between 1900 and 2100")
        except ValueError:
            messagebox.showerror("Error", "Invalid year. Please enter a valid year between 1900 and 2100")
            return
        
        self.list_result.delete(1.0, tk.END)
        self.status_bar.config(text="Loading holidays...")
        
        try:
            holidays = self.checker.get_holidays(year, country)
            
            self.list_result.insert(tk.END, f"Holidays in {country} - {year}\n")
            self.list_result.insert(tk.END, f"Total: {len(holidays)} holidays\n")
            self.list_result.insert(tk.END, "=" * 50 + "\n\n")
            
            if holidays:
                # Group by month
                current_month = None
                for date_str, info in sorted(holidays.items()):
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
                    month_name = date_obj.strftime('%B')
                    
                    if month_name != current_month:
                        current_month = month_name
                        self.list_result.insert(tk.END, f"\n{month_name}:\n", "month")
                        self.list_result.tag_config("month", foreground="blue", font=('TkDefaultFont', 10, 'bold'))
                    
                    self.list_result.insert(tk.END, f"  {date_str} ({date_obj.strftime('%A')}): ")
                    self.list_result.insert(tk.END, f"{info['name']}\n", "holiday_name")
                    self.list_result.tag_config("holiday_name", foreground="green")
            else:
                self.list_result.insert(tk.END, "No holidays found for this year.")
            
            self.status_bar.config(text=f"Loaded {len(holidays)} holidays for {country} {year}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to list holidays: {str(e)}")
            self.status_bar.config(text="Error occurred")
    
    def show_upcoming(self, days_str, country):
        """Show upcoming holidays."""
        try:
            days = int(days_str)
            if days <= 0:
                raise ValueError("Days must be positive")
        except ValueError:
            messagebox.showerror("Error", "Invalid number of days. Please enter a positive number")
            return
        
        self.upcoming_result.delete(1.0, tk.END)
        self.status_bar.config(text="Loading upcoming holidays...")
        
        try:
            holidays = self.checker.get_upcoming_holidays(country, days)
            
            self.upcoming_result.insert(tk.END, f"Upcoming Holidays in {country}\n")
            self.upcoming_result.insert(tk.END, f"Next {days} days (from {datetime.now().strftime('%Y-%m-%d')})\n")
            self.upcoming_result.insert(tk.END, "=" * 50 + "\n\n")
            
            if holidays:
                for holiday in holidays:
                    self.upcoming_result.insert(tk.END, f"{format_date(holiday['date'])} ({holiday['date'].strftime('%A')})\n")
                    self.upcoming_result.insert(tk.END, f"  Holiday: {holiday['name']}\n")
                    self.upcoming_result.insert(tk.END, f"  Type: {holiday['type']}\n")
                    self.upcoming_result.insert(tk.END, f"  Days until: {holiday['days_until']}\n\n")
            else:
                self.upcoming_result.insert(tk.END, f"No holidays found in the next {days} days.")
            
            self.status_bar.config(text=f"Found {len(holidays)} upcoming holidays")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get upcoming holidays: {str(e)}")
            self.status_bar.config(text="Error occurred")
    
    def search_holidays(self, query, country):
        """Search for holidays by name."""
        if not query:
            messagebox.showwarning("Warning", "Please enter a search query")
            return
        
        self.search_result.delete(1.0, tk.END)
        self.status_bar.config(text="Searching holidays...")
        
        try:
            results = self.checker.search_holidays(query, country)
            
            self.search_result.insert(tk.END, f"Search Results in {country}\n")
            self.search_result.insert(tk.END, f"Query: '{query}'\n")
            self.search_result.insert(tk.END, "=" * 50 + "\n\n")
            
            if results:
                self.search_result.insert(tk.END, f"Found {len(results)} matching holidays:\n\n")
                for i, holiday in enumerate(results, 1):
                    self.search_result.insert(tk.END, f"{i}. {holiday['name']}\n")
                    self.search_result.insert(tk.END, f"   Type: {holiday.get('type', 'unknown')}\n")
                    if 'month' in holiday and holiday['month']:
                        date_info = f"{holiday['month']}/{holiday.get('day', '?')}"
                        if 'weekday' in holiday:
                            date_info += f" (week {holiday.get('week', '?')})"
                        self.search_result.insert(tk.END, f"   Date: {date_info}\n")
                    self.search_result.insert(tk.END, "\n")
            else:
                self.search_result.insert(tk.END, f"No holidays found matching '{query}'.")
            
            self.status_bar.config(text=f"Found {len(results)} matching holidays")
            
        except Exception as e:
            messagebox.showerror("Error", f"Search failed: {str(e)}")
            self.status_bar.config(text="Error occurred")
    
    def run(self):
        """Run the GUI application."""
        try:
            self.root.mainloop()
        except Exception as e:
            messagebox.showerror("Fatal Error", f"Failed to start GUI: {str(e)}")
            sys.exit(1)
