from app.config import client

def generate_story_llm(first_line: str, genre: str, creativity: float):
    prompt = f"""
    Continue the following story in {genre} genre.
    Write a detailed multi-paragraph story.
    Starting line:"{first_line}"
    Creativity level: {creativity}
    """
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )
    return response.text






