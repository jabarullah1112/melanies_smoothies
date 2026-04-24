import streamlit as st
import pandas as pd
import requests

# 🔹 Try Snowflake session safely
try:
    from snowflake.snowpark.context import get_active_session
    session = get_active_session()
except:
    st.error("❌ Snowflake session கிடைக்கவில்லை (SiS அல்லாத environment)")
    st.stop()

# 🔹 Title
st.title("🍹 Smoothie Order App")

# 🔹 Name input
name_on_order = st.text_input("Enter your name")

# 🔹 Load fruits
fruit_df = session.table("smoothies.public.fruit_options").to_pandas()

st.subheader("Available Fruits")
st.dataframe(fruit_df)

# 🔹 Lists
fruit_name_list = fruit_df["FRUIT_NAME"].tolist()
fruit_map = dict(zip(fruit_df["FRUIT_NAME"], fruit_df["SEARCH_ON"]))

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

        query = f"""
        insert into smoothies.public.orders
        (name_on_order, ingredients, order_filled)
        values (
            '{name_on_order}',
            '{ingredients_string}',
            {filled_value}
        )
        """

        try:
            session.sql(query).collect()
            st.success("✅ Order placed successfully!")
        except Exception as e:
            st.error(f"❌ Insert error: {e}")

    else:
        st.warning("⚠️ Name & fruits select பண்ணுங்கள்")

# 🔹 Nutrition API
st.subheader("🍎 Nutrition Information")

for fruit_chosen in ingredients_list:

    search_value = fruit_map.get(fruit_chosen)

    st.write("Selected:", fruit_chosen)
    st.write("Search value:", search_value)

    if not search_value:
        st.warning(f"{fruit_chosen} mapping இல்ல ❌")
        continue

    try:
        response = requests.get(
            f"https://my.smoothiefroot.com/api/fruit/{search_value}",
            timeout=5
        )

        if response.status_code == 200:
            data = response.json()
            st.dataframe([data])
        else:
            st.warning("API response error")

    except:
        st.info("⚠️ இந்த environmentல API access முடியாது")
