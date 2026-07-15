import streamlit as st
from database.db_queries import get_accessibility_profile, update_accessibility_profile
from utils.helpers import display_success, display_info

def show():
    st.title("♿ Accessibility Profile")
    
    user_id = st.session_state.user_id
    profile = get_accessibility_profile(user_id)
    
    display_info("""
    Your accessibility profile helps us recommend the most suitable routes and services.
    Update your preferences to personalize your experience.
    """)
    
    st.subheader("Mobility Challenges")
    
    col1, col2 = st.columns(2)
    
    with col1:
        wheelchair_accessible = st.checkbox(
            "Wheelchair Accessible Routes Required",
            value=profile[2] if profile else False
        )
        avoid_stairs = st.checkbox(
            "Avoid Stairs",
            value=profile[3] if profile else True
        )
        require_ramp = st.checkbox(
            "Require Ramps",
            value=profile[4] if profile else False
        )
        require_elevator = st.checkbox(
            "Require Elevators",
            value=profile[5] if profile else False
        )
    
    with col2:
        avoid_curbs = st.checkbox(
            "Avoid Curbs",
            value=profile[6] if profile else False
        )
        smooth_surface = st.checkbox(
            "Prefer Smooth Surfaces",
            value=profile[7] if profile else True
        )
        visual_impaired = st.checkbox(
            "Visually Impaired",
            value=profile[8] if profile else False
        )
        hearing_impaired = st.checkbox(
            "Hearing Impaired",
            value=profile[9] if profile else False
        )
    
    st.markdown("---")
    st.subheader("Comfort Preferences")
    
    col1, col2 = st.columns(2)
    
    with col1:
        prefer_lit_areas = st.checkbox(
            "Prefer Well-Lit Areas",
            value=profile[10] if profile else False
        )
        regular_rest = st.checkbox(
            "Need Regular Rest Areas",
            value=profile[11] if profile else False
        )
    
    with col2:
        good_lighting = st.checkbox(
            "Good Lighting Required",
            value=profile[12] if profile else False
        )
        clear_sidewalk = st.checkbox(
            "Clear Sidewalk Required",
            value=profile[13] if profile else True
        )
    
    # Save button
    if st.button("💾 Save Profile", use_container_width=True):
        update_accessibility_profile(
            user_id,
            wheelchair_accessible=wheelchair_accessible,
            avoid_stairs=avoid_stairs,
            require_ramp=require_ramp,
            require_elevator=require_elevator,
            avoid_curbs=avoid_curbs,
            smooth_surface=smooth_surface,
            visual_impaired=visual_impaired,
            hearing_impaired=hearing_impaired,
            prefer_lit_areas=prefer_lit_areas,
            regular_rest_areas=regular_rest,
            good_lighting=good_lighting,
            clear_sidewalk=clear_sidewalk
        )
        display_success("✅ Profile saved successfully!")
    
    st.markdown("---")
    st.subheader("Profile Summary")
    
    selected_items = []
    if wheelchair_accessible:
        selected_items.append("♿ Wheelchair accessibility needed")
    if avoid_stairs:
        selected_items.append("🚫 Avoid stairs")
    if require_ramp:
        selected_items.append("📐 Require ramps")
    if require_elevator:
        selected_items.append("⬆️ Require elevators")
    if visual_impaired:
        selected_items.append("👓 Visually impaired")
    if hearing_impaired:
        selected_items.append("🎧 Hearing impaired")
    
    if selected_items:
        for item in selected_items:
            st.write(f"✓ {item}")
    else:
        display_info("No specific accessibility requirements selected")