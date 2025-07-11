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
    token = os.getenv("LOCATIONIQ_TOKEN")
    if not token:
        raise ValueError("LOCATIONIQ_TOKEN not set in environment.")
    return token

def find_places(query, region):
    """
    Use LocationIQ Search API to find places matching the query in the given region.
    Returns a list of dictionaries containing place details.
    """
    token = get_locationiq_token()
    url = "https://us1.locationiq.com/v1/search.php"
    params = {
        'key': token,
        'q': f"{query} {region}",
        'format': 'json',
        'limit': 5  
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        places = response.json()

        results = []
        for place in places:
            results.append({
                'name': place.get('display_name'),
                'latitude': place.get('lat'),
                'longitude': place.get('lon'),
                'type': place.get('type'),
                'icon': place.get('icon', '')
            })

        logger.info(f"Fetched {len(results)} places for query '{query}' in region '{region}'")
        return results

    except requests.exceptions.HTTPError as errh:
        logger.error(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        logger.error(f"Connection Error: {errc}")
    except requests.exceptions.Timeout as errt:
        logger.error(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        logger.error(f"Unexpected Error: {err}")

    return []

# if __name__ == "__main__":
#     query = "restaurants"
#     region = "Malad Mumbai India"
#     places = find_places(query, region)

#     if places:
#         for idx, place in enumerate(places, 1):
#             print(f"{idx}. {place['name']} (Lat: {place['latitude']}, Lon: {place['longitude']})")
#     else:
#         print("No places found.")
