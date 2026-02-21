from dotenv import load_dotenv
import os
from google import genai

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Initialize client
client = genai.Client(api_key=api_key)


# ---------- Story Generator Function ----------
def generate_story(first_line, genre, creativity):
    prompt = f"""
    Continue the following story in {genre} genre.
    Write a detailed multi-paragraph story.

    Starting line: "{first_line}"

    Creativity level: {creativity}
    """

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )

    return response.text


# ---------- Example Usage ----------
story = generate_story(
    first_line="The door opened at midnight without a sound.",
    genre="mystery",
    creativity="high"
)

print("\nGenerated Story:\n")
print(story)