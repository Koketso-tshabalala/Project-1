import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sales Dashboard", layout="wide")

# Load real dataset
df=pd.read_excel('SuperStore sales DataSet.xlsx', sheet_name='Sheet1')
df=df.drop(columns=['ind1', 'ind2', 'Row ID + 06G3A1:R6'], errors='ignore')
df['Order Date']=pd.to_datetime(df['Order Date'])

st.title("Sales Performance Dashboard - Project 1")
st.caption("Built in VS Code | Data: SuperStore 5901 rows")

# KPIs
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Revenue", f"${df['Sales'].sum():,.0f}")
c2.metric("Total Profit", f"${df['Profit'].sum():,.0f}")
c3.metric("Total Orders", df['Order ID'].nunique())
c4.metric("Profit Margin", f"{df['Profit'].sum()/df['Sales'].sum()*100:.1f}%")

col1, col2 = st.columns(2)
with col1:
    region = df.groupby('Region')['Sales'].sum().reset_index()
    fig = px.bar(region, x='Region', y='Sales', color='Region', title='Region-wise Sales Comparison')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    cat = df.groupby('Category')['Sales'].sum().reset_index()
    fig = px.pie(cat, values='Sales', names='Category', title='Category-wise Sales')
    st.plotly_chart(fig, use_container_width=True)

col3, col4 = st.columns(2)
with col3:
    monthly = df.groupby(df['Order Date'].dt.to_period('M').astype(str))['Sales'].sum().reset_index()
    fig = px.line(monthly, x='Order Date', y='Sales', markers=True, title='Monthly Sales Trend (2019-2020)')
    st.plotly_chart(fig, use_container_width=True)

with col4:
    top = df.groupby('Product Name')['Sales'].sum().nlargest(5).reset_index()
    fig = px.bar(top, x='Sales', y='Product Name', orientation='h', title='Top 5 Selling Products')
    st.plotly_chart(fig, use_container_width=True)

low = df.groupby('Product Name')['Sales'].sum().nsmallest(5).reset_index()
fig = px.bar(top, x='Sales', y='Product Name', orientation='h', title='Low 5 Products (Opportunity)', color_discrete_sequence=['red'])
st.plotly_chart(fig, use_container_width=True)

          