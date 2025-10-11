#!/usr/bin/env python3
"""
Docs-Agent API Server
FastAPI-based REST API for cloud deployment
"""

import os
from pathlib import Path
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from contextlib import asynccontextmanager

from docs_agent import DocsAgent

# Import API monitor (check if available)
try:
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from api_monitor import APIMonitor
    API_MONITOR_AVAILABLE = True
except ImportError:
    API_MONITOR_AVAILABLE = False

# Configuration
INDEX_DIR = Path(os.getenv("INDEX_DIR", "./index"))
API_KEY = os.getenv("DOCS_API_KEY", "")  # Set this in production!
PORT = int(os.getenv("PORT", 8000))


# Initialize DocsAgent and API Monitor on startup
docs_agent = None
api_monitor = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize on startup, cleanup on shutdown"""
    global docs_agent, api_monitor
    print("🚀 Initializing Docs-Agent...")
    docs_agent = DocsAgent(INDEX_DIR, embedding_provider="openrouter")
    print("✅ Docs-Agent ready!")
    
    if API_MONITOR_AVAILABLE:
        print("🔍 Initializing API Monitor...")
        api_monitor = APIMonitor()
        print("✅ API Monitor ready!")
    
    yield
    print("👋 Shutting down Docs-Agent...")


# FastAPI app
app = FastAPI(
    title="📚 Docs-Agent API",
    description="Semantic documentation search API - Stop hallucinating, start referencing!",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS middleware (allow requests from anywhere)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production: specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response models
class IngestRequest(BaseModel):
    sources: List[str]
    show_progress: bool = False

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5
    method: str = "hybrid"

class LookupRequest(BaseModel):
    query: str


# Authentication dependency (optional)
async def verify_api_key(x_api_key: Optional[str] = Header(None)):
    """Verify API key if configured"""
    if API_KEY and x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return True


# Health check
@app.get("/")
async def root():
    """Health check and API info"""
    return {
        "status": "operational",
        "service": "Docs-Agent API",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "search": "/search",
            "lookup": "/lookup",
            "stats": "/stats",
            "ingest": "/ingest (POST)",
            "api_monitor": "/api/monitor",
            "api_status": "/api/status",
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    stats = docs_agent.get_stats()
    return {
        "status": "healthy",
        "total_documents": stats.total_documents,
        "total_sections": stats.total_sections,
        "last_updated": stats.last_updated.isoformat(),
    }


@app.get("/search")
async def search(
    q: str = Query(..., description="Search query"),
    top_k: int = Query(5, ge=1, le=50, description="Number of results"),
    method: str = Query("hybrid", description="Search method: keyword, semantic, or hybrid"),
):
    """
    Search the documentation index
    
    Returns top_k most relevant document sections
    """
    try:
        results = docs_agent.search(q, top_k, method)
        return {
            "query": q,
            "total_results": len(results),
            "results": [r.to_dict() for r in results]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/lookup")
async def lookup(
    q: str = Query(..., description="Lookup query"),
):
    """
    Quick lookup - Returns best matching documentation
    
    Optimized for AI integration
    """
    try:
        result = docs_agent.lookup(q)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ingest")
async def ingest(
    request: IngestRequest,
    authenticated: bool = Depends(verify_api_key)
):
    """
    Ingest new documentation sources
    
    Requires API key authentication
    """
    try:
        docs = docs_agent.ingest_sources(
            request.sources, 
            show_progress=request.show_progress
        )
        return {
            "status": "success",
            "ingested": len(docs),
            "documents": [
                {
                    "id": doc.id,
                    "title": doc.title,
                    "source": doc.source_url,
                    "sections": len(doc.sections),
                }
                for doc in docs
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats")
async def stats():
    """Get index statistics"""
    try:
        stats = docs_agent.get_stats()
        return stats.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/documents")
async def list_documents():
    """List all indexed documents"""
    import sqlite3
    
    try:
        conn = sqlite3.connect(docs_agent.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, source_url, title, doc_type, date_fetched, num_sections
            FROM documents
            ORDER BY date_fetched DESC
        """)
        
        documents = []
        for row in cursor.fetchall():
            documents.append({
                "id": row[0],
                "source_url": row[1],
                "title": row[2],
                "doc_type": row[3],
                "date_fetched": row[4],
                "num_sections": row[5],
            })
        
        conn.close()
        
        return {
            "total": len(documents),
            "documents": documents
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/monitor")
async def api_monitor_status():
    """
    Get API integration monitoring status
    
    Returns health status, response times, and usage metrics for all API providers
    """
    if not API_MONITOR_AVAILABLE:
        raise HTTPException(
            status_code=503, 
            detail="API monitoring not available. Install required dependencies: httpx"
        )
    
    if not api_monitor:
        raise HTTPException(status_code=500, detail="API monitor not initialized")
    
    try:
        # Check all providers
        await api_monitor.check_all_providers()
        
        # Generate report
        report = api_monitor.get_status_report()
        
        # Add alerts
        report["alerts"] = api_monitor.alert_on_failures()
        
        # Add optimization suggestions
        report["optimization_suggestions"] = api_monitor.get_cost_optimization_suggestions()
        
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/status")
async def api_quick_status():
    """
    Quick API status check (lightweight)
    
    Returns summary of API health without detailed metrics
    """
    if not API_MONITOR_AVAILABLE:
        return {
            "monitoring_available": False,
            "message": "API monitoring not available"
        }
    
    if not api_monitor:
        return {
            "monitoring_available": False,
            "message": "API monitor not initialized"
        }
    
    try:
        healthy = api_monitor.get_healthy_providers()
        
        return {
            "monitoring_available": True,
            "healthy_providers": healthy,
            "provider_count": len(api_monitor.metrics),
            "timestamp": api_monitor.metrics[list(api_monitor.metrics.keys())[0]].last_check if api_monitor.metrics else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Run server
if __name__ == "__main__":
    import uvicorn
    
    print("╔═══════════════════════════════════════════════════════════════╗")
    print("║          📚 Docs-Agent API Server Starting 📚                 ║")
    print("╚═══════════════════════════════════════════════════════════════╝")
    print(f"")
    print(f"🌐 Server: http://localhost:{PORT}")
    print(f"📖 Docs: http://localhost:{PORT}/docs")
    print(f"📊 Stats: http://localhost:{PORT}/stats")
    print(f"")
    if API_KEY:
        print(f"🔐 Authentication: ENABLED (X-API-Key header required for /ingest)")
    else:
        print(f"⚠️  Authentication: DISABLED (set DOCS_API_KEY env var)")
    print(f"")
    
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=PORT,
        reload=True,
        log_level="info"
    )

