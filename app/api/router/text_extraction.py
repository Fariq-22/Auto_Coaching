import logging
from fastapi import APIRouter
from langchain_core.output_parsers import JsonOutputParser
from fastapi.responses import JSONResponse

from models.schemas import Section_creation
from utils.file_utils import download_with_presigned
from utils.text_utils import text_extract

from dependencies.llm_services import summarizer_with_llm
from mongodb.dumping import dump_section_data

router = APIRouter()


@router.post("/section_generation", summary="Generating Sections With Documents",
    description="""
    Generates Summary of the Document with client_id,document_link

    - client_id: ID of the client
    - Test id : Test id of the client
    - link : List of linkS
    """)
async def section_generation(payload:Section_creation):
    parser = JsonOutputParser()
    try:
        logging.info(f"processing {payload.link}")
        all_text=""
        for li in payload.link:
            download_file_from_s3 = await download_with_presigned(li)
            extracted_text =await text_extract(download_file_from_s3) #TODO: make async
            all_text+=extracted_text
        raw_result = await summarizer_with_llm(all_text)
        try:

            parsed_result = parser.parse(raw_result)
        except Exception as pe:
            logging.exception("Failed to parse LLM response")
            await dump_section_data(data=None, client_id=payload.client_id, test_id=payload.test_id,link=payload.link, error=f"ParseError: {str(pe)}")
            return JSONResponse(status_code=500, content={"message": "Invalid response format from LLM"})

        await dump_section_data(data=parsed_result, client_id=payload.client_id, test_id=payload.test_id,link=payload.link)
        return JSONResponse(status_code=200, content=parsed_result)
    
    except Exception as e:
        logging.exception(f"Error in Section segragration: {e}")
        await dump_section_data(data=None, client_id=payload.client_id, test_id=payload.test_id,link=payload.link, error=str(e))
        return JSONResponse(status_code=500, content={"message": "Internal Server Error"})

