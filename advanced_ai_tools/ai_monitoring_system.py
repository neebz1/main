#!/usr/bin/env python3
"""
Advanced AI Monitoring and Observability System
Real-time monitoring, debugging, and performance tracking for AI systems
"""

import time
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json

class MetricType(Enum):
    """Types of metrics"""
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"

class AlertSeverity(Enum):
    """Alert severity levels"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

@dataclass
class Metric:
    """Represents a metric"""
    name: str
    type: MetricType
    value: float
    timestamp: float = field(default_factory=time.time)
    labels: Dict[str, str] = field(default_factory=dict)
    unit: Optional[str] = None

@dataclass
class Alert:
    """Represents an alert"""
    name: str
    severity: AlertSeverity
    message: str
    timestamp: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)
    resolved: bool = False

@dataclass
class Trace:
    """Distributed trace for AI operations"""
    trace_id: str
    span_id: str
    operation: str
    start_time: float
    end_time: Optional[float] = None
    duration_ms: Optional[float] = None
    status: str = "in_progress"
    metadata: Dict[str, Any] = field(default_factory=dict)
    parent_span_id: Optional[str] = None

class MetricsCollector:
    """Collect and aggregate metrics"""
    
    def __init__(self):
        self.metrics: List[Metric] = []
        self.counters: Dict[str, float] = {}
        self.gauges: Dict[str, float] = {}
        self.histograms: Dict[str, List[float]] = {}
    
    def counter(self, name: str, value: float = 1, labels: Optional[Dict[str, str]] = None):
        """Increment a counter"""
        key = self._make_key(name, labels)
        self.counters[key] = self.counters.get(key, 0) + value
        
        metric = Metric(
            name=name,
            type=MetricType.COUNTER,
            value=self.counters[key],
            labels=labels or {},
        )
        self.metrics.append(metric)
    
    def gauge(self, name: str, value: float, labels: Optional[Dict[str, str]] = None):
        """Set a gauge value"""
        key = self._make_key(name, labels)
        self.gauges[key] = value
        
        metric = Metric(
            name=name,
            type=MetricType.GAUGE,
            value=value,
            labels=labels or {},
        )
        self.metrics.append(metric)
    
    def histogram(self, name: str, value: float, labels: Optional[Dict[str, str]] = None):
        """Record a value in histogram"""
        key = self._make_key(name, labels)
        if key not in self.histograms:
            self.histograms[key] = []
        self.histograms[key].append(value)
        
        metric = Metric(
            name=name,
            type=MetricType.HISTOGRAM,
            value=value,
            labels=labels or {},
        )
        self.metrics.append(metric)
    
    def _make_key(self, name: str, labels: Optional[Dict[str, str]]) -> str:
        """Create unique key for metric"""
        if labels:
            label_str = ",".join(f"{k}={v}" for k, v in sorted(labels.items()))
            return f"{name}{{{label_str}}}"
        return name
    
    def get_summary(self) -> Dict[str, Any]:
        """Get metrics summary"""
        return {
            "total_metrics": len(self.metrics),
            "counters": len(self.counters),
            "gauges": len(self.gauges),
            "histograms": len(self.histograms),
            "recent_metrics": self.metrics[-10:],
        }

class AIPerformanceMonitor:
    """Monitor AI model and agent performance"""
    
    def __init__(self):
        self.metrics = MetricsCollector()
        self.traces: List[Trace] = []
        self.alerts: List[Alert] = []
        self.current_traces: Dict[str, Trace] = {}
    
    def track_inference(
        self,
        model_name: str,
        latency_ms: float,
        tokens: int,
        success: bool = True
    ):
        """Track model inference metrics"""
        # Latency
        self.metrics.histogram(
            "model_inference_latency_ms",
            latency_ms,
            labels={"model": model_name}
        )
        
        # Throughput
        tokens_per_second = tokens / (latency_ms / 1000)
        self.metrics.gauge(
            "model_throughput_tokens_per_second",
            tokens_per_second,
            labels={"model": model_name}
        )
        
        # Success rate
        self.metrics.counter(
            "model_inference_total",
            1,
            labels={"model": model_name, "status": "success" if success else "error"}
        )
        
        # Check for performance issues
        if latency_ms > 5000:  # > 5 seconds
            self.create_alert(
                "high_inference_latency",
                AlertSeverity.WARNING,
                f"High latency detected for {model_name}: {latency_ms:.2f}ms",
                metadata={"model": model_name, "latency_ms": latency_ms}
            )
    
    def track_agent_task(
        self,
        agent_name: str,
        task_duration_ms: float,
        success: bool = True,
        subtasks: int = 0
    ):
        """Track agent task metrics"""
        self.metrics.histogram(
            "agent_task_duration_ms",
            task_duration_ms,
            labels={"agent": agent_name}
        )
        
        self.metrics.counter(
            "agent_tasks_total",
            1,
            labels={"agent": agent_name, "status": "success" if success else "error"}
        )
        
        if subtasks > 0:
            self.metrics.gauge(
                "agent_subtasks",
                subtasks,
                labels={"agent": agent_name}
            )
    
    def track_memory_usage(
        self,
        component: str,
        memory_mb: float,
        gpu_memory_mb: Optional[float] = None
    ):
        """Track memory usage"""
        self.metrics.gauge(
            "memory_usage_mb",
            memory_mb,
            labels={"component": component, "type": "ram"}
        )
        
        if gpu_memory_mb is not None:
            self.metrics.gauge(
                "memory_usage_mb",
                gpu_memory_mb,
                labels={"component": component, "type": "gpu"}
            )
            
            # Alert if GPU memory is high
            if gpu_memory_mb > 15000:  # > 15GB
                self.create_alert(
                    "high_gpu_memory",
                    AlertSeverity.WARNING,
                    f"High GPU memory usage: {gpu_memory_mb:.0f}MB",
                    metadata={"component": component, "memory_mb": gpu_memory_mb}
                )
    
    def track_vector_store_operation(
        self,
        operation: str,  # "insert", "search", "update"
        duration_ms: float,
        items: int
    ):
        """Track vector store operations"""
        self.metrics.histogram(
            "vector_store_operation_duration_ms",
            duration_ms,
            labels={"operation": operation}
        )
        
        self.metrics.counter(
            "vector_store_operations_total",
            1,
            labels={"operation": operation}
        )
        
        self.metrics.gauge(
            "vector_store_items",
            items,
            labels={"operation": operation}
        )
    
    def start_trace(
        self,
        trace_id: str,
        operation: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Start a distributed trace"""
        import uuid
        span_id = str(uuid.uuid4())[:8]
        
        trace = Trace(
            trace_id=trace_id,
            span_id=span_id,
            operation=operation,
            start_time=time.time(),
            metadata=metadata or {}
        )
        
        self.current_traces[span_id] = trace
        return span_id
    
    def end_trace(self, span_id: str, status: str = "success", metadata: Optional[Dict[str, Any]] = None):
        """End a trace"""
        if span_id in self.current_traces:
            trace = self.current_traces[span_id]
            trace.end_time = time.time()
            trace.duration_ms = (trace.end_time - trace.start_time) * 1000
            trace.status = status
            
            if metadata:
                trace.metadata.update(metadata)
            
            self.traces.append(trace)
            del self.current_traces[span_id]
            
            # Track trace duration
            self.metrics.histogram(
                "trace_duration_ms",
                trace.duration_ms,
                labels={"operation": trace.operation, "status": status}
            )
    
    def create_alert(
        self,
        name: str,
        severity: AlertSeverity,
        message: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Create an alert"""
        alert = Alert(
            name=name,
            severity=severity,
            message=message,
            metadata=metadata or {}
        )
        self.alerts.append(alert)
        
        print(f"🚨 [{severity.value.upper()}] {message}")
    
    def get_dashboard(self) -> Dict[str, Any]:
        """Get monitoring dashboard data"""
        # Calculate statistics
        recent_metrics = self.metrics.metrics[-100:]
        
        # Inference stats
        inference_metrics = [m for m in recent_metrics if "inference" in m.name]
        avg_latency = (
            sum(m.value for m in inference_metrics if "latency" in m.name) / len(inference_metrics)
            if inference_metrics else 0
        )
        
        # Alert stats
        unresolved_alerts = [a for a in self.alerts if not a.resolved]
        critical_alerts = [a for a in unresolved_alerts if a.severity == AlertSeverity.CRITICAL]
        
        return {
            "timestamp": datetime.now().isoformat(),
            "metrics_summary": self.metrics.get_summary(),
            "performance": {
                "avg_inference_latency_ms": round(avg_latency, 2),
                "total_traces": len(self.traces),
                "active_traces": len(self.current_traces),
            },
            "alerts": {
                "total": len(self.alerts),
                "unresolved": len(unresolved_alerts),
                "critical": len(critical_alerts),
                "recent": [
                    {
                        "name": a.name,
                        "severity": a.severity.value,
                        "message": a.message,
                        "timestamp": datetime.fromtimestamp(a.timestamp).isoformat(),
                    }
                    for a in self.alerts[-5:]
                ],
            },
        }

class AIDebugger:
    """Advanced AI debugging tools"""
    
    def __init__(self):
        self.execution_log: List[Dict[str, Any]] = []
        self.breakpoints: List[str] = []
    
    def log_llm_call(
        self,
        model: str,
        prompt: str,
        response: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Log LLM call for debugging"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "llm_call",
            "model": model,
            "prompt": prompt[:200] + "..." if len(prompt) > 200 else prompt,
            "response": response[:200] + "..." if len(response) > 200 else response,
            "prompt_length": len(prompt),
            "response_length": len(response),
            "metadata": metadata or {},
        }
        self.execution_log.append(entry)
    
    def log_agent_decision(
        self,
        agent: str,
        decision: str,
        reasoning: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Log agent decision for debugging"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "agent_decision",
            "agent": agent,
            "decision": decision,
            "reasoning": reasoning,
            "metadata": metadata or {},
        }
        self.execution_log.append(entry)
    
    def analyze_execution(self) -> Dict[str, Any]:
        """Analyze execution log"""
        llm_calls = [e for e in self.execution_log if e["type"] == "llm_call"]
        agent_decisions = [e for e in self.execution_log if e["type"] == "agent_decision"]
        
        return {
            "total_events": len(self.execution_log),
            "llm_calls": len(llm_calls),
            "agent_decisions": len(agent_decisions),
            "timeline": self.execution_log[-20:],
        }

def demo_monitoring():
    """Demo monitoring system"""
    print("=" * 70)
    print("Advanced AI Monitoring Demo")
    print("=" * 70)
    
    monitor = AIPerformanceMonitor()
    
    # Simulate some metrics
    print("\n📊 Tracking metrics...")
    
    # Model inference
    monitor.track_inference("gpt-4-turbo", 1234.5, 512, success=True)
    monitor.track_inference("codellama-34b", 567.8, 256, success=True)
    monitor.track_inference("gpt-4-turbo", 5678.9, 1024, success=True)  # Slow!
    
    # Agent tasks
    monitor.track_agent_task("Architect", 2345.6, success=True, subtasks=5)
    monitor.track_agent_task("Coder", 3456.7, success=True, subtasks=3)
    
    # Memory usage
    monitor.track_memory_usage("ollama", 4096.0, gpu_memory_mb=8192.0)
    monitor.track_memory_usage("vector_store", 2048.0)
    
    # Vector store operations
    monitor.track_vector_store_operation("search", 45.6, 1000)
    monitor.track_vector_store_operation("insert", 123.4, 100)
    
    # Distributed tracing
    print("\n🔍 Tracing operations...")
    trace_id = "trace-001"
    span1 = monitor.start_trace(trace_id, "process_user_request")
    time.sleep(0.1)
    
    span2 = monitor.start_trace(trace_id, "llm_inference")
    time.sleep(0.05)
    monitor.end_trace(span2, "success")
    
    monitor.end_trace(span1, "success", metadata={"user": "demo_user"})
    
    # Get dashboard
    print("\n📈 Dashboard:")
    dashboard = monitor.get_dashboard()
    print(json.dumps(dashboard, indent=2))
    
    print("\n" + "=" * 70)
    print("✅ Monitoring demo completed!")
    print("=" * 70)

if __name__ == "__main__":
    demo_monitoring()

