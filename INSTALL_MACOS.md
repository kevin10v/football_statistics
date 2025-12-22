# 🍎 Installation Guide for macOS

## Quick Install (Recommended)

### Option 1: Using Python 3 (Most Common)

```bash
pip3 install -r requirements.txt
```

### Option 2: Using Virtual Environment (Best Practice) ⭐

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

---

## 🔧 Detailed Setup for macOS

### Step 1: Check Python Installation

```bash
python3 --version
```

**Expected output:** `Python 3.8.0` or higher

**If Python is not installed:**
```bash
# Install using Homebrew
brew install python3
```

---

### Step 2: Navigate to Project Directory

```bash
cd ~/football_statistics
```

Or wherever your project is located.

---

### Step 3: Create Virtual Environment (Recommended)

**Why use a virtual environment?**
- Keeps dependencies isolated
- Prevents conflicts with system packages
- Easy to manage and clean up

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# You'll see (venv) in your prompt
```

---

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

**If you get permission errors, try:**
```bash
pip install --user -r requirements.txt
```

---

### Step 5: Verify Installation

```bash
pip list
```

You should see:
- pandas
- numpy
- scikit-learn
- flask
- matplotlib
- seaborn
- streamlit
- plotly
- joblib
- scipy

---

## 🚀 Complete Setup Commands (Copy & Paste)

```bash
# Navigate to project
cd ~/football_statistics

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Train the model
python train_model.py

# Run the website
python run_website.py
```

---

## ⚠️ Troubleshooting

### Issue 1: "pip3: command not found"

**Solution:**
```bash
# Install Python 3 using Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python3
```

### Issue 2: "Permission denied"

**Solution 1 (Recommended):** Use virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Solution 2:** Install with --user flag
```bash
pip3 install --user -r requirements.txt
```

### Issue 3: "No module named 'tkinter'" (for matplotlib)

**Solution:**
```bash
brew install python-tk@3.11
```

### Issue 4: Installation is slow

**Solution:** Use faster mirrors
```bash
pip install -r requirements.txt -i https://pypi.org/simple
```

### Issue 5: SSL Certificate Error

**Solution:**
```bash
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

---

## 🔄 Deactivating Virtual Environment

When you're done working:

```bash
deactivate
```

---

## 🗑️ Clean Installation

If you need to start fresh:

```bash
# Remove virtual environment
rm -rf venv

# Remove any cached files
rm -rf __pycache__
find . -type d -name "__pycache__" -exec rm -r {} +

# Start over
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## ✅ Quick Test

After installation, test that everything works:

```bash
python -c "import pandas, numpy, sklearn, flask, plotly; print('✅ All packages installed successfully!')"
```

---

## 🎯 Next Steps

Once installation is complete:

1. **Train the model:**
   ```bash
   python train_model.py
   ```

2. **Run the website:**
   ```bash
   python run_website.py
   ```

3. **Open browser:**
   Visit `http://localhost:5000`

---

## 💡 Pro Tips for macOS

- **Use virtual environments** - Keeps your system Python clean
- **Homebrew is your friend** - Best package manager for macOS
- **Check M1/M2 compatibility** - All packages in requirements.txt are compatible with Apple Silicon
- **Terminal.app works great** - No need for special terminal emulators

---

## 🆘 Still Having Issues?

1. Check Python version: `python3 --version` (need 3.8+)
2. Update pip: `pip install --upgrade pip`
3. Try with sudo (last resort): `sudo pip3 install -r requirements.txt`
4. Check Xcode Command Line Tools: `xcode-select --install`

---

**You're all set for macOS! 🍎⚽**

