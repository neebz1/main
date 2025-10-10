"""
Document ingestion and parsing module
"""

import hashlib
import re
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import markdown
from collections import Counter

from .models import Document, DocumentSection, DocumentType


class DocumentIngester:
    """Handles fetching and parsing documents from various sources"""
    
    def __init__(self, cache_dir: Path):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'DocsAgent/1.0 (Cursor AI Documentation Indexer)'
        })
    
    def ingest(self, source: str, doc_type: Optional[DocumentType] = None) -> Document:
        """
        Ingest a document from URL or file path
        
        Args:
            source: URL or file path
            doc_type: Optional explicit document type
            
        Returns:
            Parsed Document object
        """
        # Detect if source is URL or local path
        is_url = source.startswith(('http://', 'https://'))
        
        if is_url:
            content = self._fetch_url(source)
        else:
            content = self._read_file(source)
        
        # Detect document type if not provided
        if doc_type is None:
            doc_type = self._detect_type(source, content)
        
        # Parse based on type
        if doc_type == DocumentType.HTML:
            return self._parse_html(source, content)
        elif doc_type == DocumentType.MARKDOWN:
            return self._parse_markdown(source, content)
        elif doc_type == DocumentType.OPENAPI:
            return self._parse_openapi(source, content)
        elif doc_type == DocumentType.JSON:
            return self._parse_json(source, content)
        else:
            return self._parse_plaintext(source, content)
    
    def _fetch_url(self, url: str) -> str:
        """Fetch content from URL"""
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        return response.text
    
    def _read_file(self, path: str) -> str:
        """Read content from local file"""
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _detect_type(self, source: str, content: str) -> DocumentType:
        """Detect document type from source and content"""
        lower_source = source.lower()
        
        # Check file extension
        if lower_source.endswith('.md'):
            return DocumentType.MARKDOWN
        elif lower_source.endswith('.html') or lower_source.endswith('.htm'):
            return DocumentType.HTML
        elif lower_source.endswith('.pdf'):
            return DocumentType.PDF
        elif lower_source.endswith(('.json', '.yaml', '.yml')):
            if 'openapi' in content.lower() or 'swagger' in content.lower():
                return DocumentType.OPENAPI
            return DocumentType.JSON
        
        # Check content
        if content.strip().startswith('<'):
            return DocumentType.HTML
        elif content.strip().startswith('{') or content.strip().startswith('['):
            return DocumentType.JSON
        elif re.match(r'^#+\s', content):
            return DocumentType.MARKDOWN
        
        return DocumentType.PLAINTEXT
    
    def _generate_id(self, source: str) -> str:
        """Generate unique ID for document"""
        return hashlib.md5(source.encode()).hexdigest()
    
    def _extract_keywords(self, text: str, top_n: int = 20) -> List[str]:
        """Extract keywords using simple frequency analysis"""
        # Remove common words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 
                     'to', 'for', 'of', 'with', 'by', 'from', 'is', 'are', 'was',
                     'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do',
                     'does', 'did', 'will', 'would', 'could', 'should', 'may',
                     'might', 'must', 'can', 'this', 'that', 'these', 'those'}
        
        # Extract words
        words = re.findall(r'\b[a-z]{3,}\b', text.lower())
        words = [w for w in words if w not in stop_words]
        
        # Count frequency
        counter = Counter(words)
        return [word for word, _ in counter.most_common(top_n)]
    
    def _parse_html(self, source: str, content: str) -> Document:
        """Parse HTML document"""
        soup = BeautifulSoup(content, 'lxml')
        
        # Extract title
        title_tag = soup.find('title')
        title = title_tag.text if title_tag else urlparse(source).path.split('/')[-1]
        
        # Remove script and style tags
        for tag in soup(['script', 'style', 'nav', 'footer', 'header']):
            tag.decompose()
        
        doc_id = self._generate_id(source)
        sections = []
        section_order = 0
        
        # Find all headings and their content
        for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            level = int(heading.name[1])
            heading_text = heading.get_text(strip=True)
            
            # Get content until next heading
            content_parts = []
            for sibling in heading.find_next_siblings():
                if sibling.name and sibling.name.startswith('h'):
                    break
                text = sibling.get_text(strip=True)
                if text:
                    content_parts.append(text)
            
            section_content = '\n\n'.join(content_parts)
            
            if section_content or heading_text:
                section_id = f"{doc_id}_{section_order}"
                keywords = self._extract_keywords(heading_text + " " + section_content, 10)
                
                section = DocumentSection(
                    id=section_id,
                    document_id=doc_id,
                    title=heading_text,
                    content=section_content,
                    heading_level=level,
                    keywords=keywords,
                    order=section_order,
                )
                sections.append(section)
                section_order += 1
        
        # If no sections found, use whole body
        if not sections:
            body = soup.find('body')
            if body:
                content_text = body.get_text(separator='\n\n', strip=True)
                sections.append(DocumentSection(
                    id=f"{doc_id}_0",
                    document_id=doc_id,
                    title=title,
                    content=content_text,
                    heading_level=1,
                    keywords=self._extract_keywords(content_text, 20),
                    order=0,
                ))
        
        # Extract overall keywords
        all_text = ' '.join([s.content for s in sections])
        doc_keywords = self._extract_keywords(all_text, 30)
        
        return Document(
            id=doc_id,
            source_url=source,
            title=title,
            doc_type=DocumentType.HTML,
            date_fetched=datetime.now(),
            sections=sections,
            keywords=doc_keywords,
            raw_content=content,
            metadata={'num_sections': len(sections)},
        )
    
    def _parse_markdown(self, source: str, content: str) -> Document:
        """Parse Markdown document"""
        # Convert to HTML first for easier parsing
        html_content = markdown.markdown(content, extensions=['extra', 'toc'])
        
        # Use HTML parser
        doc = self._parse_html(source, html_content)
        doc.doc_type = DocumentType.MARKDOWN
        
        # Extract title from first heading or filename
        lines = content.split('\n')
        title = None
        for line in lines:
            if line.startswith('# '):
                title = line[2:].strip()
                break
        
        if not title:
            title = Path(source).stem.replace('-', ' ').replace('_', ' ').title()
        
        doc.title = title
        return doc
    
    def _parse_openapi(self, source: str, content: str) -> Document:
        """Parse OpenAPI/Swagger specification"""
        import json
        import yaml
        
        # Try JSON first, then YAML
        try:
            spec = json.loads(content)
        except json.JSONDecodeError:
            spec = yaml.safe_load(content)
        
        doc_id = self._generate_id(source)
        title = spec.get('info', {}).get('title', 'API Documentation')
        sections = []
        section_order = 0
        
        # Parse paths
        paths = spec.get('paths', {})
        for path, methods in paths.items():
            for method, details in methods.items():
                if not isinstance(details, dict):
                    continue
                
                section_title = f"{method.upper()} {path}"
                section_content = f"**Summary:** {details.get('summary', 'N/A')}\n\n"
                section_content += f"**Description:** {details.get('description', 'N/A')}\n\n"
                
                # Parameters
                if 'parameters' in details:
                    section_content += "**Parameters:**\n"
                    for param in details['parameters']:
                        section_content += f"- {param.get('name')} ({param.get('in')}): {param.get('description', '')}\n"
                    section_content += "\n"
                
                # Responses
                if 'responses' in details:
                    section_content += "**Responses:**\n"
                    for code, response in details['responses'].items():
                        desc = response.get('description', 'N/A')
                        section_content += f"- {code}: {desc}\n"
                
                section_id = f"{doc_id}_{section_order}"
                keywords = self._extract_keywords(section_title + " " + section_content, 10)
                keywords.extend([method.upper(), path.split('/')[1] if '/' in path else path])
                
                sections.append(DocumentSection(
                    id=section_id,
                    document_id=doc_id,
                    title=section_title,
                    content=section_content,
                    heading_level=2,
                    keywords=list(set(keywords)),
                    order=section_order,
                    metadata={'method': method, 'path': path},
                ))
                section_order += 1
        
        return Document(
            id=doc_id,
            source_url=source,
            title=title,
            doc_type=DocumentType.OPENAPI,
            date_fetched=datetime.now(),
            sections=sections,
            keywords=list(set([k for s in sections for k in s.keywords])),
            raw_content=content,
            metadata={'version': spec.get('info', {}).get('version', 'unknown')},
        )
    
    def _parse_json(self, source: str, content: str) -> Document:
        """Parse generic JSON document"""
        import json
        
        data = json.loads(content)
        doc_id = self._generate_id(source)
        title = Path(source).stem if not source.startswith('http') else urlparse(source).path.split('/')[-1]
        
        # Create a single section with formatted JSON
        formatted = json.dumps(data, indent=2)
        
        section = DocumentSection(
            id=f"{doc_id}_0",
            document_id=doc_id,
            title=title,
            content=formatted,
            heading_level=1,
            keywords=self._extract_keywords(formatted, 20),
            order=0,
        )
        
        return Document(
            id=doc_id,
            source_url=source,
            title=title,
            doc_type=DocumentType.JSON,
            date_fetched=datetime.now(),
            sections=[section],
            keywords=section.keywords,
            raw_content=content,
        )
    
    def _parse_plaintext(self, source: str, content: str) -> Document:
        """Parse plain text document"""
        doc_id = self._generate_id(source)
        title = Path(source).stem if not source.startswith('http') else urlparse(source).path.split('/')[-1]
        
        # Split by paragraphs
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        sections = []
        
        for i, para in enumerate(paragraphs):
            section = DocumentSection(
                id=f"{doc_id}_{i}",
                document_id=doc_id,
                title=f"Section {i+1}",
                content=para,
                heading_level=2,
                keywords=self._extract_keywords(para, 10),
                order=i,
            )
            sections.append(section)
        
        return Document(
            id=doc_id,
            source_url=source,
            title=title,
            doc_type=DocumentType.PLAINTEXT,
            date_fetched=datetime.now(),
            sections=sections,
            keywords=self._extract_keywords(content, 30),
            raw_content=content,
        )

