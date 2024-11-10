# cleaning.py

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from utils import retry_generate_code, retry_execute_code
import constants

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.8,
    api_key=OPENAI_API_KEY
)

def save_cleaning_prompt(dataframe_info):
    info_str = f"DataFrame ('{dataframe_info['file_name']}'):\n"
    info_str += "Columns and Data Types:\n"
    for col_info in dataframe_info['columns']:
        info_str += f"  - {col_info['name']}: {col_info['type']}\n"
    info_str += "Sample Data:\n"
    for row in dataframe_info['sample_data']:
        row_str = ', '.join(f"{k}: {v}" for k, v in row.items())
        info_str += f"  - {row_str}\n"
    
    return f"""
Write Python code to clean the CSV file provided in the variable 'file_path'. The CSV file has the following structure and sample data:

{info_str}

For the CSV file:
- Clean the DataFrame by:
  - Converting date columns to datetime format.
  - Converting time columns to time format.
  - Ensuring text columns are strings.
  - Stripping leading/trailing spaces.
  - Converting numerical columns to numeric types.
  - Converting categorical columns like 'Yes/No' to booleans.
  - Handling missing values.
  - Removing duplicates.
Only generate Python code for cleaning, nothing else.
No comments are needed in the code.

"""

def clean_dataframe(dataframe_info, local_path):
    cleaning_task = save_cleaning_prompt(dataframe_info)
    cleaning_code = retry_generate_code(cleaning_task, llm)
    cleaned_file_name = os.path.basename(local_path).replace('.csv', constants.CLEANED_SUFFIX)
    cleaned_file_path = os.path.join(constants.OUTPUT_DIR, cleaned_file_name)
    retry_execute_code(cleaning_code, local_path, cleaned_file_path)
    return cleaned_file_path
