import streamlit as st
import pathlib
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# Model generation configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model_name = "gemini-1.5-pro-latest"
model = genai.GenerativeModel(model_name=model_name, generation_config=generation_config)
chat_session = model.start_chat(history=[])

def send_message_to_model(message, image_path=None):
    if image_path:
        image_input = {
            'mime_type': 'image/jpeg',
            'data': pathlib.Path(image_path).read_bytes()
        }
        response = chat_session.send_message([message, image_input])
    else:
        response = chat_session.send_message([message])
    
    # Ensure "Hi Ishani" is prepended to the response without extra greetings
    return "Hi Ishani, " + response.text.split("Hi there!")[0].strip()

def process_uploaded_image(uploaded_file):
    image = Image.open(uploaded_file)
    if image.mode == 'RGBA':
        image = image.convert('RGB')
    temp_image_path = pathlib.Path("temp_image.jpg")
    image.save(temp_image_path, format="JPEG")
    return temp_image_path

def generate_image_response(temp_image_path, question):
    st.spinner("🧑‍💻 Analyzing your image...")
    description_prompt = f"Describe the image in detail to answer the user's question. The user asked: '{question}'"
    response = send_message_to_model(description_prompt, temp_image_path)
    return response

def main():
    st.header(":blue[AI Chatbot]🤖")
    mode = st.radio("Select Mode", ("Text Mode", "Image Mode"), index=0)  # index=1 sets default to "Image Mode"
    question = st.text_input("Ask a question:")
    uploaded_file = None

    if mode == "Image Mode":
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

    submit_button = st.button("Submit Question")

    if mode == "Image Mode" and uploaded_file is not None:
        try:
            temp_image_path = process_uploaded_image(uploaded_file)
            # st.image(Image.open(temp_image_path), caption='Uploaded Image', use_container_width=True)

            if submit_button and question:
                response = generate_image_response(temp_image_path, question)
                st.write("**:blue[Chatbot's Response]**: ",response)
            elif submit_button and not question:
                st.warning("Please provide a question to ask the chatbot.")

        except Exception as e:
            st.error(f"An error occurred: {e}")

    elif mode == "Text Mode" and submit_button:
        if question:
            response = send_message_to_model(question)
            st.write("**:blue[Chatbot's Answer]**: ", response)
        else:
            st.warning("Please provide a question to ask the chatbot.")
    
    elif mode == "Image Mode" and submit_button:
        st.warning("Please upload an image first.")

if __name__ == "__main__":
    main()
