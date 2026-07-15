import streamlit as st
import pandas as pd
from database.db_queries import get_user_statistics
from utils.helpers import display_info

def show():
    st.title("📊 Dashboard")
    
    user_id = st.session_state.user_id
    stats = get_user_statistics(user_id)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Routes", stats['total_routes'], help="Routes you've navigated")
    
    with col2:
        st.metric("Avg Distance", f"{stats['avg_distance']:.2f} km", help="Average route distance")
    
    with col3:
        st.metric("Accessibility Score", f"{stats['avg_accessibility_score']*100:.1f}%", 
                  help="Average accessibility score")
    
    with col4:
        st.metric("Total Feedback", stats['total_feedback'], help="Feedback submissions")
    
    # Recent activity
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Quick Stats")
        display_info("""
        **Your Accessibility Profile**: Based on your recent usage
        - Total routes explored: {}
        - Average route difficulty: Medium
        - Preferred transportation: Mixed
        """.format(stats['total_routes']))
    
    with col2:
        st.subheader("🎯 Recommendations")
        display_info("""
        **Personalized Suggestions**:
        1. Try the new high-accessibility downtown route
        2. Check out newly accessible facilities
        3. Review your accessibility preferences
        """)
    
    # Recent routes
    st.markdown("---")
    st.subheader("📍 Recent Routes")
    
    from database.db_queries import get_user_routes
    routes = get_user_routes(user_id, limit=5)
    
    if routes:
        for route in routes:
            with st.container():
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.write(f"**{route[2]} → {route[3]}**")
                with col2:
                    st.write(f"📏 {route[8]:.1f} km")
                with col3:
                    accessibility = route[9] * 100
                    st.write(f"♿ {accessibility:.0f}%")
    else:
        display_info("No routes yet. Start navigating to see your history!")
    
    # Call to action
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🗺️ Find a Route", use_container_width=True):
            st.switch_page("pages/map_navigator.py")
    
    with col2:
        if st.button("📷 Upload Image", use_container_width=True):
            st.switch_page("pages/image_upload.py")
    
    with col3:
        if st.button("♿ Update Profile", use_container_width=True):
            st.switch_page("pages/accessibility_profile.py")