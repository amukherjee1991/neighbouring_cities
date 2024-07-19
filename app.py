import pandas as pd
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any

app = FastAPI()

# Load the CSV file and filter cities with a population of more than 1 million
file_path = 'uscities.csv'
df = pd.read_csv(file_path)
main_cities_df = df[df['population'] > 100000]

# Function to find nearby places
def find_nearby_places(latitude, longitude):
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json];
    node(around:50000,{latitude},{longitude})["place"~"city|town|village"];
    out body;
    """
    response = requests.get(overpass_url, params={'data': overpass_query})
    if response.status_code == 200:
        data = response.json()
        places = data.get('elements', [])
        return places
    else:
        print(f"Failed to find nearby places. Status code: {response.status_code}")
        return []

@app.get("/major_cities", response_model=List[str])
def get_major_cities():
    major_cities = main_cities_df['city'].tolist()
    return major_cities

@app.get("/major_cities/{state}", response_model=List[str])
def get_major_cities_by_state(state: str):
    state_cities_df = main_cities_df[main_cities_df['state_name'].str.lower() == state.lower()]
    if not state_cities_df.empty:
        major_cities_by_state = state_cities_df['city'].tolist()
        return major_cities_by_state
    else:
        raise HTTPException(status_code=404, detail="State not found or no major cities in this state")

@app.get("/city/{main_city}", response_model=Dict[str, Any])
def get_city(main_city: str):
    city_row = main_cities_df[main_cities_df['city'].str.lower() == main_city.lower()]
    if not city_row.empty:
        city_data = city_row.iloc[0].to_dict()
        latitude = city_data['lat']
        longitude = city_data['lng']
        neighbors = find_nearby_places(latitude, longitude)
        neighbors_data = [
            {
                'name': place.get('tags', {}).get('name', 'Unnamed place'),
                'latitude': place.get('lat', 'Unknown latitude'),
                'longitude': place.get('lon', 'Unknown longitude')
            }
            for place in neighbors if place.get('tags', {}).get('name') != main_city
        ]
        city_data['neighbors'] = neighbors_data
        return city_data
    else:
        raise HTTPException(status_code=404, detail="City not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
