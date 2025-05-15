import os
import subprocess
import sys
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Configure Azure OpenAI client
client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-01"
)

# Ask the user for a description of the desired script
description = input("What should the desired script do?\n-> ")

def generate_script(description):
    """Creates a Python script based on the description."""
    response = client.chat.completions.create(
        max_tokens=10000,
        model="gpt-4o-mini",  # Replace with the correct model name or deployment name
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates Python code."},
            {"role": "user", "content": f"Create a Python script that does the following: {description}"}
        ]
    )

    # The generated code (the output often contains explanations that need to be removed)
    generated_code = response.choices[0].message.content

    # Extract only the actual Python code (between ```python and ``` tags)
    start_marker = "```python"
    end_marker = "```"

    # Extract the code block from the response
    if start_marker in generated_code and end_marker in generated_code:
        generated_code = generated_code.split(start_marker)[1].split(end_marker)[0].strip()

    # Add UTF-8 declaration to the generated code
    utf8_declaration = "# -*- coding: utf-8 -*-\n"
    return utf8_declaration + generated_code

def run_script(script_filename):
    """Runs the generated script and returns the error output, if any."""
    try:
        # Run the script and redirect both stdout and stderr to capture the output
        result = subprocess.run(
            ["python", script_filename], 
            text=True, 
            capture_output=True, 
            check=True
        )
        return None  # No error
    except subprocess.CalledProcessError as e:
        # Return the standard output and error output of the script
        return e.stderr  # Return error output

def fix_script(error_message, description):
    """Makes a request to OpenAI to repair the script based on the error."""
    fix_response = client.chat.completions.create(
        max_tokens=400,
        model="gpt-4o-mini",  # Replace with the correct model name or deployment name
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates Python code."},
            {"role": "user", "content": f"The following script caused an error: {error_message}. "
                                        f"Fix the script that should do the following: {description}"}
        ]
    )

    # Extract only the actual Python code (between ```python and ``` tags)
    generated_code = fix_response.choices[0].message.content
    start_marker = "```python"
    end_marker = "```"

    if start_marker in generated_code and end_marker in generated_code:
        generated_code = generated_code.split(start_marker)[1].split(end_marker)[0].strip()

    utf8_declaration = "# -*- coding: utf-8 -*-\n"
    return utf8_declaration + generated_code

def install_missing_module(module_name):
    """Installs a missing module with pip."""
    print(f"The module '{module_name}' is missing.")
    install = input(f"Should '{module_name}' be installed? (yes/no): ").strip().lower()
    if install == 'yes':
        print(f"Installing {module_name}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])
        print(f"The module '{module_name}' was successfully installed.")
    else:
        print(f"Installation of module '{module_name}' rejected.")
        sys.exit(1)

def handle_missing_module_error(error_message):
    """Checks for an error due to a missing module and attempts to install it."""
    if "ModuleNotFoundError" in error_message:
        # Extract the module name from the error message
        missing_module = error_message.split("'")[1]
        install_missing_module(missing_module)
        return True
    return False

# First attempt to create and run the script
generated_code = generate_script(description)

# Save the generated script to a file
script_filename = "generated_script.py"
with open(script_filename, "w", encoding="utf-8") as file:
    file.write(generated_code)

# First execution attempt of the script
print("\nRunning script...\n")
error_message = run_script(script_filename)

# Check if an error occurred
while error_message:
    print(f"Error detected: {error_message}")
    
    # Check if the error was caused by a missing module
    if handle_missing_module_error(error_message):
        # If a module was installed, run the script again
        print("Trying to run the script again...\n")
        error_message = run_script(script_filename)
    else:
        # If it's not a missing module, try to fix the script
        print("Attempting to fix the script...\n")
        fixed_code = fix_script(error_message, description)
        
        # Write the fixed script to the file
        with open(script_filename, "w", encoding="utf-8") as file:
            file.write(fixed_code)

        # Run again
        print("Running fixed script...\n")
        error_message = run_script(script_filename)

        if error_message:
            print(f"The fixed script still has errors: {error_message}")
            break
else:
    print("Script was executed successfully.")
