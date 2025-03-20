import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser

# Load environment variables
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Initialize LLM model
llm = ChatGroq(model="llama3-70b-8192", temperature=0.0)
output_parser = StrOutputParser()

def generate_code_review_report(code, prompt_template):
    """
    Generates optimized code and improvement analysis using the LLM model while preserving the original code structure.
    
    Args:
    - code (str): The Python code that needs to be reviewed.
    - prompt_template (str): The template to format the prompt for code review.

    Returns:
    - tuple: A tuple containing the optimized code and explanation of improvements.
    """
    try:
        # Generate the response using the LLM model
        chain = prompt_template | llm | output_parser
        review_results = chain.invoke({"code": code})

        # Extract optimized code and improvements from the response
        optimized_code, improvements = review_results.split("### EXPLANATION ###")
        
        return optimized_code.strip(), improvements.strip()

    except Exception as e:
        raise Exception(f"Error during code review generation: {e}")
