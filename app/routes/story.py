from fastapi import APIRouter
from app.schemas import StoryRequest
from app.llm.openai_client import generate_story_llm

router = APIRouter()


@router.get("/")
def home():
    return {"message": "Story Generator API Running"}


@router.post("/generate-story")
def generate_story(request: StoryRequest):

    story = generate_story_llm(
        request.first_line,
        request.genre,
        request.creativity,
    )

    return {"story": story}