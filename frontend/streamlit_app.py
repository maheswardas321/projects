import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/generate-story"

st.title("📚 Genre-Based Story Completion App")

first_line = st.text_input("Enter the first line of your story")

genre = st.selectbox(
    "Choose Genre",
    ["Fantasy", "Horror", "Romance", "Sci-Fi", "Mystery"]
)

creativity = st.slider(
    "Creativity Level",
    min_value=0.1,
    max_value=1.0,
    value=0.7,
)

if st.button("Generate Story"):

    if first_line.strip() == "":
        st.warning("Please enter a starting line!")
    else:
        payload = {
            "first_line": first_line,
            "genre": genre,
            "creativity": creativity
        }

        with st.spinner("Generating story..."):
            response = requests.post(API_URL, json=payload)

        if response.status_code == 200:
            story = response.json()["story"]
            st.subheader("Generated Story")
            st.write(story)
        else:
            st.error("Error generating story.")