from dotenv import load_dotenv
import os
load_dotenv() # load all enviroment variable from .env
from PIL import Image  # For image processing
import streamlit as st
import google.generativeai as genai  # Assuming this library is available

# Configure API key (assuming you have set GEMINI_API_KEY in .env)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Function to get response from Gemini-Pro-Vision model
def get_gemini_response(input_text, image, prompt):
    """
    Gets a response from the Gemini-Pro-Vision model for invoice extraction.

    Args:
        input_text (str): Text prompt for the model.
        image (PIL.Image.Image): Image object (not raw bytes).
        prompt (str): Additional prompt for the model.

    Returns:
        str: Text response from the model.
    """
    try:
        # Load the Gemini-Pro-Vision model
        model = genai.GenerativeModel('gemini-1.5-flash')

        # Generate content using the model
        response = model.generate_content([input_text, image, prompt])
        return response.text
    except Exception as e:
        return f"Error while processing the image: {str(e)}"


# Function to handle uploaded image
def input_image_setup(uploaded_file):
    """
    Processes the uploaded invoice image.

    Args:
        uploaded_file (streamlit.UploadedFile): Uploaded image file.

    Returns:
        PIL.Image.Image: Processed PIL image.
    """
    if uploaded_file is not None:
        # Open the image file and return as PIL.Image.Image
        image = Image.open(uploaded_file)
        return image
    else:
        raise FileNotFoundError('No file uploaded!')


# Streamlit app layout and functionality
st.set_page_config(page_title="Invoice Extractor")

st.header("Gemini Invoice Extractor")
input_text = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an invoice image...", type=["jpg", "jpeg", "png"])

input_prompt = """
You are an expert in understanding invoices. You will 
receive input images as invoices and you will have to
answer questions based on the input image.
"""

# Display uploaded image if available
if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Invoice.", use_container_width=True)

submit_button = st.button("Extract Invoice Information")

if submit_button:
    if uploaded_file is None:
        st.error("Please upload an invoice image.")
    else:
        # Display loading spinner while the model processes
        with st.spinner('Processing...'):
            # Get the image as a PIL.Image.Image
            image = input_image_setup(uploaded_file)

            # Get response from the model
            response = get_gemini_response(input_text, image, input_prompt)

            st.subheader("Extracted Information:")
            st.write(response)
