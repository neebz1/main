# Copilot Coding Agent Instructions

## Purpose
This repository is a multi-agent AI development environment with:
- Music production tools (Logic Pro Copilot, AI Mixing Engineer)
- Code development agents (Cline, Cursor AI, GitHub Copilot)
- Documentation indexing (Docs-Agent)
- Super Agent orchestration system for coordinating multiple agents

## Setup
1. Install Python dependencies: `pip install -r requirements.txt`
2. Install super agent: `pip install -r super_agent/requirements.txt`
3. Configure API keys in `.env` (Kimi K2, OpenRouter, Gemini, etc.)
4. Launch super agent: `./start-super-agent.sh`

## Repository Structure
- `super_agent/` - Multi-agent orchestration system
- `CursorDocsIndex/` - Documentation indexing agent
- `logic_copilot_lite.py` - Music production AI (port 7860)
- `ai_mixing_engineer.py` - Audio analysis AI (port 7861)
- `live_ai_assistant.py` - Real-time voice/vision assistant
- `logic_ai_plugin.py` - Logic Pro integration
- Documentation in markdown files

## Coding Conventions
- Python: Follow PEP 8
- Use type hints for function parameters and returns
- Add docstrings for all public functions and classes
- Keep functions focused and small
- Use async/await for I/O operations

## Multi-Agent Coordination
- Use `super_agent/` system to coordinate multiple agents
- Check `super_agent/context.py` for shared state
- Avoid file conflicts by using context.lock_file()
- Share knowledge between agents via context.share_knowledge()
- Route tasks automatically with super_agent router

## Copilot Usage
- This is a multi-agent AI system - agents should work together
- When making changes, consider impact on other agents
- Use super agent for complex tasks requiring multiple agents
- Test agent coordination to ensure no conflicts
- Document any new agents or capabilities added
