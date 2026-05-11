import streamlit as st
from snowflake.snowpark import Session

connection_parameters = {
    "account": st.secrets["account"],
    "user": st.secrets["user"],
    "password": st.secrets["password"],
    "role": st.secrets["role"],
    "warehouse": st.secrets["warehouse"],
    "database": st.secrets["database"],
    "schema": st.secrets["schema"]
}

session = Session.builder.configs(
    connection_parameters
).create()

# Title
st.title("🍹 Smoothie Order App")

# Name input
name_on_order = st.text_input("Enter your name")

# Load fruits
fruit_df = session.table(
    "smoothies.public.fruit_options"
).to_pandas()

# Display fruits
st.subheader("Available Fruits")
st.dataframe(fruit_df)

# Fruit list
fruit_name_list = fruit_df["FRUIT_NAME"].tolist()

# Multiselect
ingredients_list = st.multiselect(
    "Choose fruits",
    fruit_name_list
)

# Checkbox
order_filled = st.checkbox("Order Filled")

# Submit
if st.button("Submit Order"):

    if not name_on_order or not ingredients_list:
        st.warning("⚠️ Enter name and select fruits")

    else:

        ingredients_string = ",".join(ingredients_list)

        safe_name = name_on_order.replace("'", "")

        filled_value = (
            "TRUE" if order_filled else "FALSE"
        )

        query = f"""
        INSERT INTO smoothies.public.orders
        (name_on_order, ingredients, order_filled, order_ts)

        VALUES (
            '{safe_name}',
            '{ingredients_string}',
            {filled_value},
            CURRENT_TIMESTAMP()
        )
        """

        session.sql(query).collect()

        st.success("✅ Order placed successfully!")
