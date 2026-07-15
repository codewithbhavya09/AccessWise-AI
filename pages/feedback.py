import streamlit as st
from database.db_queries import add_feedback, get_user_routes, get_feedback_for_route
from utils.helpers import display_success, display_info
from ai.feedback_learner import add_feedback as add_feedback_to_learner

def show():
    st.title("💬 User Feedback")
    
    display_info("""
    Your feedback helps us improve route recommendations and obstacle detection.
    Please share your experience with recent routes.
    """)
    
    # Get user routes
    user_id = st.session_state.user_id
    routes = get_user_routes(user_id, limit=10)
    
    if not routes:
        st.info("👈 No routes yet. Navigate a route first to provide feedback.")
        return
    
    # Route selection
    st.subheader("Select Route")
    
    route_options = {f"{r[2]} → {r[3]}" : r[0] for r in routes}
    selected_route_label = st.selectbox("Choose a route", list(route_options.keys()))
    selected_route_id = route_options[selected_route_label]
    
    st.markdown("---")
    st.subheader("📝 Feedback Form")
    
    # Rating
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.write("**Rating:**")
    
    with col2:
        rating = st.slider(
            "How satisfied are you with this route?",
            min_value=1,
            max_value=5,
            value=3,
            label_visibility='collapsed'
        )
        
        rating_text = {
            1: "😞 Very Poor",
            2: "😕 Poor",
            3: "😐 Neutral",
            4: "🙂 Good",
            5: "😍 Excellent"
        }
        st.write(rating_text[rating])
    
    st.markdown("---")
    
    # Comments
    st.write("**Comments:**")
    comments = st.text_area(
        "Tell us about your experience",
        placeholder="Share your experience with this route...",
        height=150,
        label_visibility='collapsed'
    )
    
    # Obstacle reporting
    st.markdown("---")
    st.write("**Obstacles Encountered:**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        stairs = st.checkbox("Stairs")
    with col2:
        potholes = st.checkbox("Potholes")
    with col3:
        broken_sidewalk = st.checkbox("Broken Sidewalk")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        construction = st.checkbox("Construction")
    with col2:
        curbs = st.checkbox("Curbs")
    with col3:
        water = st.checkbox("Standing Water")
    
    # Collect reported obstacles
    reported_obstacles = []
    if stairs:
        reported_obstacles.append('stairs')
    if potholes:
        reported_obstacles.append('pothole')
    if broken_sidewalk:
        reported_obstacles.append('broken_sidewalk')
    if construction:
        reported_obstacles.append('construction')
    if curbs:
        reported_obstacles.append('curb')
    if water:
        reported_obstacles.append('water')
    
    # Additional feedback
    st.markdown("---")
    st.write("**Additional Feedback:**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        would_recommend = st.checkbox("Would recommend this route", value=rating >= 4)
    
    with col2:
        report_issue = st.checkbox("Report a specific issue")
    
    if report_issue:
        issue_type = st.selectbox(
            "Issue type",
            ["Safety Concern", "Accessibility Problem", "Route Inaccuracy", "Other"]
        )
        issue_description = st.text_area("Describe the issue")
    
    # Submit button
    st.markdown("---")
    
    if st.button("📤 Submit Feedback", use_container_width=True):
        if not comments and not reported_obstacles:
            st.error("❌ Please provide at least some feedback")
        else:
            add_feedback(
                route_id=selected_route_id,
                user_id=user_id,
                rating=rating,
                comments=comments
            )
            
            add_feedback_to_learner(
                route_id=selected_route_id,
                user_id=user_id,
                rating=rating,
                comments=comments,
                obstacles_reported=reported_obstacles
            )
            
            display_success("✅ Thank you for your feedback! It helps us improve.")
    
    # View existing feedback
    st.markdown("---")
    st.subheader("📊 Route Feedback Summary")
    
    route_feedback = get_feedback_for_route(selected_route_id)
    
    if route_feedback:
        total_feedback = len(route_feedback)
        avg_rating = sum(f[3] for f in route_feedback if f[3]) / total_feedback if route_feedback else 0
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Feedback", total_feedback)
        
        with col2:
            st.metric("Avg Rating", f"{avg_rating:.1f}/5")
        
        with col3:
            recommend_count = sum(1 for f in route_feedback if f[3] and f[3] >= 4)
            st.metric("Would Recommend", f"{recommend_count}/{total_feedback}")