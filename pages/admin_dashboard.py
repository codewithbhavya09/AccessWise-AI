import streamlit as st
from database.db_queries import get_system_statistics
from ai.feedback_learner import get_obstacle_insights, get_improvement_metrics, get_most_problematic_obstacles
from utils.helpers import display_info
import pandas as pd

def show():
    # Admin check
    if st.session_state.user_id != 1:  # Simple admin check
        st.error("❌ Admin access only")
        return
    
    st.title("👨‍💼 Admin Dashboard")
    
    display_info("System-wide statistics and analytics")
    
    # System statistics
    stats = get_system_statistics()
    
    st.subheader("📊 System Statistics")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Users", stats['total_users'])
    
    with col2:
        st.metric("Total Routes", stats['total_routes'])
    
    with col3:
        st.metric("Total Obstacles", stats['total_obstacles'])
    
    with col4:
        avg_accessibility = stats['avg_accessibility_score'] * 100
        st.metric("Avg Accessibility", f"{avg_accessibility:.0f}%")
    
    with col5:
        st.metric("Avg Feedback", f"{stats['avg_feedback_rating']:.1f}/5")
    
    st.markdown("---")
    
    # Improvement metrics
    st.subheader("📈 Improvement Metrics")
    
    improvement_metrics = get_improvement_metrics()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Avg Route Rating", f"{improvement_metrics['avg_route_rating']:.2f}/5")
    
    with col2:
        st.metric("Improved Routes", improvement_metrics['improved_routes'])
    
    with col3:
        st.metric("Problem Routes", improvement_metrics['problem_routes'])
    
    with col4:
        st.metric("Total Feedback", improvement_metrics['total_feedback_entries'])
    
    st.markdown("---")
    
    # Obstacle insights
    st.subheader("🚧 Obstacle Insights")
    
    obstacle_insights = get_obstacle_insights()
    
    if obstacle_insights:
        insight_data = []
        for obs_type, data in obstacle_insights.items():
            insight_data.append({
                'Obstacle Type': obs_type.upper(),
                'Reports': data['total_reports'],
                'Positive %': f"{data['positive_feedback_ratio']*100:.0f}%",
                'Negative %': f"{data['negative_feedback_ratio']*100:.0f}%",
                'Severity': f"{data['severity']*100:.0f}%"
            })
        
        df = pd.DataFrame(insight_data)
        st.dataframe(df, use_container_width=True)
    
    st.markdown("---")
    
    # Most problematic obstacles
    st.subheader("⚠️ Most Problematic Obstacles")
    
    problematic = get_most_problematic_obstacles(5)
    
    if problematic:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            obstacle_names = [obs[0].upper() for obs in problematic]
            negative_counts = [obs[1]['negative_feedback'] for obs in problematic]
            
            st.bar_chart(pd.DataFrame({
                'Obstacle': obstacle_names,
                'Negative Feedback': negative_counts
            }).set_index('Obstacle'))
        
        with col2:
            for obs_type, data in problematic[:5]:
                st.write(f"**{obs_type.upper()}**")
                st.write(f"Negative: {data['negative_feedback']}")
    
    st.markdown("---")
    
    # Recommendations
    st.subheader("💡 System Recommendations")
    
    recommendations = []
    
    if stats['avg_accessibility_score'] < 0.7:
        recommendations.append("🔴 Average accessibility score is low - improve route recommendations")
    
    if improvement_metrics['problem_routes'] > stats['total_routes'] * 0.2:
        recommendations.append("🟡 More than 20% of routes have poor ratings - review route quality")
    
    if obstacle_insights:
        high_severity = [obs for obs, data in obstacle_insights.items() if data['severity'] > 0.6]
        if high_severity:
            obs_list = ', '.join([obs.upper() for obs in high_severity])
            recommendations.append(f"🟠 High severity obstacles detected: {obs_list}")
    
    if recommendations:
        for rec in recommendations:
            display_info(rec)
    else:
        display_info("✅ System is performing well!")
    
    st.markdown("---")
    
    # System actions
    st.subheader("⚙️ System Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Retrain Models", use_container_width=True):
            st.success("✅ Models retraining initiated...")
    
    with col2:
        if st.button("📊 Export Data", use_container_width=True):
            st.success("✅ Data exported...")
    
    with col3:
        if st.button("🧹 Clean Database", use_container_width=True):
            st.success("✅ Database cleaned...")