"""Streamlit web interface for JurisAI.

This module provides a web-based user interface for the JurisAI application
using Streamlit.

Author: a13xh (a13x.h.cc@gmail.com)
"""

import streamlit as st
from langchain_community.vectorstores import FAISS

from src.jurisai.models.document_processor import DocumentProcessor
from src.jurisai.models.rag_chain import RAGChain
from src.jurisai.utils.log_config import get_logger, configure_logging

# Configure logging
configure_logging(level="INFO")
logger = get_logger(__name__)


def initialize_session_state():
    """Initialize session state variables."""
    if "processor" not in st.session_state:
        st.session_state.processor = DocumentProcessor()
    
    if "rag_chain" not in st.session_state:
        st.session_state.rag_chain = RAGChain()
    
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = None
    
    if "qa_chain" not in st.session_state:
        st.session_state.qa_chain = None
    
    if "uploaded_file_name" not in st.session_state:
        st.session_state.uploaded_file_name = None


def main():
    """Run the Streamlit application."""
    st.set_page_config(
        page_title="JurisAI - Legal Document Assistant",
        page_icon="⚖️",
        layout="wide",
    )
    
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.title("JurisAI - Legal Document Assistant")
    st.markdown(
        "Upload a legal document and ask questions to receive concise answers based on the content."
    )
    
    # Sidebar
    with st.sidebar:
        st.header("Settings")
        
        # Model selection
        model_name = st.selectbox(
            "Select LLM Model",
            ["deepseek-r1:1.5b", "llama2:7b", "orca-mini:7b", "mistral:7b", "gemma:7b"],
            index=0,
        )
        
        # Update RAG chain if model changed
        if "current_model" not in st.session_state or st.session_state.current_model != model_name:
            st.session_state.rag_chain = RAGChain(model_name=model_name)
            st.session_state.current_model = model_name
            if st.session_state.vector_store is not None:
                st.session_state.qa_chain = st.session_state.rag_chain.create_chain(
                    st.session_state.vector_store
                )
        
        # Temperature for generation
        temperature = st.slider(
            "Temperature", min_value=0.0, max_value=1.0, value=0.1, step=0.1
        )
        
        # Number of retrieved chunks
        k_value = st.slider(
            "Number of chunks to retrieve", min_value=1, max_value=10, value=3, step=1
        )
        
        st.markdown("---")
        st.markdown("### About")
        st.markdown(
            "JurisAI uses LLMs with retrieval augmented generation to analyze legal documents."
        )
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("Document Upload")
        
        # PDF file uploader
        uploaded_file = st.file_uploader("Upload a legal document", type="pdf")
        
        if uploaded_file is not None:
            if (st.session_state.uploaded_file_name != uploaded_file.name or 
                st.session_state.vector_store is None):
                # Process new document
                with st.spinner("Processing document..."):
                    try:
                        # Process the PDF and create vector store
                        st.session_state.vector_store = st.session_state.processor.process_pdf(
                            uploaded_file.getvalue(),
                            filename=uploaded_file.name
                        )
                        
                        # Create QA chain
                        st.session_state.qa_chain = st.session_state.rag_chain.create_chain(
                            st.session_state.vector_store,
                            k=k_value
                        )
                        
                        # Update session state
                        st.session_state.uploaded_file_name = uploaded_file.name
                        
                        st.success(f"Document '{uploaded_file.name}' processed successfully!")
                    except Exception as e:
                        st.error(f"Error processing document: {str(e)}")
                        logger.error(
                            "Error processing document",
                            error=str(e),
                            filename=uploaded_file.name
                        )
        
        # Document status
        if st.session_state.vector_store is not None:
            st.info(f"Active document: {st.session_state.uploaded_file_name}")
        else:
            st.warning("Please upload a document to begin.")
    
    with col2:
        st.header("Ask Questions")
        
        # Question input
        user_question = st.text_input("What would you like to know about the document?")
        
        # Submit button
        if st.button("Ask"):
            if user_question and st.session_state.qa_chain is not None:
                with st.spinner("Generating answer..."):
                    try:
                        # Get answer from RAG chain
                        answer = st.session_state.rag_chain.answer_question(
                            st.session_state.qa_chain, 
                            user_question
                        )
                        
                        # Display answer
                        st.markdown("### Answer")
                        st.markdown(answer)
                    except Exception as e:
                        st.error(f"Error generating answer: {str(e)}")
                        logger.error(
                            "Error generating answer",
                            error=str(e),
                            question=user_question
                        )
            elif user_question:
                st.error("Please upload a document first.")
            else:
                st.error("Please enter a question.")
        
        # Example questions
        with st.expander("Example Questions"):
            st.markdown("""
            Try asking questions like:
            - What are the key terms of this agreement?
            - Who are the parties involved in this contract?
            - What are the termination conditions?
            - What liabilities are mentioned in the document?
            """)


if __name__ == "__main__":
    main()