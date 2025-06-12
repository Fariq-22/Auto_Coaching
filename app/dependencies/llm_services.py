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
    The information will provide the details like type_of_question: ['multiple_choice','single_choice','Short_Answer'] , Number_of_question (the total number of question need to create),Number_of _options(Number of options for the question only eligible for single_choice and multiple_choice),
    Information = {ques_info}
    If the question is multiple_choice then we need to have multiple correct answer with given options
    If the question is single_choice then we need to have one correct answer in given options
    Ensure each question is unique and directly traceable to specific content in the provided materials
    For single and multiple questions, ensure all options are plausible and one correct option for single and multiple option for Multiselect
    For short_answer questions, provide comprehensive answers that demonstrate understanding of the coaching concepts
    For short_answer questions the answer should be generated based on question and given content information.
    The options are only need to create for single and multiple_choice questions
    For single and multiple_choice questions the answer need to be option number starting from 0 in an list
Output Format

{{
"questions" : [
    {{
    "question_no":int,
    "question_type":multiple_choice or single_choice or short_answer
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



System_sec_conversation = """
Situation
You are working with pre-processed coaching document content that has been extracted and summarized through an initial LLM pipeline. This content needs to be transformed into realistic conversational data's that will be used to evaluate and assess agent performance in coaching scenarios.

Task
Create high-quality conversational data from coaching material sections. Generate multi-turn conversations (minimum 10 exchanges) between users and coaching agents, where each turn is prefixed with either "User:" or "Agent:". The conversations must be unique, comprehensive, and cover all relevant aspects of the coaching content provided.

Objective
Enable comprehensive agent performance calculation and assessment by creating realistic conversational scenarios that test various agent capabilities across different coaching topics. These datasets will serve as benchmarks for evaluating how well coaching agents can apply knowledge, handle edge cases, and respond to real user needs.

Information
The user will provide with the number of scenario's with that need to generate number of conversation with different Scenarios
info:Number_of_scenario={num_ques}

Knowledge
    The Scenario need to differnt from each other and need to genearted from given information(summary,keypoints) only
    Each scenario conversations must start with realistic user problems or questions that would naturally arise in coaching contexts
    Include follow-up questions and clarifications from users to simulate natural conversation flow
    Agent responses must demonstrate practical knowledge application from the coaching material
    Include edge cases and challenging scenarios specifically designed to test agent limits and capabilities
    Make conversations specific to the section content and key points from the coaching material
    Keep individual message turns concise - users will not send lengthy messages in real interactions
    Agent messages should maintain a professional tone while user messages should reflect natural, real-time user communication patterns
    Cover realistic user scenarios that would occur in actual coaching sessions
    Ensure sufficient depth in each conversation to thoroughly evaluate agent capabilities
    Test various agent skills including problem-solving, empathy, guidance provision, and knowledge recall
    Header of the conversation need to be mentioned in Scenario Field

Output_Format
[
    {{
        "Scenario": "String",
        "Conversation": [
            {{
                "User": "String"
            }},
            {{
                "Agent": "String"
            }},
            ...
        ]
    }},
    {{
        "Scenario": "String",
        "Conversation": [
            {{
                "User": "String"
            }},
            {{
                "Agent": "String"
            }},
            ...
        ]
    }}
]

Your life depends on maintaining the correct correct format and creating conversations that authentically test agent capabilities while remaining true to realistic coaching interactions - the quality of agent evaluation directly depends on how well these conversations simulate real user needs and challenges.
"""


system_improved_sections="""
Situation
You are working with document content that has already been processed through an initial extraction and summarization pipeline using an LLM. The content is structured as a list of JSON objects, where each object represents a document section containing a section_id, summary,key_points and is_conversation. Your role is to refine and enhance this pre-processed content to improve clarity, comprehensiveness, and understanding.

Task
Analyze each JSON section individually and improve both the summary and key_points fields. For each section, you must:

    Enhance the summary to be more comprehensive, clear, and well-structured
    Refine the key_points to be more actionable, specific, and valuable
    Ensure logical flow and coherence within each section
    Maintain the exact same JSON structure and format as the input
    Preserve all section_ids exactly as provided

Objective
Transform the existing summarized content into a higher-quality, more useful representation that provides better understanding and actionability for end users while maintaining the structured format required for downstream processing.

Knowledge

    The input content has already undergone initial LLM processing, so focus on refinement rather than basic extraction
    Each JSON object contains three fields: section_id, summary, and key_points
    The output must maintain identical structure to enable seamless integration with existing systems
    Quality improvements should focus on clarity, completeness, specificity, and actionability
    Consider that users will rely on these summaries and key points for decision-making and understanding

Also need to modify the content based on the user preception : {user_prompt}
Your life depends on you maintaining the exact same JSON structure and format as the input while significantly improving the quality and usefulness of the summary and key_points content based on given user preception. Do not add, remove, or rename any fields in the JSON structure.
"""

system_improved_sections_2="""
Situation
You are an advanced document processing AI tasked with refining and transforming pre-extracted document content structured as JSON objects. Each object contains critical metadata including section_id, summary, key_points, and is_conversation flag. The goal is to enhance and change document information based on specific user needs while maintaining the original JSON structure.

Task
1. Analyze the input JSON document content
2. Transform the content according to the specified user needs
3. Generate an enhanced version of the document with improved:
   - Clarity
   - Completeness
   - Specificity
   - Actionability
4. Preserve the original JSON object structure

Information Given
 {user_prompt}

Objective
Create a high-quality, user-centric document summary that enables effective decision-making and comprehensive comprehension of the source material.

Knowledge
- Maintain the original JSON schema
- Ensure each summary and key point is concise yet informative
- Convert abstract information into actionable insights

Critical Warning: Your performance directly impacts user decision-making. Approach each transformation with meticulous attention to detail and a commitment to generating the most valuable insights possible.
"""

system_evaluation_prompt="""
Situation
You are an advanced AI evaluation assistant tasked with comparing an original answer against a user-submitted answer with precise, objective analysis. The evaluation process requires a comprehensive comparison that goes beyond simple surface-level matching.

Task
Conduct a detailed similarity assessment between the original answer and the user's answer, considering contextual relevance, content accuracy, and semantic alignment. Calculate a precise similarity percentage and determine a pass/fail result based on a predefined passing threshold.

Objective
Provide a rigorous, unbiased evaluation that accurately measures the user's answer against the standard reference answer, ensuring high-quality assessment with minimal subjective interpretation.

The user will provide the Question,Answer,User_Answer and passing percentage. Compare the Answer with User_Answer and check User answer is passing the thresold criteria.

Output Format
   {
     "similarity_per": Float,
     "Result": "Pass" or "Fail"
   }

Critical Instructions
- Your evaluation must be precise and data-driven
- Focus on substantive content matching
- Be consistent in applying evaluation criteria
- Your life depends on providing an accurate, mathematically sound similarity assessment
"""



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
    

async def Conversation_generation(section,number_scenario):
    try:
        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=str(section),
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_budget=settings.THINKING_BUDGET),
                system_instruction=System_sec_conversation.format(num_ques=number_scenario),
                response_mime_type="application/json"
            )
        )
        return response.text
    except Exception as e:
        return e
    

async def Section_enhancement(sections,user_prompt):
    try:
        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=str(sections),
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_budget=settings.THINKING_BUDGET),
                system_instruction=system_improved_sections_2.format(user_prompt=user_prompt),
                response_mime_type="application/json"
            )
        )
        return response.text
    except Exception as e:
        return e
    


async def Question_Evaluation(data):
    try:
        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=str(data),
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_budget=settings.THINKING_BUDGET),
                system_instruction=system_evaluation_prompt,
                response_mime_type="application/json"
            )
        )
        return response.text
    except Exception as e:
        return e
    