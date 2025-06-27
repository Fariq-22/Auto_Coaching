from mongodb.client import get_mongodb_connection
import uuid
import datetime
from typing import Dict,List
async def dump_section_data(data, client_id, test_id, link,error=None):
    _, db = get_mongodb_connection()
    document = {
        "_id": str(uuid.uuid4()) + str(datetime.datetime.now().timestamp()),
        "client_id": client_id,
        "test_id":test_id,
        "document_name": "AutoCoahing_documents",
        "link": link,
        "added_at": datetime.datetime.now().isoformat(),
        "sections": data if not error else None,
        "error": str(error) if error else None
    }
    await db["Document_Sections"].insert_one(document)

async def dump_questions(questions,client_id,test_id,section_id,error=None):
    _, db = get_mongodb_connection()
    document={
        "_id" : str(uuid.uuid4()) + str(datetime.datetime.now().timestamp()),
        "client_id":client_id,
        "test_id":test_id,
        "section_id":section_id,
        "document_name" : "AutoCoahing_documents",
        "added_at": datetime.datetime.now().isoformat(),
        "questions":questions,
        "error": error
        }
    await db["Question_Creation"].insert_one(document)



async def dump_conversation(conv,client_id,test_id,section_id,error=None):
    _, db = get_mongodb_connection()
    document={
        "_id" : str(uuid.uuid4()) + str(datetime.datetime.now().timestamp()),
        "client_id":client_id,
        "test_id":test_id,
        "section_id":section_id,
        "document_name" : "AutoCoahing_documents",
        "added_at": datetime.datetime.now().isoformat(),
        "Conversation":conv,
        "error": error
        }
    await db["Conversation_Creation"].insert_one(document)


async def dump_evaluation(client_id:str,test_id:str,question_eval:List[Dict],conv_eval:List[Dict],error=None):
    _, db = get_mongodb_connection()
    document={
        "_id" : str(uuid.uuid4()) + str(datetime.datetime.now().timestamp()),
        "client_id":client_id,
        "test_id":test_id,
        "Question_Evaluation":question_eval,
        "Conversation_Evaluation":conv_eval,
        "error": error
        }
    await db["Result_Evaluation"].insert_one(document)