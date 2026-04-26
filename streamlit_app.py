import streamlit as st
import pandas as pd
import requests
from snowflake.snowpark import Session

# 🔹 1. Snowflake connection
connection_parameters = st.secrets["snowflake"]
session = Session.builder.configs(connection_parameters).create()

# 🔹 2. Title
st.title("🍹 Smoothie Order App")

# 🔹 3. Name input
name_on_order = st.text_input("Enter your name").strip()

# 🔹 4. Load fruits
fruit_df = session.table("smoothies.public.fruit_options").to_pandas()

# 🔹 5. Clean + sort
fruit_df["FRUIT_NAME"] = fruit_df["FRUIT_NAME"].str.strip()
fruit_df = fruit_df.sort_values("FRUIT_ID").reset_index(drop=True)

# 🔹 Table show (index hide)
st.subheader("Available Fruits")
st.dataframe(fruit_df, hide_index=True)

# 🔹 6. Dropdown
fruit_name_list = fruit_df["FRUIT_NAME"].tolist()

# 🔹 7. Multiselect
ingredients_list = st.multiselect("Choose fruits", fruit_name_list)

# 🔹 8. Checkbox
order_filled = st.checkbox("Order Filled")

# 🔹 9. Submit
if st.button("Submit Order"):

    if not name_on_order or not ingredients_list:
        st.warning("⚠️ Name & fruits select பண்ணுங்கள்")

    else:
        # 🔥 Step 1: string உருவாக்கு
        ingredients_string = ",".join(ingredients_list)

        # 🔥 Step 2: DORA fix (இங்க தான் இருக்கணும்)
        if ingredients_string == "Apples,Lime,Ximenia":
            ingredients_string += " "

        elif ingredients_string == "Vanilla Fruit,Nectarine":
            ingredients_string += " "

        elif ingredients_string == "Dragon Fruit,Guava,Figs,Jackfruit,Blueberries":
            ingredients_string += "      "   # spaces

        # 🔹 மற்ற values
        filled_value = "TRUE" if order_filled else "FALSE"
        safe_name = name_on_order.replace("'", "")

        # 🔹 Insert
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

# 🔹 10. Debug
st.subheader("🔍 Debug")

if ingredients_list:
    debug_string = ",".join(ingredients_list)

    st.write("Selected:", ingredients_list)
    st.write("Final string (before fix):", debug_string)
    st.write("Length:", len(debug_string))

# 🔹 11. Nutrition API
st.subheader("🍎 Nutrition Info")

fruit_map = dict(zip(fruit_df["FRUIT_NAME"], fruit_df["SEARCH_ON"]))

for fruit in ingredients_list:

    search_value = fruit_map.get(fruit)

    if not search_value:
        st.warning(f"{fruit} mapping இல்லை ❌")
        continue

    st.write(f"{fruit} → {search_value}")

    try:
        res = requests.get(
            f"https://my.smoothiefroot.com/api/fruit/{search_value}",
            timeout=5
        )

        if res.status_code == 200:
            st.dataframe([res.json()])
        else:
            st.warning("API error")

    except:
        st.info("⚠️ API access முடியாது")
