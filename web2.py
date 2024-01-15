import streamlit as st
import pandas as pd
import pydeck as pdk

# Load country location data
country_loc_data = pd.read_csv("country_loc.csv", encoding='latin1')

# Simplified Pydeck map
st.pydeck_chart(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state=pdk.ViewState(
        latitude=0,
        longitude=0,
        zoom=1,
        pitch=0,
    ),
    layers=[
        pdk.Layer(
            'HexagonLayer',
            data=country_loc_data,
            get_position='[Longitude, Latitude]',
            radius=200,
            elevation_scale=4,
            elevation_range=[0, 1000],
            pickable=True,
            extruded=True,
        ),
    ],
), use_container_width=True)


    

# Streamlit app
st.title("TikTok Analytics Dashboard")

# Sample data
tiktok_data = pd.read_csv("cleaned_data_TikTok.csv")

# Advanced Sidebar
st.sidebar.markdown('**<font color="#ffc72c">User Input Features</font>**', unsafe_allow_html=True)

# Dropdown for selecting a country/region
unique_countries = tiktok_data['Region of Focus'].unique().tolist()
selected_country = st.sidebar.selectbox('Select Country/Region', unique_countries)

# Follower Count Threshold Slider
st.sidebar.subheader("Follower Count Threshold")
follower_threshold = st.sidebar.slider("Select Follower Count Threshold", min_value=0, max_value=100000, value=5000, step=100)

# Filter data based on user input
filtered_data = filter_data(tiktok_data, selected_country, follower_threshold)

# Check if the filtered_data DataFrame is not empty
if not filtered_data.empty:
    st.info("Hover over hexagons to explore more details.")
    generate_pydeck_map(filtered_data, f"User Distribution Map for {selected_country}")
else:
    st.warning(f"No data available for {selected_country} with the selected follower threshold.")
# Map visualization for all countries
st.subheader("Advanced Geographical Map - Followers Distribution for All Countries")

# Choose a base map style for Folium
map_style = st.sidebar.selectbox("Select Map Style", ["OpenStreetMap", "Stamen Terrain", "Stamen Toner", "Stamen Watercolor", "CartoDB Positron", "CartoDB Dark_Matter"])

# Create a Folium Map
folium_map_all_countries = folium.Map(location=[tiktok_data['Your_Latitude_Column'].mean(), tiktok_data['Your_Longitude_Column'].mean()], zoom_start=2, tiles=map_style)

# Add a Marker Cluster for better visualization of dense areas
marker_cluster_all_countries = folium.plugins.MarkerCluster().add_to(folium_map_all_countries)

# Customizing markers based on FollowerCount for all countries
for index, row in tiktok_data.iterrows():
    radius = row['FollowerCount'] / 1000  # Adjust the radius based on FollowerCount for better visualization
    color = 'green' if row['FollowerCount'] >= 5000 else 'blue'  # Custom color based on a threshold
    folium.CircleMarker([row['Your_Latitude_Column'], row['Your_Longitude_Column']], radius=radius, color=color, fill=True, fill_color=color, fill_opacity=0.6).add_to(marker_cluster_all_countries)

# Add a Fullscreen button for better user experience
folium.plugins.Fullscreen().add_to(folium_map_all_countries)

# Display the map for all countries with additional controls
folium_static(folium_map_all_countries)
