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

st.set_page_config(page_title="Ask your CSV")

# Get the current working directory (will be the project root in Streamlit Cloud)
project_root = Path(os.getcwd()) 
st.write(f"Current working directory: {project_root}")

project_root = Path(__file__).resolve().parent.parent  # Go up one level
st.write(f"Current working directory: {project_root}")

# =============================================================================
# Paths and Variables
# =============================================================================

# Adjust paths relative to the working directory
IMAGE_PATH_TITANIC = project_root / "illustrations" / "titanic.jpg"

if not IMAGE_PATH_TITANIC.exists():
    st.error(f"❌ Image not found: {IMAGE_PATH_TITANIC}")
else:
    st.success(f"✅ Image exists: {IMAGE_PATH_TITANIC}")

IMAGE_PATH_CLIMATE = project_root / "illustrations" / "extremeweather.jpg"
IMAGE_PATH_GDP = project_root / "illustrations" / "economic_growth.jpg"

CSV_ID_CLIMATE = "GlobalLandTemperaturesByMajorCity.csv"
CSV_ID_TITANIC = "titanic_1.csv"
CSV_ID_GPD = "gdp.csv"

# =============================================================================
# Functions
# =============================================================================

def main():
    
    st.header("Ask your CSV")
    
    # Create a placeholder for the image
    image_placeholder = st.empty()
    
    # Display an image
    image_placeholder.image(IMAGE_PATH_TITANIC)
    
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
        llm = ChatOpenAI(temperature=0)
        agent = create_csv_agent(llm, user_csv, verbose=True, 
                                 allow_dangerous_code=True)
        if user_question is not None and user_question != "": 
            
            response = agent.run(user_question)
            
            st.write(response)
    

# =============================================================================
# Execution
# =============================================================================
    
if __name__ == "__main__":
    main()
