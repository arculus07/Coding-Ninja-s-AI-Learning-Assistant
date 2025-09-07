from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint,ChatHuggingFace
load_dotenv()


def get_content_agent():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)
    # llm = ChatOpenAI(model = "gpt-5-nano")
    # llm = ChatOpenAI(model = "gpt-5", temperature = 0.5)
    # model = HuggingFaceEndpoint(
    #     repo_id='google/gemma-2-2b-it',
    #     task='text-generation'
    # )
    # llm = ChatHuggingFace(llm=model)

    content_prompt_template = """
    You are an expert Computer Science professor. Your task is to explain a concept to a college student
    in a clear, concise, and easy-to-understand way. The total explanation should be 3-4 paragraphs but straightforward, strictly about the topic understandable.
    - Start with a simple definition.
    - Use an analogy or a real-world example to make the concept relatable.

    - **Conditional Logic for Code:** First, determine if the topic is directly related to a 
      programming language, data structure, or algorithm. 
      - **If it is a programming topic**, provide a short, simple code snippet or pseudo-code to demonstrate it.
      - **If the topic is conceptual or theoretical** (e.g., 'Wormholes', 'General Relativity'), 
        **DO NOT** include a code snippet. Instead, you can expand on the implications or history of the concept.

    Topic to explain: "{sub_topic}"
    """

    prompt = PromptTemplate(
        template=content_prompt_template,
        input_variables=["sub_topic"]
    )

    parser = StrOutputParser()

    content_agent_chain = prompt | llm | parser

    return content_agent_chain