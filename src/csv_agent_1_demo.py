# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 09:41:40 2024

@author: Wolfgang Reuter

This script is an exercise for beginners. Try to: 
    
    1) Give the agent a prompt. 
    2) Give it some memory
    3) Generally try to improve the agent

USAGE: Run from command line: 
    streamlit run src\csv_agent_1_demo.py

"""

# =============================================================================
# Imports
# =============================================================================

import streamlit as st

OPENAI_API_KEY = st.secrets["openai"]["api_key"]

import os
from pathlib import Path

from langchain_experimental.agents import create_csv_agent 
from langchain_openai import ChatOpenAI 
from langchain.prompts import PromptTemplate

st.set_page_config(page_title="Ask your CSV")

# Get the current working directory (will be the project root in Streamlit Cloud)
project_root = Path(os.getcwd()) 

# =============================================================================
# Paths and Variables
# =============================================================================

IMAGE_PATH_TITANIC = project_root / "titanic.jpg"
IMAGE_PATH_CLIMATE = project_root / "extremeweather.jpg"
IMAGE_PATH_GDP = project_root / "economic_growth.jpg"

CSV_ID_CLIMATE = "GlobalLandTemperaturesByMajorCity.csv"
CSV_ID_TITANIC = "titanic_1.csv"
CSV_ID_GPD = "gdp.csv"

agent_prompt = """
You are an expert in statistics - and you also have a general broad knowledge. 
You are absolutetely familiar with Python and pandas dataframes. You are 
provided with some data - and when a user asks you a question, you analyze 
the data and you try to find the answer. 
When you analyze the data, you first of all look in the provided data. If you 
can't analyze the data because there are NaN values in it, you may think about
a reasonable way to replace or clean the data. If you have not enough 
information within the dataset that you are provided with, you may look 
elsewhere. In that case you mention in some way which information was not 
available in the dataset you are provided with. 
You always think about the question and how to analyze it first. If a user 
question is unspecific or seems strange to you, 
you **will ask the user what he or she means** by anserwing with a question. 
You **formulate your questions in full sentences** and in a way 
that the user understands what information with regards to the question you 
need. 
Your final answers are **also in full sentences**. You are polite - 
but **also to the point**.'
"""

# =============================================================================
# Functions
# =============================================================================

def main():
    
    st.header("Ask your CSV")
    
    # Create a placeholder for the image
    image_placeholder = st.empty()
    
    # Display an image
    image_placeholder.image(IMAGE_PATH_TITANIC)
    
    # Define the custom prompt with a system message
    custom_prompt = PromptTemplate(
            input_variables=["query"],
            template=agent_prompt
        )
    
    
    
    user_csv = st.file_uploader("Upload your CSV file", type="csv")
    if user_csv is not None: 
        file_name = user_csv.name 
        if file_name == CSV_ID_CLIMATE: 
            image_placeholder.image(IMAGE_PATH_CLIMATE)
        elif file_name == CSV_ID_GPD: 
            image_placeholder.image(IMAGE_PATH_GDP)
        else: 
            image_placeholder.image(IMAGE_PATH_TITANIC)
        user_question = st.text_input("Ask a question about your CSV: ")
        llm = ChatOpenAI(model="gpt-4o", temperature=0, 
                         openai_api_key=OPENAI_API_KEY)
        # Create the agent with the custom prompt
        agent = create_csv_agent(
            llm, 
            user_csv, 
            verbose=True, 
            allow_dangerous_code=True, 
            prompt=custom_prompt,
            handle_parsing_errors=True
        )
        if user_question is not None and user_question != "": 
            
            response = agent.invoke(user_question)
            
            st.write(response["output"])
    

# =============================================================================
# Execution
# =============================================================================
    
if __name__ == "__main__":
    main()
