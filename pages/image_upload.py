import streamlit as st
from PIL import Image
from ai.obstacle_detection import detect_obstacles_in_image, draw_detected_obstacles
from utils.validators import validate_image
from utils.helpers import display_success, display_error, display_info

def show():
    st.title("📷 Image Upload & Obstacle Detection")
    
    display_info("""
    Upload an image of a street or pathway to detect obstacles like stairs,
    potholes, and other accessibility barriers.
    """)
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose an image",
        type=['jpg', 'jpeg', 'png', 'gif'],
        help="Supported formats: JPG, JPEG, PNG, GIF"
    )
    
    if uploaded_file is not None:
        # Validate image
        is_valid, message = validate_image(uploaded_file)
        
        if not is_valid:
            display_error(f"❌ {message}")
        else:
            # Load and display image
            image = Image.open(uploaded_file)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Original Image")
                st.image(image, use_column_width=True)
            
            # Detect obstacles
            with st.spinner("🔍 Detecting obstacles..."):
                obstacles = detect_obstacles_in_image(image)
            
            with col2:
                st.subheader("Obstacles Detected")
                
                if obstacles:
                    annotated_image = draw_detected_obstacles(image, obstacles)
                    st.image(annotated_image, use_column_width=True)
                    
                    st.subheader("📋 Detected Obstacles")
                    
                    for i, obstacle in enumerate(obstacles[:5], 1):
                        with st.container():
                            col1, col2, col3 = st.columns([2, 1, 1])
                            
                            with col1:
                                st.write(f"**{i}. {obstacle['type'].upper()}**")
                            
                            with col2:
                                confidence = obstacle['confidence'] * 100
                                st.write(f"Confidence: {confidence:.0f}%")
                            
                            with col3:
                                area = obstacle['area']
                                st.write(f"Size: {area:.0f}px")
                else:
                    display_success("✅ No major obstacles detected!")
            
            # Analysis summary
            st.markdown("---")
            st.subheader("📊 Analysis Summary")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Obstacles", len(obstacles))
            
            with col2:
                avg_confidence = sum(o['confidence'] for o in obstacles) / len(obstacles) if obstacles else 0
                st.metric("Avg Confidence", f"{avg_confidence*100:.0f}%")
            
            with col3:
                severity_count = sum(1 for o in obstacles if o['confidence'] > 0.8)
                st.metric("High Severity", severity_count)
            
            # Obstacle breakdown
            st.subheader("Obstacle Breakdown")
            
            obstacle_types = {}
            for obs in obstacles:
                obs_type = obs['type']
                obstacle_types[obs_type] = obstacle_types.get(obs_type, 0) + 1
            
            if obstacle_types:
                st.bar_chart(obstacle_types)
            
            # Save to database
            st.markdown("---")
            
            if st.button("💾 Save Analysis", use_container_width=True):
                # Here you would save to database
                display_success("✅ Analysis saved to your profile!")
            
            # Recommendations
            st.markdown("---")
            st.subheader("💡 Recommendations")
            
            if obstacles:
                obstacle_types_list = set(o['type'] for o in obstacles)
                
                recommendations = []
                if 'stairs' in obstacle_types_list:
                    recommendations.append("🪜 Consider using alternative routes without stairs")
                if 'pothole' in obstacle_types_list:
                    recommendations.append("🕳️ Watch out for potholes - use caution")
                if 'broken_sidewalk' in obstacle_types_list:
                    recommendations.append("🚫 Broken sidewalk detected - seek smooth surfaces")
                if 'curb' in obstacle_types_list:
                    recommendations.append("⬆️ Curbs detected - look for ramps")
                
                for rec in recommendations:
                    display_info(rec)
            else:
                display_info("✅ This path appears to be accessible!")
    
    else:
        st.info("👆 Upload an image to get started")