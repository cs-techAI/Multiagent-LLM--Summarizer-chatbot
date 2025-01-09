import os
# Disable symlink warning for huggingface_hub
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

import streamlit as st
from PyPDF2 import PdfReader
from transformers import pipeline

# Function to read PDF file and extract text
def read_pdf(file):
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

# Caching the summarization model
@st.cache_resource()
def load_summarizer(api_key=None):
    if api_key:
        # Use the API key if provided (for models that require it)
        return pipeline("summarization", model="facebook/bart-large-cnn", api_key=api_key)
    else:
        # Load the model without an API key
        return pipeline("summarization", model="facebook/bart-large-cnn")

# Function to summarize text using specified model
def summarize_text(pdf_text, summary_type, api_key=None):
    summarizer = load_summarizer(api_key)

    if summary_type == "5 Bullet Points":
        response = summarizer(pdf_text, max_length=150, min_length=30, do_sample=False, truncation=True)
        return "\n".join([f"- {point.strip()}" for point in response[0]['summary_text'].split('. ') if point])

    elif summary_type == "10 Bullet Points":
        response = summarizer(pdf_text, max_length=250, min_length=50, do_sample=False, truncation=True)
        return "\n".join([f"- {point.strip()}" for point in response[0]['summary_text'].split('. ') if point])

    elif summary_type == "Paragraph":
        response = summarizer(pdf_text, max_length=130, min_length=30, do_sample=False, truncation=True)
        return response[0]['summary_text']

    elif summary_type == "Sentence":
        response = summarizer(pdf_text, max_length=60, min_length=10, do_sample=False, truncation=True)
        return response[0]['summary_text']

# Caching the chatbot model
@st.cache_resource()
def load_chatbot(api_key=None):
    if api_key:
        # Use the API key if provided (for models that require it)
        return pipeline("text-generation", model="microsoft/DialoGPT-medium", api_key=api_key)
    else:
        # Load the model without an API key
        return pipeline("text-generation", model="microsoft/DialoGPT-medium")

# Function to generate chatbot responses based on user input and PDF content
def chat_with_bot(user_input, pdf_text, api_key=None):
    # Check for specific keywords in user input
    if "requirements" in user_input.lower():
        # Extract the requirements section from PDF text
        start_index = pdf_text.lower().find("requirements:")
        end_index = pdf_text.lower().find("internship benefits:", start_index)

        if start_index != -1 and end_index != -1:
            requirements_section = pdf_text[start_index:end_index].strip()
            return f"Requirements extracted from PDF:\n{requirements_section}"

    # Fallback to general conversation if no specific keywords matched
    chatbot = load_chatbot(api_key)

    # Combine user input with PDF content for context
    full_input = f"User: {user_input}\nContext: {pdf_text}\nChatbot:"

    # Generate a response based on user input and context
    response = chatbot(full_input, max_new_tokens=100, num_return_sequences=1, pad_token_id=50256)  # Use max_new_tokens instead of max_length
    return response[0]['generated_text'].strip()

# Streamlit UI
st.title("PDF Summarizer & Chatbot")
st.write("Choose between summarizing a PDF or chatting.")

# Option to choose functionality
functionality = st.radio("Select Functionality:", ["Summarization", "Chat"])

# Option to choose API Key usage
use_api_key = st.radio("Do you want to use an API key?", ["Yes", "No"], index=1)

api_key = None
if use_api_key == "Yes":
    api_key = st.text_input("Enter your API Key (if applicable):")

# File uploader
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Read and extract text from the PDF
    pdf_text = read_pdf(uploaded_file)

    if functionality == "Summarization":
        # Summary Type Selection
        st.subheader("Select Summary Type:")
        summary_type = st.radio("Choose how you want to summarize:",
                                 ["5 Bullet Points", "10 Bullet Points", "Paragraph", "Sentence"],
                                 index=0)

        # Summarize button
        if st.button("Summarize"):
            with st.spinner("Summarizing..."):
                summary = summarize_text(pdf_text, summary_type, api_key)
                st.subheader("Summary Output:")
                st.write(summary)

    elif functionality == "Chat":
        # Chat input
        user_input = st.text_input("Ask something about the PDF content:")

        if st.button("Send"):
            if user_input:
                with st.spinner("Chatting..."):
                    bot_response = chat_with_bot(user_input, pdf_text, api_key)
                    st.subheader("Chatbot Response:")
                    st.write(bot_response)
            else:
                st.warning("Please enter a message to chat.")
else:
    st.warning("Please upload a PDF file to proceed.")
