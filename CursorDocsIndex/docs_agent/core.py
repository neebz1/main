"""
Core Docs-Agent orchestrator
"""

import json
import sqlite3
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from .models import Document, SearchResult, IndexStats
from .ingestion import DocumentIngester
from .search import SemanticSearch

console = Console()


class DocsAgent:
    """
    Main orchestrator for documentation indexing and search
    """
    
    def __init__(self, index_dir: Path, embedding_provider: str = "openrouter"):
        """
        Initialize Docs-Agent
        
        Args:
            index_dir: Directory to store index and cache
            embedding_provider: "openrouter", "openai", or "local"
        """
        self.index_dir = Path(index_dir)
        self.index_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        self.parsed_dir = self.index_dir / "parsed"
        self.parsed_dir.mkdir(exist_ok=True)
        
        self.cache_dir = self.index_dir / "cache"
        self.cache_dir.mkdir(exist_ok=True)
        
        # Initialize components
        self.ingester = DocumentIngester(self.cache_dir)
        self.search_engine = SemanticSearch(self.index_dir, embedding_provider)
        
        # Metadata database
        self.db_path = self.index_dir / "metadata.db"
        self._init_database()
    
    def _init_database(self):
        """Initialize SQLite metadata database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id TEXT PRIMARY KEY,
                source_url TEXT NOT NULL,
                title TEXT,
                doc_type TEXT,
                date_fetched TEXT,
                num_sections INTEGER,
                keywords TEXT,
                metadata TEXT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sections (
                id TEXT PRIMARY KEY,
                document_id TEXT,
                title TEXT,
                content TEXT,
                heading_level INTEGER,
                keywords TEXT,
                order_num INTEGER,
                FOREIGN KEY (document_id) REFERENCES documents(id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS index_metadata (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)
        
        conn.commit()
        conn.close()
    
    def ingest_sources(self, sources: List[str], show_progress: bool = True) -> List[Document]:
        """
        Ingest multiple documentation sources
        
        Args:
            sources: List of URLs or file paths
            show_progress: Show progress bar
            
        Returns:
            List of ingested documents
        """
        documents = []
        
        if show_progress:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                task = progress.add_task("[cyan]Ingesting documents...", total=len(sources))
                
                for source in sources:
                    progress.update(task, description=f"[cyan]Ingesting: {source}")
                    try:
                        doc = self.ingester.ingest(source)
                        self._save_document(doc)
                        self.search_engine.index_document(doc)
                        documents.append(doc)
                        console.print(f"✅ Ingested: {doc.title}", style="green")
                    except Exception as e:
                        console.print(f"❌ Failed: {source} - {e}", style="red")
                    progress.advance(task)
        else:
            for source in sources:
                try:
                    doc = self.ingester.ingest(source)
                    self._save_document(doc)
                    self.search_engine.index_document(doc)
                    documents.append(doc)
                except Exception as e:
                    console.print(f"❌ Failed: {source} - {e}", style="red")
        
        return documents
    
    def _save_document(self, doc: Document):
        """Save document to database and filesystem"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Save document metadata
        cursor.execute("""
            INSERT OR REPLACE INTO documents 
            (id, source_url, title, doc_type, date_fetched, num_sections, keywords, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            doc.id,
            doc.source_url,
            doc.title,
            doc.doc_type.value,
            doc.date_fetched.isoformat(),
            len(doc.sections),
            json.dumps(doc.keywords),
            json.dumps(doc.metadata),
        ))
        
        # Save sections
        for section in doc.sections:
            cursor.execute("""
                INSERT OR REPLACE INTO sections
                (id, document_id, title, content, heading_level, keywords, order_num)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                section.id,
                doc.id,
                section.title,
                section.content,
                section.heading_level,
                json.dumps(section.keywords),
                section.order,
            ))
        
        conn.commit()
        conn.close()
        
        # Save full document as JSON
        doc_file = self.parsed_dir / f"{doc.id}.json"
        with open(doc_file, 'w') as f:
            json.dump(doc.to_dict(), f, indent=2)
    
    def search(self, query: str, top_k: int = 5, method: str = "hybrid") -> List[SearchResult]:
        """
        Search the document index
        
        Args:
            query: Search query
            top_k: Number of results to return
            method: "semantic", "keyword", or "hybrid"
            
        Returns:
            List of search results
        """
        return self.search_engine.search(query, top_k, method)
    
    def lookup(self, query: str) -> Dict[str, Any]:
        """
        Simplified lookup interface for AI integration
        
        Args:
            query: Search query
            
        Returns:
            Dict with source, excerpt, score
        """
        results = self.search(query, top_k=3, method="hybrid")
        
        if not results:
            return {
                "found": False,
                "message": "No relevant documentation found"
            }
        
        best_result = results[0]
        
        return {
            "found": True,
            "source": best_result.document.source_url,
            "doc_title": best_result.document.title,
            "section_title": best_result.section.title,
            "excerpt": best_result.section.content[:500] + "..." if len(best_result.section.content) > 500 else best_result.section.content,
            "score": best_result.score,
            "keywords": best_result.section.keywords,
            "all_results": [r.to_dict() for r in results]
        }
    
    def get_stats(self) -> IndexStats:
        """Get index statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM documents")
        total_docs = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM sections")
        total_sections = cursor.fetchone()[0]
        
        cursor.execute("SELECT doc_type, COUNT(*) FROM documents GROUP BY doc_type")
        doc_types = dict(cursor.fetchall())
        
        conn.close()
        
        return IndexStats(
            total_documents=total_docs,
            total_sections=total_sections,
            total_tokens=0,  # TODO: Calculate
            document_types=doc_types,
            last_updated=datetime.now(),
            embedding_model=self.search_engine.embedding_provider,
            index_version="1.0.0",
        )

