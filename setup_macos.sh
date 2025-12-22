#!/bin/bash
# 🍎 Automatic Setup Script for macOS
# This script will set up your Football Statistics project automatically

echo ""
echo "========================================"
echo "⚽ Football Statistics - macOS Setup"
echo "========================================"
echo ""

# Check if Python 3 is installed
echo "🔍 Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    echo "📦 Please install Python 3 using Homebrew:"
    echo "   brew install python3"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "✅ Found: $PYTHON_VERSION"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists"
    read -p "Do you want to recreate it? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🗑️  Removing old virtual environment..."
        rm -rf venv
        python3 -m venv venv
        echo "✅ New virtual environment created"
    fi
else
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi
echo ""

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip --quiet
echo "✅ Pip upgraded"
echo ""

# Install requirements
echo "📥 Installing dependencies..."
echo "   (This may take 2-3 minutes)"
echo ""
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ All dependencies installed successfully!"
else
    echo ""
    echo "❌ Error installing dependencies"
    echo "💡 Try running manually:"
    echo "   source venv/bin/activate"
    echo "   pip install -r requirements.txt"
    exit 1
fi
echo ""

# Verify installation
echo "🔍 Verifying installation..."
python -c "import pandas, numpy, sklearn, flask, plotly, streamlit" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✅ All packages verified!"
else
    echo "⚠️  Some packages may not have installed correctly"
fi
echo ""

echo "========================================"
echo "✅ Setup Complete!"
echo "========================================"
echo ""
echo "📝 Next steps:"
echo ""
echo "1️⃣  Train the model:"
echo "   python train_model.py"
echo ""
echo "2️⃣  Run the website:"
echo "   python run_website.py"
echo ""
echo "3️⃣  Open your browser:"
echo "   http://localhost:5000"
echo ""
echo "💡 Remember to activate the virtual environment next time:"
echo "   source venv/bin/activate"
echo ""
echo "========================================"

