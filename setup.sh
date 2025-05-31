#!/bin/bash

# TDS Virtual TA Setup and Run Script

echo "🚀 TDS Virtual TA Setup Script"
echo "================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip."
    exit 1
fi

echo "✅ Python and pip found"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️ Creating .env file..."
    cp .env.example .env
    echo "📝 Please edit .env file with your API keys before running the application"
fi

# Create data directory if it doesn't exist
mkdir -p data

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API keys"
echo "2. Run: source venv/bin/activate"
echo "3. Run: python app.py"
echo ""
echo "Optional: Run scrapers to collect fresh data:"
echo "- python scraper/discourse_scraper.py"
echo "- python scraper/course_scraper.py"
echo ""
echo "To test the API:"
echo "- Update project-tds-virtual-ta-promptfoo.yaml with your API URL"
echo "- Run: npx -y promptfoo eval --config project-tds-virtual-ta-promptfoo.yaml"
