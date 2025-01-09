import requests
import pandas as pd
from typing import List, Dict, Optional
from dotenv import load_dotenv
import os

# Load environment variables - this should come BEFORE accessing any env variables
load_dotenv()

# Get API keys after loading environment variables

YELP_API_KEY = os.getenv('YELP_API')



def get_yelp_data(
    lat: float,
    lon: float, 
    radius: int = 1000, 
    terms: List[str] = ['restaurants', 'libraries', 'shopping']
) -> pd.DataFrame:
    """
    Fetch Yelp POI data for given latitude and longitude, including distance in meters.
    """
    if not YELP_API_KEY:
        raise ValueError("YELP_API key not found in environment variables")
        
    api_url = "https://api.yelp.com/v3/businesses/search"
    headers = {
        "Authorization": f"Bearer {YELP_API_KEY}",
        "Content-Type": "application/json",
    }
    all_yelp_results = []

    for term in terms:
        params = {
            'term': term,
            'latitude': lat,
            'longitude': lon,
            'radius': radius,
            'limit': 50
        }

        print(f"Making request to Yelp for term '{term}'...")
        response = requests.get(api_url, headers=headers, params=params)

        if response.status_code == 200:
            try:
                yelp_pois = response.json().get('businesses', [])
                for poi in yelp_pois:
                    all_yelp_results.append({
                        'name': poi.get('name'),
                        'address': poi.get('location', {}).get('address1', 'N/A'),
                        'latitude': poi.get('coordinates', {}).get('latitude'),
                        'longitude': poi.get('coordinates', {}).get('longitude'),
                        'rating': poi.get('rating', 'N/A'),
                        'review_count': poi.get('review_count', 'N/A'),
                        'distance_meters': poi.get('distance'),
                        'term': term
                    })
            except Exception as e:
                print(f"Error parsing Yelp response for term '{term}':", e)
        else:
            print(f"Error fetching data from Yelp for term '{term}': {response.status_code}")
            print(response.text)

    yelp_df = pd.DataFrame(all_yelp_results)
    return yelp_df