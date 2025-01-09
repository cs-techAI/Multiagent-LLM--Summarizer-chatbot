# PDF Summarizer & Chatbot

This application allows users to upload a PDF file and either summarize its content or interact with a chatbot that can answer questions based on the PDF content. The application provides an option to use an API key for models that require authentication or to run without an API key.

## Features

- **PDF Summarization**: Users can choose different summary formats (bullet points, paragraph, etc.) to get concise summaries of the uploaded PDF content.
- **Chatbot Interaction**: Users can ask questions about the PDF content, and the chatbot will provide relevant responses.
- **API Key Support**: Users have the option to enter an API key for models that require it, or they can run the application without an API key.

## Requirements

To run this application, you need the following Python packages:

- Streamlit
- PyPDF2
- Transformers
- Torch

You can install these packages using pip:


## Usage

1. Clone this repository or download the code files.
2. Navigate to the directory where the code is located.
3. Run the application using Streamlit:


4. Open your web browser and go to `http://localhost:8501` to access the application.
5. Upload a PDF file using the file uploader.
6. Choose whether you want to summarize the PDF or chat with the chatbot.
7. If you choose to use an API key, enter it in the provided input field.
8. Click on "Summarize" or "Send" to get results.

## Example Usage

- **Summarization**: Select "Summarization" from the functionality options, choose your preferred summary type, and click "Summarize" to see the output.
- **Chat**: Select "Chat," enter your question about the PDF content, and click "Send" to receive a response from the chatbot.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- This application uses models from Hugging Face's Transformers library for summarization and text generation.
- Special thanks to the developers of Streamlit for creating an excellent framework for building interactive web applications.

