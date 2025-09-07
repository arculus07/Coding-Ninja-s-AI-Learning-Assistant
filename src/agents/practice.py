from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint,ChatHuggingFace

load_dotenv()


def get_practice_agent():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    # llm = ChatOpenAI(model = "gpt-5-nano")
    # llm = ChatOpenAI(model = "gpt-5", temperature = 0.5)
    # model = HuggingFaceEndpoint(
    #     repo_id='google/gemma-2-2b-it',
    #     task='text-generation'
    # )
    # llm = ChatHuggingFace(llm=model)

    practice_prompt_template = """
    You are an expert question generator for a computer science quiz.
    Your task is to create a set of FOUR multiple-choice questions (MCQs) to test a student's 
    understanding of the following concept. The questions should progressively get harder.

    - Generate 4 questions in total.
    - The difficulty should increase in this order: Easy, Medium, Medium, Hard.
    - Each question must have 4 options (A, B, C, D).
    - You must clearly indicate the correct answer for each question.
    - Output the result strictly in a JSON format containing a single key "questions" which holds a list of the four question objects.

    Example Output Structure:
    {{
      "questions": [
        {{
          "question": "An easy, definitional question?",
          "options": {{ "A": "...", "B": "...", "C": "...", "D": "..." }},
          "answer": "A",
          "difficulty": "Easy"
        }},
        {{
          "question": "A slightly more complex, conceptual question?",
          "options": {{ "A": "...", "B": "...", "C": "...", "D": "..." }},
          "answer": "C",
          "difficulty": "Medium"
        }},
        {{
          "question": "Another conceptual or application-based question?",
          "options": {{ "A": "...", "B": "...", "C": "...", "D": "..." }},
          "answer": "D",
          "difficulty": "Medium"
        }},
        {{
          "question": "A challenging question that requires deeper understanding or synthesis?",
          "options": {{ "A": "...", "B": "...", "C": "...", "D": "..." }},
          "answer": "B",
          "difficulty": "Hard"
        }}
      ]
    }}

    Concept to test: "{sub_topic} make sure it should be good level and strictly about the sub topic , nothing stupid and vague generic questions , questions should be good"
    """

    prompt = PromptTemplate(
        template=practice_prompt_template,
        input_variables=["sub_topic"]
    )

    parser = JsonOutputParser()

    practice_agent_chain = prompt | llm | parser

    return practice_agent_chain