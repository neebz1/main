"""
Data models for Docs-Agent
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum


class DocumentType(Enum):
    """Supported document formats"""
    HTML = "html"
    MARKDOWN = "markdown"
    PDF = "pdf"
    OPENAPI = "openapi"
    PLAINTEXT = "plaintext"
    JSON = "json"
    UNKNOWN = "unknown"


@dataclass
class DocumentSection:
    """A section or chunk of a document"""
    id: str
    document_id: str
    title: str
    content: str
    heading_level: int
    keywords: List[str] = field(default_factory=list)
    embedding: Optional[List[float]] = None
    parent_section_id: Optional[str] = None
    order: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "document_id": self.document_id,
            "title": self.title,
            "content": self.content,
            "heading_level": self.heading_level,
            "keywords": self.keywords,
            "embedding": self.embedding,
            "parent_section_id": self.parent_section_id,
            "order": self.order,
            "metadata": self.metadata,
        }


@dataclass
class Document:
    """A complete document with metadata"""
    id: str
    source_url: str
    title: str
    doc_type: DocumentType
    date_fetched: datetime
    sections: List[DocumentSection] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    raw_content: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "source_url": self.source_url,
            "title": self.title,
            "doc_type": self.doc_type.value,
            "date_fetched": self.date_fetched.isoformat(),
            "sections": [s.to_dict() for s in self.sections],
            "keywords": self.keywords,
            "metadata": self.metadata,
            "raw_content": self.raw_content,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Document":
        """Create Document from dictionary"""
        sections = [
            DocumentSection(**s) for s in data.get("sections", [])
        ]
        return cls(
            id=data["id"],
            source_url=data["source_url"],
            title=data["title"],
            doc_type=DocumentType(data["doc_type"]),
            date_fetched=datetime.fromisoformat(data["date_fetched"]),
            sections=sections,
            keywords=data.get("keywords", []),
            metadata=data.get("metadata", {}),
            raw_content=data.get("raw_content"),
        )


@dataclass
class SearchResult:
    """A search result with relevance score"""
    section: DocumentSection
    document: Document
    score: float
    match_type: str  # "semantic", "keyword", "hybrid"
    excerpt: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "source": self.document.source_url,
            "doc_title": self.document.title,
            "section_title": self.section.title,
            "content": self.section.content,
            "excerpt": self.excerpt,
            "score": self.score,
            "match_type": self.match_type,
            "keywords": self.section.keywords,
            "heading_level": self.section.heading_level,
        }
    
    def format_for_display(self) -> str:
        """Format for terminal display"""
        return f"""
╔══════════════════════════════════════════════════════════════╗
║ Score: {self.score:.3f} | Type: {self.match_type}
╠══════════════════════════════════════════════════════════════╣
║ Source: {self.document.title}
║ Section: {self.section.title}
║ URL: {self.document.source_url}
╠══════════════════════════════════════════════════════════════╣
{self.excerpt or self.section.content[:500]}...
╚══════════════════════════════════════════════════════════════╝
"""


@dataclass
class IndexStats:
    """Statistics about the document index"""
    total_documents: int
    total_sections: int
    total_tokens: int
    document_types: Dict[str, int]
    last_updated: datetime
    embedding_model: str
    index_version: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "total_documents": self.total_documents,
            "total_sections": self.total_sections,
            "total_tokens": self.total_tokens,
            "document_types": self.document_types,
            "last_updated": self.last_updated.isoformat(),
            "embedding_model": self.embedding_model,
            "index_version": self.index_version,
        }

