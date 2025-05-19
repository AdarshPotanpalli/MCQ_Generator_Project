import os
import pandas as pd
import json
import traceback
from dotenv import load_dotenv
# from langchain.chat_models import init_chat_model
from src.mcqgenerator.logger import logging

# langchain imports
from langchain_openai import ChatOpenAI
from langchain_community.callbacks.manager import get_openai_callback
# from langchain.callbacks import get_openai_callback
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain

load_dotenv() # loads env variables from .env file
# KEY = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(name="gpt-3.5-turbo", temperature=0.7)


## quiz prompt template
RESPONSE_JSON = {
    "1": {
        "mcq": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here",
        },
        "correct": "correct answer",
    },
    "2": {
        "mcq": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here",
        },
        "correct": "correct answer",
    },
    "3": {
        "mcq": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here",
        },
        "correct": "correct answer",
    },
}

TEMPLATE = """
Text: {text}

You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz of {number} multiple choice questions for {subject} students in {tone} tone. \
Make sure the questions are not repeated and check all the questions to be conforming to the text as well. \
Make sure to format your response like RESPONSE_JSON below and use it as a guide. \
Ensure to make {number} MCQs

### RESPONSE_JSON
{response_json}
"""


quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "number", "subject", "tone", "response_json"],
    template= TEMPLATE
)

quiz_chain = LLMChain(llm= llm, prompt = quiz_generation_prompt, output_key="quiz", verbose=True)

# quiz evalutation prompt
TEMPLATE2="""
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis. 
if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""
quiz_evaluation_prompt=PromptTemplate(input_variables=["subject", "quiz"], template=TEMPLATE)

# second chain, review chain
review_chain=LLMChain(llm=llm, prompt=quiz_evaluation_prompt, output_key="review", verbose=True)

# Sequential chain to join both chains
generate_evaluate_chain=SequentialChain(chains=[quiz_chain, review_chain], input_variables=["text", "number", "subject", "tone", "response_json"],
                                        output_variables=["quiz", "review"], verbose=True,)