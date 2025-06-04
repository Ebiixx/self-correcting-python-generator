# AutoCorrectingPythonGenerator

A tool that automatically generates Python scripts based on user descriptions and self-corrects errors.

## Features

- Generates Python scripts from natural language descriptions
- Automatically executes the generated scripts
- Detects and handles errors in the generated code
- Installs missing Python modules as needed
- Automatically corrects faulty code with the help of AI

## Requirements

- Python 3.6 or higher
- Azure OpenAI API access
- The following Python packages:
  - openai
  - python-dotenv

## Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install openai python-dotenv
   ```
3. Create a `.env` file with the required API credentials:
   ```
   GLOBAL_LLM_SERVICE="***"
   AZURE_OPENAI_CHAT_DEPLOYMENT_NAME="***"
   AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME="***"
   AZURE_OPENAI_ENDPOINT="***"
   AZURE_OPENAI_API_KEY="***"
   ```

## Usage

Start the program with:

```
python main.py
```

Describe the desired script when prompted. The tool will attempt to generate an appropriate Python script, execute it, and correct it if necessary.

## How it Works

1. The user describes the desired script
2. The tool generates a suitable Python script using Azure OpenAI
3. The generated script is automatically executed
4. If errors occur:
   - Missing modules are identified and optionally installed
   - Syntax errors or other problems are detected and the code is automatically corrected
5. The corrected script is executed again
