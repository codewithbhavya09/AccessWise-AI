import streamlit as st
import folium
from streamlit_folium import st_folium
from database.db_queries import create_route, get_route_by_id
from utils.helpers import display_success, display_error, display_info, calculate_distance
from utils.config import DEFAULT_LAT, DEFAULT_LNG, DEFAULT_ZOOM
from ai.accessibility_scorer import score_from_obstacles
from ai.route_recommender import recommend_route
import random

def show():
    st.title("🗺️ Route Navigator")
    
    display_info("""
    Find the most accessible routes based on your profile and preferences.
    """)
    
    # Route input
    col1, col2 = st.columns(2)
    
    with col1:
        start_location = st.text_input("📍 Start Location", "Central Station")
    
    with col2:
        end_location = st.text_input("🎯 End Location", "City Hall")
    
    # Get some sample coordinates for demo
    locations_map = {
        'Central Station': (40.7128, -74.0060),
        'City Hall': (40.7138, -74.0070),
        'Museum': (40.7148, -74.0080),
        'Park': (40.7158, -74.0090),
        'Hospital': (40.7168, -74.0100),
        'Library': (40.7178, -74.0110),
        'Airport': (40.7188, -74.0120),
        'Beach': (40.7198, -74.0130),
    }
    
    start_coords = locations_map.get(start_location, (DEFAULT_LAT, DEFAULT_LNG))
    end_coords = locations_map.get(end_location, (DEFAULT_LAT + 0.01, DEFAULT_LNG + 0.01))
    
    # Preferences
    st.subheader("Route Preferences")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        wheelchair = st.checkbox("Wheelchair Friendly", value=True)
        avoid_stairs = st.checkbox("Avoid Stairs", value=True)
    
    with col2:
        smooth_surface = st.checkbox("Smooth Surface", value=True)
        elevators = st.checkbox("Prefer Elevators", value=False)
    
    with col3:
        shorter_distance = st.checkbox("Shorter Distance", value=True)
        well_lit = st.checkbox("Well-Lit Areas", value=False)
    
    # Find route button
    if st.button("🔍 Find Best Route", use_container_width=True):
        distance = calculate_distance(start_coords[0], start_coords[1], 
                                     end_coords[0], end_coords[1])
        
        # Mock obstacles for demo
        mock_obstacles = []
        if random.random() > 0.6:
            mock_obstacles.append({'type': 'stairs', 'confidence': 0.85})
        if random.random() > 0.7:
            mock_obstacles.append({'type': 'pothole', 'confidence': 0.75})
        
        accessibility_score = score_from_obstacles(mock_obstacles)
        
        # Create route
        route_id = create_route(
            user_id=st.session_state.user_id,
            start_point=start_location,
            end_point=end_location,
            start_lat=start_coords[0],
            start_lng=start_coords[1],
            end_lat=end_coords[0],
            end_lng=end_coords[1],
            distance=distance,
            accessibility_score=accessibility_score,
            obstacles_detected=len(mock_obstacles)
        )
        
        st.session_state.selected_route = route_id
        display_success(f"✅ Route found! ID: {route_id}")
    
    st.markdown("---")
    
    # Map display
    st.subheader("📍 Route Map")
    
    m = folium.Map(
        location=[start_coords[0], start_coords[1]],
        zoom_start=DEFAULT_ZOOM,
        tiles='OpenStreetMap'
    )
    
    # Add markers
    folium.Marker(
        location=start_coords,
        popup=start_location,
        icon=folium.Icon(color='green', icon='play'),
        tooltip='Start'
    ).add_to(m)
    
    folium.Marker(
        location=end_coords,
        popup=end_location,
        icon=folium.Icon(color='red', icon='stop'),
        tooltip='End'
    ).add_to(m)
    
    # Draw route line
    folium.PolyLine(
        locations=[start_coords, end_coords],
        color='blue',
        weight=3,
        opacity=0.7
    ).add_to(m)
    
    st_folium(m, width=700, height=500)
    
    # Route details
    if 'selected_route' in st.session_state:
        st.markdown("---")
        st.subheader("📊 Route Details")
        
        route_id = st.session_state.selected_route
        route = get_route_by_id(route_id)
        
        if route:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Distance", f"{route[8]:.2f} km")
            
            with col2:
                duration = int(route[8] * 12)  # Estimate: 12 min per km
                st.metric("Estimated Time", f"{duration} min")
            
            with col3:
                accessibility = route[9] * 100
                st.metric("Accessibility", f"{accessibility:.0f}%")
            
            with col4:
                st.metric("Obstacles", route[10])
            
            # Action buttons
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("✅ Accept Route", use_container_width=True):
                    display_success("Route accepted! Start navigating.")
            
            with col2:
                if st.button("💬 Give Feedback", use_container_width=True):
                    st.session_state.feedback_route = route_id
            
            with col3:
                if st.button("🆘 Emergency SOS", use_container_width=True):
                    display_success("Emergency services contacted!")