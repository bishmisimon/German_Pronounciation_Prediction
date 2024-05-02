import streamlit as st
import base64

# Set page configuration
st.set_page_config(layout="wide")

# Read the logo image as bytes and encode it to base64
with open("Logo.png", "rb") as f:
    image_bytes = f.read()
    image_base64 = base64.b64encode(image_bytes).decode()

# Custom HTML/CSS for the banner and background
custom_html = f"""
<style>
    .banner {{
        text-align: center;
        margin-top: 2px;
    }}
    hr {{
        width: 80%;
        border: none;
        border-top: 2px solid #FF0000;
        margin: 20px auto;
    }}
</style>
<div class="banner">
    <img src="data:image/png;base64,{image_base64}" alt="Logo" style="max-width: 100%; height: auto;">
</div>
<hr>
"""

# Display the custom HTML with the base64-encoded image
st.markdown(custom_html, unsafe_allow_html=True)

# Main content
st.markdown("<h1 style='text-align: center; color: #4169E1;'>Ihre Lieblings Deutsche Ausprache Bewerter</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; font-style: italic; font-family: cursive;'>Your German Pronunciation Feedback</h2>", unsafe_allow_html=True)
