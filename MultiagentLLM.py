import streamlit as st
import json
from transformers import pipeline
import fitz  # PyMuPDF
from docx import Document

# Initialize the summarization and question-answering pipelines with specific models
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
question_answering = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

# Function to summarize text using Hugging Face Transformers
def summarize_text(text):
    summary = summarizer(text, max_length=500, min_length=200, do_sample=False)  # Allow longer summaries
    return summary[0]['summary_text']

# Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    uploaded_file.seek(0)  # Reset file pointer
    pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in pdf_document:
        text += page.get_text()
    return text

# Function to extract text from DOCX
def extract_text_from_docx(file):
    doc = Document(file)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

# Streamlit app layout
st.title("Multi-Agent LLM Application")

# Option to choose between Summarizer and Chat agent
agent_type = st.selectbox("Choose Agent Type", ["Summarizer", "Chat"])

# Input JSON for agent data (for Summarizer)
json_input = st.text_area("Input JSON (for Summarization)", '{"data": "Your text goes here."}')

# File uploader for PDF and DOCX
uploaded_file = st.file_uploader("Upload a PDF or DOCX file", type=["pdf", "docx"])

if 'messages' not in st.session_state:
    st.session_state.messages = []

if agent_type == "Chat":
    # Chat input handling
    user_input = st.text_input("You:", "")

    if user_input:
        # Append user message to session state
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Generate a response based on uploaded document content if available
        if uploaded_file is not None:
            if uploaded_file.type == "application/pdf":
                document_content = extract_text_from_pdf(uploaded_file)
            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                document_content = extract_text_from_docx(uploaded_file)
            else:
                document_content = ""

            # Use question-answering pipeline to respond to user queries
            response = question_answering(question=user_input, context=document_content)

            # Append assistant message to session state with the answer
            answer = response['answer']
            if answer.strip():  # Check if the answer is not empty
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                st.session_state.messages.append({"role": "assistant", "content": "I couldn't find an answer in the document."})

if st.button("Run Agent"):
    try:
        data = None

        # Check if a file is uploaded for summarization
        if uploaded_file is not None:
            if uploaded_file.type == "application/pdf":
                data = extract_text_from_pdf(uploaded_file)
            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                data = extract_text_from_docx(uploaded_file)
            else:
                st.error("Unsupported file type.")

        # If no file is uploaded, check JSON input for Summarizer
        if data is None and agent_type == "Summarizer":
            input_data = json.loads(json_input)
            data = input_data.get('data')

        if data:  # Proceed only if there's data to summarize or use in chat
            if agent_type == 'Summarizer':
                summary = summarize_text(data)
                st.subheader("Summary:")
                st.write(summary)

            elif agent_type == 'Chat':
                # Display chat messages from session state
                for message in st.session_state.messages:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])

        else:
            st.error("No data available for processing.")

    except json.JSONDecodeError:
        st.error("Invalid JSON format. Please check your input.")
