from fastapi import FastAPI
from app.routes.story import router as story_router

app = FastAPI(title="Genre Story Generator API")

app.include_router(story_router)