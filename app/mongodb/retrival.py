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
