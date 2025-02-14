import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio  # Add this line
from datetime import datetime
from reportlab.lib.pagesizes import letter  # Add this line
from reportlab.pdfgen import canvas  # Add this line


# Title of the app
st.title("Sales Data Analysis Dashboard")

# File uploader
uploaded_file = st.file_uploader("Upload your sales data (CSV file)", type=["csv"])

if uploaded_file is not None:
    # Load the dataset
    df = pd.read_csv(uploaded_file)

    # Display dataset
    st.write("### Dataset Preview")
    st.write(df.head())

    # Data cleaning
    st.write("### Data Cleaning")
    if 'Order Date' in df.columns:
        df['Order Date'] = pd.to_datetime(df['Order Date'])
    if 'Ship Date' in df.columns:
        df['Ship Date'] = pd.to_datetime(df['Ship Date'])
    df = df.drop_duplicates()
    st.write("Cleaned Dataset:")
    st.write(df.head())

    # Add Month and Year columns for time-based analysis
    df['Month'] = df['Order Date'].dt.to_period('M')
    df['Year'] = df['Order Date'].dt.year

    # 1. Total Sales and Profit Over Time
    st.write("### Total Sales and Profit Over Time")
    time_sales_profit = df.groupby('Month').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
    time_sales_profit['Month'] = time_sales_profit['Month'].astype(str)

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=time_sales_profit['Month'], y=time_sales_profit['Sales'], mode='lines+markers', name='Sales'))
    fig1.add_trace(go.Scatter(x=time_sales_profit['Month'], y=time_sales_profit['Profit'], mode='lines+markers', name='Profit'))
    fig1.update_layout(title='Total Sales and Profit Over Time', xaxis_title='Month', yaxis_title='Amount')
    st.plotly_chart(fig1)

    # 2. Sales and Profit by Category
    st.write("### Sales and Profit by Category")
    category_sales_profit = df.groupby('Category').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()

    fig2 = px.bar(category_sales_profit, x='Category', y=['Sales', 'Profit'], barmode='group',
                  title='Sales and Profit by Category', labels={'value': 'Amount'})
    st.plotly_chart(fig2)

    # 3. Profit by Region
    st.write("### Profit by Region")
    region_profit = df.groupby('Region')['Profit'].sum().reset_index()

    fig3 = px.bar(region_profit, x='Region', y='Profit', title='Profit by Region')
    st.plotly_chart(fig3)

    # 4. Top 10 Best-Selling Products
    st.write("### Top 10 Best-Selling Products")
    top_products = df.groupby('Product Name')['Sales'].sum().nlargest(10).reset_index()

    fig4 = px.bar(top_products, x='Product Name', y='Sales', title='Top 10 Best-Selling Products')
    st.plotly_chart(fig4)

    # 5. Sales Distribution by Sub-Category
    st.write("### Sales Distribution by Sub-Category")
    subcategory_sales = df.groupby('Sub-Category')['Sales'].sum().reset_index()

    fig5 = px.pie(subcategory_sales, values='Sales', names='Sub-Category', title='Sales Distribution by Sub-Category')
    st.plotly_chart(fig5)

    # 6. Discount vs Sales and Profit
    st.write("### Discount vs Sales and Profit")
    discount_sales_profit = df.groupby('Discount').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()

    fig6 = px.scatter(discount_sales_profit, x='Discount', y='Sales', size='Profit',
                      title='Discount vs Sales and Profit', labels={'Sales': 'Total Sales', 'Profit': 'Total Profit'})
    st.plotly_chart(fig6)

    # 7. Customer Segmentation (Sales vs Profit)
    st.write("### Customer Segmentation (Sales vs Profit)")
    fig7 = px.scatter(df, x='Sales', y='Profit', color='Category',
                      title='Customer Segmentation: Sales vs Profit', labels={'Sales': 'Total Sales', 'Profit': 'Total Profit'})
    st.plotly_chart(fig7)

    # Generate Report
    # Generate Report
st.write("### Generate Report")
if st.button("Generate PDF Report"):
    # Create PDF
    # Generate PDF using reportlab
def generate_pdf():
    c = canvas.Canvas("sales_report.pdf", pagesize=letter)
    
    # Add title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, "Sales Data Analysis Report")
    
    # Add date
    c.setFont("Helvetica", 12)
    c.drawString(100, 730, f"Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Add insights
    c.drawString(100, 710, "Key Insights:")
    insights = [
        f"1. Total Sales: ${df['Sales'].sum():,.2f}",
        f"2. Total Profit: ${df['Profit'].sum():,.2f}",
        f"3. Best-Selling Category: {category_sales_profit.loc[category_sales_profit['Sales'].idxmax(), 'Category']}",
        f"4. Most Profitable Region: {region_profit.loc[region_profit['Profit'].idxmax(), 'Region']}",
        f"5. Top-Selling Product: {top_products.loc[top_products['Sales'].idxmax(), 'Product Name']}"
    ]
    y = 690
    for line in insights:
        c.drawString(100, y, line)
        y -= 20
    
    # Save plots as images
    pio.write_image(fig1, "monthly_sales_profit.png")
    pio.write_image(fig2, "category_sales_profit.png")
    pio.write_image(fig3, "region_profit.png")
    pio.write_image(fig4, "top_products.png")
    pio.write_image(fig5, "subcategory_sales.png")
    pio.write_image(fig6, "discount_sales_profit.png")
    pio.write_image(fig7, "customer_segmentation.png")
    
    # Add plots to PDF
    y = 650
    for image in ["monthly_sales_profit.png", "category_sales_profit.png", "region_profit.png", 
                  "top_products.png", "subcategory_sales.png", "discount_sales_profit.png", 
                  "customer_segmentation.png"]:
        c.drawImage(image, 50, y - 200, width=500, height=200)
        y -= 250
    
    # Save PDF
    c.save()

# Generate Report
st.write("### Generate Report")
if st.button("Generate PDF Report"):
    generate_pdf()
    st.success("Report generated successfully!")
    
    # Provide download link
    with open("sales_report.pdf", "rb") as file:
        st.download_button(
            label="Download Report",
            data=file,
            file_name="sales_report.pdf",
            mime="application/pdf"
        )

    # Provide download link
    with open("sales_report.pdf", "rb") as file:
        st.download_button(
            label="Download Report",
            data=file,
            file_name="sales_report.pdf",
            mime="application/pdf"
        )