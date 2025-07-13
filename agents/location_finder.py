import requests
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
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
    url = "https://us1.locationiq.com/v1/search.php"
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
            lat, lon = data[0]["lat"], data[0]["lon"]
            logger.info(f"Geocoded region '{region}' to lat: {lat}, lon: {lon}")
            return lat, lon
        else:
            logger.error("No geocode results found.")
            return None, None

    except requests.exceptions.RequestException as e:
        logger.error(f"Geocoding error: {e}")
        return None, None

def find_places(query, region):
    """
    Find nearby places matching the query within a region using LocationIQ.
    """
    api_key = get_locationiq_token()

    lat, lon = geocode_region(region, api_key)
    if not lat or not lon:
        logger.error("Failed to geocode region.")
        return []

    # First attempt: Nearby search
    nearby_url = "https://us1.locationiq.com/v1/nearby.php"
    nearby_params = {
        "key": api_key,
        "lat": lat,
        "lon": lon,
        "tag": "restaurant",
        "radius": 5000,
        "format": "json",
        "limit": 10
    }

    try:
        response = requests.get(nearby_url, params=nearby_params)
        response.raise_for_status()
        data = response.json()

        # Filter brand-specific results (e.g., McDonald's) within nearby results
        brand_results = [
            place for place in data
            if query.lower() in place.get("name", "").lower()
        ]

        if brand_results:
            logger.info(f"Found {len(brand_results)} brand-specific results in nearby search.")
            return [{
                "name": place.get("name"),
                "latitude": place.get("lat"),
                "longitude": place.get("lon"),
                "type": place.get("type"),
                "category": place.get("category", "")
            } for place in brand_results]

        logger.warning(f"No brand-specific places found for '{query}' in nearby search. Performing fallback search scoped to user region '{region}'...")

    except requests.exceptions.RequestException as e:
        logger.error(f"Nearby search error: {e}")

    # Fallback: General search scoped to region
    fallback_url = "https://us1.locationiq.com/v1/search.php"
    combined_query = f"{query} {region} Mumbai India"
    fallback_params = {
        "key": api_key,
        "q": combined_query,
        "format": "json",
        "limit": 10
    }

    logger.info(f"Fallback search URL: {fallback_url} with params: {fallback_params}")

    try:
        fallback_response = requests.get(fallback_url, params=fallback_params)
        fallback_response.raise_for_status()
        fallback_data = fallback_response.json()

        # Filter fallback results to only those containing user-specified region dynamically
        filtered_results = [
            place for place in fallback_data
            if region.lower() in place.get("display_name", "").lower()
        ]

        if filtered_results:
            logger.info(f"Fallback search returned {len(filtered_results)} results in user-specified region '{region}'.")
            return [{
                "name": place.get("display_name"),
                "latitude": place.get("lat"),
                "longitude": place.get("lon"),
                "type": place.get("type"),
                "icon": place.get("icon", "")
            } for place in filtered_results]
        else:
            logger.warning(f"Fallback search returned no results in user-specified region '{region}'.")
            return []

    except requests.exceptions.RequestException as e:
        logger.error(f"LocationIQ fallback search error: {e}")
        return []

if __name__ == "__main__":
    # Independent test
    query = "McDonald's"
    region = "Kandivali"
    places = find_places(query, region)

    if places:
        for idx, place in enumerate(places, 1):
            print(f"{idx}. {place['name']} (Lat: {place['latitude']}, Lon: {place['longitude']})")
    else:
        print("No places found.")
