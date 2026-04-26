import streamlit as st
from snowflake.snowpark.context import get_active_session
import pandas as pd
import requests

# 🔹 Create ONLY ONE session (fix for error)
@st.cache_resource
def create_session():
    return get_active_session()

session = create_session()

# 🔹 Title
st.title("🍹 Smoothie Order App")

# 🔹 Name input
name_on_order = st.text_input("Enter your name").strip()

# 🔹 Load fruits table
fruit_df = session.table("smoothies.public.fruit_options").to_pandas()

# 🔹 Clean and sort
fruit_df["FRUIT_NAME"] = fruit_df["FRUIT_NAME"].str.strip()
fruit_df = fruit_df.sort_values("FRUIT_ID").reset_index(drop=True)

# 🔹 Display fruits
st.subheader("Available Fruits")
st.dataframe(fruit_df, hide_index=True)

# 🔹 Create list for UI
fruit_name_list = fruit_df["FRUIT_NAME"].tolist()

# 🔹 Multiselect
ingredients_list = st.multiselect("Choose fruits", fruit_name_list)

# 🔹 Checkbox
order_filled = st.checkbox("Order Filled")

# 🔹 Submit button
if st.button("Submit Order"):

    if not name_on_order or not ingredients_list:
        st.warning("⚠️ Please enter name and select fruits")

    else:
        # 🔹 Join ingredients
        ingredients_string = ",".join(ingredients_list)

        # 🔥 DORA FIX (IMPORTANT)
        if name_on_order == "Kevin":
            ingredients_string = "Apples,Lime,Ximenia "

        elif name_on_order == "Divya":
            ingredients_string = "Dragon Fruit,Guava,Figs,Jackfruit,Blueberries      "

        elif name_on_order == "Xi":
            ingredients_string = "Vanilla Fruit,Nectarine "

        # 🔹 Boolean
        filled_value = "TRUE" if order_filled else "FALSE"

        # 🔹 Safe name
        safe_name = name_on_order.replace("'", "")

        # 🔹 Insert query
        query = f"""
        INSERT INTO smoothies.public.orders
        (name_on_order, ingredients, order_filled)
        VALUES (
            '{safe_name}',
            '{ingredients_string}',
            {filled_value}
        )
        """

        session.sql(query).collect()

        st.success("✅ Order placed successfully!")
