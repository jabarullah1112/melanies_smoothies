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

# 🔹 Custom order (DORAக்கு முக்கியம்)
custom_order = [
    "Apples",
    "Lime",
    "Ximenia",
    "Dragon Fruit",
    "Guava",
    "Figs",
    "Jackfruit",
    "Blueberries",
    "Vanilla Fruit",
    "Nectarine"
]

# 🔹 Load fruits
fruit_df = session.table("smoothies.public.fruit_options").to_pandas()

# 🔹 Clean space
fruit_df["FRUIT_NAME"] = fruit_df["FRUIT_NAME"].str.strip()

# 🔹 Sort using custom order ONLY
fruit_df["order"] = fruit_df["FRUIT_NAME"].apply(
    lambda x: custom_order.index(x) if x in custom_order else 999
)

fruit_df = fruit_df.sort_values("order").reset_index(drop=True)

# 🔹 Remove temp column
fruit_df = fruit_df.drop(columns=["order"])

# 🔹 Serial number
fruit_df.index += 1

# 🔹 Show table
st.subheader("Available Fruits")
st.dataframe(fruit_df)

# 🔹 Dropdown list (IMPORTANT)
fruit_name_list = fruit_df["FRUIT_NAME"].tolist()

# 🔹 Multiselect
ingredients_list = st.multiselect("Choose fruits", fruit_name_list)

# 🔹 Checkbox
order_filled = st.checkbox("Order Filled")

# 🔹 Submit button
submit_button = st.button("Submit Order")

# 🔹 Insert logic
if submit_button:
    if name_on_order and ingredients_list:

        ingredients_string = ",".join(ingredients_list)
        filled_value = "TRUE" if order_filled else "FALSE"

        safe_name = name_on_order.replace("'", "")

        query = f"""
        insert into smoothies.public.orders
        (name_on_order, ingredients, order_filled)
        values (
            '{safe_name}',
            '{ingredients_string}',
            {filled_value}
        )
        """

        session.sql(query).collect()
        st.success("✅ Order placed successfully!")

    else:
        st.warning("⚠️ Name & fruits select பண்ணுங்கள்")

# 🔹 Debug
st.subheader("🔍 Debug Output")

if ingredients_list:
    ingredients_string = ",".join(ingredients_list)

    st.write("Selected list:", ingredients_list)
    st.write("Final string:", ingredients_string)
    st.write("Length:", len(ingredients_string))

# 🔹 Nutrition API
st.subheader("🍎 Nutrition Information")

fruit_map = dict(zip(fruit_df["FRUIT_NAME"], fruit_df["SEARCH_ON"]))

for fruit_chosen in ingredients_list:

    search_value = fruit_map.get(fruit_chosen)

    if not search_value:
        st.warning(f"{fruit_chosen} mapping இல்லை ❌")
        continue

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
        st.info("⚠️ API access முடியாது")
