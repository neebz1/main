"""
Semantic search module with hybrid search capabilities
"""

import os
import json
import sqlite3
from pathlib import Path
from typing import List, Optional, Dict, Any
from collections import defaultdict
import re

from .models import Document, DocumentSection, SearchResult


class SemanticSearch:
    """
    Hybrid semantic + keyword search engine
    """
    
    def __init__(self, index_dir: Path, embedding_provider: str = "openrouter"):
        self.index_dir = Path(index_dir)
        self.embedding_provider = embedding_provider
        self.db_path = self.index_dir / "metadata.db"
        
        # Check if embeddings are available
        self.embeddings_available = False
        if embedding_provider == "openrouter":
            self.embeddings_available = bool(os.getenv("OPENROUTER_API_KEY"))
        elif embedding_provider == "openai":
            self.embeddings_available = bool(os.getenv("OPENAI_API_KEY"))
        
        if not self.embeddings_available:
            print("⚠️  No API keys found - using keyword search only")
    
    def index_document(self, doc: Document):
        """Index a document for search"""
        # Currently just stores in DB via DocsAgent
        # TODO: Add vector indexing when embeddings are available
        pass
    
    def search(self, query: str, top_k: int = 5, method: str = "hybrid") -> List[SearchResult]:
        """
        Search the document index
        
        Args:
            query: Search query
            top_k: Number of results
            method: "semantic", "keyword", or "hybrid"
            
        Returns:
            List of SearchResults sorted by relevance
        """
        # For now, use keyword search
        # TODO: Add semantic search when embeddings are ready
        
        if method == "semantic" and not self.embeddings_available:
            method = "keyword"
        
        if method in ["keyword", "hybrid"]:
            return self._keyword_search(query, top_k)
        else:
            # Semantic search placeholder
            return self._keyword_search(query, top_k)
    
    def _keyword_search(self, query: str, top_k: int) -> List[SearchResult]:
        """
        Keyword-based search using TF-IDF-like scoring
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Extract query terms
        query_terms = set(re.findall(r'\b\w{3,}\b', query.lower()))
        
        # Get all sections
        cursor.execute("""
            SELECT 
                s.id, s.document_id, s.title, s.content, 
                s.heading_level, s.keywords, s.order_num,
                d.source_url, d.title as doc_title, d.doc_type
            FROM sections s
            JOIN documents d ON s.document_id = d.id
        """)
        
        results = []
        
        for row in cursor.fetchall():
            section_id, doc_id, title, content, heading_level, keywords_json, order_num, source_url, doc_title, doc_type = row
            
            # Parse keywords
            try:
                keywords = json.loads(keywords_json)
            except:
                keywords = []
            
            # Calculate relevance score
            score = 0.0
            
            # Title match (highest weight)
            title_lower = title.lower()
            for term in query_terms:
                if term in title_lower:
                    score += 5.0
            
            # Keyword match
            keywords_lower = [k.lower() for k in keywords]
            for term in query_terms:
                if term in keywords_lower:
                    score += 3.0
            
            # Content match
            content_lower = content.lower()
            for term in query_terms:
                # Count occurrences with diminishing returns
                count = content_lower.count(term)
                if count > 0:
                    score += min(count * 0.5, 2.0)  # Cap at 2.0 per term
            
            # Exact phrase bonus
            if query.lower() in content_lower:
                score += 10.0
            
            if score > 0:
                # Create section and document objects
                section = DocumentSection(
                    id=section_id,
                    document_id=doc_id,
                    title=title,
                    content=content,
                    heading_level=heading_level,
                    keywords=keywords,
                    order=order_num,
                )
                
                # Get full document (simplified)
                document = Document(
                    id=doc_id,
                    source_url=source_url,
                    title=doc_title,
                    doc_type=doc_type,  # String, will need conversion if used
                    date_fetched=None,  # Not loaded for search results
                    sections=[],  # Don't load all sections
                )
                
                # Create excerpt with highlighted terms
                excerpt = self._create_excerpt(content, query_terms)
                
                result = SearchResult(
                    section=section,
                    document=document,
                    score=score,
                    match_type="keyword",
                    excerpt=excerpt,
                )
                results.append(result)
        
        conn.close()
        
        # Sort by score and return top_k
        results.sort(key=lambda r: r.score, reverse=True)
        return results[:top_k]
    
    def _create_excerpt(self, content: str, query_terms: set, context_chars: int = 200) -> str:
        """
        Create an excerpt showing query terms in context
        """
        content_lower = content.lower()
        
        # Find first occurrence of any query term
        best_pos = len(content)
        for term in query_terms:
            pos = content_lower.find(term)
            if pos != -1 and pos < best_pos:
                best_pos = pos
        
        if best_pos == len(content):
            # No matches, return start
            return content[:context_chars] + "..."
        
        # Get context around match
        start = max(0, best_pos - context_chars // 2)
        end = min(len(content), best_pos + context_chars // 2)
        
        excerpt = content[start:end]
        
        # Add ellipsis
        if start > 0:
            excerpt = "..." + excerpt
        if end < len(content):
            excerpt = excerpt + "..."
        
        return excerpt
    
    def _semantic_search(self, query: str, top_k: int) -> List[SearchResult]:
        """
        Semantic search using embeddings (placeholder for future)
        """
        # TODO: Implement when embeddings are ready
        return self._keyword_search(query, top_k)

