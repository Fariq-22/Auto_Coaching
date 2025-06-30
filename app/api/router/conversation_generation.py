import logging
from fastapi import APIRouter
from langchain_core.output_parsers import JsonOutputParser
from fastapi.responses import JSONResponse



from dependencies.llm_services import Conversation_generation
from models.schemas import Questions

from mongodb.retrival import section_retrival_for_conversation
from mongodb.dumping import dump_conversation


router=APIRouter(tags=["Auto_Coaching"])



@router.post("/conv_generation",summary="Generate Conversation with section information",
    description="""
    Generates Real-world conversation with the Section information

    - client_id: ID of the client
    - test_id: Test identifier
    - section : Section id
    - Number_of question: Number of scenario
    """)
async def conversation(payload : Questions):
    parser = JsonOutputParser()
    try:
        logging.info("Checking section is eligible for Conversation")
        section_data= await section_retrival_for_conversation(client_id=payload.client_id,test_id=payload.test_id,section_id=payload.section_id)
        conver_gen= await Conversation_generation(section=section_data,number_scenario=payload.num_questions)
        try:
            parsed_result =parser.parse(conver_gen)
        except Exception as pe:
                logging.exception("Failed to parse LLM response")
                await dump_conversation(conv=None, client_id=payload.client_id, test_id=payload.test_id,section_id=payload.section_id, error=f"ParseError: {str(pe)}")
                return JSONResponse(status_code=500, content={"message": "Invalid response format from LLM"})
        
        await dump_conversation(conv=parsed_result, client_id=payload.client_id, test_id=payload.test_id,section_id=payload.section_id)
        return JSONResponse(status_code=200, content=parsed_result)
    except Exception as e:
        logging.exception(f"Error in Conversation creation: {e}")
        await dump_conversation(conv=None, client_id=payload.client_id, test_id=payload.test_id,section_id=payload.section_id, error=str(e))
        return JSONResponse(status_code=500, content={"message": "Internal Server Error"})
