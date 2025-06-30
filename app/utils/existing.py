from mongodb.retrival import retrive_links,document_exists
from typing import List



async def existing_section_info(client_id:str,test_id:str,links:List[str]):
    try :
        """
        Check if the document exists for the given client_id and test_id
        If it exists, retrieve the links and compare them with the provided links
        If they match, return True; otherwise, return False
        If the document does not exist, return False
        If an error occurs, return the error """


        if await document_exists(client_id=client_id,test_id=test_id):
            retr_links = await retrive_links(client_id=client_id,test_id=test_id)
            print(retr_links)
            return set(retr_links) == set(links)
        else:
            return False
    except Exception as e:
        return e
