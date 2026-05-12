import streamlit as st
from snowflake.snowpark import Session

# Snowflake connection
connection_parameters = {
    "account": st.secrets["account"],
    "user": st.secrets["user"],
    "password": st.secrets["password"],
    "role": st.secrets["role"],
    "warehouse": st.secrets["warehouse"],
    "database": st.secrets["database"],
    "schema": st.secrets["schema"]
}

# Create Snowflake session
session = Session.builder.configs(
    connection_parameters
).create()

# App title
st.title("🍹 Smoothie Order App")
# Customer name input
name_on_order = st.text_input(
    "Enter your name"
)

# Load fruit table from Snowflake
fruit_df = session.table(
    "smoothies.public.fruit_options"
).to_pandas()

# Show available fruits
st.subheader("Available Fruits")
st.dataframe(fruit_df)

# Convert FRUIT_NAME column to list
fruit_name_list = (
    fruit_df["FRUIT_NAME"]
    .dropna()
    .tolist()
)

# Fruit selection
ingredients_list = st.multiselect(
    "Choose fruits",
    fruit_name_list
)

# Order status checkbox
order_filled = st.checkbox(
    "Order Filled"
)

# Submit button
submit_button = st.button(
    "Submit Order"
)

# Run when button clicked
if submit_button:

    # Validation
    if (
        not name_on_order
        or not ingredients_list
    ):

        st.warning(
            "⚠️ Enter name and select fruits"
        )

    else:

        # IMPORTANT
        # No spaces after comma
        ingredients_string = ",".join(
            ingredients_list
        )

        # Remove quotes/spaces
        safe_name = (
            name_on_order
            .replace("'", "")
            .strip()
        )

        # Boolean value
        filled_value = (
            "TRUE"
            if order_filled
            else "FALSE"
        )

        # Insert query
        query = f"""
        INSERT INTO smoothies.public.orders
        (
            name_on_order,
            ingredients,
            order_filled,
            order_ts
        )

        VALUES
        (
            '{safe_name}',
            '{ingredients_string}',
            {filled_value},
            CURRENT_TIMESTAMP()
        )
        """

        # Execute query
        session.sql(query).collect()

        # Success message
        st.success(
            "✅ Order placed successfully!"
        )

# Debug section
st.subheader("🔍 Debug")

if ingredients_list:

    st.write(
        "Ingredients:",
        ",".join(ingredients_list)
    )

    st.write(
        "Length:",
        len(",".join(ingredients_list))
    )
