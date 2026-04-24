import streamlit as st
import pandas as pd
import requests

# 🔹 Snowflake session
from snowflake.snowpark.context import get_active_session
session = get_active_session()

# 🔹 Title
st.title("🍹 Smoothie Order App")

# 🔹 Name input
name_on_order = st.text_input("Enter your name")

# 🔹 Load fruits
fruit_df = session.table("smoothies.public.fruit_options").to_pandas()

st.subheader("Available Fruits")
st.dataframe(fruit_df)

# 🔹 Fruit list (UI)
fruit_name_list = fruit_df["FRUIT_NAME"].tolist()

# 🔹 Multiselect
ingredients_list = st.multiselect("Choose fruits", fruit_name_list)

# 🔹 Filled checkbox
order_filled = st.checkbox("Order Filled")

# 🔹 Submit button
submit_button = st.button("Submit Order")

# 🔹 Insert logic (IMPORTANT FIX)
if submit_button:
    if name_on_order and ingredients_list:

        # 🔥 IMPORTANT: NO SPACE JOIN
        ingredients_string = ",".join(ingredients_list)

        # 🔹 TRUE / FALSE
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

        st.success("✅ Order placed successfully!")

    else:
        st.warning("⚠️ Enter name and select fruits")

# 🔹 Debug (VERY IMPORTANT)
st.subheader("🔍 Debug Output")

if ingredients_list:
    st.write("Selected list:", ingredients_list)
    st.write("Final string:", ",".join(ingredients_list))
    st.write("Length:", len(",".join(ingredients_list)))

# 🔹 Nutrition API
st.subheader("🍎 Nutrition Information")

fruit_map = dict(zip(fruit_df["FRUIT_NAME"], fruit_df["SEARCH_ON"]))

for fruit_chosen in ingredients_list:

    search_value = fruit_map.get(fruit_chosen)

    if search_value:
        st.write(f"{fruit_chosen} → {search_value}")

        try:
            response = requests.get(
                f"https://my.smoothiefroot.com/api/fruit/{search_value}",
                timeout=5
            )

            if response.status_code == 200:
                st.dataframe([response.json()])
            else:
                st.warning("API response error")

        except:
            st.info("API blocked in this environment")
