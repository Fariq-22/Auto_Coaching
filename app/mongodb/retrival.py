from mongodb.client import get_mongodb_connection
from fastapi import APIRouter , HTTPException

async def section_retrieval_for_question_gen(client_id, test_id, section_id):
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