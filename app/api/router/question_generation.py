import logging
from fastapi import APIRouter, HTTPException
from langchain_core.output_parsers import JsonOutputParser
from fastapi.responses import JSONResponse

from models.schemas import Questions
from mongodb.retrival import section_retrieval_for_question_gen
from mongodb.dumping import dump_questions
from dependencies.llm_services import question_generator

router = APIRouter(tags=["Auto_Coaching"])

@router.post(
    "/questions_generate",
    summary="Generate Assessment Questions",
    description="""
    Generates subjective or objective questions based on the provided client ID, test ID, and section ID.

    - client_id: ID of the client
    - section_id: Section index in the document
    - question_type: 'single_choice'/'multiple_choice'/'short_answer'
    - num_questions: Number of questions to generate
    - num_options: Number of options for single_choice and multiple_choice questions (ignored for subjective)
    """
)
async def question_generation(payload: Questions):
    """
    Generate assessment questions for a given section.
    """
    logger = logging.getLogger(__name__)
    parser = JsonOutputParser()
    try:
        # Retrieve section for question generation
        try:
            section = await section_retrieval_for_question_gen(
                client_id=payload.client_id,
                test_id=payload.test_id,
                section_id=payload.section_id
            )
        except HTTPException as he:
            logger.error(f"Section not found: {he.detail}")
            return JSONResponse(status_code=404, content={"message": f"Section not found: {he.detail}"})
        except Exception as db_exc:
            logger.exception(f"Database error during section retrieval: {db_exc}")
            return JSONResponse(status_code=500, content={"message": "Database error during section retrieval."})

        ques_info = {
            "type_of_question": payload.question_type,
            "num_questions": payload.num_questions,
            "num_options": payload.num_options
        }
        try:
            ques_generation = await question_generator(section=section, info=ques_info)
        except Exception as llm_exc:
            logger.exception(f"Error during LLM question generation: {llm_exc}")
            await dump_questions(questions=None, client_id=payload.client_id, test_id=payload.test_id, section_id=payload.section_id, error=str(llm_exc))
            return JSONResponse(status_code=500, content={"message": "Error during LLM question generation."})

        logger.info(f"Storing the data in mongo db for client_id={payload.client_id}, test_id={payload.test_id}, section_id={payload.section_id}")
        try:
            parsed_result = parser.parse(ques_generation)
        except Exception as pe:
            logger.exception("Failed to parse LLM response")
            await dump_questions(questions=None, client_id=payload.client_id, test_id=payload.test_id, section_id=payload.section_id, error=f"ParseError: {str(pe)}")
            return JSONResponse(status_code=500, content={"message": "Invalid response format from LLM"})

        await dump_questions(questions=parsed_result, client_id=payload.client_id, test_id=payload.test_id, section_id=payload.section_id)
        return JSONResponse(status_code=200, content=parsed_result)

    except Exception as e:
        logger.exception(f"Error in Question generation: {e}")
        await dump_questions(questions=None, client_id=payload.client_id, test_id=payload.test_id, section_id=payload.section_id, error=str(e))
        return JSONResponse(status_code=500, content={"message": "Internal Server Error"})
