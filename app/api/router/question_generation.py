import logging
from fastapi import APIRouter
from langchain_core.output_parsers import JsonOutputParser
from fastapi.responses import JSONResponse

from models.schemas import Questions


from dependencies.llm_services import question_generator
from mongodb.dumping import dump_section_data

router = APIRouter()