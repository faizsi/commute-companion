import time
import requests
import math
import os
from twilio.rest import Client

DESTINATION_LATITUDE = os.environ['DESTINATION_LATITUDE']
DESTINATION_LONGITUDE = os.environ['DESTINATION_LONGITUDE']
START_LATITUDE = os.environ['START_LATITUDE']
START_LONGITUDE = os.environ['START_LONGITUDE']
GOOGLE_MAPS_API_KEY = os.environ['GOOGLE_MAPS_API_KEY']
TWILIO_SID = os.environ['TWILIO_SID']
TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
TWILIO_PHONE_NUMBER = os.environ['TWILIO_PHONE_NUMBER']
MY_PHONE_NUMBER = os.environ['MY_PHONE_NUMBER']
DESTINATION = os.environ['DESTINATION']


# Function to calculate ETA using Google Routes API
def get_eta():
    # Build the Google Maps API URL
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={START_LATITUDE},{START_LONGITUDE}&destination={DESTINATION_LATITUDE},{DESTINATION_LONGITUDE}&key={GOOGLE_MAPS_API_KEY}"

    # Make a request to Google Routes API
    response = requests.get(url)
    data = response.json()

    # Extract ETA information
    if 'routes' in data and data['routes']:
        route = data['routes'][0]
        if 'legs' in route and route['legs']:
            leg = route['legs'][0]
            if 'duration' in leg:
                eta_seconds = leg['duration']['value']
                eta_minutes = math.ceil(eta_seconds / 60)  # Calculate and round up to the nearest minute
                return eta_minutes

    return None


# Function to get the current weather conditions for destination
def get_weather():
    # open-meteo url
    url = f"https://api.open-meteo.com/v1/forecast?latitude={DESTINATION_LATITUDE}&longitude={DESTINATION_LONGITUDE}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_hours,precipitation_probability_max,windspeed_10m_max&temperature_unit=fahrenheit&windspeed_unit=mph&precipitation_unit=inch&timezone=America%2FNew_York"
    response = requests.get(url)
    data = response.json()
    return data


# Function to send ETA message using Twilio
def lambda_handler(event, context):
    eta = get_eta()
    weather = get_weather()

    if eta:
        eta_minutes = eta
        temperature_2m_max = weather["daily"]["temperature_2m_max"][0]
        temperature_2m_min = weather["daily"]["temperature_2m_min"][0]
        precipitation_sum = weather["daily"]["precipitation_sum"][0]
        precipitation_hours = weather["daily"]["precipitation_hours"][0]
        precipitation_probability_max = weather["daily"]["precipitation_probability_max"][0]
        windspeed_10m_max = weather["daily"]["windspeed_10m_max"][0]

    message = (
        f"Your ETA to {DESTINATION} is approximately {eta_minutes} minutes today. "
        f"The weather forecast for today is as follows:\n"
        f"- Max Temperature: {temperature_2m_max}°F\n"
        f"- Min Temperature: {temperature_2m_min}°F\n"
        f"- Precipitation Sum: {precipitation_sum} inch\n"
        f"- Precipitation Hours: {precipitation_hours} hours\n"
        f"- Max Precipitation Chance: {precipitation_probability_max}%\n"
        f"- Max Windspeed: {windspeed_10m_max} mp/h\n"
        f"Have a great day!"
    )

    # Initialize the Twilio client
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    # Send the message
    client.messages.create(
        to=MY_PHONE_NUMBER,
        from_=TWILIO_PHONE_NUMBER,
        body=message
    )
    print("ETA message sent!")
    return
