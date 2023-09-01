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
st.text('''
        AF Afghanistan, AL Albania, DZ Algeria, AD Andorra, AO Angola, AR Argentina,
        AU Australia, AT Austria, AZ Azerbaijan, BS Bahamas, BH Bahrain, BD Bangladesh,
        BB Barbados, BY Belarus, BE Belgium, BZ Belize, BJ Benin, BT Bhutan, BO Bolivia,
        BA Bosnia and Herzegovina, BW Botswana, BR Brazil, BN Brunei, BG Bulgaria,
        BF Burkina Faso, BI Burundi, KH Cambodia, CM Cameroon, CA Canada, CF Central 
        African Republic, TD Chad, CL Chile, CN China, CO Colombia, KM Comoros, CD Congo,
        Democratic Republic of the, CG Congo, CR Costa Rica, HR Croatia, CU Cuba, CY Cyprus,
        CZ Czech Republic, DK Denmark, DJ Djibouti, DM Dominica, DO Dominican Republic,
        EC Ecuador, EG Egypt, SV El Salvador, GQ Equatorial Guinea, ER Eritrea, EE Estonia,
        SZ Eswatini, ET Ethiopia, FJ Fiji, FI Finland, FR France, GA Gabon, GM Gambia,GE 
        Georgia, DE Germany, GH Ghana, GR Greece, GD Grenada, GT Guatemala, GN Guinea,GW
        Guinea-Bissau, GY Guyana, HT Haiti, HN Honduras, HU Hungary, IS Iceland, IN India,
        ID Indonesia, IR Iran, IQ Iraq, IE Ireland, IL Israel, IT Italy, CI Ivory Coast,
        JM Jamaica, JP Japan, JO Jordan, KZ Kazakhstan, KE Kenya, KI Kiribati, XK Kosovo,
        KW Kuwait, KG Kyrgyzstan, LA Laos, LV Latvia, LB Lebanon, LS Lesotho, LR Liberia,
        LY Libya, LI Liechtenstein, LT Lithuania, LU Luxembourg, MG Madagascar, MW Malawi,
        MY Malaysia, MV Maldives, ML Mali, MT Malta, MH Marshall Islands, MR Mauritania,
        MU Mauritius, MX Mexico, FM Micronesia, MD Moldova, MC Monaco, MN Mongolia, ME 
        Montenegro, MA Morocco, MZ Mozambique, MM Myanmar (Burma), NA Namibia, NR Nauru,
        NP Nepal, NL Netherlands, NZ New Zealand, NI Nicaragua, NE Niger, NG Nigeria, KP
        North Korea, MK North Macedonia, NO Norway, OM Oman, PK Pakistan, PW Palau, PS 
        Palestine, PA Panama, PG Papua New Guinea, PY Paraguay, PE Peru, PH Philippines,
        PL Poland, PT Portugal, QA Qatar, RO Romania, RU Russia, RW Rwanda, KN Saint 
        Kitts and Nevis, LC Saint Lucia, VC Saint Vincent and the Grenadines, WS 
        Samoa, SM San Marino, ST Sao Tome and Principe, SA Saudi Arabia, SN Senegal, 
        RS Serbia, SC Seychelles, SL Sierra Leone, SG Singapore, SK Slovakia, SI 
        Slovenia, SB Solomon Islands, SO Somalia, ZA South Africa, KR South Korea, SS 
        South Sudan, ES Spain, LK Sri Lanka, SD Sudan, SR Suriname, SE Sweden, CH 
        Switzerland, SY Syria, TW Taiwan, TJ Tajikistan, TZ Tanzania, TH Thailand, TL 
        Timor-Leste, TG Togo, TO Tonga, TT Trinidad and Tobago, TN Tunisia, TR Turkey, 
        TM Turkmenistan, TV Tuvalu, UG Uganda, UA Ukraine, AE United Arab Emirates, GB
        United Kingdom, US United States, UY Uruguay, UZ Uzbekistan, VU Vanuatu, VA 
        Vatican City, VE Venezuela, VN Vietnam, EH Western Sahara, YE Yemen, ZM Zambia,
         ZW Zimbabwe')
''')
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
