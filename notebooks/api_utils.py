import requests
import pandas as pd
from typing import List, Dict, Optional
from dotenv import load_dotenv
import os

# Load environment variables - this should come BEFORE accessing any env variables
load_dotenv()

# Get API keys after loading environment variables
FOURSQUARE_API_KEY = os.getenv('FOURSQUARE_KEY')

def get_city_bikes_data(city: str) -> pd.DataFrame:
    """
    Retrieves bike station data from CityBikes API and returns it as a DataFrame.
    """
    base_url = "http://api.citybik.es/v2/networks"
    response = requests.get(base_url)

    if response.status_code != 200:
        raise Exception("Failed to fetch data from CityBikes API")

    data = response.json()

    city_network = next(
        (network for network in data['networks'] 
         if 'location' in network 
         and 'city' in network['location'] 
         and city.lower() in network['location']['city'].lower()),
        None
    )

    if not city_network:
        raise Exception(f"{city} network not found in the API")

    city_network_id = city_network['id']
    city_url = f"{base_url}/{city_network_id}"
    city_response = requests.get(city_url)
    
    if city_response.status_code != 200:
        raise Exception(f"Failed to fetch {city} network data")

    city_data = city_response.json()
    stations = city_data['network']['stations']

    df = pd.DataFrame(stations)
    columns = ['id', 'name', 'latitude', 'longitude', 'free_bikes', 'empty_slots']
    
    missing_columns = [col for col in columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    return df[columns]

def get_foursquare_data(
    lat: float, 
    lon: float, 
    radius: int = 1000, 
    categories: List[str] = ['13065', '13032', '11044']
) -> pd.DataFrame:
    """
    Fetch Foursquare POI data for a given location.
    """
    if not FOURSQUARE_API_KEY:
        raise ValueError("Foursquare API key not found in environment variables")

    search_url = 'https://api.foursquare.com/v3/places/search'
    headers = {
        "Authorization": FOURSQUARE_API_KEY,
        "Accept": "application/json"
    }
    params = {
        'll': f'{lat},{lon}',
        'radius': radius,
        'categories': ','.join(categories),
        'limit': 50,
        'sort': 'DISTANCE'
    }

    try:
        response = requests.get(search_url, params=params, headers=headers)
        response.raise_for_status()
        
        foursquare_pois = response.json().get('results', [])
        
        if not foursquare_pois:
            return pd.DataFrame()

        foursquare_results = [{
            'POI_name': poi.get('name'),
            'address': poi.get('location', {}).get('formatted_address', 'N/A'),
            'latitude': poi.get('geocodes', {}).get('main', {}).get('latitude'),
            'longitude': poi.get('geocodes', {}).get('main', {}).get('longitude'),
            'rating': poi.get('rating', 'N/A'),
            'distance_meters': poi.get('distance'),
            'category_id': poi.get('categories', [{}])[0].get('id'),
            'category_name': poi.get('categories', [{}])[0].get('name', 'N/A'),
            'total_ratings': poi.get('stats', {}).get('total_ratings', 0)
        } for poi in foursquare_pois]

        return pd.DataFrame(foursquare_results)

    except requests.exceptions.RequestException as e:
        raise Exception(f"Foursquare API request failed: {str(e)}")
    except Exception as e:
        raise Exception(f"Error processing Foursquare data: {str(e)}")

