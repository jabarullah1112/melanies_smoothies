import streamlit as st
from snowflake.snowpark import Session
import pandas as pd

# 🔹 Create session using secrets (IMPORTANT)
@st.cache_resource
def create_session():
    return Session.builder.configs(st.secrets["snowflake"]).create()

session = create_session()

# 🔹 Title
st.title("🍹 Smoothie Order App")

# 🔹 Name input
name_on_order = st.text_input("Enter your name").strip()

# 🔹 Load fruits
fruit_df = session.table("smoothies.public.fruit_options").to_pandas()

# 🔹 Clean + sort
fruit_df["FRUIT_NAME"] = fruit_df["FRUIT_NAME"].str.strip()
fruit_df = fruit_df.sort_values("FRUIT_ID").reset_index(drop=True)

st.subheader("Available Fruits")
st.dataframe(fruit_df, hide_index=True)

# 🔹 Dropdown
fruit_name_list = fruit_df["FRUIT_NAME"].tolist()

# 🔹 Multiselect
ingredients_list = st.multiselect("Choose fruits", fruit_name_list)

# 🔹 Checkbox
order_filled = st.checkbox("Order Filled")

# 🔹 Submit
if st.button("Submit Order"):

    if not name_on_order or not ingredients_list:
        st.warning("⚠️ Name & fruits select பண்ணுங்கள்")

    else:
        ingredients_string = ",".join(ingredients_list)

      

        session.sql(query).collect()
        st.success("✅ Order placed successfully!")
