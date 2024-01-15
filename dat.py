import streamlit as st
import pandas as pd
from io import BytesIO
import zipfile
import folium
from streamlit_folium import folium_static

# Function to create a map using Folium
def create_map(data, title):
    m = folium.Map(location=[0, 0], zoom_start=2)
    for index, row in data.iterrows():
        folium.Marker([row['Latitude'], row['Longitude']], popup=row['Username']).add_to(m)
    st.subheader(title)
    folium_static(m)

# Function to read data
def read_data(platform):
    return pd.read_csv(platform)

# Sample data
fb_data = read_data("cleaned_data_Facebook.csv")
insta_data = read_data("cleaned_data_Instragram.csv")
twitter_data = read_data("cleaned_data_Twitter.csv")
tiktok_data = read_data("cleaned_data_TikTok.csv")
yt_data = read_data("cleaned_data_YouTube.csv")
thrd_data = read_data("cleaned_data_Threads.csv")

zip_buffer = BytesIO()

# Create a ZipFile object
with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
    # Add each CSV file to the zip file
    zip_file.writestr('Facebook_data.csv', fb_data.to_csv(index=False))
    zip_file.writestr('Instagram_data.csv', insta_data.to_csv(index=False))
    zip_file.writestr('Twitter_data.csv', twitter_data.to_csv(index=False))
    zip_file.writestr('TikTok_data.csv', tiktok_data.to_csv(index=False))
    zip_file.writestr('YouTube_data.csv', yt_data.to_csv(index=False))
    zip_file.writestr('Threads_data.csv', thrd_data.to_csv(index=False))

# Download Zip Button for all data
st.download_button(label='Download All Data as CSV Files', data=zip_buffer.getvalue(), file_name='All_data.zip', mime='application/zip')

# Advanced Sidebar
st.sidebar.markdown('**<font color="#ffc72c">User Input Features</font>**', unsafe_allow_html=True)
st.sidebar.markdown("*Select the social media platform you want to analyze:*")

# Multiselect for social media
input_media = st.sidebar.multiselect('Social Media', ["Facebook", "Instagram", "Threads", "Tiktok", "Twitter", "Youtube"])

# Load country location data
country_loc_data = pd.read_csv("country_loc.csv", encoding='latin1')

# Display map for selected social media platforms
for media in input_media:
    if media == "Facebook":
        create_map(fb_data, "Facebook User Locations")
    elif media == "Instagram":
        create_map(insta_data, "Instagram User Locations")
    elif media == "Threads":
        create_map(thrd_data, "Threads User Locations")
    elif media == "Tiktok":
        create_map(tiktok_data, "TikTok User Locations")
    elif media == "Twitter":
        create_map(twitter_data, "Twitter User Locations")
    elif media == "Youtube":
        create_map(yt_data, "YouTube User Locations")
