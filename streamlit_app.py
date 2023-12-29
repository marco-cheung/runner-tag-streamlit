# Import libraries
import streamlit as st
import pandas as pd
from PIL import Image
import requests
from io import BytesIO

# Page setup
st.set_page_config(page_title="Running Photos - Bib Number Search 號碼布搵相", page_icon="🏃", layout="wide")

# Create three columns with different widths on the same row
col_a, col_b, col_c = st.columns([.2,2,2])

col_a.image("https://raw.githubusercontent.com/marco-cheung/runner-tag-streamlit/main/.streamlit/running-bib-icon.png", width=60)

# Hide the full screen option for every image displayed
hide_img_fs = '''
<style>
button[title="View fullscreen"]{
    visibility: hidden;}
</style>
'''
st.markdown(hide_img_fs, unsafe_allow_html=True)

with col_b:
  st.markdown("<h1 style='text-align: left; color: black; font-size: 35px;'>Bib Number Search 號碼布搵相</h1>", unsafe_allow_html=True)


#st.title("Bib Number Search 號碼布搵相")


with st.form('input_form'):
    # Create two columns; adjust the ratio to your liking
    col1, col2 = st.columns([3,1]) 

    # Use the first column for text input
    with col1:
        # Use a text_input to get the keywords to filter the dataframe
        text_search = st.text_input("Input Bib Number 請輸入號碼布編號", placeholder='例子 Example: 7757', label_visibility='collapsed')
    
    # Use the second column for the submit button
    with col2:
        submitted = st.form_submit_button('Search 搜尋🔎')


# Set the font size of the textbox using markdown
st.markdown(
    f'<style>input[type="text"] {{ font-size: 18px; }}</style>',
    unsafe_allow_html=True
)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 1

# Connect to the Google Sheet
sheet_id = "1AvZtnDy43gr6ttpokX-w5F5s-4KpapjFgQaR6tKkxgk"
sheet_name = "hzmbhm2023"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&sheet={sheet_name}"

@st.cache_data
def load_df(sheet_url):
    data = pd.read_csv(sheet_url, dtype=str)

df = pd.read_csv(url, dtype=str)

# Filter the dataframe using masks
mask = df["bib_num"].str.contains(text_search)
df_search = df[mask]

# Show the cards
N_cards_per_row = 3

# Number of images per page
images_per_page = 15

# Calculate the total number of pages
@st.cache_data
def calculate_total_pages(df, images_per_page):
    total_pages = len(df) // images_per_page
    if len(df) % images_per_page:
        total_pages += 1
    return total_pages

total_pages = calculate_total_pages(df, images_per_page)


# Only show page navigation if text_search is empty
if not text_search:
    # Add buttons for page navigation
    col1, col2, col3, col4, col5 = st.columns([8,8,.9,.8,.2])

    # Define functions to increment and decrement page number
    def increment_page():
        st.session_state.page += 1

    def decrement_page():
        st.session_state.page -= 1

    if st.session_state.page > 1:
        col3.button("◀", on_click=decrement_page)

    if st.session_state.page < total_pages:
        col5.button("▶", on_click=increment_page)

    with col4:
        # Display the current page number out of the total number of pages
        # 'f' before the string indicates that it's a formatted string literal
        current_page = st.session_state.page
        st.markdown(f"<p style='font-size:18px;'>{current_page}/{total_pages}</p>", unsafe_allow_html=True)


# Filter dataframe for the selected page
start_index = (st.session_state.page - 1) * images_per_page
end_index = start_index + images_per_page
subset_df = df.iloc[start_index: end_index]


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
            st.markdown(f'<a href="{row["image_path"]}"><img src="{row["image_path"]}" width="200"></a>', unsafe_allow_html=True)

else:
    # Display the images from the subset dataframe
    for n_row, row in subset_df.iterrows():
        i = n_row%N_cards_per_row
        if i==0:
            st.write("---")
            cols = st.columns(N_cards_per_row, gap="large")
        with cols[n_row%N_cards_per_row]:
            st.caption(f"{row['event'].strip()} - {row['event_time'].strip()} ")
            st.markdown(f'<a href="{row["image_path"]}"><img src="{row["image_path"]}" width="200"></a>', unsafe_allow_html=True)