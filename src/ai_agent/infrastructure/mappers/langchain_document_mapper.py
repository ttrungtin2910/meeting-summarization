"""
langchain_document_mapper

Provides utility functions to convert between internal domain document representation
(`RetrievalDocument`) and external LangChain's `Document` class.
"""

from typing import List

from langchain.schema import Document as LangChainDocument

from ai_agent.domain.value_objects.retrieval_document import RetrievalDocument


def convert_to_langchain_document(doc: RetrievalDocument) -> LangChainDocument:
    """
    Convert a RetrievalDocument to a LangChain Document.

    Args:
        doc (RetrievalDocument): The internal document format.

    Returns:
        LangChainDocument: The equivalent LangChain document.
    """
    return LangChainDocument(page_content=doc.page_content, metadata=doc.metadata)


def convert_from_langchain_document(doc: LangChainDocument) -> RetrievalDocument:
    """
    Convert a LangChain Document to a RetrievalDocument.

    Args:
        doc (LangChainDocument): The LangChain document.

    Returns:
        RetrievalDocument: The internal document format.
    """
    return RetrievalDocument(page_content=doc.page_content, metadata=doc.metadata)


def convert_to_langchain_documents(docs: List[RetrievalDocument]) -> List[LangChainDocument]:
    """
    Convert a list of RetrievalDocuments to LangChain Documents.

    Args:
        docs (List[RetrievalDocument]): A list of internal documents.

    Returns:
        List[LangChainDocument]: A list of LangChain-compatible documents.
    """
    return [convert_to_langchain_document(doc) for doc in docs]


def convert_from_langchain_documents(docs: List[LangChainDocument]) -> List[RetrievalDocument]:
    """
    Convert a list of LangChain Documents to RetrievalDocuments.

    Args:
        docs (List[LangChainDocument]): A list of LangChain documents.

    Returns:
        List[RetrievalDocument]: A list of internal document objects.
    """
    return [convert_from_langchain_document(doc) for doc in docs]
