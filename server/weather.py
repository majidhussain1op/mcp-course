from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("weather")

# Your OpenWeatherMap API key (replace with your actual key)
API_KEY = "6f1d07e1019631481d5aa4d7b12a41cf"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

async def get_weather_data(city: str) -> dict[str, Any] | None:
    """Fetch weather data from OpenWeatherMap API."""
    params = {
        "q": f"{city},PK",      # City in Pakistan
        "appid": API_KEY,
        "units": "metric"       # Temperature in Celsius
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(BASE_URL, params=params, timeout=10.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error: {e}")
            return None

@mcp.tool()
async def get_weather(city: str) -> str:
    """Get current weather for a given city in Pakistan.

    Args:
        city: Name of the city (e.g.,Hyderabad, Lahore, Karachi)

    Returns:
        A formatted string of current weather.
    """
    data = await get_weather_data(city)

    if not data:
        return f"Could not fetch weather data for {city}."

    try:
        weather = data["weather"][0]["description"].title()
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        return f"""
City: {city.title()}
Weather: {weather}
Temperature: {temp}°C
Humidity: {humidity}%
Wind Speed: {wind_speed} m/s
""".strip()
    except KeyError:
        return f"Unexpected data format received for {city}."


@mcp.resource("echo://{message}")
def echo_resource(message:str) -> str:
    """Echo a message as a resource  """
    return f"Resource echo: {message}"

@mcp.prompt(title="Code Review")
def review_code(code: str) -> str:
    return f"Please review this code:\n\n{code}"