import streamlit as st
import requests
from datetime import datetime, timedelta
import pytz
import pandas as pd
from cryptography.fernet import Fernet


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
    # To avoid using the API Key as it is in the code we will use encrypted values
    encryption_key = b'bxcWy0bgeAGdzktvpT_FNVXnSFs4LSLEyqNeVi3hPjA='
    cipher_text = b'gAAAAABmauEkdvGwEUWfCXpzjWsLIYHFH3OxNzLUVMZ2RR4EeOYcxZ3q3m_rSBTDsAvUDiW9c3If6fkYxFrDIrDTavjk7nKu8tT7HzD84dgnZdhM6GX0a5-k49FRB8i3G0L3VTPS6cqu'

    cipher_suite = Fernet(encryption_key)
    api_key = cipher_suite.decrypt(cipher_text).decode()
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
