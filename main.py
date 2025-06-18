import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage
import requests
import json
from datetime import datetime, timedelta
import threading
import os


class WeatherApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Weather Forecast App")
        self.root.geometry("1000x700")
        self.root.configure(bg='#2c3e50')

        # API configuration
        self.api_key = ""
        self.current_weather_url = "http://api.openweathermap.org/data/2.5/weather"
        self.forecast_url = "http://api.openweathermap.org/data/2.5/forecast"
        self.geocoding_url = "http://api.openweathermap.org/geo/1.0/direct"

        # Weather icons mapping
        self.weather_icons = {
            '01d': '☀️', '01n': '🌙', '02d': '⛅', '02n': '☁️',
            '03d': '☁️', '03n': '☁️', '04d': '☁️', '04n': '☁️',
            '09d': '🌧️', '09n': '🌧️', '10d': '🌦️', '10n': '🌧️',
            '11d': '⛈️', '11n': '⛈️', '13d': '❄️', '13n': '❄️',
            '50d': '🌫️', '50n': '🌫️'
        }

        self.setup_ui()
        self.setup_api_key()

    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Title
        title_label = tk.Label(main_frame, text="🌤️ Weather Forecast",
                               font=('Arial', 24, 'bold'),
                               fg='#ecf0f1', bg='#2c3e50')
        title_label.pack(pady=(0, 20))

        # Search frame
        search_frame = tk.Frame(main_frame, bg='#2c3e50')
        search_frame.pack(fill='x', pady=(0, 20))

        # Location input
        input_frame = tk.Frame(search_frame, bg='#2c3e50')
        input_frame.pack(side='left', fill='x', expand=True)

        tk.Label(input_frame, text="Enter Location:",
                 font=('Arial', 12), fg='#ecf0f1', bg='#2c3e50').pack(side='left')

        self.location_var = tk.StringVar()
        self.location_entry = tk.Entry(input_frame, textvariable=self.location_var,
                                       font=('Arial', 12), width=30)
        self.location_entry.pack(side='left', padx=(10, 0))
        self.location_entry.bind('<Return>', lambda e: self.get_weather())

        # Buttons frame
        button_frame = tk.Frame(search_frame, bg='#2c3e50')
        button_frame.pack(side='right', padx=(10, 0))

        self.search_btn = tk.Button(button_frame, text="Get Weather",
                                    command=self.get_weather,
                                    bg='#3498db', fg='white',
                                    font=('Arial', 10, 'bold'),
                                    relief='flat', padx=20)
        self.search_btn.pack(side='left', padx=(0, 5))

        self.gps_btn = tk.Button(button_frame, text="📍 Use GPS",
                                 command=self.get_gps_location,
                                 bg='#e74c3c', fg='white',
                                 font=('Arial', 10, 'bold'),
                                 relief='flat', padx=15)
        self.gps_btn.pack(side='left')

        # Main content notebook
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill='both', expand=True)

        # Current weather tab
        self.current_frame = tk.Frame(self.notebook, bg='#34495e')
        self.notebook.add(self.current_frame, text="Current Weather")

        # Hourly forecast tab
        self.hourly_frame = tk.Frame(self.notebook, bg='#34495e')
        self.notebook.add(self.hourly_frame, text="Hourly Forecast")

        # Daily forecast tab
        self.daily_frame = tk.Frame(self.notebook, bg='#34495e')
        self.notebook.add(self.daily_frame, text="5-Day Forecast")

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready - Enter a location to get weather data")
        status_bar = tk.Label(main_frame, textvariable=self.status_var,
                              bg='#2c3e50', fg='#95a5a6',
                              font=('Arial', 9), anchor='w')
        status_bar.pack(fill='x', side='bottom', pady=(10, 0))

        self.setup_current_weather_ui()
        self.setup_hourly_forecast_ui()
        self.setup_daily_forecast_ui()

    def setup_api_key(self):
        self.api_key = os.environ.get('WEATHER_API_KEY')
        if not self.api_key:
            api_dialog = ApiKeyDialog(self.root)
            self.root.wait_window(api_dialog.dialog)
            self.api_key = api_dialog.api_key
            if not self.api_key:
                messagebox.showerror("Error", "API key is required to use this app")
                self.root.quit()

    def setup_current_weather_ui(self):
        # Main weather display
        self.current_main = tk.Frame(self.current_frame, bg='#34495e')
        self.current_main.pack(fill='both', expand=True, padx=20, pady=20)

        # Location and time
        self.location_label = tk.Label(self.current_main, text="",
                                       font=('Arial', 18, 'bold'),
                                       fg='#ecf0f1', bg='#34495e')
        self.location_label.pack(pady=(0, 10))

        self.time_label = tk.Label(self.current_main, text="",
                                   font=('Arial', 12),
                                   fg='#bdc3c7', bg='#34495e')
        self.time_label.pack(pady=(0, 20))

        # Weather info frame
        weather_info = tk.Frame(self.current_main, bg='#34495e')
        weather_info.pack(fill='x', pady=(0, 20))

        # Left side - main weather
        left_weather = tk.Frame(weather_info, bg='#34495e')
        left_weather.pack(side='left', fill='both', expand=True)

        self.weather_icon = tk.Label(left_weather, text="",
                                     font=('Arial', 48),
                                     bg='#34495e')
        self.weather_icon.pack()

        self.temperature_label = tk.Label(left_weather, text="",
                                          font=('Arial', 36, 'bold'),
                                          fg='#ecf0f1', bg='#34495e')
        self.temperature_label.pack()

        self.description_label = tk.Label(left_weather, text="",
                                          font=('Arial', 14),
                                          fg='#bdc3c7', bg='#34495e')
        self.description_label.pack()

        # Right side - details
        right_details = tk.Frame(weather_info, bg='#34495e')
        right_details.pack(side='right', fill='both', expand=True)

        self.details_frame = tk.Frame(right_details, bg='#34495e')
        self.details_frame.pack(expand=True)

    def setup_hourly_forecast_ui(self):
        # Scrollable frame for hourly forecast
        canvas = tk.Canvas(self.hourly_frame, bg='#34495e')
        scrollbar = ttk.Scrollbar(self.hourly_frame, orient="horizontal", command=canvas.xview)
        self.hourly_scroll_frame = tk.Frame(canvas, bg='#34495e')

        self.hourly_scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.hourly_scroll_frame, anchor="nw")
        canvas.configure(xscrollcommand=scrollbar.set)

        canvas.pack(side="top", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="bottom", fill="x", padx=10)

    def setup_daily_forecast_ui(self):
        self.daily_scroll_frame = tk.Frame(self.daily_frame, bg='#34495e')
        self.daily_scroll_frame.pack(fill='both', expand=True, padx=20, pady=20)

    def get_weather(self):
        location = self.location_var.get().strip()
        if not location:
            messagebox.showwarning("Warning", "Please enter a location")
            return

        self.status_var.set("Fetching weather data...")
        self.search_btn.config(state='disabled')

        # Run API calls in separate thread to prevent UI freezing
        thread = threading.Thread(target=self._fetch_weather_data, args=(location,))
        thread.daemon = True
        thread.start()

    def _fetch_weather_data(self, location):
        try:
            # Get current weather
            current_params = {
                'q': location,
                'appid': self.api_key,
                'units': 'metric'
            }
            current_response = requests.get(self.current_weather_url, params=current_params, timeout=10)
            current_response.raise_for_status()
            current_data = current_response.json()

            # Get forecast data
            forecast_params = {
                'q': location,
                'appid': self.api_key,
                'units': 'metric'
            }
            forecast_response = requests.get(self.forecast_url, params=forecast_params, timeout=10)
            forecast_response.raise_for_status()
            forecast_data = forecast_response.json()

            # Update UI on main thread
            self.root.after(0, self._update_weather_display, current_data, forecast_data)

        except requests.exceptions.RequestException as e:
            self.root.after(0, self._handle_error, f"Network error: {str(e)}")
        except json.JSONDecodeError:
            self.root.after(0, self._handle_error, "Invalid response from weather service")
        except Exception as e:
            self.root.after(0, self._handle_error, f"Error: {str(e)}")

    def _update_weather_display(self, current_data, forecast_data):
        if current_data.get('cod') != 200:
            self._handle_error(current_data.get('message', 'Unknown error'))
            return

        # Update current weather
        self._update_current_weather(current_data)

        # Update forecasts
        self._update_hourly_forecast(forecast_data)
        self._update_daily_forecast(forecast_data)

        self.status_var.set("Weather data updated successfully")
        self.search_btn.config(state='normal')

    def _update_current_weather(self, data):
        city = data['name']
        country = data['sys']['country']
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        description = data['weather'][0]['description'].title()
        icon_code = data['weather'][0]['icon']
        wind_speed = data['wind']['speed']
        wind_deg = data.get('wind', {}).get('deg', 0)
        visibility = data.get('visibility', 0) / 1000 if data.get('visibility') else 0

        timestamp = datetime.fromtimestamp(data['dt'])

        # Update labels
        self.location_label.config(text=f"{city}, {country}")
        self.time_label.config(text=f"Last updated: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        self.weather_icon.config(text=self.weather_icons.get(icon_code, '🌤️'))
        self.temperature_label.config(text=f"{temp:.1f}°C")
        self.description_label.config(text=description)

        # Clear and update details
        for widget in self.details_frame.winfo_children():
            widget.destroy()

        details = [
            ("Feels like", f"{feels_like:.1f}°C"),
            ("Humidity", f"{humidity}%"),
            ("Pressure", f"{pressure} hPa"),
            ("Wind Speed", f"{wind_speed} m/s"),
            ("Wind Direction", f"{wind_deg}°"),
            ("Visibility", f"{visibility:.1f} km")
        ]

        for i, (label, value) in enumerate(details):
            row = i // 2
            col = i % 2

            detail_frame = tk.Frame(self.details_frame, bg='#34495e')
            detail_frame.grid(row=row, column=col, padx=10, pady=5, sticky='w')

            tk.Label(detail_frame, text=f"{label}:",
                     font=('Arial', 10, 'bold'),
                     fg='#bdc3c7', bg='#34495e').pack(side='left')
            tk.Label(detail_frame, text=value,
                     font=('Arial', 10),
                     fg='#ecf0f1', bg='#34495e').pack(side='left', padx=(5, 0))

    def _update_hourly_forecast(self, data):
        # Clear existing hourly forecast
        for widget in self.hourly_scroll_frame.winfo_children():
            widget.destroy()

        # Display next 24 hours (8 entries * 3-hour intervals)
        for i, item in enumerate(data['list'][:8]):
            hour_frame = tk.Frame(self.hourly_scroll_frame, bg='#2c3e50', relief='solid', bd=1)
            hour_frame.pack(side='left', padx=5, pady=10, fill='y')

            time_dt = datetime.fromtimestamp(item['dt'])
            temp = item['main']['temp']
            icon_code = item['weather'][0]['icon']
            description = item['weather'][0]['description'].title()

            tk.Label(hour_frame, text=time_dt.strftime('%H:%M'),
                     font=('Arial', 10, 'bold'),
                     fg='#ecf0f1', bg='#2c3e50').pack(pady=5)

            tk.Label(hour_frame, text=self.weather_icons.get(icon_code, '🌤️'),
                     font=('Arial', 24),
                     bg='#2c3e50').pack()

            tk.Label(hour_frame, text=f"{temp:.1f}°C",
                     font=('Arial', 12, 'bold'),
                     fg='#ecf0f1', bg='#2c3e50').pack()

            tk.Label(hour_frame, text=description,
                     font=('Arial', 8),
                     fg='#bdc3c7', bg='#2c3e50',
                     wraplength=80).pack(pady=(0, 5))

    def _update_daily_forecast(self, data):
        # Clear existing daily forecast
        for widget in self.daily_scroll_frame.winfo_children():
            widget.destroy()

        # Group forecast data by day
        daily_data = {}
        for item in data['list']:
            date = datetime.fromtimestamp(item['dt']).date()
            if date not in daily_data:
                daily_data[date] = []
            daily_data[date].append(item)

        # Display up to 5 days
        for i, (date, day_items) in enumerate(list(daily_data.items())[:5]):
            day_frame = tk.Frame(self.daily_scroll_frame, bg='#2c3e50', relief='solid', bd=1)
            day_frame.pack(fill='x', padx=5, pady=5)

            # Calculate daily summary
            temps = [item['main']['temp'] for item in day_items]
            min_temp = min(temps)
            max_temp = max(temps)

            # Most common weather condition
            conditions = [item['weather'][0]['icon'] for item in day_items]
            most_common_icon = max(set(conditions), key=conditions.count)
            most_common_desc = day_items[0]['weather'][0]['description'].title()

            # Day header
            header_frame = tk.Frame(day_frame, bg='#2c3e50')
            header_frame.pack(fill='x', padx=10, pady=10)

            tk.Label(header_frame, text=date.strftime('%A, %B %d'),
                     font=('Arial', 14, 'bold'),
                     fg='#ecf0f1', bg='#2c3e50').pack(side='left')

            tk.Label(header_frame, text=self.weather_icons.get(most_common_icon, '🌤️'),
                     font=('Arial', 20),
                     bg='#2c3e50').pack(side='right', padx=(0, 10))

            tk.Label(header_frame, text=f"{max_temp:.1f}°/{min_temp:.1f}°C",
                     font=('Arial', 14, 'bold'),
                     fg='#ecf0f1', bg='#2c3e50').pack(side='right', padx=(0, 10))

            tk.Label(header_frame, text=most_common_desc,
                     font=('Arial', 12),
                     fg='#bdc3c7', bg='#2c3e50').pack(side='right', padx=(0, 20))

    def get_gps_location(self):
        self.status_var.set("Getting GPS location...")
        self.gps_btn.config(state='disabled')

        thread = threading.Thread(target=self._get_gps_location)
        thread.daemon = True
        thread.start()

    def _get_gps_location(self):
        try:
            # Use IP-based geolocation as GPS alternative
            response = requests.get('http://ip-api.com/json/', timeout=10)
            data = response.json()

            if data['status'] == 'success':
                city = data['city']
                self.root.after(0, self._update_gps_location, city)
            else:
                self.root.after(0, self._handle_gps_error, "Could not determine location")

        except Exception as e:
            self.root.after(0, self._handle_gps_error, f"GPS error: {str(e)}")

    def _update_gps_location(self, city):
        self.location_var.set(city)
        self.status_var.set(f"GPS location found: {city}")
        self.gps_btn.config(state='normal')
        self.get_weather()

    def _handle_gps_error(self, error_msg):
        self.status_var.set(f"GPS error: {error_msg}")
        self.gps_btn.config(state='normal')
        messagebox.showwarning("GPS Error", error_msg)

    def _handle_error(self, error_msg):
        self.status_var.set(f"Error: {error_msg}")
        self.search_btn.config(state='normal')
        messagebox.showerror("Error", error_msg)

    def run(self):
        self.root.mainloop()


class ApiKeyDialog:
    def __init__(self, parent):
        self.api_key = ""
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("API Key Required")
        self.dialog.geometry("500x300")
        self.dialog.configure(bg='#2c3e50')
        self.dialog.resizable(False, False)

        # Center the dialog
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Main frame
        main_frame = tk.Frame(self.dialog, bg='#2c3e50')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Title
        title = tk.Label(main_frame, text="🔑 API Key Setup",
                         font=('Arial', 18, 'bold'),
                         fg='#ecf0f1', bg='#2c3e50')
        title.pack(pady=(0, 20))

        # Instructions
        instructions = tk.Text(main_frame, height=6, width=60,
                               font=('Arial', 10),
                               bg='#34495e', fg='#ecf0f1',
                               relief='flat', wrap='word')
        instructions.pack(pady=(0, 20))

        instructions.insert('1.0',
                            "To use this weather app, you need a free API key from OpenWeatherMap:\n\n"
                            "1. Go to https://openweathermap.org/api\n"
                            "2. Sign up for a free account\n"
                            "3. Get your API key from the dashboard\n"
                            "4. Enter it below and click 'Save'\n\n"
                            "Your API key will be stored as an environment variable.")
        instructions.config(state='disabled')

        # API key input
        input_frame = tk.Frame(main_frame, bg='#2c3e50')
        input_frame.pack(fill='x', pady=(0, 20))

        tk.Label(input_frame, text="Enter API Key:",
                 font=('Arial', 12),
                 fg='#ecf0f1', bg='#2c3e50').pack(anchor='w')

        self.api_entry = tk.Entry(input_frame, font=('Arial', 12), width=50)
        self.api_entry.pack(fill='x', pady=(5, 0))
        self.api_entry.focus()

        # Buttons
        button_frame = tk.Frame(main_frame, bg='#2c3e50')
        button_frame.pack()

        save_btn = tk.Button(button_frame, text="Save & Continue",
                             command=self.save_api_key,
                             bg='#27ae60', fg='white',
                             font=('Arial', 12, 'bold'),
                             relief='flat', padx=20)
        save_btn.pack(side='left', padx=(0, 10))

        cancel_btn = tk.Button(button_frame, text="Cancel",
                               command=self.dialog.destroy,
                               bg='#e74c3c', fg='white',
                               font=('Arial', 12, 'bold'),
                               relief='flat', padx=20)
        cancel_btn.pack(side='left')

        # Bind Enter key
        self.api_entry.bind('<Return>', lambda e: self.save_api_key())

    def save_api_key(self):
        api_key = self.api_entry.get().strip()
        if api_key:
            self.api_key = api_key
            # Set environment variable for current session
            os.environ['WEATHER_API_KEY'] = api_key
            self.dialog.destroy()
        else:
            messagebox.showwarning("Warning", "Please enter a valid API key")


def main():
    app = WeatherApp()
    app.run()


if __name__ == "__main__":
    main()