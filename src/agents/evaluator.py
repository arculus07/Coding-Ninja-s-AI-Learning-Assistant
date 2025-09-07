from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint,ChatHuggingFace
load_dotenv()


def get_evaluator_agent():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    # llm = ChatOpenAI(model = "gpt-5-nano")
    # llm = ChatOpenAI(model = "gpt-5", temperature = 0.5)
    # model = HuggingFaceEndpoint(
    #     repo_id='google/gemma-2-2b-it',
    #     task='text-generation'
    # )
    # llm = ChatHuggingFace(llm=model)

    evaluator_prompt_template = """
    You are an expert and friendly AI evaluator for a quiz. Your task is to analyze a student's answer to a multiple-choice question.

    Here is the data:
    - Question: "{question}"
    - Options: {options}
    - Correct Answer Key: "{correct_answer}"
    - Student's Submitted Answer Key: "{student_answer}"

    Your analysis must be in two parts:
    1.  Determine if the student's answer is correct by comparing their submitted key to the correct answer key.
    2.  Provide constructive feedback based on the correctness.
        - If the answer is correct: Congratulate the student with a short, encouraging message.
        - If the answer is incorrect: DO NOT reveal the correct answer. Instead, provide a small, guiding hint based on why their chosen option is wrong or what concept they might be misunderstanding.

    Respond strictly in the following JSON format:
    {{
      "correct": boolean,
      "feedback": "Your feedback or hint here"
    }}
    """

    prompt = PromptTemplate(
        template=evaluator_prompt_template,
        input_variables=["question", "options", "correct_answer", "student_answer"]
    )

    parser = JsonOutputParser()

    evaluator_agent_chain = prompt | llm | parser

    return evaluator_agent_chain