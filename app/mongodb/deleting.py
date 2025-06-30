from mongodb.client import get_mongodb_connection



async def delete_older_sections(client_id: str, test_id: str):

    """
     It will take client_id and test_id as input and delete the older sections
     from the Document_Sections collection in MongoDB.
    """
    _, db = get_mongodb_connection()
    try:
        result = await db['Document_Sections'].delete_one({
            "client_id": client_id,
            "test_id": test_id
        })
        return True
    except Exception as e:
        return False
