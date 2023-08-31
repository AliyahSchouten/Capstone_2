import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image
import requests

st.set_page_config(page_title='Holidays')
st.header('Holidays in Different Countries')

# Load an image from a file
#image = Image.open("C:/Users/ALIYA/OneDrive/Documents/Coding_Temple/Week 8/Capstone_2/Two-Letter-Country-Codes.png")

# Streamlit UI
st.title("Example of Country Codes")
st.text("Code Name||\nAR  Argentina\nAT Austria")

#st.image(image, caption="", use_column_width=True)

### --- Load Dataframe
input_country_name = st.text_input("Enter a country Code:")

year = 2023
country_code = input_country_name
api_url = f"https://date.nager.at/api/v3/publicholidays/{year}/{country_code}"
response = requests.get(api_url)

if response.status_code == 200:
    holidays_data = response.json()
else:
    st.error("Enter a country code and hit enter")

def is_holiday(date):
    for holiday in holidays_data:
        if holiday['date'] == date:
            return holiday['name']
    return None

# Streamlit UI
st.title("Holiday Checker")

input_date = st.date_input("Select a date:")
if st.button("Check"):
    holiday_name = is_holiday(str(input_date))
    if holiday_name:
        st.write(f"{input_date} is a holiday: {holiday_name}")
    else:
        st.write(f"{input_date} is not a holiday.")
if input_country_name!='':

    # Process holidays data
    holidays_df = pd.DataFrame(holidays_data)

    # Group by date and count the number of holidays
    holidays_per_date = holidays_df.groupby('date').size().reset_index(name='count')

    # Sort the data by the count of holidays in descending order
    holidays_per_date = holidays_per_date.sort_values(by='count', ascending=False)

    # Create a bar chart using Plotly Express
    fig = px.bar(holidays_per_date, x='date', y='count', title=f"Holidays per Date in {input_country_name}")
    fig.update_traces(marker=dict(color='red'))
    st.plotly_chart(fig)
