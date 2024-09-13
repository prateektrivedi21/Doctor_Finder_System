import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse
import base64

def get_base64_image(image_file):
    with open(image_file, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def set_bg_and_css(image_file):
    base64_image = get_base64_image(image_file)
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{base64_image}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        h1 {{
            color: navy !important;
        }}
        label {{
            color: navy !important;
        }}
        .stSelectbox > div > div {{
            background-color: transparent;
            color: #000080;
            border: 2px solid #e50914;
            border-radius: 5px;
        }}
        input[type="text"]{{
            background-color: white;
            color: #000080;
            border: 2px solid #e50914;
            border-radius: 5px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def doct_prof_cnt(location, specialization):
    encoded_location = urllib.parse.quote(location)
    encoded_specialization = urllib.parse.quote(specialization)

    profiles_count = 0
    page = 1

    while True:
        url = f"https://www.practo.com/search/doctors?results_type=doctor&q=%5B%7B%22word%22%3A%22{encoded_specialization}%22%2C%22autocompleted%22%3Atrue%2C%22category%22%3A%22subspeciality%22%7D%2C%7B%22word%22%3A%22{encoded_location}%22%2C%22autocompleted%22%3Atrue%2C%22category%22%3A%22locality%22%7D%5D&city={encoded_location}&page={page}"
        request = requests.get(url)

        if request.status_code == 200:
            soup = BeautifulSoup(request.text, 'html.parser')
            profiles = soup.find_all('div', class_='u-border-general--bottom')
            if not profiles:
                break

            profiles_count += len(profiles)
            page += 1
        else:
            st.error("Failed to retrieve data from website")
            return None
    return profiles_count

set_bg_and_css("doc.jpg")

st.title("Find Doctor")
location = st.text_input("Enter your Location (Must be some city/towns situated in INDIA)")
specializations = ["Dentist", "Gynecologist/obstetrician", "General Physician", "Dermatologist", "Pediatrician", "Cardiologist",
                   "Cardiac Surgeon", "Urologist", "Ear-nose-throat (ent) Specialist"]
specialization = st.selectbox("Select the Specialization: ", specializations)

if st.button("Search"):
    if location and specialization:
        with st.spinner("Searching doctor...."):
            profiles_count = doct_prof_cnt(location.lower(), specialization.lower())
            if profiles_count is not None:
                st.success(f"Found {profiles_count} doctor profiles in {location} for {specialization}.")
            else:
                st.error("Failed to retrieve data. Please try again")
    else:
        st.warning("Please enter a location and select a specialization")
