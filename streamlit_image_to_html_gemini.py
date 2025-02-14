import pathlib
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv
import os
import streamlit as st

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# Configure the model
generation_config = {
    "temperature": 0.3,
    "top_p": 0.95,
    "top_k": 1,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model_name = "gemini-1.5-pro-latest"
model = genai.GenerativeModel(model_name=model_name, generation_config=generation_config)
chat_session = model.start_chat(history=[])

def send_message_to_model(message, image_path):
    image_input = {
        'mime_type': 'image/jpeg',
        'data': pathlib.Path(image_path).read_bytes()
    }
    response = chat_session.send_message([message, image_input])
    return response.text

def process_uploaded_image(uploaded_file):
    image = Image.open(uploaded_file)
    if image.mode == 'RGBA':
        image = image.convert('RGB')
    temp_image_path = pathlib.Path("temp_image.jpg")
    image.save(temp_image_path, format="JPEG")
    return temp_image_path

def generate_ui_code(temp_image_path):
    prompt1 = (
        "Describe this UI in accurate details. When you reference a UI element, "
        "put its name and bounding box in the format: [object name (y_min, x_min, y_max, x_max)]. "
        "Also describe the color of the elements."
    )
    description = send_message_to_model(prompt1, temp_image_path)
    # st.write("Initial Description:", description)
    
    refine_prompt = (
        f"Compare the described UI elements with the provided image and "
        f"identify any missing elements or inaccuracies. Provide a refined "
        f"and accurate description based on this comparison. Here is the initial description: {description}"
    )
    refined_description = send_message_to_model(refine_prompt, temp_image_path)
    st.write("Refined Description:", refined_description)
    
    html_prompt = (
        f"Please create a complete HTML document that includes the following: "
        f"1. A structured layout based on the provided UI description. "
        f"2. Use inline CSS styles for each element to ensure they are visually appealing and match the original design. "
        f"3. Include responsive design principles where appropriate, so the UI adapts well to different screen sizes. "
        f"4. If there are interactive elements, provide corresponding JavaScript code to enhance functionality. "
        f"5. Ensure that all UI elements are properly labeled and organized for clarity and maintainability. "
        f"6. Here is the refined description of the UI elements and their attributes: {refined_description}. "
        f"Make sure to include details like colors, fonts, sizes, and any specific functionalities mentioned in the description. "
    )
    initial_html = send_message_to_model(html_prompt, temp_image_path)
    # st.write("Initial HTML Code:", initial_html)
    
    refine_html_prompt = (
        f"Please review and validate the following HTML code for accuracy and best practices. "
        f"Your tasks are as follows: "
        f"1. Check for any syntactical errors or inconsistencies in the HTML structure. "
        f"2. Ensure that all HTML elements are appropriately nested and follow standard conventions. "
        f"3. Verify that the inline CSS styles applied to each element are correctly implemented and enhance the visual appearance. "
        f"4. Assess the JavaScript code included (if any) for functionality, ensuring it works as intended without errors. "
        f"5. Optimize the HTML for performance and accessibility, ensuring it is user-friendly and compliant with web standards. "
        f"6. Provide a refined version of the HTML code that incorporates your corrections and improvements. "
        f"Here is the initial HTML: {initial_html}"
    )
    refined_html = send_message_to_model(refine_html_prompt, temp_image_path)
    st.write("Refined HTML Code:", refined_html)
    return refined_html

# Streamlit UI
st.title("UI to HTML Code Generator")
uploaded_file = st.file_uploader("Upload an image of a UI", type=["jpg", "jpeg", "png"])

# Add a submit button
if uploaded_file is not None:
    if st.button("Submit"):
        with st.spinner("Processing image and generating code..."):
            temp_image_path = process_uploaded_image(uploaded_file)
            refined_html = generate_ui_code(temp_image_path)
            st.success("HTML code generated successfully!")
            st.code(refined_html, language='html')