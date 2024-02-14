import requests
import json
from datetime import datetime
from flask import Flask, jsonify, request

app = Flask(__name__)
INNER_TOKEN = ""

@app.route("/")
def home_page():
    return "<p><h2>KMA2024. Get Weather Forecast SAAS.</h2></p>"


@app.route(
    "/getweather",
    methods=["POST"],
)
def get_weather():
    json_data = request.get_json()
    token_inner = json_data.get("token_inner") 
    vc_token = json_data.get("token")
    name = json_data.get("requester_name")
    location = json_data.get("location")
    date = json_data.get("date")
    units = json_data.get("units")
    
    if token_inner != INNER_TOKEN:
        return {
            "issue" : "invalid_inner_token"
        }
    url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{date}?key={vc_token}&unitGroup={units}'
    response = requests.get(url).json()
    
    utc_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    units_default = {
        "us" : {"temp" : "°F", "wind" : "miles per hour", "precip" : "inches", "visibility" : "miles"},
        "metric" : {"temp" : "°C", "wind" : "kms per hour", "precip" : "millimeters", "visibility" : "kilometrs"},
        "uk" : {"temp" : "°C", "wind" : "miles per hour", "precip" : "millimeters", "visibility" : "miles"},
        "base" : {"temp" : "°K", "wind" : "meters per second", "precip" : "millimeters", "visibility" : "kilometrs"},
    }
    result = {
        "requster_name": name,
        "timestamp": utc_time,
        "location" : location,
        "date" : date,
        "weather" : 
        {
            "Description": response["days"][0]["description"],
            "Conditions": response["days"][0]["conditions"],
            "Max temeperature" : str(response["days"][0]["tempmax"])  + units_default[units]["temp"],
            "Min temeperature" : str(response["days"][0]["tempmin"])   + units_default[units]["temp"],
            "Feels like max": str(response["days"][0]["feelslikemax"])   + units_default[units]["temp"],
            "Feels like min": str(response["days"][0]["feelslikemin"])  + units_default[units]["temp"],
            "UV Index" : str(response["days"][0]["uvindex"]) + " / 10",
            "Precip amnt" : str(response["days"][0]["precip"]) + " " + units_default[units]["precip"],
            "Precipitation Probability" : str(response["days"][0]["precipprob"]) + "%",
            "Wind Speed": str(response["days"][0]["windspeed"]) + " " + units_default[units]["wind"],
            "Visibility": str(response["days"][0]["visibility"]) + " " + units_default[units]["visibility"],
            "Humidity" : str(response["days"][0]["humidity"]) + "%"
        }
    }

    return result
