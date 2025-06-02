from fastapi import FastAPI
from api.router import text_extraction
from api.router import question_generation
app=FastAPI()
app.include_router(text_extraction.router,prefix="/auto_coaching")
app.include_router(question_generation.router,prefix="/auto_coaching")
