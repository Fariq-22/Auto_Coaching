from google import genai
from google.genai import types
from core.config import settings

# Initialize Gemini Client
client= genai.Client(api_key=settings.GOOGLE_API_KEY)

# Prompt used for document section summarization
SECTION_ANALYSIS_PROMPT = """
Situation
You are a professional document analysis specialist working with various types of documents. Users will provide you with complete documents that require systematic breakdown and analysis to extract the most critical information in a digestible format.

Task
Analyze the provided document by first reading through it entirely, then intelligently dividing it into logical sections that follow a natural progression from beginning to end. For each identified section, give an Apppropiate Header and generate a concise summary and extract the  important points. Present your analysis in the specified JSON format with section_id, header, summary, and key_points fields And need to check with sections information treal-world conversation can be made out of it.

Objective
Transform lengthy, complex documents into structured, actionable insights that enable quick comprehension of the document's core content while maintaining accuracy and completeness of the source material.

Knowledge
- You must work exclusively with the information provided in the user's document - do not add external knowledge or assumptions
- The Divided sections should need to make the sence of section ,cuase furter the divided sections used to make questions.
- Section divisions should be logical and follow the natural flow of the document from start to finish
- Header should have Meaning Full name of the section
- Summaries should be capture the essence of each section
- Key points should highlight the critical, actionable, or significant information from each section
- Your life depends on maintaining strict adherence to the provided document content without adding interpretations or external information
- The output must be valid JSON format that can be parsed programmatically
- Section numbering should start from 1 and increment sequentially
- Each key_points array should contain multiple distinct points as separate strings
- Need to check the section is eligible to create the realistic multi-turn conversations can be created between a user and an agent.
- With the section summary and keywords check real-time problems or need guidance conversation can be made out of it.
- If the section is elible to create the Conversation then make the is_conversation filed True
- [IMPORTANT] The sections will be marked with True when enough information is available to create conversation of real-world problem.
- Select only sections that make logical sense for conversation creation

Criteria for section selection for Conversation creation:

    Sections must contain actionable content where users might seek help
    Content should involve problem-solving, guidance, or decision-making scenarios
    Avoid purely informational sections that don't lend themselves to interactive dialogue
    Prioritize sections with practical applications and common user pain points
    
The required output format is:
[
    {
        "id" : int,
        "header": String,
        "summary" : string,
        "key_points" : list[string],
        "is_conversation" : True/False
    },
    {
        "id" : int,
        "header": String,
        "summary" : string,
        "key_points" : list[string],
        "is_conversation" : True/False
    }
]

Ensure your response contains only the JSON output with no additional text, explanations, or formatting outside the specified structure.
"""



System_Question="""
Situation
You are a Question and Answer Generator tasked with creating assessment questions from agent coaching documents. You will be working with summarized information with summaries and key points, all derived from agent coaching materials used for performance evaluation.

Task
Analyze the provided coaching document information by reading through it entirely. Generate questions with answers based on the information given. Your life depends on you generating questions that are directly derived from the provided content without adding any external knowledge or assumptions.

Objective
Generate a complete set of questions with answers that can be used for agent performance calculation and assessment, maintaining question uniqueness and adherence to specified formatting requirements.

Knowledge

    Questions and answers must be generated exclusively from the provided information - do not add external knowledge
    The information about how the questions and answers are generated are given below
    The information will provide the details like type_of_question: ['Multiselect','Single','Short_Answer'] , Number_of_question (the total number of question need to create),Number_of _options(Number of options for the question only eligible for single and Multiselect),
    Information = {ques_info}
    If the question is Multiselect then we need to have multiple correct answer with given options
    If the question is Single then we need to have one correct answer in given options
    Ensure each question is unique and directly traceable to specific content in the provided materials
    For single and multiple questions, ensure all options are plausible and one correct option for single and multiple option for Multiselect
    For short questions, provide comprehensive answers that demonstrate understanding of the coaching concepts
    The options are only need to create for single and Multiselect questions
    For single and multiselect the answer need to be option number starting from 0 in an list
Output Format

{{
"questions" : [
    {{
    "question_no":int,
    "question_type":"Single" or "Multislect" or "Short",
    "question": String,
    "options":List[String] or None for short
    "Answer": If short "String" else [correct option number]
    }},
  
]
}}

Critical requirements:

    Follow the exact JSON structure provided
    Ensure question numbering is sequential
    Verify that single and multiselect questions have multiple choice options while subjective questions have empty options lists
    Generate the exact number of questions specified in the ques_info
    Maintain professional language appropriate for agent assessment
"""



System_sec_conversation="""
Situation
You are working with pre-processed coaching document content that has been extracted and summarized through an initial LLM pipeline. This content needs to be transformed into realistic conversational data's that will be used to evaluate and assess agent performance in coaching scenarios.

Task
Create high-quality conversational data from coaching material sections. Generate multi-turn conversations (minimum 10 exchanges) between users and coaching agents, where each turn is prefixed with either "User:" or "Agent:". The conversations must be unique, comprehensive, and cover all relevant aspects of the coaching content provided.

Objective
Enable comprehensive agent performance calculation and assessment by creating realistic conversational scenarios that test various agent capabilities across different coaching topics. These datasets will serve as benchmarks for evaluating how well coaching agents can apply knowledge, handle edge cases, and respond to real user needs.

Knowledge

    Conversations must start with realistic user problems or questions that would naturally arise in coaching contexts
    Include follow-up questions and clarifications from users to simulate natural conversation flow
    Agent responses must demonstrate practical knowledge application from the coaching material
    Include edge cases and challenging scenarios specifically designed to test agent limits and capabilities
    Make conversations specific to the section content and key points from the coaching material
    Keep individual message turns concise - users will not send lengthy messages in real interactions
    Agent messages should maintain a professional tone while user messages should reflect natural, real-time user communication patterns
    Cover realistic user scenarios that would occur in actual coaching sessions
    Ensure sufficient depth in each conversation to thoroughly evaluate agent capabilities
    Test various agent skills including problem-solving, empathy, guidance provision, and knowledge recall

Output_Format
{
Conversation:List[String]
}

Your life depends on creating conversations that authentically test agent capabilities while remaining true to realistic coaching interactions - the quality of agent evaluation directly depends on how well these conversations simulate real user needs and challenges."""



async def summarizer_with_llm(document_text):
    """
    Use Gemini model to analyze and summarize the given document text
    into logical sections with summaries and key points.
    """
    try:
        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=document_text,
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_budget=settings.THINKING_BUDGET),
                system_instruction=SECTION_ANALYSIS_PROMPT,
                response_mime_type="application/json"
            )
        )
        return response.text
    except Exception as e:
        return e


async def question_generator(section,info):
    '''
    The information for info
      type_of_question
      Number of question
      number of options if single or multiselect
    '''
    try:
        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=str(section),
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_budget=settings.THINKING_BUDGET),
                system_instruction=System_Question.format(ques_info=info),
                response_mime_type="application/json"
            )
        )
        return response.text
    except Exception as e:
        return e
    

async def Conversation_generation(section):
    try:
        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=str(section),
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_budget=settings.THINKING_BUDGET),
                system_instruction=System_sec_conversation,
                response_mime_type="application/json"
            )
        )
        return response.text
    except Exception as e:
        return e