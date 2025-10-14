.PHONY: help autogpt-help autogpt-backend autogpt-frontend autogpt-format autogpt-test autogpt-start autogpt-stop status clean

# Default target
help:
	@echo "==================================="
	@echo "Main Projects Makefile"
	@echo "==================================="
	@echo ""
	@echo "AutoGPT Platform Commands:"
	@echo "  autogpt-help        - Show AutoGPT platform help"
	@echo "  autogpt-start       - Start AutoGPT core services (Supabase, Redis, RabbitMQ)"
	@echo "  autogpt-stop        - Stop AutoGPT core services"
	@echo "  autogpt-logs        - View logs for AutoGPT core services"
	@echo "  autogpt-backend     - Run AutoGPT backend server"
	@echo "  autogpt-frontend    - Run AutoGPT frontend development server"
	@echo "  autogpt-format      - Format and lint AutoGPT code"
	@echo "  autogpt-migrate     - Run AutoGPT database migrations"
	@echo "  autogpt-test-be     - Run AutoGPT backend tests"
	@echo "  autogpt-test-fe     - Run AutoGPT frontend tests"
	@echo ""
	@echo "General Commands:"
	@echo "  status              - Show git status"
	@echo "  clean               - Clean build artifacts"
	@echo ""
	@echo "Note: This Makefile provides shortcuts to AutoGPT platform targets."
	@echo "      For more AutoGPT-specific commands, navigate to AutoGPT/autogpt_platform/"

# AutoGPT Platform targets
autogpt-help:
	@cd AutoGPT/autogpt_platform && make help

autogpt-start:
	@cd AutoGPT/autogpt_platform && make start-core

autogpt-stop:
	@cd AutoGPT/autogpt_platform && make stop-core

autogpt-logs:
	@cd AutoGPT/autogpt_platform && make logs-core

autogpt-backend:
	@cd AutoGPT/autogpt_platform && make run-backend

autogpt-frontend:
	@cd AutoGPT/autogpt_platform && make run-frontend

autogpt-format:
	@cd AutoGPT/autogpt_platform && make format

autogpt-migrate:
	@cd AutoGPT/autogpt_platform && make migrate

autogpt-test-be:
	@cd AutoGPT/autogpt_platform/backend && poetry run test

autogpt-test-fe:
	@cd AutoGPT/autogpt_platform/frontend && pnpm test

# Quick setup for new developers
autogpt-setup:
	@echo "Setting up AutoGPT Platform..."
	@cd AutoGPT/autogpt_platform && make init-env
	@cd AutoGPT/autogpt_platform/backend && poetry install
	@cd AutoGPT/autogpt_platform/frontend && pnpm install
	@echo "✅ Setup complete! Start services with 'make autogpt-start'"

# Git status
status:
	@git status -s

# Cleanup
clean:
	@echo "Cleaning build artifacts..."
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type d -name node_modules -prune -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Cleanup complete!"

