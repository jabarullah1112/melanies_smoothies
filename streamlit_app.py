import streamlit as st
import pandas as pd
import requests
from snowflake.snowpark import Session

# 🔹 1. Snowflake connection (முதலில் இதை மட்டும் setup பண்ணணும்)
connection_parameters = st.secrets["snowflake"]
session = Session.builder.configs(connection_parameters).create()

# 🔹 2. Title
st.title("🍹 Smoothie Order App")

# 🔹 3. Name input
name_on_order = st.text_input("Enter your name").strip()

# 🔹 4. Fruits table load (ஒரே தடவை மட்டும்)
fruit_df = session.table("smoothies.public.fruit_options").to_pandas()

# 🔹 5. Space clean (extra space remove)
fruit_df["FRUIT_NAME"] = fruit_df["FRUIT_NAME"].str.strip()

# 🔹 6. FRUIT_ID வைத்து sort (முக்கியம் 🔥)
fruit_df = fruit_df.sort_values("FRUIT_ID").reset_index(drop=True)

# 🔹 7. Table display
st.subheader("Available Fruits")
st.dataframe(fruit_df)

# 🔹 8. Dropdown list (same order follow ஆகும்)
fruit_name_list = fruit_df["FRUIT_NAME"].tolist()

# 🔹 9. Multiselect
ingredients_list = st.multiselect("Choose fruits", fruit_name_list)

# 🔹 10. Checkbox
order_filled = st.checkbox("Order Filled")

# 🔹 11. Submit button
if st.button("Submit Order"):

    if not name_on_order or not ingredients_list:
        st.warning("⚠️ Name & fruits select பண்ணுங்கள்")
    else:
        # 🔥 முக்கியம்: comma join (space இல்லாமல்)
        ingredients_string = ",".join(ingredients_list)

        filled_value = "TRUE" if order_filled else "FALSE"

        # 🔹 பாதுகாப்பு (quotes remove)
        safe_name = name_on_order.replace("'", "")

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

# 🔹 12. Debug section
st.subheader("🔍 Debug")

if ingredients_list:
    debug_string = ",".join(ingredients_list)

    st.write("Selected:", ingredients_list)
    st.write("Final string:", debug_string)
    st.write("Length:", len(debug_string))

# 🔹 13. Nutrition API
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
