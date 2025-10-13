#!/bin/bash

# Security Check Script
# Run this to verify security posture

echo "🔒 SECURITY CHECKLIST"
echo "===================="
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track issues
CRITICAL=0
WARNINGS=0
PASSED=0

# Check 1: .env file exists
echo "1. Checking for .env file..."
if [ -f ".env" ]; then
    echo -e "${GREEN}✓${NC} .env file exists"
    ((PASSED++))

    # Check SECRET_KEY
    if grep -q "SECRET_KEY.*your-secret-key" .env 2>/dev/null; then
        echo -e "${RED}✗ CRITICAL: Default SECRET_KEY detected!${NC}"
        echo "  Fix: openssl rand -hex 32"
        ((CRITICAL++))
    else
        echo -e "${GREEN}✓${NC} SECRET_KEY appears to be customized"
        ((PASSED++))
    fi
else
    echo -e "${YELLOW}⚠${NC} .env file not found (copy from .env.example)"
    ((WARNINGS++))
fi

echo ""

# Check 2: .gitignore properly configured
echo "2. Checking .gitignore..."
if grep -q "^\.env" .gitignore 2>/dev/null; then
    echo -e "${GREEN}✓${NC} .env is in .gitignore"
    ((PASSED++))
else
    echo -e "${RED}✗ CRITICAL: .env not in .gitignore!${NC}"
    ((CRITICAL++))
fi

echo ""

# Check 3: Check for hardcoded secrets in code
echo "3. Scanning for hardcoded secrets..."
SECRET_FOUND=0
for pattern in "sk-[a-zA-Z0-9]{32,}" "AIza[a-zA-Z0-9]{35}" "hf_[a-zA-Z0-9]{32,}"; do
    if grep -r -E "$pattern" --include="*.py" --exclude-dir=venv --exclude-dir=env . 2>/dev/null | grep -v "test" | grep -v "example" | head -1 | grep -q .; then
        SECRET_FOUND=1
        break
    fi
done

if [ $SECRET_FOUND -eq 0 ]; then
    echo -e "${GREEN}✓${NC} No obvious API keys found in code"
    ((PASSED++))
else
    echo -e "${RED}✗ CRITICAL: Potential API keys found in code!${NC}"
    ((CRITICAL++))
fi

echo ""

# Check 4: CORS configuration
echo "4. Checking CORS configuration..."
if grep -r "allow_origins.*\[.*\*.*\]" api/ 2>/dev/null | grep -q .; then
    echo -e "${RED}✗ CRITICAL: CORS allows all origins!${NC}"
    echo "  Fix: Set specific origins in ALLOWED_ORIGINS env var"
    ((CRITICAL++))
else
    echo -e "${GREEN}✓${NC} CORS configuration appears safe"
    ((PASSED++))
fi

echo ""

# Check 5: Rate limiting
echo "5. Checking rate limiting..."
if grep -r "slowapi" api/ 2>/dev/null | grep -q .; then
    echo -e "${GREEN}✓${NC} Rate limiting library detected"
    ((PASSED++))
else
    echo -e "${RED}✗ HIGH: Rate limiting not implemented${NC}"
    echo "  Fix: pip install slowapi"
    ((CRITICAL++))
fi

echo ""

# Check 6: HTTPS configuration
echo "6. Checking HTTPS configuration..."
if grep -r "HTTPSRedirectMiddleware" api/ 2>/dev/null | grep -q .; then
    echo -e "${GREEN}✓${NC} HTTPS redirect configured"
    ((PASSED++))
else
    echo -e "${YELLOW}⚠${NC} HTTPS redirect not found (OK for development)"
    ((WARNINGS++))
fi

echo ""

# Check 7: Logging configuration
echo "7. Checking security logging..."
if [ -d "logs" ]; then
    echo -e "${GREEN}✓${NC} Logs directory exists"
    ((PASSED++))
else
    echo -e "${YELLOW}⚠${NC} Logs directory not found"
    ((WARNINGS++))
fi

echo ""

# Check 8: Git hooks (pre-commit for secrets)
echo "8. Checking git hooks..."
if [ -f ".git/hooks/pre-commit" ]; then
    echo -e "${GREEN}✓${NC} Pre-commit hook exists"
    ((PASSED++))
else
    echo -e "${YELLOW}⚠${NC} No pre-commit hook (recommended)"
    ((WARNINGS++))
fi

echo ""

# Check 9: Database security
echo "9. Checking database configuration..."
if grep -r "sqlite" api/database.py 2>/dev/null | grep -q .; then
    echo -e "${YELLOW}⚠${NC} Using SQLite (OK for dev, use PostgreSQL for production)"
    ((WARNINGS++))
else
    echo -e "${GREEN}✓${NC} Using production database"
    ((PASSED++))
fi

echo ""

# Check 10: Dependency vulnerabilities
echo "10. Checking for dependency scanning tools..."
if command -v safety &> /dev/null; then
    echo -e "${GREEN}✓${NC} safety is installed"
    echo "   Running vulnerability scan..."
    safety check --short 2>&1 | head -10
    ((PASSED++))
else
    echo -e "${YELLOW}⚠${NC} safety not installed (pip install safety)"
    ((WARNINGS++))
fi

echo ""
echo "===================="
echo "SUMMARY"
echo "===================="
echo -e "${GREEN}✓ Passed:${NC} $PASSED"
echo -e "${YELLOW}⚠ Warnings:${NC} $WARNINGS"
echo -e "${RED}✗ Critical:${NC} $CRITICAL"
echo ""

if [ $CRITICAL -gt 0 ]; then
    echo -e "${RED}⚠️  FIX CRITICAL ISSUES BEFORE PRODUCTION DEPLOYMENT!${NC}"
    exit 1
elif [ $WARNINGS -gt 0 ]; then
    echo -e "${YELLOW}⚠️  Address warnings for better security${NC}"
    exit 0
else
    echo -e "${GREEN}✅ All security checks passed!${NC}"
    exit 0
fi

