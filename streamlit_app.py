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
text_search = st.text_input("Input Bib Number", placeholder = 'e.g. 7757')

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

# Calculate the number of pages
num_pages = len(df) // images_per_page
if len(df) % images_per_page:
    num_pages += 1

# Create a selection box for the page number
page = st.selectbox('Select page', options=range(1, num_pages + 1))

# Calculate start and end indices for image paths
start = (page - 1) * images_per_page
end = start + images_per_page

# Show the filtered results
if text_search:
    for n_row, row in df_search.reset_index().iterrows():
        i = n_row%N_cards_per_row
        if i==0:
            st.write("---")
            cols = st.columns(N_cards_per_row, gap="large")
        # draw the card
        with cols[n_row%N_cards_per_row]:
            st.caption(f"{row['event'].strip()} - {row['event_time'].strip()} ")
            st.image(row['image_path'])

else:
    # Display images for the selected page
    for _, row in df.iloc[start:end].iterrows():
        image_url = row['image_path']
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))
        st.image(image)