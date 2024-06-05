import requests
from datetime import datetime, timedelta
import pytz


def display_date_time(timezone):
    user_timezone = pytz.timezone('UTC')
    user_time = datetime.now(user_timezone)

    city_time = user_time + timedelta(seconds=timezone)
    formatted_city_time = city_time.strftime("%A, %B %d, %Y, %I:%M %p %Z")
    return formatted_city_time


# Function to get weather data - Create the URL that the weather API needs
def get_weather_data(city_name, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city_name,
        'appid': api_key,
        'units': 'metric'  # To get temperature in Celsius
    }
    response = requests.get(base_url, params=params)
    return response.json()


# Function to display weather data
# Use the output JSON file to extract the relevan parameters about the weather and diaply them
def display_weather_data(weather_data, current_location_data):
    if weather_data.get('cod') != 200:
        print("City not found.")
        return

    # Display times in your current & destination location
    city_time = display_date_time(weather_data['timezone'])
    location_time = display_date_time(current_location_data['timezone'])

    print(f"\n{weather_data['name']} time: {city_time}")
    print(f"{current_location_data['name']} time: {location_time}\n")

    # display_date_time(weather_data, current_location_data)

    city = weather_data['name']
    country = weather_data['sys']['country']
    temp = weather_data['main']['temp']
    weather_description = weather_data['weather'][0]['description']
    humidity = weather_data['main']['humidity']

    print("Weather Parameters:")
    print(f"City: {city}, {country}")
    print(f"Temperature: {temp}°C")
    print(f"Weather description: {weather_description}")
    print(f"Humidity: {humidity}%")


# Main function
def main():
    api_key = input("Please enter your OpenWeatherMap API key that you have received to your mail:")
    current_location = input("Please enter your current location: ")
    city_name = input("Please enter city name to check the weather: ")

    weather_data = get_weather_data(city_name, api_key)
    current_location_data = get_weather_data(current_location, api_key)
    display_weather_data(weather_data, current_location_data)


# Run the application
if __name__ == "__main__":
    main()
