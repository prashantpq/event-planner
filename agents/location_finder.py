import requests
import os
import json
from dotenv import load_dotenv
import logging
from geopy.distance import geodesic

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_locationiq_token():
    token = os.getenv("LOCATIONIQ_API_KEY")
    if not token:
        raise ValueError("LOCATIONIQ_API_KEY not set in environment.")
    return token

def geocode_region(region, api_key):
    url = "https://us1.locationiq.com/v1/search.php"
    params = {"key": api_key, "q": region, "format": "json", "limit": 1}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if data:
            lat, lon = data[0]["lat"], data[0]["lon"]
            logger.info(f"Geocoded region '{region}' to lat: {lat}, lon: {lon}")
            return lat, lon
        else:
            logger.error("No geocode results found.")
            return None, None
    except requests.exceptions.RequestException as e:
        logger.error(f"Geocoding error: {e}")
        return None, None

def nearby_search(lat, lon, api_key, query, radius=5000):
    url = "https://us1.locationiq.com/v1/nearby.php"
    params = {
        "key": api_key,
        "lat": lat,
        "lon": lon,
        "tag": "restaurant",
        "radius": radius,
        "format": "json",
        "limit": 20
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        brand_results = [place for place in data if query.lower() in place.get("name", "").lower()]

        if brand_results:
            logger.info(f"Found {len(brand_results)} '{query}' results in nearby search.")
            return [{
                "name": place.get("name"),
                "latitude": place.get("lat"),
                "longitude": place.get("lon"),
                "type": place.get("type"),
                "category": place.get("category", "")
            } for place in brand_results]
        else:
            logger.warning(f"No '{query}' results found in nearby search.")
            return []

    except requests.exceptions.RequestException as e:
        logger.error(f"Nearby search error: {e}")
        return []

def direct_text_search(lat, lon, api_key, query, region, radius=5000):
    url = "https://us1.locationiq.com/v1/search.php"
    params = {
        "key": api_key,
        "q": f"{query} {region} Mumbai India",
        "format": "json",
        "limit": 20
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        within_radius = []
        for place in data:
            place_lat = float(place.get("lat"))
            place_lon = float(place.get("lon"))
            dist_km = geodesic((float(lat), float(lon)), (place_lat, place_lon)).km
            if dist_km <= (radius / 1000):
                within_radius.append({
                    "name": place.get("display_name"),
                    "latitude": place_lat,
                    "longitude": place_lon,
                    "type": place.get("type"),
                    "icon": place.get("icon", "")
                })

        logger.info(f"Direct text search found {len(within_radius)} '{query}' results within {radius/1000} km of '{region}'.")
        return within_radius

    except requests.exceptions.RequestException as e:
        logger.error(f"Direct text search error: {e}")
        return []

def find_places(brand_name, query_type, region):
    api_key = get_locationiq_token()
    lat, lon = geocode_region(region, api_key)
    if not lat or not lon:
        logger.error("Failed to geocode region.")
        return []

    search_query = brand_name if brand_name else query_type
    results = nearby_search(lat, lon, api_key, search_query)
    if results:
        return results

    return direct_text_search(lat, lon, api_key, search_query, region)
