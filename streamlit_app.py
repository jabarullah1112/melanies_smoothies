import streamlit as st
from snowflake.snowpark.context import get_active_session
import pandas as pd
import requests

# 🔹 Snowflake session
session = get_active_session()

# 🔹 Title
st.title("🍹 Smoothie Order App")

# 🔹 Name input
name_on_order = st.text_input("Enter your name")

# 🔹 DBல இருந்து fruits எடுக்க
fruit_df = session.table("smoothies.public.fruit_options").to_pandas()

st.subheader("Available Fruits")
st.dataframe(fruit_df)

# 🔹 UI list
fruit_name_list = fruit_df["FRUIT_NAME"].tolist()

# 🔹 Mapping (UI → API)
fruit_map = dict(zip(fruit_df["FRUIT_NAME"], fruit_df["SEARCH_ON"]))

# 🔹 Multiselect
ingredients_list = st.multiselect("Choose fruits", fruit_name_list)

# 🔹 Checkbox
order_filled = st.checkbox("Order Filled")

# 🔹 Button
submit_button = st.button("Submit Order")

# 🔹 Insert logic (ONLY HERE)
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

    else:
        st.warning("Enter name and select fruits")

# 🔹 Nutrition API
st.subheader("🍎 Nutrition Information")

for fruit_chosen in ingredients_list:

    search_value = fruit_map.get(fruit_chosen)

    st.write("Selected:", fruit_chosen)
    st.write("Search value:", search_value)

    if search_value:
        try:
            response = requests.get(
                f"https://my.smoothiefroot.com/api/fruit/{search_value}",
                timeout=5
            )

            if response.status_code == 200:
                data = response.json()
                st.dataframe([data])

        except:
            st.warning("⚠️ API not available in this environment")

    else:
        st.warning(f"{fruit_chosen} mapping error")
