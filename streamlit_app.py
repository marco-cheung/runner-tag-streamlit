# Import libraries
import streamlit as st
import pandas as pd

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

# Show the filtered results
# Show the cards
N_cards_per_row = 3
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
    #show image gallery from image url in dataframe columns
    for n_row, row in df.reset_index().iterrows():
        i = n_row%N_cards_per_row
        if i==0:
            st.write("---")
            cols = st.columns(N_cards_per_row, gap="large")
        with cols[n_row%N_cards_per_row]:
            st.caption(f"{row['event'].strip()} - {row['event_time'].strip()} ")
            st.image(row['image_path'], width=180)
