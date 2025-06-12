from fastapi import FastAPI
from api.router import text_extraction
from api.router import question_generation
from api.router import conversation_generation
from api.router import promt_section
from api.router import question_evaluation
app=FastAPI()

app.include_router(text_extraction.router,prefix="/auto_coaching")
app.include_router(question_generation.router,prefix="/auto_coaching")
app.include_router(conversation_generation.router,prefix="/auto_coaching")
app.include_router(promt_section.router,prefix="/auto_coaching")
app.include_router(question_evaluation.router,prefix="/auto_coaching")
