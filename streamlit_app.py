import streamlit as st
from snowflake.snowpark import Session
import pandas as pd

# 🔹 Snowflake connection
connection_parameters = st.secrets["snowflake"]
session = Session.builder.configs(connection_parameters).create()

# 🔹 Title
st.title("🍹 Smoothie Order App")

# 🔹 Name input
name_on_order = st.text_input("Enter your name")

# 🔹 Fruit list (DBல இருந்து fetch)
fruit_df = session.table("smoothies.public.fruit_options").to_pandas()

# index start from 1
fruit_df.index = fruit_df.index + 1

st.subheader("Available Fruits")
st.dataframe(fruit_df)

# 🔹 Multiselect
fruit_list = fruit_df.iloc[:, 0].tolist()   # first column values
ingredients_list = st.multiselect("Choose fruits", fruit_list)

# 🔹 Convert list → string
ingredients_string = ",".join(ingredients_list)

# 🔹 Button
submit_button = st.button("Submit Order")

# 🔹 Insert logic
if submit_button:
    if name_on_order and ingredients_string:
        query = f"""
        insert into smoothies.public.orders(name_on_order, ingredients)
        values ('{name_on_order}','{ingredients_string}')
        """
        session.sql(query).collect()

        st.success(f"{name_on_order} order placed successfully! ✅")
    else:
        st.warning("Please enter name and select fruits")

# 🔹 Debug (optional)
st.write("Query Preview:")
st.code(f"""
insert into smoothies.public.orders(name_on_order, ingredients)
values ('{name_on_order}','{ingredients_string}')
""")

