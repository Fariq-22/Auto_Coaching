import logging
import requests
from typing import List, Dict, Any

from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import JSONResponse

from langchain_core.output_parsers import JsonOutputParser
from dependencies.llm_services import (
    Question_Evaluation,
    Conversation_Evaluation
)
from core.config import settings
from models.schemas import Evaluation
from mongodb.dumping import dump_evaluation

router = APIRouter()



async def processing(
    data: List[Dict[str, Any]],
    batch_size: int = settings.batch_size
) -> List[Dict[str, Any]]:
    """
    Iterate over `data` in chunks of `batch_size`, call the LLM,
    parse JSON output and accumulate results.
    """
    parser = JsonOutputParser()
    pointer = 0
    processed: List[Dict[str, Any]] = []
    while pointer < len(data):
        logging.info("Batch processing started")
        batch_slice = data[pointer : pointer + batch_size]

        # 1) call your LLM service
        raw = await Question_Evaluation(data=batch_slice, batch_size=batch_size)
        logging.info("Raw batch response received")

        # 2) parse it
        parsed = parser.parse(raw)
        logging.info("Batch response parsed")

        processed.extend(parsed)
        pointer += batch_size

    return processed
    

async def batch_question_evaluation(payload: Evaluation):
    """
    Background task that does:
     1) Q/A batch processing
     2) Conversation evaluation
     3) Callback to external API
    """
    try:
        results = await processing(payload.question_answer, batch_size=settings.batch_size)
        logging.info(f"Completed batch eval for {payload.client_id}/{payload.test_id}")

        conversation = await Conversation_Evaluation(data=payload.conversation)

        # Fire-and-forget callback to your external API
        callback_payload = {
            "client_id": payload.client_id,
            "test_id": payload.test_id,
            "question_result": results,
            "conversation_result":conversation
        }
        await dump_evaluation(client_id = payload.client_id,test_id = payload.test_id , question_eval=results,conv_eval=conversation)

        resp = requests.post(settings.callback_url, json=callback_payload)
        resp.raise_for_status()
        logging.info(
            f"Callback succeeded ({resp.status_code}) "
            f"for {payload.client_id}/{payload.test_id}"
        )


    except Exception as e:
        logging.exception("Error in background batch evaluation")
        await dump_evaluation(client_id = payload.client_id,test_id = payload.test_id , question_eval=None,conv_eval=None,error=str(e))





@router.post(
    "/question_evaluation",
    summary="Evaluate user answers + conversation asynchronously",
    description="""
Starts two parallel evaluations (Q/A in batches, then full conversation)
and returns 202 immediately. """
)
async def question_ans_evaluation(
    payload: Evaluation,
    background_tasks: BackgroundTasks
):
    # schedule and return right away
    background_tasks.add_task(batch_question_evaluation, payload)
    return JSONResponse(
        status_code=202,
        content={"message": "Evaluation started; results will be sent to callback_url."}
    )

