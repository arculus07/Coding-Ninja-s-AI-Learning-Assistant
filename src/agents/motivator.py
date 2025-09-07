from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint,ChatHuggingFace
load_dotenv()

def get_motivator_agent():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    # llm = ChatOpenAI(model = "gpt-5-nano")
    # llm = ChatOpenAI(model = "gpt-5", temperature = 0.5)
    # model = HuggingFaceEndpoint(
    #     repo_id='google/gemma-2-2b-it',
    #     task='text-generation'
    # )
    # llm = ChatHuggingFace(llm=model)

    motivator_prompt_template = """
    You are a fun and motivating AI Tutor. A student has just finished a quiz and didn't score very well
    on the topic of "{topic}".

    Your goal is to lift their spirits and encourage them to keep trying without sounding generic.
    - Share a short, inspiring quote, a surprising fun fact, or a light-hearted joke related to programming or the specific topic.
    - End with a supportive message that encourages them to try the re-test.

    Example for "Recursion": 
    "Hey, don't worry! To understand recursion, you must first understand recursion. 😉 It's a classic programmer joke for a reason! Every expert was once a beginner. Let's try breaking it down again. You've got this!"

    Now, generate a unique and motivational message for the topic: "{topic}"
    """

    prompt = PromptTemplate(
        template=motivator_prompt_template,
        input_variables=["topic"]
    )

    parser = StrOutputParser()

    motivator_agent_chain = prompt | llm | parser

    return motivator_agent_chain
