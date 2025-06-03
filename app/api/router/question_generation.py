import logging
from fastapi import APIRouter,HTTPException
from langchain_core.output_parsers import JsonOutputParser
from fastapi.responses import JSONResponse

from models.schemas import Questions


from dependencies.llm_services import question_generator
from mongodb.dumping import dump_section_data

router = APIRouter()

# @router.post(
#     "/questions_generate",
#     summary="Generate Assessment Questions",
#     description="""
#     Generates subjective or objective questions based on the provided client ID, test ID, and section ID.

#     - client_id: ID of the client
#     - section_id: Section index in the document
#     - question_type: 'Single'/'Multiselect'/'Short'
#     - num_questions: Number of questions to generate
#     - num_options: Number of options for single and multiselect questions (ignored for subjective)
#     """
# )
# async def question_generation(payload: Questions):
#     parser = JsonOutputParser()
#     _, db = get_mongodb_connection()
#     try:
#         logging.info("Retriving the data from DB")
#         doc = db['Document_Sections'].find_one({
#             'client_id': str(payload.client_id) if isinstance(payload.client_id, int) else payload.client_id,
#             'test_id': payload.test_id,
#             'sections.id': payload.section_id
#         })

#         if not doc:
#             raise HTTPException(status_code=404, detail="Document not found")

#         section = next((s for s in doc['sections'] if s['id'] == payload.section_id), None)
#         if section is None:
#             raise HTTPException(status_code=404, detail="Section not found")

#         ques_info={"type_of_question":payload.question_type,"num_questions":payload.num_questions,"num_options":payload.num_options}
#         ques_generation=question_generator(section=section,info=ques_info)
#         logging.info("Storing the data in mongo db")
#         parsed_result =parser.parse(ques_generation)
#         db['Question_Creation'].insert_one({
#         "_id" : str(uuid.uuid4()) + str(datetime.datetime.now().timestamp()),
#         "client_id":payload.client_id,
#         "test_id":payload.test_id,
#         "section_id":payload.section_id,
#         "document_name" : "AutoCoahing_documents",
#         "added_at": datetime.datetime.now().isoformat(),
#         "questions":parsed_result,
#         "error": None
#         }
#         )
#         return JSONResponse(status_code=200, content=parsed_result)

#     except Exception as e:
#         logging.exception(f"Error Question Creation: {e}")
#         db['Question_Creation'].insert_one({
#         "_id" : str(uuid.uuid4()) + str(datetime.datetime.now().timestamp()),
#         "client_id":payload.client_i,
#         "test_id":payload.test_id,
#         "section_id":payload.section_id,
#         "document_name" : "AutoCoahing_documents",
#         "added_at": datetime.datetime.now().isoformat(),
#         "questions":None,
#         "error": str(e)
#         }
#         )
#         return JSONResponse(status_code=500, content={"message": "Internal Server Error"})