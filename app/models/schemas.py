from pydantic import BaseModel,Field
from typing import Optional,List,Dict, Any

class Section_creation(BaseModel):
    '''    The Validator used to validate the section creation information
    '''
    client_id :str = Field(...,description="The client id to retrive the documents")
    test_id : str = Field(...,description="The test id of the client")
    # link : str = Field(...,description="The link of the documenst")
    link: List[str] = Field(..., description="List of document links")


class Questions(BaseModel):
    '''
        The Validator used to validate the question information
    '''
    client_id :str = Field(...,description="The client id to retrive the documents")
    test_id : str = Field(...,description="The test id for filter with client")
    section_id: int =Field(...,description="To retrive the section information")
    question_type: str = Field(...,description="The type of questions need  to generated subjective or objective")
    num_questions: int =Field(...,description="The Number of questions need to be generated")
    num_options: Optional[int] = Field(None, description="Number of options (only for objective questions)")

class Conversational(BaseModel):
    '''
        Used for the Conversatinal Creation
    '''
    client_id:str = Field(...,description="The client id for data retrival")
    test_id : str = Field(...,description="The test_if for matching the test")
    section_id:int = Field(...,description="The section id for the data retrivak")

class Prompt(BaseModel):
    '''
        Used for Section Enhancement
    '''
    client_id : str = Field(...,description="The Clint id for retrive the Document")
    test_id : str = Field(...,description="The Test id to match the test ")
    user_prompt : str =Field(...,description="The prompt for section enhancement")



class Evaluation(BaseModel):
    '''
        Creating payload for evaluation API
    '''
    client_id : str = Field(...,description="The client id")
    test_id : str = Field(...,description="The test id")
    question_answer: List[Dict[str, Any]] = Field(..., description="List of JSON objects as question and answer information")
    conversation: Optional[List[Dict[str, Any]]] = Field(None, description="List of JSON objects as conversation information")

    