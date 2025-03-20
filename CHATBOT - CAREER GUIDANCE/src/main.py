import streamlit as st
from prompting import get_career_guidance_prompt
from utils import generate_career_report, generate_pdf

# Streamlit UI
st.title("💡 LEAMON: AI-Powered Career Guidance Assistant")

# Initialize session state variables
def init_session():
    """
    Function for asking initial details from user to guide them by road map.
    """
    if "step" not in st.session_state:
        st.session_state.step = 1
    if "user_data" not in st.session_state:
        st.session_state.user_data = {}
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "report_generated" not in st.session_state:
        st.session_state.report_generated = False
init_session()

# Questions mapping
questions = {
    1: "What is your name?",
    2: "Are you currently employed? If yes, what is your profession?",
    3: "How old are you?",
    4: "Where is your native place?",
    5: "What is your passion or career interest?"
}
keys = {1: "name", 2: "profession", 3: "age", 4: "native_place", 5: "passion"}

# Display chat history
def display_chat_history():
    """ As per name function is designed in such a way for user experiance to observe previous chat"""
    st.subheader("Coversation")
    for qa in st.session_state.chat_history:
        st.markdown(f"**{qa['question']}**")
        st.markdown(f"You: {qa['answer']}")

display_chat_history()

# Ask next question
def ask_question():
    """ Fiunction will ask pre-defined question to user."""
    return questions.get(st.session_state.step, "Generating your career guidance Roaadmap... Please wait.")

# Handle user input
user_input = st.text_input(ask_question(), key="user_input")

if user_input:
    if st.session_state.step <= 5:
        st.session_state.user_data[keys[st.session_state.step]] = user_input
        st.session_state.chat_history.append({"question": ask_question(), "answer": user_input})
        st.session_state.step += 1
        st.rerun()

# Automatically generate report after collecting user's passion
if st.session_state.step > 5 and not st.session_state.report_generated:
    with st.spinner("Generating your career guidance Roadmap..."):
        prompt_template = get_career_guidance_prompt()
        st.session_state.generated_report = generate_career_report(st.session_state.user_data, prompt_template)
        st.session_state.report_generated = True
        st.rerun()

# Display report and PDF download option
if st.session_state.report_generated:
    st.subheader("Your Career Guidance Roadmap")
    st.markdown(st.session_state.generated_report)

    # Generate PDF Button
    pdf_buffer = generate_pdf(st.session_state.generated_report)
    st.download_button(
        label="📄 Download PDF",
        data=pdf_buffer,
        file_name="Career_Guidance_Roadmap.pdf",
        mime="application/pdf"
    )

    # Reset session
    if st.button("Start Over"):
        st.session_state.clear()
        st.rerun()
