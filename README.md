# ⚽ Football Player Statistics & Predictions Dashboard

A complete Machine Learning web application for analyzing football player performance with interactive visualizations.

## ✨ Features

- 🔍 **Search Functionality** - Find any player instantly
- 📸 **Player Profiles** - Photos, birthdates, complete information
- 📊 **Interactive Dashboard** - Charts, heatmaps, statistics
- 🤖 **ML Predictions** - Predict player performance ratings
- 📈 **Performance Analytics** - Trends, radar charts, detailed stats
- 🗺️ **Field Coverage Heatmaps** - Visualize player positioning

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Generate Data & Train Model

```bash
python load_data.py      # Create player database
python train_model.py    # Train ML model
```

### 3. Launch Website

```bash
python app.py
```

Open your browser: **http://localhost:8080**

---

## 📁 Project Structure

```
football_statistics/
├── app.py                  # Main Flask web application
├── app_epl.py             # Alternative EPL-focused version
├── model.py               # ML model (Random Forest)
├── load_data.py           # Data loader
├── train_model.py         # Model training script
├── data_generator.py      # Heatmap generation
├── config.py              # Configuration
├── requirements.txt       # Dependencies
├── templates/             # HTML templates
│   ├── index.html         # Main dashboard
│   ├── about.html         # About page
│   └── ...
├── static/                # CSS & JavaScript
│   ├── css/style.css
│   └── js/main.js
├── player_data.csv        # Player statistics (generated)
└── model.pkl              # Trained ML model (generated)
```

---

## 🎯 Usage

### Search for Players
1. Type player name in search bar (e.g., "Haaland", "Salah")
2. Or select from dropdown
3. View complete profile with photo and stats

### View Statistics
- Goals, assists, passes, tackles
- Performance ratings over time
- Field coverage heatmaps
- Radar charts

### ML Predictions
- Adjust stat sliders
- Get predicted performance rating
- See feature importance

---

## 🛠️ Technologies

- **Backend:** Python, Flask
- **ML:** Scikit-learn (Random Forest)
- **Frontend:** HTML5, CSS3, JavaScript
- **Visualizations:** Chart.js, Plotly.js
- **Data:** Pandas, NumPy

---

## 📊 Data

- Real player names and information
- Variable match statistics (realistic)
- Multiple leagues supported
- Easy to update with new data

---

## 🔧 Configuration

Edit `config.py` to customize:
- Model parameters
- Feature columns
- Dashboard settings

---

## 📝 License

Open source - Educational purposes

---

## 👨‍💻 Author

Football Statistics ML Dashboard Project

---

**Enjoy analyzing football statistics! ⚽📊**
