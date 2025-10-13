#!/usr/bin/env python3
"""
Tests for DevOps Monitoring System
"""

import os
import json
import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
from devops_monitor import DevOpsMonitor, APIKeyStatus, SystemHealth, MonitoringReport


class TestAPIKeyStatus:
    """Test APIKeyStatus dataclass"""
    
    def test_api_key_status_creation(self):
        status = APIKeyStatus(
            provider="Test Provider",
            key_present=True,
            key_valid=True,
            error_message=None,
            last_checked="2024-01-01T00:00:00"
        )
        assert status.provider == "Test Provider"
        assert status.key_present is True
        assert status.key_valid is True
    
    def test_api_key_status_to_dict(self):
        status = APIKeyStatus(
            provider="Test",
            key_present=True,
            last_checked="2024-01-01"
        )
        result = status.to_dict()
        assert isinstance(result, dict)
        assert result['provider'] == "Test"


class TestSystemHealth:
    """Test SystemHealth dataclass"""
    
    def test_system_health_creation(self):
        health = SystemHealth(
            cpu_percent=50.0,
            memory_percent=60.0,
            disk_percent=70.0,
            timestamp="2024-01-01T00:00:00",
            status="healthy"
        )
        assert health.cpu_percent == 50.0
        assert health.status == "healthy"
    
    def test_system_health_to_dict(self):
        health = SystemHealth(
            cpu_percent=50.0,
            memory_percent=60.0,
            disk_percent=70.0,
            timestamp="2024-01-01",
            status="healthy"
        )
        result = health.to_dict()
        assert isinstance(result, dict)
        assert result['status'] == "healthy"


class TestDevOpsMonitor:
    """Test DevOpsMonitor class"""
    
    @pytest.fixture
    def monitor(self):
        """Create monitor with temp directory"""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield DevOpsMonitor(report_dir=Path(tmpdir))
    
    def test_monitor_initialization(self, monitor):
        """Test monitor initializes correctly"""
        assert monitor.report_dir.exists()
        assert len(monitor.PROVIDERS) > 0
    
    def test_check_api_key_missing(self, monitor):
        """Test checking a missing API key"""
        with patch.dict(os.environ, {}, clear=True):
            status = monitor.check_api_key_status(
                'NONEXISTENT_KEY',
                {'name': 'Test Provider', 'test_endpoint': None}
            )
            assert status.key_present is False
            assert status.error_message is not None
    
    def test_check_api_key_present(self, monitor):
        """Test checking a present API key"""
        with patch.dict(os.environ, {'TEST_KEY': 'test_value'}):
            status = monitor.check_api_key_status(
                'TEST_KEY',
                {'name': 'Test Provider', 'test_endpoint': None}
            )
            assert status.key_present is True
    
    @patch('devops_monitor.psutil.cpu_percent')
    @patch('devops_monitor.psutil.virtual_memory')
    @patch('devops_monitor.psutil.disk_usage')
    def test_check_system_health_healthy(self, mock_disk, mock_mem, mock_cpu, monitor):
        """Test system health check - healthy"""
        mock_cpu.return_value = 50.0
        mock_mem.return_value = MagicMock(percent=60.0)
        mock_disk.return_value = MagicMock(percent=70.0)
        
        health = monitor.check_system_health()
        assert health.status == "healthy"
        assert health.cpu_percent == 50.0
    
    @patch('devops_monitor.psutil.cpu_percent')
    @patch('devops_monitor.psutil.virtual_memory')
    @patch('devops_monitor.psutil.disk_usage')
    def test_check_system_health_warning(self, mock_disk, mock_mem, mock_cpu, monitor):
        """Test system health check - warning"""
        mock_cpu.return_value = 85.0
        mock_mem.return_value = MagicMock(percent=60.0)
        mock_disk.return_value = MagicMock(percent=70.0)
        
        health = monitor.check_system_health()
        assert health.status == "warning"
    
    @patch('devops_monitor.psutil.cpu_percent')
    @patch('devops_monitor.psutil.virtual_memory')
    @patch('devops_monitor.psutil.disk_usage')
    def test_check_system_health_critical(self, mock_disk, mock_mem, mock_cpu, monitor):
        """Test system health check - critical"""
        mock_cpu.return_value = 95.0
        mock_mem.return_value = MagicMock(percent=60.0)
        mock_disk.return_value = MagicMock(percent=70.0)
        
        health = monitor.check_system_health()
        assert health.status == "critical"
    
    def test_identify_issues_no_api_keys(self, monitor):
        """Test issue identification with no API keys"""
        api_statuses = [
            {'provider': 'Test1', 'key_present': False, 'key_valid': None},
            {'provider': 'Test2', 'key_present': False, 'key_valid': None}
        ]
        health = SystemHealth(
            cpu_percent=50.0,
            memory_percent=60.0,
            disk_percent=70.0,
            timestamp="2024-01-01",
            status="healthy"
        )
        
        issues = monitor._identify_issues(api_statuses, health)
        assert any("No API keys configured" in issue for issue in issues)
    
    def test_identify_issues_invalid_key(self, monitor):
        """Test issue identification with invalid key"""
        api_statuses = [
            {'provider': 'Test1', 'key_present': True, 'key_valid': False}
        ]
        health = SystemHealth(
            cpu_percent=50.0,
            memory_percent=60.0,
            disk_percent=70.0,
            timestamp="2024-01-01",
            status="healthy"
        )
        
        issues = monitor._identify_issues(api_statuses, health)
        assert any("invalid" in issue.lower() for issue in issues)
    
    def test_generate_recommendations(self, monitor):
        """Test recommendation generation"""
        issues = ["No API keys configured"]
        api_statuses = [
            {'provider': 'Test1', 'key_present': False, 'key_valid': None}
        ]
        health = SystemHealth(
            cpu_percent=50.0,
            memory_percent=60.0,
            disk_percent=70.0,
            timestamp="2024-01-01",
            status="healthy"
        )
        
        recommendations = monitor._generate_recommendations(issues, api_statuses, health)
        assert len(recommendations) > 0
    
    def test_save_report(self, monitor):
        """Test report saving"""
        report = MonitoringReport(
            timestamp="2024-01-01T00:00:00",
            api_keys=[],
            system_health={},
            issues_found=[],
            recommendations=[]
        )
        
        monitor._save_report(report)
        
        # Check that latest report was created
        latest_file = monitor.report_dir / "latest_report.json"
        assert latest_file.exists()
        
        # Verify content
        with open(latest_file) as f:
            data = json.load(f)
            assert data['timestamp'] == "2024-01-01T00:00:00"
    
    def test_generate_status_badge_no_report(self, monitor):
        """Test badge generation with no report"""
        badge = monitor.generate_status_badge()
        assert "unknown" in badge
    
    def test_generate_status_badge_healthy(self, monitor):
        """Test badge generation with healthy status"""
        report = MonitoringReport(
            timestamp="2024-01-01",
            api_keys=[],
            system_health={'status': 'healthy'},
            issues_found=[],
            recommendations=[]
        )
        monitor._save_report(report)
        
        badge = monitor.generate_status_badge()
        assert "healthy" in badge
    
    @patch.dict(os.environ, {'TOGETHER_API_KEY': 'test_key'})
    def test_get_provider_fallback_order(self, monitor):
        """Test getting provider fallback order"""
        providers = monitor.get_provider_fallback_order()
        assert isinstance(providers, list)


class TestAPIKeyValidation:
    """Test API key validation"""
    
    @pytest.fixture
    def monitor(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            yield DevOpsMonitor(report_dir=Path(tmpdir))
    
    @patch('devops_monitor.requests.get')
    def test_validate_openai_key_success(self, mock_get, monitor):
        """Test OpenAI key validation - success"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        valid, message = monitor._validate_api_key(
            'OPENAI_API_KEY',
            'sk-test',
            'https://api.openai.com/v1/models'
        )
        assert valid is True
    
    @patch('devops_monitor.requests.get')
    def test_validate_api_key_unauthorized(self, mock_get, monitor):
        """Test API key validation - unauthorized"""
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_get.return_value = mock_response
        
        valid, message = monitor._validate_api_key(
            'OPENAI_API_KEY',
            'sk-invalid',
            'https://api.openai.com/v1/models'
        )
        assert valid is False
        assert "401" in message
    
    @patch('devops_monitor.requests.get')
    def test_validate_api_key_timeout(self, mock_get, monitor):
        """Test API key validation - timeout"""
        mock_get.side_effect = Exception("Timeout")
        
        valid, message = monitor._validate_api_key(
            'OPENAI_API_KEY',
            'sk-test',
            'https://api.openai.com/v1/models'
        )
        assert valid is None
        assert message is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
