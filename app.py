import folium
import streamlit as st
import openrouteservice
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

# ORS API Key (replace with your own OpenRouteService API key)
ORS_API_KEY = "5b3ce3597851110001cf6248f75e1c7df9954737b3da07ff523cfccb"

# Airoli, Navi Mumbai Coordinates (Fixed Frame)
AIROLI_COORDS = (19.1552, 72.9874)  # Latitude, Longitude

# Function to geocode place names to latitude and longitude
def geocode_location(location_name):
    geolocator = Nominatim(user_agent="streamlit_app")
    try:
        location = geolocator.geocode(location_name)
        if location:
            st.write(f"Geocoded {location_name} to: ({location.latitude}, {location.longitude})")
            return (location.longitude, location.latitude)  # Ensure it's longitude, latitude
        else:
            st.error(f"Could not find location: {location_name}")
            return None
    except GeocoderTimedOut:
        st.error("Geocoding service timed out. Please try again.")
        return None

# Function to calculate the shortest route using OpenRouteService (ORS)
def get_route(start_coords, end_coords):
    client = openrouteservice.Client(key=ORS_API_KEY)
    
    try:
        route = client.directions(
            coordinates=[start_coords, end_coords],
            profile='driving-car',  # Routing for cars
            format='geojson'
        )
        return route
    except openrouteservice.exceptions.ApiError as e:
        st.error(f"OpenRouteService API Error: {e}")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return None

# Function to create a map centered on Airoli, Navi Mumbai
def create_map(center=AIROLI_COORDS, zoom_start=14):
    m = folium.Map(location=center, zoom_start=zoom_start, control_scale=True)
    return m

# Function to plot the route on the map
def plot_route(map_, route_geometry):
    if route_geometry:
        try:
            # Check if 'features' and geometry data exists
            features = route_geometry.get('features', [])
            if features:
                coordinates = features[0].get('geometry', {}).get('coordinates', [])
                st.write(f"Route Coordinates: {coordinates}")  # Debug: Print coordinates

                if coordinates:
                    # Reverse coordinates to (latitude, longitude)
                    reversed_coordinates = [(lat, lon) for lon, lat in coordinates]

                    # Plot the route as a PolyLine on the map
                    folium.PolyLine(locations=reversed_coordinates, color="blue", weight=5, opacity=0.7).add_to(map_)
                else:
                    st.error("No coordinates found in the route geometry.")
            else:
                st.error("No features found in the route geometry.")
        except KeyError as e:
            st.error(f"Error extracting coordinates: {e}")
    else:
        st.error("No route geometry found to plot.")

# Streamlit UI
def main():
    st.title("Shortest Path Finder")

    # Display only the map once, centered on Airoli, Navi Mumbai
    map_ = create_map(center=AIROLI_COORDS)

    # Input: Source and Destination Location Names
    start_location = st.text_input("Enter Source Location (e.g., Airoli Station)")
    end_location = st.text_input("Enter Destination Location (e.g., New Horizon Public School)")

    if st.button("Find Shortest Path"):
        if start_location and end_location:
            # Geocode the locations to get coordinates
            start_coords = geocode_location(start_location)
            end_coords = geocode_location(end_location)

            if start_coords and end_coords:
                # Get the road-based route from ORS
                route_geometry = get_route(start_coords, end_coords)

                if route_geometry:
                    # Debug: Check the structure of route geometry
                    # st.write("Route Geometry:", route_geometry)  # Removed the debug print

                    if 'features' in route_geometry and len(route_geometry['features']) > 0:
                        # Plot the route on the map
                        plot_route(map_, route_geometry)

                        # Display the updated map with the route
                        st.write("Shortest Path on Road (Map):")
                        st.components.v1.html(map_._repr_html_(), height=600)
                    else:
                        st.error("No valid route data found.")
                else:
                    st.error("Failed to fetch route.")
            else:
                st.warning("Geocoding failed for one or both locations.")
        else:
            st.warning("Please enter both source and destination locations.")

if __name__ == "__main__":
    main()
