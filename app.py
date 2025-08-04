import pandas as pd
import streamlit as st
import plotly.express as px

# Load the data
df = pd.read_csv("final_crm_data.csv")

st.set_page_config(page_title="AI CRM Dashboard", layout="wide")

st.title("🤖 AI-Driven CRM Analytics Dashboard")

# KPI Section
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Customers", df.shape[0])
with col2:
    st.metric("Churned Customers", df['churn'].sum())
with col3:
    avg_score = round(df['sentiment_score'].mean(), 2)
    st.metric("Avg Sentiment Score", avg_score)

st.divider()

# 📊 Sentiment Distribution
st.subheader("🧠 Sentiment Distribution")
sentiment_counts = df['sentiment_label'].value_counts().reset_index()
sentiment_counts.columns = ['sentiment_label', 'count']  # Rename for clarity
sentiment_fig = px.pie(sentiment_counts, values='count', names='sentiment_label',title ='Sentiment Distribution',
                       color_discrete_sequence=px.colors.sequential.RdBu)
st.plotly_chart(sentiment_fig, use_container_width=True)

# 📈 Cluster Behavior
st.subheader("📊 Customer Behavior Clusters")
cluster_fig = px.scatter(df, x='purchase_count', y='service_calls',
                         color='behavior_cluster',
                         size='device_count',
                         hover_data=['sentiment_label'],
                         title='Clusters Based on Usage & Sentiment')
st.plotly_chart(cluster_fig, use_container_width=True)

# 🚨 Churn Risk Insights
st.subheader("🚨 Churn Risk by Cluster")
churn_by_cluster = df.groupby('behavior_cluster')['churn'].mean().reset_index()
churn_fig = px.bar(churn_by_cluster, x='behavior_cluster', y='churn',
                   color='behavior_cluster', title='Churn Rate per Cluster')
st.plotly_chart(churn_fig, use_container_width=True)

# 🔍 View Data
with st.expander("📄 View Raw Data"):
    st.dataframe(df)
