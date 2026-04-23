import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

session = get_active_session()

# 👇 Name input
name_on_order = st.text_input("Enter your name")

# multiselect (already இருக்கும்)
ingredients_list = st.multiselect("Choose fruits", ["Apple","Mango","Banana"])

# list → string
ingredients_string = ""

if ingredients_list:
    for fruit in ingredients_list:
        ingredients_string += fruit

# insert query
# insert query
my_insert_stmt = """ 
insert into smoothies.public.orders(name_on_order, ingredients)
values ('""" + name_on_order + """','""" + ingredients_string + """')
"""
# button
submit_button = st.button("Submit Order", key="submit_btn")


if submit_button:
    if ingredients_string:
        session.sql(my_insert_stmt).collect()
        st.success("Order placed!", icon="✅")

st.success(name_on_order + " order placed!", icon="✅")
st.write(my_insert_stmt)

# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title(f"Customize Your Smoothie  {st.__version__}")
st.write(
  """Replace this example with your own code!
  **And if you're new to Streamlit,** check
  out our easy-to-follow guides at
  [docs.streamlit.io](https://docs.streamlit.io).
  """
)
from snowflake.snowpark.context import get_active_session
import streamlit as st

session = get_active_session()

# முக்கியம்: dataframe define பண்ணணும்
my_dataframe = session.table("smoothies.public.fruit_options")

df = my_dataframe.to_pandas()

# index 1 இருந்து start ஆக
df.index = df.index + 1

st.dataframe(df)

from snowflake.snowpark.context import get_active_session

import streamlit as st
from snowflake.snowpark.context import get_active_session

session = get_active_session()

# example list (உங்க codeல already இருக்கும்)
fruit_list = ["Apple", "Mango", "Banana"]

# multiselect
ingredients_list = st.multiselect(
    "Choose ingredients:",
    fruit_list,
    key="fruit_select"
)

# convert list to string
ingredients_string = ""

if ingredients_list:
    for fruit in ingredients_list:
        ingredients_string += fruit

if submit_button:
    if ingredients_string:
        session.sql(my_insert_stmt).collect()
        st.success("Order placed!", icon="✅")


import streamlit as st
import pandas as pd   # ✅ இது MUST

# test dataframe
df = pd.DataFrame({
    "Fruit": ["Apple", "Mango"],
    "Price": [10, 20]
})

st.dataframe(df)


st.write(my_insert_stmt)

st.success(name_on_order + " order placed!", icon="✅")
