import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from utils import retry_generate_code, retry_execute_code
import constants

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

llm = ChatOpenAI(
    model="gpt-4",
    temperature=0.8,
    api_key=OPENAI_API_KEY
)

def save_renaming_prompt(column_names):
    columns_str = ', '.join(column_names)
    return f"""
Given the following column names: {columns_str}.
Generate Python code to rename these columns to business-friendly names using clear and descriptive words.
Rename the columns using the dictionary mapping and save the DataFrame.
Only generate Python code for renaming columns, nothing else.
No comments are needed in the code.
"""

def rename_columns(dataframe_info, cleaned_file_path):
    renaming_task = save_renaming_prompt(dataframe_info['column_names'])
    renaming_code = retry_generate_code(renaming_task, llm)
    final_file_name = os.path.basename(cleaned_file_path).replace(constants.CLEANED_SUFFIX, constants.FINAL_SUFFIX)
    final_file_path = os.path.join(constants.OUTPUT_DIR, final_file_name)
    retry_execute_code(renaming_code, cleaned_file_path, final_file_path)
    return final_file_path
