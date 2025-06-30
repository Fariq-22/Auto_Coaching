from fastapi import FastAPI
from api.router import text_extraction
from api.router import question_generation
from api.router import conversation_generation
from api.router import promt_section
from api.router import question_evaluation
from core.logging import setup_logging

setup_logging()

# This is the main entry point for the FastAPI application.
# It initializes the FastAPI app and includes various routers for different functionalities.
app = FastAPI(
    title="Auto_Coaching End_points",
    summary="It includes Various functinality requirements for Auto_Coaching",
    version="0.0.1",
    docs_url=f"/auto_coaching/api/docs",
    openapi_url=f"/auto_coaching/api/openapi.json",
    contact={
        "name": "Fariq Rahman"}
)
# Include the routers for different functionalities
# Each router corresponds to a specific feature or module in the application.
# The routers are imported from the api.router package, which contains the individual modules for each functionality
# such as text extraction, question generation, conversation generation, prompt section, and question evaluation.
app.include_router(text_extraction.router)
app.include_router(question_generation.router)
app.include_router(conversation_generation.router)
app.include_router(promt_section.router)
app.include_router(question_evaluation.router)
