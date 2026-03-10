import streamlit as st
import os
from llm import extract_document_content, generate_document_summary, chat_with_document

# Check if user is logged in
if "login" not in st.session_state:
    st.session_state.login = False



# Page title and description
st.title("📄 Document Chat Assistant")

if not st.session_state.login:
    st.error("Please LogIn First to Use the ChatBot", icon = "🚨")
    st.stop()


# Initialize session state variables
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None
if 'document_text' not in st.session_state:
    st.session_state.document_text = None
if 'document_summary' not in st.session_state:
    st.session_state.document_summary = None
if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = []

def reset_document():
    st.session_state.uploaded_file = None
    st.session_state.document_text = None
    st.session_state.document_summary = None
    st.session_state.chat_messages = []

# File upload section
st.markdown("### 📁 Upload Document")
uploaded_file = st.file_uploader(
    "Choose a document file",
    type=['pdf', 'docx', 'doc', 'txt'],
    help="Supported formats: PDF, DOCX, DOC, TXT"
)

if uploaded_file is not None:
    # Process the uploaded file
    if st.session_state.uploaded_file != uploaded_file.name:
        with st.spinner("📄 Processing document..."):
            # Extract text from document
            document_text = extract_document_content(uploaded_file)
            
            if document_text:
                st.session_state.document_text = document_text
                st.session_state.uploaded_file = uploaded_file.name
                st.session_state.chat_messages = []  # Reset chat history
                
                # Generate summary
                with st.spinner("📝 Generating summary..."):
                    summary = generate_document_summary(document_text)
                    st.session_state.document_summary = summary
                
                st.success("✅ Document processed successfully!")
                st.rerun()
            else:
                st.error("❌ Failed to process the document")

# Show tabs only when document is uploaded
if st.session_state.document_text:
    st.markdown("---")
    st.markdown(f"**Current document:** `{st.session_state.uploaded_file}`")
    
    # Create tabs
    tab1, tab2 = st.tabs(["📋 Summary", "💬 Chat"])
    
    with tab1:
        st.markdown("### Document Summary")
        if st.session_state.document_summary:
            st.markdown(st.session_state.document_summary)
        else:
            st.info("Summary is being generated...")
    
    with tab2:
        st.markdown("### Chat with Document")
        
        # Display chat messages
        chat_container = st.container()
        with chat_container:
            for message in st.session_state.chat_messages:
                with st.chat_message(message["role"], avatar="🤖" if message["role"] == "assistant" else "👤"):
                    st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask about your document...", key="document_chat"):
            # Add user message
            st.session_state.chat_messages.append({"role": "user", "content": prompt})
            
            with st.chat_message("user", avatar="👤"):
                st.markdown(prompt)
            
            # Generate assistant response
            with st.chat_message("assistant", avatar="🤖"):
                with st.spinner("Thinking..."):
                    response_stream = chat_with_document(
                        st.session_state.document_text, 
                        prompt, 
                        st.session_state.chat_messages[:-1]  # Exclude current user message
                    )
                    
                    if response_stream:
                        response = st.write_stream(response_stream)
                        st.session_state.chat_messages.append({"role": "assistant", "content": response})
                    else:
                        st.error("Failed to get response. Please try again.")
            
            st.rerun()
        
        # Clear chat 
        if st.session_state.chat_messages and st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat_messages = []
            st.rerun()



st.markdown("---")

if st.button("📄 Reset", use_container_width=True, on_click=reset_document):
    st.rerun()