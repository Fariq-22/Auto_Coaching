from mongodb.retrival import retrive_links,document_exists
from typing import List



async def existing_section_info(client_id:str,test_id:str,links:List[str]):
    try :
        if await document_exists(client_id=client_id,test_id=test_id):
            retr_links = await retrive_links(client_id=client_id,test_id=test_id)
            print(retr_links)
            return set(retr_links) == set(links)
        else:
            return False
    except Exception as e:
        return e
