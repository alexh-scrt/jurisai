"""Document processing module.

This module handles loading and processing PDF documents.

Author: a13xh (a13x.h.cc@gmail.com)
"""

import os
import tempfile
from typing import Any, Dict, List, Optional

from langchain_community.document_loaders import PDFPlumberLoader
from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document

from src.jurisai.utils.log_config import get_logger

logger = get_logger(__name__)


class DocumentProcessor:
    """Process and split documents for analysis."""

    def __init__(self, embeddings_model: str = "all-MiniLM-L6-v2"):
        """Initialize the document processor.

        Args:
            embeddings_model: Name of the Hugging Face embeddings model to use
        """
        self.embeddings = HuggingFaceEmbeddings(model_name=embeddings_model)
        self.temp_dir = tempfile.mkdtemp()
        logger.info(
            "Document processor initialized",
            embeddings_model=embeddings_model,
            temp_dir=self.temp_dir,
        )

    def load_pdf(self, pdf_content: bytes, filename: str = "document.pdf") -> List[Document]:
        """Load and parse a PDF from binary content.

        Args:
            pdf_content: Binary content of the PDF file
            filename: Name to use for the temp file

        Returns:
            List of document objects with text content
        """
        # Create a temporary file to save the PDF
        temp_path = os.path.join(self.temp_dir, filename)
        
        with open(temp_path, "wb") as f:
            f.write(pdf_content)
        
        logger.info("PDF saved to temporary file", file_path=temp_path)
        
        # Load PDF using PDFPlumberLoader
        loader = PDFPlumberLoader(temp_path)
        documents = loader.load()
        
        logger.info(
            "PDF loaded successfully", 
            file_path=temp_path, 
            pages=len(documents)
        )
        
        return documents

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """Split documents into semantic chunks.

        Args:
            documents: List of documents to split

        Returns:
            List of document chunks split by semantic meaning
        """
        # Split documents into semantic chunks
        text_splitter = SemanticChunker(self.embeddings)
        chunks = text_splitter.split_documents(documents)
        
        logger.info(
            "Documents split into chunks", 
            original_docs=len(documents),
            chunks=len(chunks)
        )
        
        return chunks

    def create_vector_store(self, documents: List[Document]) -> FAISS:
        """Create a vector store from document chunks.

        Args:
            documents: List of document chunks

        Returns:
            FAISS vector store containing document embeddings
        """
        # Generate embeddings and store in FAISS
        vector_store = FAISS.from_documents(documents, self.embeddings)
        
        logger.info(
            "Vector store created",
            documents=len(documents),
            store_type="FAISS"
        )
        
        return vector_store
        
    def process_pdf(self, pdf_content: bytes, filename: str = "document.pdf") -> FAISS:
        """Process a PDF document and create a vector store.

        This is a convenience method that combines loading, splitting and vectorizing.

        Args:
            pdf_content: Binary content of the PDF file
            filename: Name to use for the temp file

        Returns:
            FAISS vector store ready for queries
        """
        docs = self.load_pdf(pdf_content, filename)
        chunks = self.split_documents(docs)
        vector_store = self.create_vector_store(chunks)
        
        return vector_store

    def cleanup(self) -> None:
        """Remove temporary files."""
        import shutil
        
        try:
            shutil.rmtree(self.temp_dir)
            logger.info("Temporary files cleaned up", temp_dir=self.temp_dir)
        except Exception as e:
            logger.error(
                "Failed to clean up temporary files",
                error=str(e),
                temp_dir=self.temp_dir
            )