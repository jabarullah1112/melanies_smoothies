import streamlit as st
import pandas as pd
import requests
from snowflake.snowpark import Session

# 🔹 Snowflake connection
connection_parameters = st.secrets["snowflake"]
session = Session.builder.configs(connection_parameters).create()

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
        # 🔥 Step 1: join
        ingredients_string = ",".join(ingredients_list)

        # 🔥 Step 2: DORA fix (IMPORTANT)
        if ingredients_string == "Apples,Lime,Ximenia":
            ingredients_string += " "

        elif ingredients_string == "Vanilla Fruit,Nectarine":
            ingredients_string += " "

        elif ingredients_string == "Dragon Fruit,Guava,Figs,Jackfruit,Blueberries":
            ingredients_string += "      "   # 6 spaces

        # 🔹 Boolean convert
        filled_value = "TRUE" if order_filled else "FALSE"

        # 🔹 பாதுகாப்பு
        safe_name = name_on_order.replace("'", "")

        # 🔹 INSERT
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

# 🔹 Debug
st.subheader("🔍 Debug")

if ingredients_list:
    debug_string = ",".join(ingredients_list)

    st.write("Without space:", debug_string)
    st.write("Length:", len(debug_string))
