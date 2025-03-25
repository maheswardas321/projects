import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

class TestCaseToFunctionAgent:
    def __init__(self, google_api_key: str):
        self.api_key = google_api_key
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")
    
    def format_test_case(self, test_case: str):
        """
        Formats the test case steps into a structured input that the model can understand.
        """
        return f"""
        Given the following test case steps:
        {test_case}
        Please generate a selenium script for mentioned test case, use proper locators.
        """

    def generate_function(self, formatted_test_case: str):
        """
        Uses Google's Generative AI model to generate selenium script for mentioned test case.
        """
        response = self.model.generate_content(formatted_test_case)
        return response.text.strip()

    def create_function_from_test_case(self, test_case: str):
        """
        Main function that takes a test case and generates a Python function.
        """
        formatted_test_case = self.format_test_case(test_case)
        python_function_code = self.generate_function(formatted_test_case)
        return python_function_code


model = genai.GenerativeModel("gemini-1.5-flash")
st.title("AI Chatbot")
st.markdown("Type your query below and the chatbot will respond.")
user_input = st.text_input("Your Message:", "", placeholder="Ask me anything...")
if user_input:
    response = model.generate_content(user_input)
    st.write("### Chatbot Response:")
    output = response.text
    st.write(output)
    agent = TestCaseToFunctionAgent(google_api_key=os.getenv("GOOGLE_API_KEY"))
    generated_function = agent.create_function_from_test_case(output)
    st.write(generated_function)
