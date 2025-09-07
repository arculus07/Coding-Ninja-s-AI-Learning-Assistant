from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint,ChatHuggingFace
load_dotenv()


def get_planner_agent():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    # llm = ChatOpenAI(model = "gpt-5-nano")
    # llm = ChatOpenAI(model = "gpt-5", temperature = 0.5)
    # model = HuggingFaceEndpoint(
    #     repo_id='google/gemma-2-2b-it',
    #     task = 'text-generation'
    # )
    # llm = ChatHuggingFace(llm = model)
    planner_prompt_template = """
    
    You are an expert curriculum planner for computer science. A student wants to learn a topic.

    Your task is to:
    1.  Identify the core topic from the user's input: "{user_input}".
    2.  Generate a logical, step-by-step learning roadmap with a clear progression 
        from fundamentals to advanced concepts.
    3.  The roadmap must be structured as a JSON object containing a single key "roadmap" 
        which holds a list of strings.

    Example Output for "Dynamic Programming":
    {{
      "roadmap": [
        "1. Introduction to Dynamic Programming: What is it?",
        "2. The Concept of Overlapping Subproblems",The Concept of Optimal Substructure",
        "3. Top-Down Approach: Memoization", Bottom-Up Approach: Tabulation",
        "4. Classic DP Problem: Fibonacci Sequence"
      ]
    }}

    Now, generate the roadmap for the user's input: "{user_input} but it can't be more than 4-5 Steps it should be strictly not more than 5 steps it can be 2-3 also if required 4-5 but not more than this"
    Note:- If input doesn't make sense , or say like Hi Hello , anything which is not related to any topic or any question , THEN THE TOPIC WILL BE "CODING NINJAS Company and it's History foundation and everything not technical"
    """
    prompt = PromptTemplate(
        template=planner_prompt_template,
        input_variables=["user_input"]
    )

    parser = JsonOutputParser()
    planner_agent_chain = prompt | llm | parser

    return planner_agent_chain