#!/bin/bash
# 🔧 Automatic Fix for Python 3.14 Compatibility Issues

echo ""
echo "========================================"
echo "🔧 Python 3.14 Compatibility Fix"
echo "========================================"
echo ""

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1-2)
echo "📍 Detected Python version: $PYTHON_VERSION"
echo ""

if [ "$PYTHON_VERSION" = "3.14" ]; then
    echo "⚠️  Python 3.14 detected - using updated package versions"
    echo ""
    
    # Activate virtual environment
    if [ -d "venv" ]; then
        echo "🔌 Activating virtual environment..."
        source venv/bin/activate
    else
        echo "📦 Creating new virtual environment..."
        python3 -m venv venv
        source venv/bin/activate
    fi
    
    echo "⬆️  Upgrading pip..."
    pip install --upgrade pip --quiet
    
    echo ""
    echo "📥 Installing packages (latest versions for Python 3.14)..."
    echo ""
    
    # Install packages without version constraints
    pip install pandas numpy scikit-learn matplotlib seaborn flask plotly joblib scipy streamlit
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Installation successful!"
        echo ""
        echo "🔍 Verifying installation..."
        python -c "import pandas, numpy, sklearn, flask, plotly; print('✅ All packages working!')"
        
        if [ $? -eq 0 ]; then
            echo ""
            echo "========================================"
            echo "✅ Fix Complete!"
            echo "========================================"
            echo ""
            echo "📝 Next steps:"
            echo "1️⃣  python train_model.py"
            echo "2️⃣  python run_website.py"
            echo ""
        fi
    else
        echo ""
        echo "❌ Installation failed"
        echo ""
        echo "💡 Recommendation: Use Python 3.12 instead"
        echo ""
        echo "Run these commands:"
        echo "   brew install python@3.12"
        echo "   rm -rf venv"
        echo "   python3.12 -m venv venv"
        echo "   source venv/bin/activate"
        echo "   pip install -r requirements.txt"
        echo ""
    fi
else
    echo "✅ Python $PYTHON_VERSION should work fine with the original requirements"
    echo ""
    echo "Try running:"
    echo "   source venv/bin/activate"
    echo "   pip install -r requirements.txt"
    echo ""
fi

