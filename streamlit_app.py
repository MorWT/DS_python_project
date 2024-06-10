import streamlit as st
import requests
from datetime import datetime, timedelta
import pytz
import pandas as pd


# Function to display date and time
def display_date_time(timezone):
    user_timezone = pytz.timezone('UTC')
    user_time = datetime.now(user_timezone)
    city_time = user_time + timedelta(seconds=timezone)
    formatted_city_time = city_time.strftime("%A, %B %d, %Y, %I:%M %p %Z")
    return formatted_city_time


# Function to get weather data
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
def display_weather_data(weather_data, current_location_data):
    if weather_data.get('cod') != 200:
        st.error("City not found.")
        return

    # Display times in your current & destination location
    city_time = display_date_time(weather_data['timezone'])
    location_time = display_date_time(current_location_data['timezone'])

    st.write(f"**{weather_data['name']} time:** {city_time}")
    st.write(f"**{current_location_data['name']} time:** {location_time}")

    city = weather_data['name']
    country = weather_data['sys']['country']
    temp = weather_data['main']['temp']
    weather_description = weather_data['weather'][0]['description']
    humidity = weather_data['main']['humidity']

    weather_params = {
        "Parameter": ["City", "Temperature", "Weather description", "Humidity"],
        "Value": [f"{city}, {country}", f"{temp}°C", weather_description, f"{humidity}%"]
    }

    df = pd.DataFrame(weather_params)
    st.table(df)

# Main Streamlit App
def main():
    st.title("Weather App")

    api_key = st.text_input("Enter your OpenWeatherMap API key")
    current_location = st.text_input("Enter your current location")
    city_name = st.text_input("Enter city name to check the weather")

    if st.button("Get Weather"):
        if api_key and current_location and city_name:
            weather_data = get_weather_data(city_name, api_key)
            current_location_data = get_weather_data(current_location, api_key)
            display_weather_data(weather_data, current_location_data)
        else:
            st.error("Please enter all fields")


if __name__ == "__main__":
    main()
