# ⚽ Using Kaggle EPL Dataset

## 🔗 Dataset Information

**Dataset:** English Premier League Players Statistics  
**Source:** https://www.kaggle.com/code/desalegngeb/english-premier-league-players-statistics  
**Season:** 2024-2025  
**League:** Premier League (England)

---

## 🚀 Quick Start (3 Steps)

### Step 1: Load EPL Data

```bash
python kaggle_epl_loader.py
```

**This will:**
- ✅ Check for downloaded Kaggle dataset
- ✅ Or create sample EPL data with 30 real players
- ✅ Save to `player_statistics_epl.csv`

### Step 2: Train Model with EPL Data

```bash
python train_model_epl.py
```

**This will:**
- ✅ Load EPL player statistics
- ✅ Train ML model on Premier League data
- ✅ Save as `player_performance_model_epl.pkl`

### Step 3: Launch EPL Website

```bash
python app_epl.py
```

**Open:** http://localhost:8080

---

## 📥 How to Download Kaggle Dataset (Optional)

### Option 1: Manual Download

1. Visit: https://www.kaggle.com/code/desalegngeb/english-premier-league-players-statistics
2. Click **"Data"** tab on the right
3. Click **"Download"** button
4. Save CSV file to your project folder
5. Run: `python kaggle_epl_loader.py`

### Option 2: Kaggle API

```bash
# Install Kaggle CLI
pip install kaggle

# Set up API credentials (get from kaggle.com/settings)
# Place kaggle.json in ~/.kaggle/

# Download dataset
kaggle datasets download -d [dataset-name]

# Extract and place in project folder
```

---

## ⚽ Premier League Players Included

### 🔵 Manchester City
- Erling Haaland
- Kevin De Bruyne
- Phil Foden
- Bernardo Silva

### 🔴 Liverpool
- Mohamed Salah
- Luis Diaz
- Darwin Nunez
- Alexis Mac Allister

### 🔴 Arsenal
- Bukayo Saka
- Martin Odegaard
- Gabriel Martinelli
- Kai Havertz

### 🔵 Chelsea
- Cole Palmer
- Nicolas Jackson
- Enzo Fernandez
- Raheem Sterling

### 🔴 Manchester United
- Bruno Fernandes
- Rasmus Hojlund
- Marcus Rashford
- Alejandro Garnacho

### ⚪ Tottenham
- Son Heung-min
- James Maddison
- Dejan Kulusevski
- Brennan Johnson

### ⚫ Newcastle United
- Alexander Isak
- Anthony Gordon
- Bruno Guimaraes

### 🟣 Aston Villa
- Ollie Watkins
- John McGinn
- Moussa Diaby

**Total: 30 real Premier League players!**

---

## 📊 Data Features

Each player record includes:
- ✅ Player name, team, position
- ✅ Nationality
- ✅ Goals, assists, shots
- ✅ Passing statistics
- ✅ Defensive stats (tackles, interceptions)
- ✅ Dribbles completed
- ✅ Fouls committed
- ✅ Performance rating

---

## 🔧 How the Loader Works

1. **Searches** for Kaggle CSV in project directory
2. **Processes** and maps columns to our format
3. **Falls back** to sample data if CSV not found
4. **Calculates** performance ratings
5. **Saves** processed data

---

## 📁 Files Created

```
player_statistics_epl.csv              ← EPL player data
player_performance_model_epl.pkl       ← ML model
kaggle_epl_loader.py                   ← Data loader
train_model_epl.py                     ← Training script
app_epl.py                             ← Web application
```

---

## 🎯 Features

### Automatic Column Mapping
The loader automatically maps common EPL dataset columns:
- `Player` → `player_name`
- `Squad` → `team`
- `Gls` → `goals`
- `Ast` → `assists`
- `Pass%` → `pass_accuracy`
- And many more...

### Smart Fallback
If Kaggle dataset isn't found, it creates realistic sample data with 30 real EPL players!

### Performance Ratings
Automatically calculates performance ratings based on:
- Goals × 10
- Assists × 7
- Pass accuracy × 0.25
- Tackles × 1.5
- Interceptions × 1.5
- Dribbles × 1.2

---

## 💡 Usage Tips

### Use Sample Data (Default)
```bash
python kaggle_epl_loader.py    # Creates sample data
python train_model_epl.py      # Trains model
python app_epl.py              # Launches website
```

### Use Real Kaggle Dataset
1. Download CSV from Kaggle
2. Place in project folder
3. Run the same commands above

### View Top Players
The loader automatically shows top 10 players by performance rating!

---

## 🔄 Switching Between Datasets

| Command | Dataset Used |
|---------|-------------|
| `python app.py` | Synthetic data |
| `python app_real.py` | Real multi-league data |
| `python app_epl.py` | Premier League only |

---

## 🎨 Dashboard Features

When you launch `app_epl.py`, you get:
- ✅ **30 Real EPL Players** in dropdown
- ✅ **Team badges** and colors
- ✅ **League context** (Premier League)
- ✅ **Nationality** information
- ✅ **Match-by-match** statistics
- ✅ **Heatmaps** for field coverage
- ✅ **ML predictions** based on EPL patterns

---

## 🆘 Troubleshooting

### "No Kaggle dataset found"
✅ This is normal! The script creates sample data automatically

### "Error reading CSV"
✅ Place the CSV directly in project folder (not in subdirectory)

### "Column not found"
✅ The loader handles different column formats automatically

### Need more players?
✅ Edit `kaggle_epl_loader.py` and add to the `epl_players` list

---

## 📈 Advantages

1. **Premier League Focus** - Only EPL players
2. **Real Teams** - Manchester City, Liverpool, Arsenal, etc.
3. **Current Season** - 2024-2025 data
4. **Position-Specific** - Forwards vs Midfielders
5. **Team Context** - Compare players from same team

---

## 🎉 You're Ready!

```bash
# 1. Load EPL data
python kaggle_epl_loader.py

# 2. Train model
python train_model_epl.py

# 3. Launch website
python app_epl.py

# 4. Open browser
# Visit: http://localhost:8080
```

**Select Erling Haaland, Mohamed Salah, or any other EPL star! ⚽🏴󠁧󠁢󠁥󠁮󠁧󠁿**

