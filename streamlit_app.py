# Import libraries
import streamlit as st
import pandas as pd
from PIL import Image
import requests
from io import BytesIO

# Page setup
st.set_page_config(page_title="Running Photos - Bib Number Search Engine", page_icon="🏃", layout="wide")
st.title("Bib Number Search Engine")

# Use a text_input to get the keywords to filter the dataframe
text_search = st.text_input("Input Bib Number", placeholder='e.g. 7757')

# Connect to the Google Sheet
sheet_id = "1AvZtnDy43gr6ttpokX-w5F5s-4KpapjFgQaR6tKkxgk"
sheet_name = "hzmbhm2023"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&sheet={sheet_name}"
df = pd.read_csv(url, dtype=str)

# Filter the dataframe using masks
mask = df["bib_num"].str.contains(text_search)
df_search = df[mask]

# Show the cards
N_cards_per_row = 3

# Number of images per page
images_per_page = 15

# Calculate the total number of pages
total_pages = len(df) // images_per_page
if len(df) % images_per_page:
    total_pages += 1

# Add a selection box for page navigation
page = st.selectbox('Select a page', options=list(range(1, total_pages + 1)))

# Filter dataframe for the selected page
start_index = (page - 1) * images_per_page
end_index = start_index + images_per_page
subset_df = df.iloc[start_index: end_index]

# Show the filtered results
if text_search:
    container = st.beta_container()
    for n_row, row in df_search.reset_index().iterrows():
        i = n_row % N_cards_per_row
        if i == 0:
            container.write("---")
            cols = container.beta_columns(N_cards_per_row, gap="large")
        # draw the card
        with cols[n_row % N_cards_per_row]:
            st.caption(f"{row['event'].strip()} - {row['event_time'].strip()} ")
            st.image(row['image_path'])

else:
    container = st.beta_container()
    # Display the images from the subset dataframe
    for n_row, row in subset_df.reset_index().iterrows():
        i = n_row % N_cards_per_row
        if i == 0:
            container.write("---")
            cols = container.beta_columns(N_cards_per_row, gap="large")
        with cols[n_row % N_cards_per_row]:
            response = requests.get(row['image_path'])
            img = Image.open(BytesIO(response.content))
            st.caption(f"{row['event'].strip()} - {row['event_time'].strip()} ")
            st.image(img, width=180)