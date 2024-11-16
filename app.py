import streamlit as st
import plotly.express as px
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import pandas as pd
import urllib
from utils import Data

st.set_page_config(layout="wide")

# load data
df_all = pd.read_csv("dataset/df_all.csv")
df_geoloc = pd.read_csv("dataset/geolocation_dataset.csv")
data = Data(df_all)


# Data
# The code snippet you provided is calling various methods from the `Data` class to perform different
# types of data analysis on the datasets loaded earlier in the script.
demografis_customer_df = data.demografis_analysis("customer")
demografis_order_df = data.demografis_analysis("order")
geografis_df = data.geografis_analysis(df_geoloc)
produk_df = data.product_analysis()
customer_payment = data.customer_payment_analysis()
grow_customer_year_df = data.customer_grow_analysis("year")
grow_customer_month_df = data.customer_grow_analysis("month")
revenue_year_df = data.product_revenue("year")
revenue_month_df = data.product_revenue("month")


# The code snippet you provided is creating a sidebar in the Streamlit web application interface.
# Within this sidebar, it is adding two select boxes using `st.selectbox`.
with st.sidebar:
    option_grow_customer = st.selectbox(
        "Showing Grow Customer Year or Month",
        ("month", "year")
    )

    option_revenue = st.selectbox(
        "Showing revenue Year or Month",
        ("month", "year")
    )


st.title("Dashboard")
# The code snippet you provided is creating a layout in the Streamlit web application interface with
# two columns (`col1` and `col2`). In the first column (`col1`), it is displaying a scatter plot
# overlaid on an image of Brazil. Here's a breakdown of what each part of the code is doing:
col1, col2 = st.columns(2)
with col1:
    brazil = mpimg.imread(urllib.request.urlopen('https://i.pinimg.com/originals/3a/0c/e1/3a0ce18b3c842748c255bc0aa445ad41.jpg'),'jpg')
    fig, ax = plt.subplots(figsize=(10, 12))
    geografis_df.plot(kind="scatter", x="geolocation_lng", y="geolocation_lat", ax=ax, s=0.5)
    ax.imshow(brazil, extent=[-73.98283055, -33.8,-33.75116944,5.4], aspect='auto')
    ax.axis("off")
    st.pyplot(fig)

with col2:
    fig_customer = px.bar(demografis_customer_df,
            x="customer_state",
            y="total_customer",
            title="Total customer by State",
            height=400,
            color="total_customer",
            color_continuous_scale=["#E9FBFD", "#1F77B4"],
            labels={"customer_state": "Customer State", "total_customer": "Total Customers"})
        
    st.plotly_chart(fig_customer)

    
    fig_order = px.bar(demografis_order_df,
            x="customer_city",
            y="total_order",
            title="Most Ordered Items by City",
            height=400,
            color="total_order",
            color_continuous_scale=["#E9FBFD", "#1F77B4"],
            labels={"customer_city": "Customer City", "total_order": "Total Orders"})
        
    st.plotly_chart(fig_order)

# This code snippet is responsible for creating a layout in the Streamlit web application interface
# with two columns (`col1` and `col2`). Here's a breakdown of what each part of the code is doing:
col1, col2 = st.columns(2)
with col1:
    if option_grow_customer == "month":
        fig_grow = px.line(grow_customer_month_df, 
                            x="month",
                            y="total_order",
                            markers=True,
                            title="Grow Customer by Month",
                            labels={"month": "Month", "total_order":"Total Order"})
                
        st.plotly_chart(fig_grow, use_container_width=True)
    
    elif option_grow_customer == "year":
        fig_grow = px.line(grow_customer_year_df, 
                            x="year",
                            y="total_order",
                            markers=True,
                            title="Grow Customer by Year",
                            labels={"year": "Year", "total_order":"Total Order"})
                
        st.plotly_chart(fig_grow, use_container_width=True)

 
with col2:
    if option_revenue == "month":
        fig_revenue = px.line(revenue_month_df,
                            x="month", 
                            y="price", 
                            title="Revenue by Month", 
                            markers=True,
                            labels={"month": "Month", "price":"Price"})
            
        st.plotly_chart(fig_revenue, use_container_width=True)
    
    elif option_revenue == "year":
        fig_revenue = px.line(revenue_year_df,
                            x="year", 
                            y="price", 
                            title="Revenue by Month", 
                            markers=True,
                            labels={"year": "Year", "price":"Price"})
            
        st.plotly_chart(fig_revenue, use_container_width=True)


# This code snippet is creating a layout in the Streamlit web application interface with two columns
# (`col1` and `col2`). Within `col1`, it is generating two bar charts using Plotly Express (`px.bar`)
# to visualize the top and lower order products based on the `produk_df` DataFrame. The top order
# products are determined by sorting the DataFrame in descending order based on the "total_order"
# column and selecting the top 10 entries. The lower order products are similarly visualized by
# sorting the DataFrame in ascending order based on the "total_order" column and selecting the top 10
# entries.
col1, col2 = st.columns(2)
with col1:
    fig_top_order =px.bar(produk_df.sort_values(by="total_order", ascending=False).head(10),
            x="product_name",
            y="total_order",
            title="Top Order Product",
            color="total_order",
            color_continuous_scale=["#E9FBFD", "#1F77B4"],
            labels={"product_name": "Product Name", "total_order": "Total Orders"})
        
    st.plotly_chart(fig_top_order)

    fig_lower_order =px.bar(produk_df.sort_values(by="total_order", ascending=True).head(10),
            x="product_name",
            y="total_order",
            title="Lower Order Product",
            color="total_order",
            color_continuous_scale=["#E9FBFD", "#1F77B4"],
            labels={"product_name": "Product Name", "total_order": "Total Orders"})
        
    st.plotly_chart(fig_lower_order)

    

with col2:
    fig_top_product_income =px.bar(produk_df.sort_values(by="total_pendapatan", ascending=False).head(10),
            x="product_name",
            y="total_pendapatan",
            title="Top Product Income",
            color="total_pendapatan",
            color_continuous_scale=["#E9FBFD", "#1F77B4"],
            labels={"product_name": "Product Name", "total_pendapatan": "Total Incomes"})
        
    st.plotly_chart(fig_top_product_income)

    fig_lower_product_income =px.bar(produk_df.sort_values(by="total_order", ascending=True).head(10),
            x="product_name",
            y="total_order",
            title="Lower Product Income",
            color="total_order",
            color_continuous_scale=["#E9FBFD", "#1F77B4"],
            labels={"product_name": "Product Name", "total_order": "Total Incomes"})
        
    st.plotly_chart(fig_lower_product_income)

# This code snippet is creating a bar chart visualization using Plotly Express (`px.bar`). Here's a
# breakdown of what each part of the code is doing:
fig_cust_payment = px.bar(customer_payment,
             x="payment_type", 
             y="payment_sequential",
             color="payment_sequential",
             color_continuous_scale=["#E9FBFD",  "#1F77B4"],
             title="Top Payment")

st.plotly_chart(fig_cust_payment)



