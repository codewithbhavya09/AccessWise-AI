import streamlit as st
import sys
import os

# Add paths
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Initialize database
from database.db_init import init_database
from database.db_queries import get_connection
from utils.helpers import set_page_config, add_custom_css, display_success, display_error
from utils.config import APP_NAME, APP_ICON

# Initialize database on startup
init_database()

# Set page configuration
set_page_config()
add_custom_css()

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.user_email = None
    st.session_state.user_name = None

# Main app
def main():
    st.markdown(f"<h1 style='text-align: center; color: #667eea;'>{APP_ICON} {APP_NAME}</h1>", unsafe_allow_html=True)
    
    if not st.session_state.logged_in:
        show_welcome()
    else:
        show_main_app()

def show_welcome():
    """Show welcome page for non-logged-in users"""
    col1, col2, col3 = st.columns(3)
    
    with col2:
        st.markdown("""
        ### Welcome to AccessWise AI
        
        An intelligent navigation system designed to help:
        - Wheelchair users
        - Visually impaired people
        - Senior citizens
        - People with temporary mobility challenges
        
        **Features:**
        - 🗺️ AI-powered route recommendations
        - 🤖 Obstacle detection from images
        - 📊 Accessibility scoring
        - 📍 Find nearby accessible facilities
        - 🆘 Emergency SOS assistance
        """)
        
        col_login, col_signup = st.columns(2)
        with col_login:
            if st.button("🔐 Login", use_container_width=True):
                st.session_state.page = "login"
                st.rerun()
        
        with col_signup:
            if st.button("📝 Sign Up", use_container_width=True):
                st.session_state.page = "signup"
                st.rerun()
    
    # Handle page navigation
    if 'page' in st.session_state:
        if st.session_state.page == "login":
            show_login_page()
        elif st.session_state.page == "signup":
            show_signup_page()

def show_login_page():
    """Show login page"""
    st.subheader("🔐 Login")
    
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Login", use_container_width=True):
        from database.db_queries import get_user_by_email
        from utils.helpers import verify_password
        
        user = get_user_by_email(email)
        
        if user and verify_password(password, user[2]):
            st.session_state.logged_in = True
            st.session_state.user_id = user[0]
            st.session_state.user_email = user[1]
            st.session_state.user_name = user[3]
            display_success(f"Welcome back, {user[3]}!")
            st.rerun()
        else:
            display_error("Invalid email or password")
    
    if st.button("Back to Welcome"):
        if 'page' in st.session_state:
            del st.session_state.page
        st.rerun()

def show_signup_page():
    """Show signup page"""
    st.subheader("📝 Sign Up")
    
    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    
    if st.button("Create Account", use_container_width=True):
        from database.db_queries import create_user
        from utils.helpers import hash_password
        from utils.validators import validate_email, validate_password
        
        if not validate_email(email):
            display_error("Invalid email format")
        elif password != confirm_password:
            display_error("Passwords do not match")
        elif not validate_password(password)[0]:
            display_error(validate_password(password)[1])
        else:
            hashed_password = hash_password(password)
            user_id = create_user(email, hashed_password, full_name)
            
            if user_id:
                st.session_state.logged_in = True
                st.session_state.user_id = user_id
                st.session_state.user_email = email
                st.session_state.user_name = full_name
                display_success(f"Account created successfully! Welcome, {full_name}!")
                st.rerun()
            else:
                display_error("Email already registered")
    
    if st.button("Back to Welcome"):
        if 'page' in st.session_state:
            del st.session_state.page
        st.rerun()

def show_main_app():
    """Show main application"""
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown(f"### Welcome, {st.session_state.user_name}! 👋")
        
        page = st.radio(
            "Navigation",
            [
                "🏠 Dashboard",
                "♿ Accessibility Profile",
                "🗺️ Route Navigator",
                "📷 Image Upload",
                "📍 Nearby Places",
                "💬 Feedback",
                "👨‍💼 Admin Dashboard",
                "🚪 Logout"
            ]
        )
        
        st.markdown("---")
        st.markdown("""
        ### About AccessWise AI
        Helping people with mobility challenges
        find safer, more accessible routes.
        """)
    
    # Route to appropriate page
    if page == "🏠 Dashboard":
        from pages import dashboard
        dashboard.show()
    elif page == "♿ Accessibility Profile":
        from pages import accessibility_profile
        accessibility_profile.show()
    elif page == "🗺️ Route Navigator":
        from pages import map_navigator
        map_navigator.show()
    elif page == "📷 Image Upload":
        from pages import image_upload
        image_upload.show()
    elif page == "📍 Nearby Places":
        from pages import nearby_places
        nearby_places.show()
    elif page == "💬 Feedback":
        from pages import feedback
        feedback.show()
    elif page == "👨‍💼 Admin Dashboard":
        from pages import admin_dashboard
        admin_dashboard.show()
    elif page == "🚪 Logout":
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.user_email = None
        st.session_state.user_name = None
        display_success("Logged out successfully!")
        st.rerun()

if __name__ == "__main__":
    main()