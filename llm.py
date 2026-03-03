import os
import streamlit as st
from openai import OpenAI
from prompts import SUMMARY_PROMPT, CHAT_WITH_PDF_PROMPT
from config import OPENAI_CHAT_MODEL
import PyPDF2
import docx
from io import BytesIO


def get_openai_client():
    return OpenAI(api_key=st.secrets["llm"]["OPENAI_API_KEY"])

def extract_text_from_pdf(uploaded_file):
    """Extract text from PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")
        return None

def extract_text_from_docx(uploaded_file):
    """Extract text from DOCX file"""
    try:
        doc = docx.Document(uploaded_file)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        st.error(f"Error reading DOCX: {str(e)}")
        return None

def extract_text_from_txt(uploaded_file):
    """Extract text from TXT file"""
    try:
        return uploaded_file.read().decode('utf-8')
    except Exception as e:
        st.error(f"Error reading TXT: {str(e)}")
        return None

def extract_document_content(uploaded_file):
    """Extract text content from various document types"""
    file_extension = uploaded_file.name.lower().split('.')[-1]
    
    # Reset file pointer
    uploaded_file.seek(0)
    
    if file_extension == 'pdf':
        return extract_text_from_pdf(uploaded_file)
    elif file_extension in ['docx', 'doc']:
        return extract_text_from_docx(uploaded_file)
    elif file_extension == 'txt':
        return extract_text_from_txt(uploaded_file)
    else:
        st.error(f"Unsupported file type: {file_extension}")
        return None

def generate_document_summary(document_text):
    """Generate a summary of the document using OpenAI"""
    client = get_openai_client()
    
    try:
        response = client.chat.completions.create(
            model=OPENAI_CHAT_MODEL,
            messages=[
                {"role": "system", "content": SUMMARY_PROMPT},
                {"role": "user", "content": f"Please summarize this document:\n\n{document_text}"}
            ],
            max_tokens=1000,
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error generating summary: {str(e)}")
        return None

def chat_with_document(document_text, user_question, chat_history=None):
    """Chat with the document content"""
    client = get_openai_client()
    
    if chat_history is None:
        chat_history = []
    
    try:
        messages = [
            {"role": "system", "content": CHAT_WITH_PDF_PROMPT},
            {"role": "user", "content": f"Document content:\n\n{document_text}"}
        ]
        
        # Add chat history
        for msg in chat_history:
            messages.append(msg)
        
        # Add current question
        messages.append({"role": "user", "content": user_question})
        
        response = client.chat.completions.create(
            model=OPENAI_CHAT_MODEL,
            messages=messages,
            max_tokens=1000,
            temperature=0.7,
            stream=True
        )
        return response
    except Exception as e:
        st.error(f"Error in chat: {str(e)}")
        return None