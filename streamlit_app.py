# Import libraries
import streamlit as st
import pandas as pd
from PIL import Image
import requests
from io import BytesIO

# Page setup
st.set_page_config(page_title="Running Photos - Bib Number Search 號碼布搵相", page_icon="🏃", layout="wide")  

# Create three columns with different widths on the same row
col_01, col_02, col_03 = st.columns([.2,2,1.5])

col_01.image("https://raw.githubusercontent.com/marco-cheung/runner-tag-streamlit/main/.streamlit/running-bib-icon.png", width=60)

# Hide the full screen option for every image displayed
hide_img_fs = '''
<style>
button[title="View fullscreen"]{
    visibility: hidden;}
</style>
'''
st.markdown(hide_img_fs, unsafe_allow_html=True)

with col_02:
  st.markdown("<h1 style='text-align: left; color: black; font-size: 36px;'>Bib Number Search 號碼布搵相</h1>", unsafe_allow_html=True)

# Connect to the Google Sheet
sheet_id = "1AvZtnDy43gr6ttpokX-w5F5s-4KpapjFgQaR6tKkxgk"
sheet_name = "hzmbhm2023"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&sheet={sheet_name}"

@st.cache_data
def load_df(sheet_url):
    data = pd.read_csv(sheet_url, dtype=str, usecols=['event','image_path','bib_num','photo_location'])

df = pd.read_csv(url, dtype=str)

# Apply a selectbox to the df's 'event' column
event_names = df['event'].unique()

# Select event for df
selected_event = st.selectbox('Select race 賽事選擇:', options=event_names)
df_event = df[df['event'] == selected_event]

# Create an empty HTML element with a unique ID,
st.markdown("<div id='image-display'></div>", unsafe_allow_html=True)

with st.form('input_form'):
    # Create two columns; adjust the ratio to your liking
    col1, col2 = st.columns([3,1]) 

    # Use the first column for text input
    with col1:
        # Use a text_input to get the keywords to filter the dataframe
        text_search = st.text_input("Input Bib Number 請輸入號碼布編號", placeholder='Example 例子: 7757', label_visibility='collapsed')
    
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

# Filter the dataframe using masks
mask = df_event["bib_num"].str.contains(text_search)
df_search = df_event[mask]

# Show the cards
N_cards_per_row = 3

# Number of images per page
images_per_page = 12

# Get the current page number
#current_page = st.session_state.page

# JavaScript code to scroll to the element with the ID 'image-display'
js = f"""
<script>
    function scrollToTop(uniqueValue){{
        var element = parent.document.getElementById('image-display');
        element.scrollIntoView();
    }}
</script>
"""

# Calculate the total number of pages
def calculate_total_pages(df_event, images_per_page):
    total_pages = len(df_event) // images_per_page
    if len(df_event) % images_per_page:
        total_pages += 1
    return total_pages

total_pages = calculate_total_pages(df_event, images_per_page)
total_pages_search = calculate_total_pages(df_search, images_per_page)

# Show the total number of photos found
if text_search:
    if len(df_search) > 0:
        st.markdown(f"<p style='font-size:18px;'>{len(df_search)} photos were found.<br>搵到{len(df_search)} 張相</p>", unsafe_allow_html=True)
    else:
        st.markdown(f"<p style='font-size:18px;'>No photos were found, try searching with part of the number.<br>唔好意思搵唔到相，試下輸入部分號碼搜尋。</p>", unsafe_allow_html=True)

# Apply CSS to the specific columns only
st.write('''<style>
[data-testid="column"]:nth-child(1) {
    width: calc(33.3333% - 1rem) !important;
    flex: 1 1 calc(33.3333% - 1rem) !important;
    min-width: calc(33% - 1rem) !important;
}
</style>''', unsafe_allow_html=True)

# Add buttons for page navigation
col_c, col_d, col_e = st.columns([.9,1,.2])

def display_page_navigation(col_03, col_04, col_05, decrement_key, increment_key):   
    # Define functions to increment and decrement page number
    def increment_page():
        st.session_state.page += 1
        #scroll up back to top after clicking a button
        st.components.v1.html(js + f"<script>scrollToTop({st.session_state.page});</script>", height=0)

    def decrement_page():
        st.session_state.page -= 1
        #scroll up back to top after clicking a button
        st.components.v1.html(js + f"<script>scrollToTop({st.session_state.page});</script>", height=0)

    # Check if text_search has changed since the last run
    if 'last_text_search' not in st.session_state or st.session_state.last_text_search != text_search:
        # Navigate to the first page if text_search has changed
        st.session_state.page = 1
        st.session_state.last_text_search = text_search

    # Get the current page number
    current_page = st.session_state.page

    if st.session_state.page > 1:
        if (text_search and len(df_search) > 0) or not text_search:
            col_03.button("◀", on_click=decrement_page, key=decrement_key)
            
            
    if st.session_state.page < total_pages:
        if (text_search and (total_pages_search!=1 and current_page!=total_pages_search)) or not text_search:
            col_05.button("▶", on_click=increment_page, key=increment_key)

    if text_search:
        with col_04:
            if len(df_search) > 0:
                st.markdown(f"<p style='font-size:18px;'>{current_page}/{total_pages_search}</p>", unsafe_allow_html=True)

    # If no input of text_search...
    else:
        with col_04:
            st.markdown(f"<p style='font-size:18px;'>{current_page}/{total_pages}</p>", unsafe_allow_html=True)

col_c_key = 'col_c_key'
col_e_key = 'col_e_key'
display_page_navigation(col_c, col_d, col_e, col_c_key, col_e_key)


# Filter dataframe for the selected page
start_index = (st.session_state.page - 1) * images_per_page
end_index = start_index + images_per_page

subset_df = df_event.iloc[start_index: end_index]
subset_df_search = df_search.iloc[start_index: end_index]


# Show the filtered results
if text_search:
    for n_row, row in subset_df_search.reset_index().iterrows():
        i = n_row%N_cards_per_row
        if i==0:
            st.write("---")
            cols = st.columns(N_cards_per_row, gap="large")

        # draw the card
        with cols[n_row%N_cards_per_row]:
            st.caption(f"Location 拍攝地點: {row['photo_location'].strip()}")
            st.markdown(f'<a href="{row["image_path"]}"><img src="{row["image_path"]}" width="200"></a>', unsafe_allow_html=True)
            
else:
    # Display the images from the subset dataframe
    for n_row, row in subset_df.iterrows():
        i = n_row%N_cards_per_row
        if i==0:
            st.write("---")
            cols = st.columns(N_cards_per_row, gap="large")
        with cols[n_row%N_cards_per_row]:
            st.caption(f"Location 拍攝地點: {row['photo_location'].strip()}")
            st.markdown(f'<a href="{row["image_path"]}"><img src="{row["image_path"]}" width="200"></a>', unsafe_allow_html=True)

# Add buttons for page navigation
col_h, col_i, col_j = st.columns([.9,1,.2])
col_h_key = 'col_h_key'
col_j_key = 'col_j_key'
display_page_navigation(col_h, col_i, col_j, col_h_key, col_j_key)

# Add footer
st.markdown("""
    <hr style='border: dashed 1px lightgrey; margin-bottom: 0;'>
    <p style='font-size: 13px; text-align: right;'>
    🧩 Creator: <a href='https://github.com/marco-cheung/runner-tag-streamlit' target='_blank'>@marco-cheung</a> <br>
    📷 Photo Source: Official Organizers</p>
""", unsafe_allow_html=True)