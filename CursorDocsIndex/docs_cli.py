#!/usr/bin/env python3
"""
Docs-Agent CLI - Command-line interface for documentation indexing and search

Usage:
    ./docs_cli.py ingest <url_or_file> [<url_or_file>...]
    ./docs_cli.py search <query>
    ./docs_cli.py lookup <query>
    ./docs_cli.py stats
    ./docs_cli.py init
"""

import sys
import os
from pathlib import Path
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown

# Add parent dir to path
sys.path.insert(0, str(Path(__file__).parent))

from docs_agent import DocsAgent

app = typer.Typer(help="📚 Docs-Agent CLI - Semantic Documentation Search")
console = Console()

# Default index directory
INDEX_DIR = Path.home() / "CursorDocsIndex"


def get_agent() -> DocsAgent:
    """Get or create DocsAgent instance"""
    if not INDEX_DIR.exists():
        console.print(f"❌ Index not initialized. Run: docs_cli.py init", style="red")
        raise typer.Exit(1)
    
    return DocsAgent(INDEX_DIR)


@app.command()
def init():
    """Initialize the documentation index"""
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    agent = DocsAgent(INDEX_DIR)
    
    console.print(Panel.fit(
        f"[green]✅ Documentation index initialized![/green]\n\n"
        f"📁 Location: {INDEX_DIR}\n"
        f"🔧 Embedding provider: {agent.search.embedding_provider}\n"
        f"📊 Ready to ingest documentation!",
        title="🎉 Docs-Agent Initialized",
        border_style="green"
    ))


@app.command()
def ingest(sources: list[str]):
    """Ingest documentation from URLs or files"""
    if not sources:
        console.print("❌ No sources provided", style="red")
        raise typer.Exit(1)
    
    agent = get_agent()
    
    console.print(f"\n📥 Ingesting {len(sources)} source(s)...\n", style="cyan bold")
    
    docs = agent.ingest_sources(sources, show_progress=True)
    
    console.print(f"\n✅ Successfully ingested {len(docs)} document(s)!", style="green bold")


@app.command()
def search(query: str, top_k: int = 5):
    """Search the documentation index"""
    agent = get_agent()
    
    console.print(f"\n🔍 Searching for: [cyan]{query}[/cyan]\n")
    
    results = agent.search(query, top_k=top_k)
    
    if not results:
        console.print("❌ No results found", style="red")
        return
    
    console.print(f"Found {len(results)} result(s):\n", style="green")
    
    for i, result in enumerate(results, 1):
        console.print(Panel(
            f"[bold]{result.section.title}[/bold]\n\n"
            f"{result.excerpt}\n\n"
            f"[dim]Source: {result.document.title}[/dim]\n"
            f"[dim]URL: {result.document.source_url}[/dim]\n"
            f"[dim]Score: {result.score:.2f} | Type: {result.match_type}[/dim]",
            title=f"Result {i}",
            border_style="blue"
        ))


@app.command()
def lookup(query: str):
    """Quick lookup (optimized for AI integration)"""
    agent = get_agent()
    
    result = agent.lookup(query)
    
    if not result['found']:
        console.print(f"❌ {result['message']}", style="red")
        return
    
    console.print(Panel.fit(
        f"[bold cyan]{result['doc_title']}[/bold cyan]\n"
        f"[bold]{result['section_title']}[/bold]\n\n"
        f"{result['excerpt']}\n\n"
        f"[dim]Source: {result['source']}[/dim]\n"
        f"[dim]Score: {result['score']:.2f}[/dim]\n"
        f"[dim]Keywords: {', '.join(result['keywords'][:5])}[/dim]",
        title="📖 Documentation Lookup",
        border_style="green"
    ))


@app.command()
def stats():
    """Show index statistics"""
    agent = get_agent()
    
    stats = agent.get_stats()
    
    table = Table(title="📊 Index Statistics", show_header=True)
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Total Documents", str(stats.total_documents))
    table.add_row("Total Sections", str(stats.total_sections))
    table.add_row("Embedding Model", stats.embedding_model)
    table.add_row("Index Version", stats.index_version)
    table.add_row("Last Updated", stats.last_updated.strftime("%Y-%m-%d %H:%M"))
    
    console.print(table)
    
    if stats.document_types:
        console.print("\n📄 Document Types:", style="bold")
        for doc_type, count in stats.document_types.items():
            console.print(f"  • {doc_type}: {count}")


@app.command()
def demo():
    """Run a demo with sample documentation"""
    console.print(Panel.fit(
        "[bold cyan]🎨 Docs-Agent Demo[/bold cyan]\n\n"
        "This will ingest sample documentation and run test searches.\n\n"
        "Sample sources:\n"
        "• Python requests library docs\n"
        "• FastAPI documentation\n"
        "• React documentation",
        border_style="cyan"
    ))
    
    if not typer.confirm("Continue with demo?"):
        return
    
    agent = get_agent() if INDEX_DIR.exists() else DocsAgent(INDEX_DIR)
    
    # Sample sources
    sample_sources = [
        "https://docs.python-requests.org/en/latest/",
        "https://fastapi.tiangolo.com/",
        "https://react.dev/learn",
    ]
    
    console.print("\n📥 Ingesting sample documentation...\n", style="cyan")
    docs = agent.ingest_sources(sample_sources[:1], show_progress=True)  # Start with just one
    
    console.print("\n✅ Demo complete! Try searching:", style="green")
    console.print("  docs_cli.py search 'HTTP requests'")
    console.print("  docs_cli.py lookup 'authentication'")


if __name__ == "__main__":
    # Check for vibe-coding environment
    if os.getenv("VIBE_CONFIG"):
        console.print("[dim]🎨 Running in vibe-coding environment[/dim]\n")
    
    app()

