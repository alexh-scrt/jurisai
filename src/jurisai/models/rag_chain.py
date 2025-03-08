"""RAG (Retrieval Augmented Generation) module.

This module handles the creation of the RAG pipeline for answering questions.

Author: a13xh (a13x.h.cc@gmail.com)
"""

from typing import Any, Dict, List, Optional

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, RetrievalQA, StuffDocumentsChain
from langchain_community.llms import Ollama
from langchain_community.vectorstores import FAISS

from src.jurisai.utils.log_config import get_logger

logger = get_logger(__name__)


class RAGChain:
    """Retrieval Augmented Generation chain for question answering."""
    
    def __init__(
        self, 
        model_name: str = "deepseek-r1:1.5b",
        prompt_template: Optional[str] = None,
        temperature: float = 0.1,
    ):
        """Initialize the RAG chain.
        
        Args:
            model_name: Name of the Ollama model to use
            prompt_template: Custom prompt template to use (or None for default)
            temperature: Temperature for LLM generation
        """
        # Initialize Ollama LLM
        self.llm = Ollama(model=model_name, temperature=temperature)
        
        # Set up the prompt template
        if prompt_template is None:
            prompt_template = """
1. Use ONLY the context below.
2. If unsure, say "I don't know".
3. Keep answers under 4 sentences.
4. Base all answers on the legal documents provided.

Context: {context}

Question: {question}

Answer:
"""
        self.qa_prompt = PromptTemplate.from_template(prompt_template)
        
        # Document formatting prompt
        self.document_prompt = PromptTemplate(
            template="Context:\ncontent: {page_content}\nsource: {source}",
            input_variables=["page_content", "source"]
        )
        
        logger.info(
            "RAG chain initialized", 
            model=model_name, 
            temperature=temperature
        )
        
    def create_chain(self, vector_store: FAISS, k: int = 3) -> RetrievalQA:
        """Create a retrieval QA chain.
        
        Args:
            vector_store: FAISS vector store containing document embeddings
            k: Number of similar documents to retrieve
            
        Returns:
            RetrievalQA chain ready for answering questions
        """
        # Set up retriever
        retriever = vector_store.as_retriever(search_kwargs={"k": k})
        
        # Chain 1: Generate answers
        llm_chain = LLMChain(llm=self.llm, prompt=self.qa_prompt)
        
        # Final RAG pipeline
        qa = RetrievalQA(
            combine_documents_chain=StuffDocumentsChain(
                llm_chain=llm_chain,
                document_prompt=self.document_prompt
            ),
            retriever=retriever
        )
        
        logger.info("QA chain created", retriever_k=k)
        
        return qa
    
    def answer_question(self, qa_chain: RetrievalQA, question: str) -> str:
        """Answer a question using the RAG chain.
        
        Args:
            qa_chain: The RetrievalQA chain to use
            question: Question to answer
            
        Returns:
            Answer to the question
        """
        logger.info("Processing question", question=question)
        
        try:
            result = qa_chain(question)
            answer = result["result"]
            
            logger.info(
                "Question answered", 
                question=question, 
                answer_length=len(answer)
            )
            
            return answer
        except Exception as e:
            logger.error(
                "Error answering question", 
                question=question, 
                error=str(e)
            )
            return "I encountered an error while trying to answer your question."