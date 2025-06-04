import logging
from fastapi import APIRouter
from langchain_core.output_parsers import JsonOutputParser
from fastapi.responses import JSONResponse
from models.schemas import Prompt

from mongodb.retrival import all_section_retrive_enhance
from models.schemas import Prompt


router = APIRouter()

@router.post(
    "/section_enhance",
    summary="",
    description="""
    Enhance the sections based on user feedback

    - client_id: ID of the client
    - Test_id : Current test id
    """
)
async def section_enhance(payload: Prompt):
    data= await all_section_retrive_enhance(payload.client_id,payload.test_id)
    return data