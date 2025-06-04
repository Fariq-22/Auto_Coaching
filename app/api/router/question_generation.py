import logging
from fastapi import APIRouter,HTTPException
from langchain_core.output_parsers import JsonOutputParser
from fastapi.responses import JSONResponse

from models.schemas import Questions
from mongodb.retrival import section_retrieval_for_question_gen
from mongodb.dumping import dump_questions
from dependencies.llm_services import question_generator

router = APIRouter()

@router.post(
    "/questions_generate",
    summary="Generate Assessment Questions",
    description="""
    Generates subjective or objective questions based on the provided client ID, test ID, and section ID.

    - client_id: ID of the client
    - section_id: Section index in the document
    - question_type: 'Single'/'Multiselect'/'Short'
    - num_questions: Number of questions to generate
    - num_options: Number of options for single and multiselect questions (ignored for subjective)
    """
)
async def question_generation(payload: Questions):
    parser = JsonOutputParser()
    try:
        section= await section_retrieval_for_question_gen(payload.client_id,payload.test_id,payload.section_id)
        ques_info={"type_of_question":payload.question_type,"num_questions":payload.num_questions,"num_options":payload.num_options}
        ques_generation=await question_generator(section=section,info=ques_info)
        logging.info("Storing the data in mongo db")
        try:
            parsed_result = parser.parse(ques_generation)
        except Exception as pe:
                logging.exception("Failed to parse LLM response")
                await dump_questions(questions=None, client_id=payload.client_id, test_id=payload.test_id,section_id=payload.section_id, error=f"ParseError: {str(pe)}")
                return JSONResponse(status_code=500, content={"message": "Invalid response format from LLM"})

        await dump_questions(questions=parsed_result, client_id=payload.client_id, test_id=payload.test_id,section_id=payload.section_id)
        return JSONResponse(status_code=200, content=parsed_result)
        
    except Exception as e:
        logging.exception(f"Error in Question generation: {e}")
        await dump_questions(questions=None, client_id=payload.client_id, test_id=payload.test_id,section_id=payload.section_id, error=str(e))
        return JSONResponse(status_code=500, content={"message": "Internal Server Error"})
