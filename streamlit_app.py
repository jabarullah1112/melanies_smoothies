import streamlit as st
from snowflake.snowpark.context import get_active_session
import pandas as pd
import requests

from snowflake.snowpark import Session
import streamlit as st

connection_parameters = st.secrets["snowflake"]

session = Session.builder.configs(connection_parameters).create()

st.title("🍹 Smoothie Order App")

# 🔹 Inputs
name_on_order = st.text_input("Enter your name")

fruit_df = session.table("smoothies.public.fruit_options").to_pandas()

st.subheader("Available Fruits")
st.dataframe(fruit_df)

fruit_name_list = fruit_df["FRUIT_NAME"].tolist()
fruit_map = dict(zip(fruit_df["FRUIT_NAME"], fruit_df["SEARCH_ON"]))

ingredients_list = st.multiselect("Choose fruits", fruit_name_list)

order_filled = st.checkbox("Order Filled")

submit_button = st.button("Submit Order")

if submit_button:
    if name_on_order and ingredients_list:

        ingredients_string = ",".join(ingredients_list)

        filled_value = "TRUE" if order_filled else "FALSE"

        query = f"""
        insert into smoothies.public.orders
        (name_on_order, ingredients, order_filled)
        values (
            '{name_on_order}',
            '{ingredients_string}',
            {filled_value}
        )
        """

        session.sql(query).collect()
        st.success("Order placed successfully!")
