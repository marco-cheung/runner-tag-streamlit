# Import libraries
import streamlit as st
import pandas as pd

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

# Show the filtered results
# Show the cards
N_cards_per_row = 3

# Specify the number of images per page and columns
images_per_page = 9  # Change this value to the desired number of images per page

# Calculate the number of pages and remaining images
num_images = len(df_search) if text_search else len(df)
num_pages = (num_images - 1) // images_per_page + 1
remaining_images = num_images % images_per_page

if text_search:
    for n_row, row in df_search.iterrows():
        i = n_row % N_cards_per_row
        if i == 0:
            st.write("---")
            cols = st.columns(N_cards_per_row, gap="large")
        # draw the card
        with cols[i]:
            st.caption(f"{row['event'].strip()} - {row['event_time'].strip()}")
            st.image(row['image_path'], width=180)

else:
    # Iterate over pages
    for page in range(num_pages):
        # Calculate the start and end indices of the current page
        start_index = page * images_per_page
        end_index = start_index + images_per_page

        # Create a sublist of images for the current page
        if text_search:
            page_images = df_search[start_index:end_index]
        else:
            page_images = df[start_index:end_index]

        # Show the cards
        if page > 0:
            st.write("---")
        cols = st.columns(N_cards_per_row, gap="large")

        # Iterate over images in the current page
        for i, (_, row) in enumerate(page_images.iterrows()):
            with cols[i % N_cards_per_row]:
                st.caption(f"{row['event'].strip()} - {row['event_time'].strip()}")
                st.image(row['image_path'], width=180)