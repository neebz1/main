"""
Docs-Agent: Semantic Documentation Indexer for Cursor AI

A production-ready system for ingesting, indexing, and semantically searching
documentation to provide authoritative context for AI-assisted coding.

Author: Vibe Coding Team
"""

__version__ = "1.0.0"
__author__ = "Vibe Coding Team"

from .core import DocsAgent
from .ingestion import DocumentIngester
from .search import SemanticSearch
from .models import Document, DocumentSection, SearchResult

__all__ = [
    "DocsAgent",
    "DocumentIngester",
    "SemanticSearch",
    "Document",
    "DocumentSection",
    "SearchResult",
]

