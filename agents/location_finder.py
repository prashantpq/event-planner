# agents/location_finder.py

import requests
import os
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_locationiq_token():
    """
    Retrieve LocationIQ token from environment variables.
    """
    token = os.getenv("LOCATIONIQ_API_KEY")
    if not token:
        raise ValueError("LOCATIONIQ_API_KEY not set in environment.")
    return token


def geocode_region(region, api_key):
    """
    Geocode a region name to latitude and longitude using LocationIQ.
    """
    url = f"https://us1.locationiq.com/v1/search.php"
    params = {
        "key": api_key,
        "q": region,
        "format": "json",
        "limit": 1
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if data:
            return data[0]["lat"], data[0]["lon"]
        else:
            logger.error("No geocode results found.")
            return None, None

    except requests.exceptions.RequestException as e:
        logger.error(f"Geocoding error: {e}")
        return None, None


def find_places(query, region):
    api_key = os.getenv('LOCATIONIQ_API_KEY')
    if not api_key:
        logger.error("No LocationIQ API key found.")
        return []

    # Clean region
    if "around" in region:
        region = region.replace("around", "").strip()

    combined_query = f"{query} {region} Mumbai India"

    url = f"https://us1.locationiq.com/v1/search.php"
    params = {
        "key": api_key,
        "q": combined_query,
        "format": "json",
        "limit": 5
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        results = []
        for place in data:
            results.append({
                "name": place.get("display_name"),
                "latitude": place.get("lat"),
                "longitude": place.get("lon"),
                "type": place.get("type"),
                "icon": place.get("icon", "")
            })

        return results

    except requests.exceptions.RequestException as e:
        logger.error(f"Search API error: {e}")
        return []


# if __name__ == "__main__":
#     # Test independently
#     query = "restaurant"
#     region = "Malad Mumbai India"
#     places = find_places(query, region)

#     if places:
#         for idx, place in enumerate(places, 1):
#             print(f"{idx}. {place['name']} (Lat: {place['latitude']}, Lon: {place['longitude']})")
#     else:
#         print("No places found.")
