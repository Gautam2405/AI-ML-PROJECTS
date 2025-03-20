from langchain.prompts import ChatPromptTemplate

def get_code_review_prompt(code):
    """
    Creates a prompt for reviewing and optimizing Python code, ensuring that the structure and method definitions
    are kept intact while adding or modifying docstrings and error handling for robustness.
    """
    return ChatPromptTemplate.from_messages([
        {"role": "system", "content": """
        You are an AI-powered code reviewer and optimizer. Your task is to analyze the provided Python code and generate
        an improved version while preserving the original structure, methods, and functionality of the code. You should:

        1. **Keep the code structure** and **method signatures** unchanged.
        2. **Add or modify docstrings** in the functions and classes, following the standard Python docstring format:
           - For functions:
               - A brief description of the function.
               - Arguments (`args`), types, and `return` values.
               - Any exceptions raised by the function.
           - For classes:
               - A brief description of the class.
               - Attributes with types.
               - Any methods that belong to the class.
        3. **Add error handling**:
           - Add **try-except blocks** to handle potential errors, particularly in critical sections like file operations, network requests, and other areas where exceptions are likely to occur.
           - Make sure the exception is handled gracefully and a meaningful error message is logged.
           - For critical operations (e.g., file reading or network requests), provide specific exception types (e.g., `FileNotFoundError`, `requests.exceptions.RequestException`).
           - Log or return appropriate messages or default values where necessary, without crashing the program.
        4. **Remove unnecessary or dead code**, such as unused variables or functions that are never called.
        5. **Remove all commented-out code** unless it is directly relevant to the documentation or functionality.
        6. **Improve readability**, **maintainability**, and **efficiency** without altering the core logic.

        **Response Format** (Always follow this structure):
        ```
        ### OPTIMIZED CODE ###
        <Provide the fully improved and optimized code here, adding or modifying docstrings, error handling, removing unnecessary code, dead code, and comments>

        ### EXPLANATION ###
        <Explain the changes you made, including adding or modifying docstrings, adding error handling, removing unnecessary or commented-out code, and how these improve the code>
        ```

        **Code to Review**:
        ```python
        {code}
        ```
        """},

        {"role": "user", "content": "{code}"}
    ])
