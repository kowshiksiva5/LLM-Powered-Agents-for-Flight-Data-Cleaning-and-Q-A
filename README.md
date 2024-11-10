

# Interactive Data Cleaning and Q&A Agent

This project is an interactive Python application that automates the cleaning and renaming of CSV files and allows users to ask questions about the data using a language model agent.

## Features

- **Automated Data Cleaning:** Utilizes GPT-4 to generate Python code for cleaning datasets.
- **Automated Column Renaming:** Generates code to rename columns with clear and descriptive names.
- **Interactive Q&A:** Enables users to ask natural language questions about the data.
- **Modular Design:** Organized into multiple files for better maintainability.

## Project Structure

```
your_project/
├── constants.py
├── main.py
├── cleaning.py
├── renaming.py
├── utils.py
├── outputs/
│   └── (cleaned and renamed files will be saved here)
├── requirements.txt
└── README.md
```

- **constants.py:** Contains constant values used throughout the application.
- **main.py:** The main script to run the application.
- **cleaning.py:** Handles data cleaning functionalities.
- **renaming.py:** Manages column renaming processes.
- **utils.py:** Provides utility functions used across modules.
- **outputs/:** Directory where all output files are stored.
- **requirements.txt:** Lists all Python dependencies.
- **README.md:** Project documentation.

## Usage

Run the main script:

```bash
python main.py
```

### Steps

1. **Enter the Number of Files:**

   ```
   Enter the number of files:
   ```

   Input the number of CSV files you wish to process.
2. **Provide File Paths:**

   For each file, you will be prompted:

   ```
   Enter the path for file X:
   ```

   Provide the full path to each CSV file.
3. **Data Cleaning and Renaming:**

   The application will:

   - Read a sample of each CSV file.
   - Generate and execute Python code to clean the data.
   - Generate and execute code to rename columns.
   - Save the cleaned and renamed files in the `outputs/` directory.
4. **Interactive Q&A Session:**

   After processing, you can ask questions about your data:

   ```
   Enter your question (or 'exit' to quit):
   ```

   - Type a question in natural language.
   - The agent will provide an answer.
   - Type `'exit'` to end the session.

### Example Session

```
Enter the number of files: 2
Enter the path for file 1: /path/to/your/first_file.csv
Enter the path for file 2: /path/to/your/second_file.csv
Cleaning the DataFrame for /path/to/your/first_file.csv...
Execution succeeded
Cleaning completed for /path/to/your/first_file.csv.
Renaming columns for outputs/first_file_cleaned.csv...
Execution succeeded
Renaming completed for outputs/first_file_cleaned.csv.
Cleaning the DataFrame for /path/to/your/second_file.csv...
Execution succeeded
Cleaning completed for /path/to/your/second_file.csv.
Renaming columns for outputs/second_file_cleaned.csv...
Execution succeeded
Renaming completed for outputs/second_file_cleaned.csv.
Enter your question (or 'exit' to quit): Which airline has the most flights listed?
[Agent's response]
Enter your question (or 'exit' to quit): exit
```

## Dependencies

- `langchain`
- `langchain_openai`
- `pandas`

Install them using:

```bash
pip install -r requirements.txt
```

## Notes

- **OpenAI Model Access:** Ensure you have access to the GPT-4 model in your OpenAI account.
- **API Key Security:** Keep your OpenAI API key secure and do not share it publicly.
- **Quality of Responses:** The effectiveness of cleaning, renaming, and Q&A depends on the performance of the language model.

---

**Disclaimer:** This application uses OpenAI's GPT-4 model for generating code and answering questions. Ensure compliance with OpenAI's usage policies when using this application.
