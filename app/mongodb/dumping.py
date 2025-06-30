from mongodb.client import get_mongodb_connection
import uuid
import datetime
from typing import Dict,List


async def dump_section_data(data, client_id, test_id, link,error=None):
    """
    Dumps the section data into the MongoDB collection.
    - data: The section data to be stored.
    - client_id: The ID of the client. 
    - test_id: The ID of the test.
    - link: The link to the document.
    - error: Optional error message if any issue occurs during section creation."""
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
    """ 
    Dumps the generated questions into the MongoDB collection.
    - questions: The list of generated questions.
    - client_id: The ID of the client.
    - test_id: The ID of the test.  """

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
    """
    Dumps the conversation data into the MongoDB collection.
    - conv: The conversation data to be stored.
    - client_id: The ID of the client.
    - test_id: The ID of the test.
    - section_id: The ID of the section.
    - error: Optional error message if any issue occurs during conversation creation.
    """
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
    """
    Dumps the evaluation results into the MongoDB collection.
    - client_id: The ID of the client.  
    - test_id: The ID of the test.
    - question_eval: List of dictionaries containing question evaluation results.
    - conv_eval: List of dictionaries containing conversation evaluation results.
    - error: Optional error message if any issue occurs during evaluation.
    """
    _, db = get_mongodb_connection()
    document={
        "_id" : str(uuid.uuid4()) + str(datetime.datetime.now().timestamp()),
        "client_id":client_id,
        "test_id":test_id,
        "Question_Evaluation":question_eval,
        "Conversation_Evaluation":conv_eval,
        "updated_at": datetime.datetime.now().isoformat(),
        "error": error
        }
    await db["Result_Evaluation"].insert_one(document)