#!/usr/bin/env python3
"""
Advanced Code Intelligence System
AI-powered semantic code search, analysis, and understanding
"""

import ast
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
import json

class CodeLanguage(Enum):
    """Supported programming languages"""
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    RUST = "rust"
    GO = "go"
    JAVA = "java"
    CPP = "cpp"
    C = "c"

@dataclass
class CodeSymbol:
    """Represents a code symbol (function, class, variable)"""
    name: str
    type: str  # function, class, variable, method
    language: CodeLanguage
    file_path: str
    line_number: int
    docstring: Optional[str] = None
    parameters: List[str] = None
    return_type: Optional[str] = None
    complexity: int = 0
    embedding: Optional[List[float]] = None
    
    def __post_init__(self):
        if self.parameters is None:
            self.parameters = []

@dataclass
class CodePattern:
    """Represents a code pattern or anti-pattern"""
    name: str
    description: str
    severity: str  # info, warning, error
    suggestion: str
    examples: List[str]

class CodeAnalyzer:
    """Advanced code analysis with AI"""
    
    def __init__(self):
        self.symbols: Dict[str, List[CodeSymbol]] = {}
        self.embeddings_model = None
    
    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze a single file"""
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Determine language
        language = self._detect_language(path)
        
        # Parse file
        with open(path, 'r') as f:
            content = f.read()
        
        # Extract symbols
        symbols = self._extract_symbols(content, language, str(path))
        
        # Calculate metrics
        metrics = self._calculate_metrics(content, symbols)
        
        # Detect patterns
        patterns = self._detect_patterns(content, language)
        
        return {
            "file": str(path),
            "language": language.value,
            "symbols": [self._symbol_to_dict(s) for s in symbols],
            "metrics": metrics,
            "patterns": patterns,
        }
    
    def analyze_directory(self, directory: str, recursive: bool = True) -> Dict[str, Any]:
        """Analyze entire directory"""
        dir_path = Path(directory)
        
        if not dir_path.is_dir():
            raise NotADirectoryError(f"Not a directory: {directory}")
        
        all_files = []
        if recursive:
            for ext in ['.py', '.js', '.ts', '.rs', '.go', '.java']:
                all_files.extend(dir_path.rglob(f'*{ext}'))
        else:
            for ext in ['.py', '.js', '.ts', '.rs', '.go', '.java']:
                all_files.extend(dir_path.glob(f'*{ext}'))
        
        results = []
        for file_path in all_files:
            try:
                result = self.analyze_file(str(file_path))
                results.append(result)
            except Exception as e:
                print(f"⚠️  Error analyzing {file_path}: {e}")
        
        # Aggregate metrics
        aggregate = self._aggregate_metrics(results)
        
        return {
            "directory": str(dir_path),
            "total_files": len(results),
            "files": results,
            "aggregate_metrics": aggregate,
        }
    
    def _detect_language(self, path: Path) -> CodeLanguage:
        """Detect programming language from file extension"""
        ext = path.suffix.lower()
        mapping = {
            '.py': CodeLanguage.PYTHON,
            '.js': CodeLanguage.JAVASCRIPT,
            '.ts': CodeLanguage.TYPESCRIPT,
            '.rs': CodeLanguage.RUST,
            '.go': CodeLanguage.GO,
            '.java': CodeLanguage.JAVA,
            '.cpp': CodeLanguage.CPP,
            '.c': CodeLanguage.C,
        }
        return mapping.get(ext, CodeLanguage.PYTHON)
    
    def _extract_symbols(
        self,
        content: str,
        language: CodeLanguage,
        file_path: str
    ) -> List[CodeSymbol]:
        """Extract code symbols (functions, classes, etc.)"""
        symbols = []
        
        if language == CodeLanguage.PYTHON:
            symbols = self._extract_python_symbols(content, file_path)
        # Would support other languages
        
        return symbols
    
    def _extract_python_symbols(self, content: str, file_path: str) -> List[CodeSymbol]:
        """Extract symbols from Python code"""
        symbols = []
        
        try:
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    symbol = CodeSymbol(
                        name=node.name,
                        type="function",
                        language=CodeLanguage.PYTHON,
                        file_path=file_path,
                        line_number=node.lineno,
                        docstring=ast.get_docstring(node),
                        parameters=[arg.arg for arg in node.args.args],
                        complexity=self._calculate_complexity(node),
                    )
                    symbols.append(symbol)
                
                elif isinstance(node, ast.ClassDef):
                    symbol = CodeSymbol(
                        name=node.name,
                        type="class",
                        language=CodeLanguage.PYTHON,
                        file_path=file_path,
                        line_number=node.lineno,
                        docstring=ast.get_docstring(node),
                    )
                    symbols.append(symbol)
        
        except SyntaxError as e:
            print(f"⚠️  Syntax error in {file_path}: {e}")
        
        return symbols
    
    def _calculate_complexity(self, node: ast.AST) -> int:
        """Calculate cyclomatic complexity"""
        complexity = 1
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        
        return complexity
    
    def _calculate_metrics(self, content: str, symbols: List[CodeSymbol]) -> Dict[str, Any]:
        """Calculate code metrics"""
        lines = content.split('\n')
        
        # Count different line types
        code_lines = 0
        comment_lines = 0
        blank_lines = 0
        
        for line in lines:
            stripped = line.strip()
            if not stripped:
                blank_lines += 1
            elif stripped.startswith('#'):
                comment_lines += 1
            else:
                code_lines += 1
        
        # Calculate complexity metrics
        avg_complexity = (
            sum(s.complexity for s in symbols if s.complexity > 0) / len(symbols)
            if symbols else 0
        )
        
        max_complexity = max((s.complexity for s in symbols), default=0)
        
        return {
            "total_lines": len(lines),
            "code_lines": code_lines,
            "comment_lines": comment_lines,
            "blank_lines": blank_lines,
            "total_symbols": len(symbols),
            "functions": sum(1 for s in symbols if s.type == "function"),
            "classes": sum(1 for s in symbols if s.type == "class"),
            "avg_complexity": round(avg_complexity, 2),
            "max_complexity": max_complexity,
            "comment_ratio": round(comment_lines / len(lines), 3) if lines else 0,
        }
    
    def _detect_patterns(self, content: str, language: CodeLanguage) -> List[Dict[str, Any]]:
        """Detect code patterns and anti-patterns"""
        patterns = []
        
        # Common anti-patterns
        if "TODO" in content or "FIXME" in content:
            patterns.append({
                "type": "todo_comment",
                "severity": "info",
                "message": "Contains TODO/FIXME comments",
            })
        
        # Check for very long functions (simplified)
        if language == CodeLanguage.PYTHON:
            try:
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        func_lines = node.end_lineno - node.lineno if hasattr(node, 'end_lineno') else 0
                        if func_lines > 50:
                            patterns.append({
                                "type": "long_function",
                                "severity": "warning",
                                "message": f"Function '{node.name}' is very long ({func_lines} lines)",
                                "line": node.lineno,
                            })
            except:
                pass
        
        return patterns
    
    def _aggregate_metrics(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Aggregate metrics across multiple files"""
        total_lines = sum(r["metrics"]["total_lines"] for r in results)
        total_code_lines = sum(r["metrics"]["code_lines"] for r in results)
        total_symbols = sum(r["metrics"]["total_symbols"] for r in results)
        
        return {
            "total_files": len(results),
            "total_lines": total_lines,
            "total_code_lines": total_code_lines,
            "total_symbols": total_symbols,
            "avg_file_size": round(total_lines / len(results)) if results else 0,
        }
    
    def _symbol_to_dict(self, symbol: CodeSymbol) -> Dict[str, Any]:
        """Convert symbol to dictionary"""
        return {
            "name": symbol.name,
            "type": symbol.type,
            "file": symbol.file_path,
            "line": symbol.line_number,
            "docstring": symbol.docstring,
            "parameters": symbol.parameters,
            "complexity": symbol.complexity,
        }

class SemanticCodeSearch:
    """Semantic code search using embeddings"""
    
    def __init__(self):
        self.index = {}
        self.embeddings = {}
    
    def index_codebase(self, directory: str):
        """Index entire codebase for semantic search"""
        print(f"🔍 Indexing codebase: {directory}")
        
        analyzer = CodeAnalyzer()
        results = analyzer.analyze_directory(directory)
        
        # Extract all symbols
        all_symbols = []
        for file_result in results["files"]:
            all_symbols.extend(file_result["symbols"])
        
        print(f"✅ Indexed {len(all_symbols)} symbols from {results['total_files']} files")
        
        self.index = {"symbols": all_symbols, "directory": directory}
    
    def search(self, query: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """Semantic search for code"""
        print(f"🔍 Searching for: '{query}'")
        
        # Would use actual embedding similarity
        # For now, simple keyword matching
        results = []
        for symbol in self.index.get("symbols", []):
            if query.lower() in symbol["name"].lower():
                results.append(symbol)
        
        return results[:top_k]
    
    def find_similar_code(self, code_snippet: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Find similar code in codebase"""
        print(f"🔍 Finding code similar to snippet...")
        
        # Would use actual embedding similarity
        return []

class AICodeReviewer:
    """AI-powered code reviewer"""
    
    def review_code(self, file_path: str) -> Dict[str, Any]:
        """Review code and provide suggestions"""
        print(f"👁️  Reviewing: {file_path}")
        
        analyzer = CodeAnalyzer()
        analysis = analyzer.analyze_file(file_path)
        
        suggestions = []
        
        # Check complexity
        for symbol in analysis["symbols"]:
            if symbol["complexity"] > 10:
                suggestions.append({
                    "type": "complexity",
                    "severity": "warning",
                    "symbol": symbol["name"],
                    "line": symbol["line"],
                    "message": f"High complexity ({symbol['complexity']}). Consider refactoring.",
                })
        
        # Check documentation
        for symbol in analysis["symbols"]:
            if not symbol["docstring"] and symbol["type"] in ["function", "class"]:
                suggestions.append({
                    "type": "documentation",
                    "severity": "info",
                    "symbol": symbol["name"],
                    "line": symbol["line"],
                    "message": "Missing docstring. Add documentation.",
                })
        
        return {
            "file": file_path,
            "analysis": analysis,
            "suggestions": suggestions,
            "overall_score": self._calculate_score(analysis, suggestions),
        }
    
    def _calculate_score(self, analysis: Dict[str, Any], suggestions: List[Dict[str, Any]]) -> str:
        """Calculate overall code quality score"""
        issues = len(suggestions)
        
        if issues == 0:
            return "A+"
        elif issues <= 2:
            return "A"
        elif issues <= 5:
            return "B"
        elif issues <= 10:
            return "C"
        else:
            return "D"

def demo_code_intelligence():
    """Demo advanced code intelligence"""
    print("=" * 70)
    print("Advanced Code Intelligence Demo")
    print("=" * 70)
    
    # Analyze current file
    current_file = __file__
    
    print("\n📊 Analyzing current file...")
    analyzer = CodeAnalyzer()
    result = analyzer.analyze_file(current_file)
    
    print(f"\nFile: {result['file']}")
    print(f"Language: {result['language']}")
    print(f"Symbols found: {result['metrics']['total_symbols']}")
    print(f"  Functions: {result['metrics']['functions']}")
    print(f"  Classes: {result['metrics']['classes']}")
    print(f"Lines of code: {result['metrics']['code_lines']}")
    print(f"Average complexity: {result['metrics']['avg_complexity']}")
    
    print("\n🔍 Top symbols:")
    for symbol in result['symbols'][:5]:
        print(f"  - {symbol['type']}: {symbol['name']} (line {symbol['line']})")
    
    # Code review
    print("\n👁️  AI Code Review...")
    reviewer = AICodeReviewer()
    review = reviewer.review_code(current_file)
    
    print(f"Overall Score: {review['overall_score']}")
    print(f"Suggestions: {len(review['suggestions'])}")
    
    for suggestion in review['suggestions'][:3]:
        print(f"  [{suggestion['severity'].upper()}] {suggestion['message']}")
    
    print("\n" + "=" * 70)
    print("✅ Code intelligence demo completed!")
    print("=" * 70)

if __name__ == "__main__":
    demo_code_intelligence()

