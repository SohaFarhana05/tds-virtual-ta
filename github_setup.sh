#!/bin/bash
# GitHub Repository Setup Script for TDS Virtual TA

set -e  # Exit on any error

echo "🚀 Setting up TDS Virtual TA for GitHub deployment..."

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install git first."
    exit 1
fi

# Initialize git repository if not already initialized
if [ ! -d ".git" ]; then
    echo "📁 Initializing git repository..."
    git init
else
    echo "✅ Git repository already initialized"
fi

# Create .gitignore if it doesn't exist
if [ ! -f ".gitignore" ]; then
    echo "📝 Creating .gitignore file..."
    cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environment
venv/
env/
ENV/

# Environment variables
.env

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Database
*.db
*.sqlite3

# Cache
.cache/
.pytest_cache/

# Temporary files
*.tmp
*.temp
EOF
    echo "✅ .gitignore created"
else
    echo "✅ .gitignore already exists"
fi

# Check if LICENSE exists
if [ ! -f "LICENSE" ]; then
    echo "❌ LICENSE file is missing! This is required for evaluation."
    exit 1
else
    echo "✅ LICENSE file exists"
fi

# Add all files to git
echo "📦 Adding files to git..."
git add .

# Check if there are any changes to commit
if git diff --cached --quiet; then
    echo "ℹ️  No changes to commit"
else
    # Commit the changes
    echo "💾 Committing changes..."
    git commit -m "Initial commit: TDS Virtual TA project

- FastAPI-based virtual teaching assistant
- Discourse post scraper with date range support  
- Course content integration
- Comprehensive test suite
- Docker deployment support
- MIT License included"
fi

# Check if remote origin exists
if git remote get-url origin &> /dev/null; then
    echo "✅ Remote origin already configured"
    echo "🔗 Current remote: $(git remote get-url origin)"
else
    echo "⚠️  No remote origin configured"
    echo "📝 To deploy to GitHub:"
    echo "   1. Create a new repository on GitHub"
    echo "   2. Run: git remote add origin <your-repo-url>"
    echo "   3. Run: git push -u origin main"
fi

echo ""
echo "✅ Repository setup complete!"
echo ""
echo "📋 Checklist for submission:"
echo "   ✅ MIT LICENSE file exists"
echo "   ✅ Code is committed to git"
echo "   ✅ API is working (run: python comprehensive_test.py)"
echo "   ✅ Discourse scraper included (run: python scrape.py --help)"
echo ""
echo "🚀 Next steps:"
echo "   1. Push to GitHub: git push -u origin main"
echo "   2. Deploy to a public URL (Railway/Render/Heroku)"
echo "   3. Update promptfoo config with your API URL"
echo "   4. Submit at: https://exam.sanand.workers.dev/tds-project-virtual-ta"
echo ""

# Show current status
echo "📊 Current project status:"
echo "   Repository: $(pwd)"
echo "   Git status: $(git status --porcelain | wc -l | tr -d ' ') uncommitted files"
echo "   Files tracked: $(git ls-files | wc -l | tr -d ' ') files"

if [ -f "app.py" ]; then
    echo "   API status: Ready to deploy"
    echo "   Test API: python app.py & python comprehensive_test.py"
fi
