from fastapi import FastAPI
from api.router import text_extraction
from api.router import question_generation
from api.router import conversation_generation
from api.router import promt_section
from api.router import question_evaluation

app = FastAPI(
    title="Auto_Coaching End_points",
    summary="It includes Various functinality requirements for Auto_Coaching",
    version="0.0.1",
    docs_url=f"/auto_coaching/api/docs",
    openapi_url=f"/auto_coaching/api/openapi.json",
    contact={
        "name": "Fariq Rahman"}
)

app.include_router(text_extraction.router)
app.include_router(question_generation.router)
app.include_router(conversation_generation.router)
app.include_router(promt_section.router)
app.include_router(question_evaluation.router)
