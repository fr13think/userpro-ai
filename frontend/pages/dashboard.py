import streamlit as st
import plotly.graph_objs as go
import plotly.express as px
from datetime import datetime, timedelta

def render(analytics_engine):
    st.title("Analytics Dashboard")

    if st.session_state.user:
        username = st.session_state.user['username']
        user_stats = analytics_engine.get_user_stats(username)
        overall_stats = analytics_engine.get_overall_stats()
        
        st.header("Your Conversation Stats")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Conversation Metrics")
            st.metric("Total Conversations", user_stats['total_conversations'])
            st.metric("Avg. Messages per Conversation", f"{user_stats['avg_messages_per_conversation']:.2f}")
            st.metric("Avg. Conversation Duration", f"{user_stats['avg_conversation_duration']:.2f} seconds")

        with col2:
            st.subheader("Your Favorite Topics")
            fig = px.pie(
                values=list(user_stats['favorite_topics'].values()),
                names=list(user_stats['favorite_topics'].keys()),
                title="Top 5 Conversation Topics"
            )
            st.plotly_chart(fig)

        st.subheader("Your Daily Usage")
        daily_usage_df = px.data.DataFrame(
            {"date": user_stats['daily_usage'].keys(), "conversations": user_stats['daily_usage'].values()}
        )
        fig = px.line(daily_usage_df, x="date", y="conversations", title="Your Daily Conversations")
        st.plotly_chart(fig)

        st.header("Platform Overview")
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Overall Metrics")
            st.metric("Total Users", overall_stats['total_users'])
            st.metric("Total Conversations", overall_stats['total_conversations'])
            st.metric("Total Prompts", overall_stats['total_prompts'])

        with col2:
            st.subheader("Hourly Platform Usage")
            hourly_usage_df = px.data.DataFrame(
                {"hour": overall_stats['hourly_usage'].keys(), "conversations": overall_stats['hourly_usage'].values()}
            )
            fig = px.bar(hourly_usage_df, x="hour", y="conversations", title="Hourly Conversation Distribution")
            st.plotly_chart(fig)

        st.subheader("Daily Active Users (Last 30 Days)")
        dau_df = px.data.DataFrame(
            {"date": overall_stats['daily_active_users'].keys(), "users": overall_stats['daily_active_users'].values()}
        )
        fig = px.line(dau_df, x="date", y="users", title="Daily Active Users")
        st.plotly_chart(fig)

        st.subheader("Your Engagement Score")
        engagement_score = analytics_engine.get_user_engagement_score(username)
        st.progress(engagement_score / 100)
        st.write(f"Your engagement score: {engagement_score:.2f}/100")

        st.subheader("Trending Topics")
        trending_topics = analytics_engine.get_trending_topics()
        fig = px.bar(
            x=list(trending_topics.keys()),
            y=list(trending_topics.values()),
            title="Top 5 Trending Topics"
        )
        st.plotly_chart(fig)

    else:
        st.warning("Please log in to view the dashboard.")