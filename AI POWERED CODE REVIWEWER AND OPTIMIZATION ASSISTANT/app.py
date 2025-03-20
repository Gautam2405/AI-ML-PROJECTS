import streamlit as st
from prompting import get_code_review_prompt
from utils import generate_code_review_report

# Streamlit UI
st.title("🚀 AI-Powered Code Reviewer & Optimizer")

# Upload Python file
uploaded_file = st.file_uploader("📂 Upload a Python file for review", type=["py"])

# Initialize session state variables
def init_session():
    if "review_results" not in st.session_state:
        st.session_state.review_results = None
    if "optimized_code" not in st.session_state:
        st.session_state.optimized_code = None
    if "improvements" not in st.session_state:
        st.session_state.improvements = None

init_session()

if uploaded_file is not None:
    code = uploaded_file.getvalue().decode("utf-8")

    # Layout: Side-by-side code display
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📜 Uploaded Code")
        st.code(code, language="python")

    # Trigger review and optimization
    if st.button("🔍 Review & Optimize Code"):
        prompt_template = get_code_review_prompt(code)
        optimized_code, improvements = generate_code_review_report(code, prompt_template)

        # Store results in session state
        st.session_state.optimized_code = optimized_code
        st.session_state.improvements = improvements

    # Display optimized code
    with col2:
        st.subheader("✨ Optimized Code")
        if st.session_state.optimized_code:
            st.code(st.session_state.optimized_code, language="python")
        else:
            st.info("Click 'Review & Optimize Code' to generate optimized output.")

# Explanation of changes
if st.session_state.improvements:
    st.subheader("🔎 How We Improved Your Code")
    st.markdown(st.session_state.improvements)

    # Reset session
    if st.button("Start Over"):
        st.session_state.clear()
        st.rerun()
