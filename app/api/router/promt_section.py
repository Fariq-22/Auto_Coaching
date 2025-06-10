import logging
from fastapi import APIRouter
from langchain_core.output_parsers import JsonOutputParser
from fastapi.responses import JSONResponse
from models.schemas import Prompt

from mongodb.retrival import all_section_retrive_enhance
from models.schemas import Prompt
from mongodb.dumping import dump_section_data
from mongodb.deleting import delete_older_sections

from dependencies.llm_services import Section_enhancement

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
    parser = JsonOutputParser()
    try:
        data= await all_section_retrive_enhance(payload.client_id,payload.test_id)
        sec_enhance= await Section_enhancement(sections=data,user_prompt=payload.user_prompt)
        sucess=await delete_older_sections(client_id=payload.client_id,test_id=payload.test_id)
        if sucess:
            logging.info(f"Deleted old sections for client_id={payload.client_id}, test_id={payload.test_id}")
            try:
                parsed_result = parser.parse(sec_enhance)
            except Exception as pe:
                logging.exception("Failed to parse LLM response")
                await dump_section_data(data=None, client_id=payload.client_id, test_id=payload.test_id,link=None, error=f"ParseError: {str(pe)}")
                return JSONResponse(status_code=500, content={"message": "Invalid response format from LLM"})

            await dump_section_data(data=parsed_result, client_id=payload.client_id, test_id=payload.test_id,link=None)
            return JSONResponse(status_code=200, content=parsed_result)
        else:
            logging.warning(f"Failed to delete old sections for client_id={payload.client_id}, test_id={payload.test_id}")
 
    except Exception as e:
        logging.exception(f"Error in Enhanced Section segragration: {e}")
        await dump_section_data(None, payload.client_id, payload.link, error=str(e))
        return JSONResponse(status_code=500, content={"message": "Internal Server Error"})

    