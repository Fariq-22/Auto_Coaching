from mongodb.client import get_mongodb_connection



async def delete_older_sections(client_id: str, test_id: str):
    _, db = get_mongodb_connection()
    try:
        result = await db['Document_Sections'].delete_one({
            "client_id": client_id,
            "test_id": test_id
        })
        return True
    except Exception as e:
        return False
