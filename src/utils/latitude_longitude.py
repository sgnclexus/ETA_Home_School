import googlemaps
import pandas as pd
from utils.time_format import convert_seconds

# Replace with your actual Google Maps API key
# API_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXX'


# Initialize the Google Maps client
gmaps = googlemaps.Client(key=API_KEY)

# function to connect to Diection API to get the ETA
def get_travel_time(origin, destination, mode='transit'):
    """
    Retrieve the travel time between two locations using Google Maps API.
    
    :param origin: The starting location as a string.
    :param destination: The destination location as a string.
    :param mode: Mode of travel, e.g., 'driving', 'walking', 'bicycling', 'transit'.
    :return: Travel time in minutes or None if there's an issue.
    """

    try:

        """
        driving (default) indicates standard driving directions or distance using the road network.
        walking requests walking directions or distance via pedestrian paths & sidewalks (where available).
        bicycling requests bicycling directions or distance via bicycle paths & preferred streets (where available).
        transit requests directions or distance via public transit routes (where available). If you set the mode to transit, 
        you can optionally specify either a departure_time or an arrival_time. 
        If neither time is specified, the departure_time defaults to now (that is, the departure time defaults to the current time). 
        You can also optionally include a transit_mode and/or a transit_routing_preference.
        """

        directions_result = gmaps.directions(origin, destination, mode=mode, region="mx", language="es", units="metric")

        if directions_result:
            # Extract the duration from the first route
            duration = directions_result[0]['legs'][0]['duration']['value']  # Duration in seconds
            duration_minutes = round(duration / 60, 3)  # Convert to minutes
            formatted_duration = convert_seconds(duration)
            return duration_minutes, formatted_duration, mode
            
        
    except Exception as e:

        print(f"Error retrieving directions: {e}")
        return None, None



def get_lat_long(school_name_address, region="Mexico"):
    """
    Get latitude and longitude for a given school name.
    
    :param school_name: The name or address of the school.
    :param region: The region where the school is located. Defaults to "Mexico".
    :return: A tuple (latitude, longitude) or (None, None) if not found.
    """
    try:
        
        geocode_result = gmaps.geocode(f"{school_name_address}, {region}")

        if geocode_result:
            location = geocode_result[0]['geometry']['location']            
            return location['lat'],location['lng'] 
        
    except Exception as e:        
        print(f"Error retrieving coordinates for {school_name_address}: {e}")
    return None


