import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import plotly.express as px
import urllib.request
import pandas as pd

class Data:
    def __init__(self, df):
        self.df = df
    
    def demografis_analysis(self, option: str, ascending: bool = False, number_data: int = 10):
        if option == "customer":
            by_demografi_state = self.df.groupby("customer_state").agg({
                "order_item_id" : "sum"
            }).reset_index()

            by_demografi_state.rename(columns={
                "order_item_id":"total_customer"
            }, inplace=True)

            return by_demografi_state.sort_values(by="total_customer", ascending=ascending).head(number_data)
        elif option == "order":
            by_demografi_city = self.df.groupby("customer_city").order_item_id.sum().reset_index()
            by_demografi_city.rename(columns={
                "order_item_id" : "total_order"
            }, inplace=True)

            return by_demografi_city.sort_values(by="total_order", ascending=ascending).head(number_data)
        else:
            raise ValueError("Invalid option provided")


    def geografis_analysis(self, df_geoloc):
        distribution_customer = pd.merge(
        left=self.df,
        right=df_geoloc,
        how="inner",
        left_on="customer_zip_code_prefix",
        right_on="geolocation_zip_code_prefix"
        )

        distribution_customer.drop(columns=["geolocation_city", "geolocation_state", "geolocation_zip_code_prefix"], inplace=True)

        return distribution_customer.drop_duplicates("customer_unique_id")

    def customer_grow_analysis(self, option: str = "month"):
        self.df["order_purchase_timestamp"] = pd.to_datetime(self.df["order_purchase_timestamp"])
        if option == "year":
            grow_customer_year = self.df.resample(rule="YE", on="order_purchase_timestamp").agg({
            "order_id" : "nunique",
            "price" : "sum"
            })

            grow_customer_year.index = grow_customer_year.index.strftime('%Y')
            grow_customer_year = grow_customer_year.reset_index() 
            grow_customer_year = grow_customer_year.rename(columns={
                "order_purchase_timestamp" : "year",
                "order_id" : "total_order",
            })

            return grow_customer_year

        elif option == "month":
            grow_customer_monthly = self.df.resample(rule="ME", on="order_purchase_timestamp").agg({
                "order_id" : "nunique",
                "price" : "sum"
            })

            grow_customer_monthly.index = grow_customer_monthly.index.strftime("%Y-%m")
            grow_customer_monthly = grow_customer_monthly.reset_index()

            grow_customer_monthly.rename(columns={
                "order_purchase_timestamp" : "month",
                "order_id" : "total_order",
            }, inplace=True)
            return grow_customer_monthly[:len(grow_customer_monthly)-1]
        else:
            raise ValueError("Invalid option provided")

    def product_analysis(self):
        try:
            product = self.df.groupby("product_category_name_english").agg({
                "product_id" : "nunique",
                "price" : "sum"
            }).reset_index()

            product.rename(columns={
                    "product_id" : "total_order",
                    "product_category_name_english" : "product_name",
                    "price" : "total_pendapatan"
                }, inplace=True)
            
            return product
        except:
            raise ValueError("Invalid Error")
        

    def product_revenue(self, option: str):
        self.df["order_purchase_timestamp"] = pd.to_datetime(self.df["order_purchase_timestamp"])
        if option == "year":
            revenue_year = self.df.resample(rule="YE", on="order_purchase_timestamp").agg({
            "price" : "sum"
            })

            revenue_year.index = revenue_year.index.strftime('%Y')
            revenue_year = revenue_year.reset_index() 
            revenue_year = revenue_year.rename(columns={
                "order_purchase_timestamp" : "year",
            })

            return revenue_year
        
        elif option == "month":
            revenue_month = self.df.resample(rule="ME", on="order_purchase_timestamp").agg({
                "price" : "sum"
            })

            revenue_month.index = revenue_month.index.strftime("%Y-%m")
            revenue_month = revenue_month.reset_index()

            revenue_month.rename(columns={
                "order_purchase_timestamp" : "month",
            }, inplace=True)

            return revenue_month[:len(revenue_month)-1]
            
    def customer_payment_analysis(self):
        customer_purchase = self.df.groupby("payment_type").agg({
            "payment_sequential" : "sum"
        }).reset_index()

        return customer_purchase.sort_values(by="payment_sequential", ascending=False)



        
    















        

    