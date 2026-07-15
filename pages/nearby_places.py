import streamlit as st
import folium
from streamlit_folium import st_folium
from database.db_queries import get_nearby_facilities, get_all_facilities
from utils.config import DEFAULT_LAT, DEFAULT_LNG, FACILITY_TYPES
import random

def show():
    st.title("📍 Nearby Accessible Places")
    
    # Get user location (mock for demo)
    user_lat = DEFAULT_LAT
    user_lng = DEFAULT_LNG
    
    st.subheader("Filter by Facility Type")
    
    selected_types = st.multiselect(
        "Select facility types",
        FACILITY_TYPES,
        default=['Hospital', 'Pharmacy', 'Restaurant']
    )
    
    # Get nearby facilities
    facilities = get_all_facilities()
    
    # Filter by selected types and distance
    filtered_facilities = []
    for facility in facilities:
        if facility[3] in selected_types:  # facility_type is at index 3
            filtered_facilities.append(facility)
    
    # Sort by distance
    filtered_facilities.sort(key=lambda x: abs(x[5] - user_lat) + abs(x[6] - user_lng))
    
    # Display map
    st.subheader("🗺️ Map View")
    
    m = folium.Map(
        location=[user_lat, user_lng],
        zoom_start=13,
        tiles='OpenStreetMap'
    )
    
    # Add user marker
    folium.Marker(
        location=[user_lat, user_lng],
        popup="Your Location",
        icon=folium.Icon(color='blue', icon='user'),
        tooltip='You are here'
    ).add_to(m)
    
    # Add facility markers
    color_map = {
        'Hospital': 'red',
        'Pharmacy': 'green',
        'Toilet': 'orange',
        'Restaurant': 'purple',
        'Bank': 'gray',
        'Library': 'blue',
        'Police Station': 'darkblue',
        'Fire Station': 'darkred'
    }
    
    for facility in filtered_facilities[:20]:
        facility_name = facility[1]
        facility_type = facility[3]
        accessibility = facility[5] * 100
        
        color = color_map.get(facility_type, 'blue')
        
        folium.Marker(
            location=[facility[4], facility[5]],
            popup=f"{facility_name}<br>Accessibility: {accessibility:.0f}%",
            icon=folium.Icon(color=color),
            tooltip=facility_name
        ).add_to(m)
    
    st_folium(m, width=700, height=500)
    
    # Facilities list
    st.markdown("---")
    st.subheader("📋 Nearby Facilities")
    
    if filtered_facilities:
        for facility in filtered_facilities[:10]:
            facility_id = facility[0]
            facility_name = facility[1]
            facility_type = facility[3]
            lat = facility[4]
            lng = facility[5]
            accessibility = facility[6] * 100
            contact = facility[7]
            
            with st.container():
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                
                with col1:
                    st.write(f"### {facility_name}")
                    st.write(f"**Type:** {facility_type}")
                    st.write(f"**Contact:** {contact}")
                
                with col2:
                    st.metric("Accessibility", f"{accessibility:.0f}%")
                
                with col3:
                    st.write(f"📍 {lat:.4f}, {lng:.4f}")
                
                with col4:
                    if st.button("📍 Navigate", key=f"nav_{facility_id}"):
                        st.session_state.nav_destination = facility_name
                        st.success(f"Navigate to {facility_name}")
                
                st.divider()
    else:
        st.info("No facilities found for selected types")
    
    # Statistics
    st.markdown("---")
    st.subheader("📊 Statistics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Facilities", len(facilities))
    
    with col2:
        if filtered_facilities:
            avg_accessibility = sum(f[6] for f in filtered_facilities[:10]) / min(10, len(filtered_facilities)) * 100
            st.metric("Avg Accessibility", f"{avg_accessibility:.0f}%")
    
    with col3:
        st.metric("Types Available", len(FACILITY_TYPES))