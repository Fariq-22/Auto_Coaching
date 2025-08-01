from mongodb.client import get_mongodb_connection
from fastapi import APIRouter , HTTPException

async def section_retrieval_for_question_gen(client_id, test_id, section_id):
    """
    Retrieves a specific section from the Document_Sections collection for question generation.
    - client_id: ID of the client
    - test_id: ID of the test
    - section_id: ID of the section to retrieve"""
    _, db = get_mongodb_connection()

    doc = await db["Document_Sections"].find_one(
        {
            "client_id": client_id,
            "test_id": test_id,
            "sections.id": section_id
        },
        {
            "sections": {"$elemMatch": {"id": section_id}},
            "_id": 0
        }
    )

    if not doc or "sections" not in doc or not doc["sections"]:
        raise HTTPException(status_code=404, detail="Section not found")

    return doc["sections"][0]


async def section_retrival_for_conversation(client_id, test_id, section_id):
    """
    Retrieves a specific section from the Document_Sections collection for conversation generation.
    - client_id: ID of the client
    - test_id: ID of the test
    - section_id: ID of the section to retrieve"""

    _, db = get_mongodb_connection()

    doc = await db["Document_Sections"].find_one(
        {
            "client_id": client_id,
            "test_id": test_id,
            "sections.id": section_id
        },
        {
            "sections": {"$elemMatch": {"id": section_id}},
            "_id": 0
        }
    )
    
    if doc["sections"][0]['is_conversation'] == 'false':
        raise HTTPException(status_code=404, detail="The Section is not elibile for creating conversation")

    return doc["sections"][0]



async def all_section_retrive_enhance(client_id,test_id):
    """
    Retrieves all sections from the Document_Sections collection for a given client and test.
    - client_id: ID of the client
    - test_id: ID of the test"""

    _, db = get_mongodb_connection()

    doc = await db["Document_Sections"].find_one(
        {
            "client_id": client_id,
            "test_id": test_id,
        }
    )

    if not doc:
        raise HTTPException(status_code=404, detail="Sections are not founded")
    return doc["sections"]


async def retrive_links(client_id,test_id):
    """
    Retrieves the links associated with a specific client and test from the Document_Sections collection.
    - client_id: ID of the client
    - test_id: ID of the test"""
    _, db = get_mongodb_connection()

    doc = await db["Document_Sections"].find_one(
        {
            "client_id": client_id,
            "test_id": test_id,
        }
    )

    if not doc:
        return False
    return doc["link"]



async def document_exists(client_id, test_id):
    """
    Checks if a document exists for the given client_id and test_id in the Document_Sections collection.
    - client_id: ID of the client
    - test_id: ID of the test"""
    _, db = get_mongodb_connection()

    doc = await db["Document_Sections"].find_one({
        "client_id": client_id,
        "test_id": test_id,
    }, {"_id": 1})  # Only fetch _id to optimize query

    return doc is not None
