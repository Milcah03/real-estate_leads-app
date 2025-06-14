import streamlit as st
import pandas as pd
import plotly.express as px
import psycopg2
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os



load_dotenv() 

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# SQLAlchemy connection string
engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Load Data 
df = pd.read_sql("SELECT * FROM leads", engine)

# Streamlit App 
st.title("📈 Leads Dashboard")
st.markdown("Visual analysis of the leads table")

#  Overview
st.subheader("🔍 Data Preview")
st.dataframe(df.head())

# by Source 
st.subheader("📊 Leads by Source")
source_count = df['source'].value_counts().reset_index()
source_count.columns = ['source', 'count']
fig_source = px.bar(
    source_count, 
    x='source', 
    y='count', 
    labels={'count': 'Lead Count'},
    color='count',
    color_continuous_scale='Tealgrn'
)
st.plotly_chart(fig_source, use_container_width=True)

# Avg Response Time by Source 
st.subheader("⏱ Avg Response Time by Source")
avg_response_by_source = df.groupby('source')['response_time'].mean().reset_index()
fig_avg_source = px.bar(
    avg_response_by_source,
    x='source',
    y='response_time',
    labels={'response_time': 'Avg Response Time (s)', 'source': 'Source'},
    color='response_time',
    color_continuous_scale='Mint',
    title="Avg Response Time by Source"
)
fig_avg_source.update_coloraxes(colorbar_title="Response Time (s)")
st.plotly_chart(fig_avg_source, use_container_width=True)

# Leads by Agent 
st.subheader("👤 Leads by Agent")
agent_count = df['agent_name'].value_counts().reset_index()
agent_count.columns = ['agent_name', 'count']
fig_agent = px.bar(
    agent_count, 
    x='agent_name', 
    y='count', 
    labels={'count': 'Lead Count'},
    color='count',
    color_continuous_scale='Purpor'
)
st.plotly_chart(fig_agent, use_container_width=True)

# Avg Response Time by Agent 
st.subheader("🚀 Avg Response Time by Agent")
avg_response_by_agent = df.groupby('agent_name')['response_time'].mean().reset_index()
fig_avg_agent = px.bar(
    avg_response_by_agent,
    x='agent_name',
    y='response_time',
    labels={'response_time': 'Avg Response Time (s)', 'agent_name': 'Agent'},
    color='response_time',
    color_continuous_scale='Plasma',
    title="Avg Response Time by Agent"
)
fig_avg_agent.update_coloraxes(colorbar_title="Response Time (s)")
st.plotly_chart(fig_avg_agent, use_container_width=True)

# Leads by Status
st.subheader("📌 Leads by Status")
status_count = df['status'].value_counts().reset_index()
status_count.columns = ['status', 'count']
fig_status = px.pie(
    status_count, 
    names='status', 
    values='count', 
    title="Lead Status Breakdown",
    color_discrete_sequence=px.colors.sequential.Sunsetdark
)
st.plotly_chart(fig_status, use_container_width=True)

# Leads over Time 
if 'timestamp' in df.columns:
    st.subheader("📆 Leads Over Time")
    leads_over_time = df.groupby(df['timestamp'].dt.date).size().reset_index(name='count')
    fig_time = px.line(
        leads_over_time, 
        x='timestamp', 
        y='count', 
        title='Leads Over Time',
        markers=True,
        color_discrete_sequence=['#4C78A8']
    )
    st.plotly_chart(fig_time, use_container_width=True)
