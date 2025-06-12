import logging
from fastapi import APIRouter
from langchain_core.output_parsers import JsonOutputParser
from fastapi.responses import JSONResponse

from models.schemas import Evaluation
from dependencies.llm_services import Question_Evaluation


router = APIRouter()

@router.post(
    "/question_evaluation",
    summary="Evaluate the user answer with the original answer",
    description="""
    It will take the Question, Answer , User_Answer , Passing Thresold and provide the percentage od user answer

    - Question: The original question,
    - Answer: True Answer for the Question
    - User_Answer: User Written Answer
    - Thresold: Passing Thresold
    """
)
async def question_ans_evaluation(payload:Evaluation):
    parser = JsonOutputParser()
    data={"Question":payload.question,"Answer":payload.answer,"User_answer":payload.us_answer,"Thresold":payload.pass_thresold}
    print(data)
    try:
        scores_from_llm = await Question_Evaluation(data)
        print(scores_from_llm)
        try:
            parsed_result = parser.parse(scores_from_llm)
        except Exception as e:
            logging.exception("Failed to parse LLM response")
            return JSONResponse(status_code=500, content={"message": "Invalid response format from LLM. The Parsing is not done well."})

        return JSONResponse(status_code=200, content=parsed_result)
    except Exception as e:
        logging.exception(f"Error in Evaluation : {e}")
        
        return JSONResponse(status_code=500, content={"message": "Internal Server Error"})


