import streamlit as st
import plotly.graph_objs as go
import plotly.express as px

def render_user_stats(user_stats):
    st.subheader("Your Conversation Stats")
    
    fig = go.Figure(data=[
        go.Bar(name='Total Conversations', x=['Conversations'], y=[user_stats['total_conversations']]),
        go.Bar(name='Avg. Messages per Conversation', x=['Avg. Messages'], y=[user_stats['avg_messages_per_conversation']])
    ])
    fig.update_layout(barmode='group')
    st.plotly_chart(fig)

    st.subheader("Your Daily Usage")
    daily_usage_df = px.data.DataFrame(
        {"date": user_stats['daily_usage'].keys(), "conversations": user_stats['daily_usage'].values()}
    )
    fig = px.line(daily_usage_df, x="date", y="conversations", title="Your Daily Conversations")
    st.plotly_chart(fig)

    st.subheader("Your Favorite Topics")
    fig = px.pie(
        values=list(user_stats['favorite_topics'].values()),
        names=list(user_stats['favorite_topics'].keys()),
        title="Top 5 Conversation Topics"
    )
    st.plotly_chart(fig)

def render_overall_stats(overall_stats):
    st.subheader("Platform Overview")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Users", overall_stats['total_users'])
        st.metric("Total Conversations", overall_stats['total_conversations'])
    with col2:
        st.metric("Total Prompts", overall_stats['total_prompts'])
    
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