import os
import pandas as pd
from dotenv import load_dotenv
import constants
from utils import read_dataframe_info
from cleaning import clean_dataframe
from renaming import rename_columns
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.8,
    api_key=OPENAI_API_KEY
)

def process_single_file(local_path):
    dataframe_info = read_dataframe_info(local_path)
    if not dataframe_info:
        return None

    print(f"Cleaning the DataFrame for {local_path}...")
    cleaned_file_path = clean_dataframe(dataframe_info, local_path)
    print(f"Cleaning completed for {local_path}.")

    print(f"Renaming columns for {cleaned_file_path}...")
    final_file_path = rename_columns(dataframe_info, cleaned_file_path)
    print(f"Renaming completed for {cleaned_file_path}.")

    return final_file_path

def process_data(file_paths):
    final_file_paths = []
    for local_path in file_paths:
        final_file_path = process_single_file(local_path)
        if final_file_path:
            final_file_paths.append(final_file_path)
    return final_file_paths

if __name__ == "__main__":
    if not os.path.exists(constants.OUTPUT_DIR):
        os.makedirs(constants.OUTPUT_DIR)
    num_files = int(input("Enter the number of files: "))
    file_paths = []
    for i in range(num_files):
        file_path = input(f"Enter the path for file {i+1}: ")
        file_paths.append(file_path)
    final_file_paths = process_data(file_paths)
    dataframes = []
    for final_file_path in final_file_paths:
        df = pd.read_csv(final_file_path)
        dataframes.append(df)

    agent = create_pandas_dataframe_agent(
        llm,
        dataframes,
        agent_type="tool-calling",
        verbose=True,
        allow_dangerous_code=True
    )
    while True:
        question = input("Enter your question (or 'exit' to quit): ")
        if question.lower() == 'exit':
            break
        response = agent.invoke(question)
        print(response.output)
