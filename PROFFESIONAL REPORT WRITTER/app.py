import os
import streamlit as st
import dotenv
from langchain_groq import ChatGroq
from langchain import PromptTemplate
from langchain.chains import LLMChain


dotenv.load_dotenv()


### Prompting
demo_template = """

### Instructions : 
You are a proffesional report writter. Your task is to generate a report on {input_topic}.if you don't have information then pass the message of not having knowladge.
The report should be True and well structured.

### **Reference Itineraries**: 
Here are some example of well structured report.
**Overview**: Overview of the report's main points.
**Content**: An index of reporter's contents in simple line-by-line format.
**Introduction**: An overview of the report's subject in proffesional structure.
**Body**: The main content of report.
**Conclusion**: Inferences, projections, and measures taken.
**References**: Source of information used in the report.


---

### **Chain of Thought Prompting (Step-by-Step Itinerary Planning Process)**:
**Know your audience**: well Structured output of details in easy english language.
**Clarity and conciseness**: Present information clearly and avoid unnecessary jargons.
**Accuricy and reliability**: Ensure all data and information is accurate ,varified and well structured.
**Visual aids**: Use  graphs, charts and tables to effectively present complex data.
**Structure and organization**: follow a logical sequences with clear headings and sub-headings with bullet points.
**Proof**: Carefully check for grammatical errors and types before submitting report.


---

### **Negative Prompting**:

**Avoid This (Negative Example)**:
- Avoid usage of informal words.
- Avoid usage of Expressions.
- Be sure about your content, Avoid to give information about which you don't have information.
- Only write what you have know.
- Must not give information if you don't have knowladge about topic.
- Avoid informal words, messages .

---

### **Output Format (Structured Report)**:
Format the report in a structured manner.



"""



### Modeling
models = {
    "Llama3-70B": "llama3-70b-8192",
    "Llama3-8B": "llama3-8b-8192",
    "Mixtral-8x": "Mixtral-8x7b-32768"
}

st.title("Chatbot")
selected_model = st.selectbox(
    "Select Model",
    ("Llama3-70B", "Llama3-8B", "Mixtral-8x"),
    index=1,
)

groq_api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(groq_api_key = groq_api_key , model = models[selected_model])

prompt = PromptTemplate(input_variables = ['input_topic'], template = demo_template)







### LLm Chain
chain = LLMChain(llm = llm, prompt = prompt)

input = st.text_input("Enter the topic for report")
if input : 
    st.write(chain.run(input))
