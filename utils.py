import pandas as pd
import os
import re
import subprocess
import constants

def read_dataframe_info(local_path):
    try:
        df_sample = pd.read_csv(local_path, nrows=5)
        columns = df_sample.columns.tolist()
        dtypes = df_sample.dtypes.astype(str).tolist()
        sample_data = df_sample.to_dict(orient='records')
        return {
            'file_name': os.path.basename(local_path),
            'columns': [{'name': col, 'type': dtype} for col, dtype in zip(columns, dtypes)],
            'sample_data': sample_data,
            'column_names': columns
        }
    except Exception as e:
        print(f"Error reading file '{local_path}': {e}")
        return None

def retry_generate_code(prompt, llm, retries=5):
    attempts = 0
    while attempts < retries:
        try:
            response = llm.invoke(prompt)
            code = re.sub(r'```python|```', '', response.content.strip()).strip()
            if code:
                return code
        except Exception as e:
            print(f"Code generation attempt {attempts + 1} failed: {e}")
        attempts += 1
    raise Exception("Code generation failed after multiple attempts.")

def retry_execute_code(code, input_file, output_file, retries=5):
    attempts = 0
    while attempts < retries:
        try:
            execute_code_in_local_env(code, input_file, output_file)
            return True
        except Exception as e:
            print(f"Execution attempt {attempts + 1} failed: {e}")
        attempts += 1
    raise Exception("Code execution failed after multiple attempts.")

def execute_code_in_local_env(code, input_file, output_file):
    script_content = f"""
import pandas as pd

file_path = '{input_file}'
output_path = '{output_file}'

df = pd.read_csv(file_path)
{code}
df.to_csv(output_path, index=False)
"""
    script_filename = os.path.join(constants.OUTPUT_DIR, os.path.basename(input_file).replace('.csv', constants.SCRIPT_SUFFIX))
    with open(script_filename, 'w') as f:
        f.write(script_content)
    
    result = subprocess.run(['python', script_filename], capture_output=True)
    if result.returncode != 0:
        print(result.stderr.decode())
        raise Exception("Execution failed")
    print("Execution succeeded")
