import os
import openai
import streamlit as st
from PyPDF2 import PdfReader

def pdf_to_text(file):
    pdf_reader = PdfReader(file)
    mytext = ""
    for pageNum in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[pageNum]
        mytext += page.extract_text()
    return mytext

def ask_gpt(question, context, context_length=2048):
    context = context[-context_length:]  # Truncate the context to the last context_length characters
    prompt = f"{context}\nQuestion: {question}\nAnswer:"
    response = openai.Completion.create(
        engine="text-davinci-002", # Use GPT-3.5 Turbo
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.8,
    )
    return response.choices[0].text.strip()

st.markdown(
    """
    <style>
    .reportview-container {
        background: #00518F;
    }
    h1, h2, h3, h4 {
        color: #C4261D;
    }
    .sidebar .sidebar-content {
        background-image: linear-gradient(#00518F,#00518F);
        color: white;
    }
    .Widget>label {
        color: white;
        font-size: 18px !important;
    }
    [class^="st-b"]  {
        color: white;
    }
    .st-bb {
        background-color: transparent;
    }
    .stTextInput input {
        color: black;
    }
    .st-ij {
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Hello, welcome to our CC Club Innovate Chatbot!")

user_name = st.text_input("What's your name?")

if user_name:
    st.markdown(f"### Nice to meet you, {user_name}! Let's get started. Please upload your documents.")

uploaded_files = st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)
conversation_history = ""

if uploaded_files:
    texts = []
    for uploaded_file in uploaded_files:
        text = pdf_to_text(uploaded_file)
        texts.append(text)
    st.success(f"We have successfully uploaded {len(uploaded_files)} file(s)!")

    with st.form("question_form"):
        question = st.text_input("What would you like to know about the documents?")
        submitted = st.form_submit_button("Submit")
    if submitted:
        answers = []
        for text in texts:
            conversation_history +=f"\nQuestion: {question}"
            answer = ask_gpt(question, text + conversation_history)
            answers.append(answer)
            conversation_history += f"\nAnswer: {answer}"
        st.subheader("Here's what we found:")
        answer_table = {'Document': [f'Document {i+1}' for i in range(len(answers))],
                        'Answer': answers}
        st.table(answer_table)
        if st.button("Ask another question"):
            question = ""  # This will clear the question text input
else:
    st.warning("Please upload PDF files")

