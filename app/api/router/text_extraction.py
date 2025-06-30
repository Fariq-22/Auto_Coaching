import logging
from fastapi import APIRouter
from langchain_core.output_parsers import JsonOutputParser
from fastapi.responses import JSONResponse

from models.schemas import Section_creation
from utils.file_utils import download_with_presigned
from utils.text_utils import text_extract
from utils.existing import existing_section_info

from dependencies.llm_services import summarizer_with_llm
from mongodb.dumping import dump_section_data
from mongodb.retrival import all_section_retrive_enhance

router = APIRouter(tags=["Auto_Coaching"])


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
        # Check if section already exists
        if await existing_section_info(client_id=payload.client_id, test_id=payload.test_id, links=payload.link):
            sections = await all_section_retrive_enhance(client_id=payload.client_id, test_id=payload.test_id)
            logging.info("The data is retrived from the mongoDB")
            return JSONResponse(status_code=200, content=sections)
    except ValueError as ve:
        logging.error(f"ValueError in existing_section_info: {ve}")
        return JSONResponse(status_code=400, content={"message": f"Invalid input: {ve}"})
    except Exception as e:
        logging.exception("Unexpected error in existing_section_info")
        return JSONResponse(status_code=500, content={"message": f"Error occurred in the using of existing data: {str(e)}"})

    try:
        logging.info(f"processing {payload.link}")
        all_text = ""
        for li in payload.link:
            try:
                download_file_from_s3 = await download_with_presigned(li)
                extracted_text = await text_extract(download_file_from_s3)
                all_text += extracted_text
            except Exception as file_exc:
                logging.error(f"Error processing file {li}: {file_exc}")
                return JSONResponse(status_code=400, content={"message": f"Failed to process file: {li}"})
        raw_result = await summarizer_with_llm(all_text)
        try:
            parsed_result = parser.parse(raw_result)
        except Exception as pe:
            logging.exception("Failed to parse LLM response")
            await dump_section_data(data=None, client_id=payload.client_id, test_id=payload.test_id, link=payload.link, error=f"ParseError: {str(pe)}")
            return JSONResponse(status_code=500, content={"message": "Invalid response format from LLM"})
        await dump_section_data(data=parsed_result, client_id=payload.client_id, test_id=payload.test_id, link=payload.link)
        return JSONResponse(status_code=200, content=parsed_result)
    except Exception as e:
        logging.exception(f"Error in Section segragration: {e}")
        await dump_section_data(data=None, client_id=payload.client_id, test_id=payload.test_id, link=payload.link, error=str(e))
        return JSONResponse(status_code=500, content={"message": "Internal Server Error"})

