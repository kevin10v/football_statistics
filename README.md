# ⚽ Football Statistics & Live Scores Platform

A complete football analytics platform with **Flashscore-style live scores**, real match data, league tables, player statistics, and ML predictions.

> **🎉 NEW!** Flashscore.com-inspired layout with real-time match display, league navigation, and comprehensive statistics!

## ✨ Features

### 🎨 Flashscore-Style Interface (NEW! ⭐)
- 🌐 **Live Scores Page** - Flashscore.com-inspired design
- 🎯 **Three-Column Layout** - League sidebar, match cards, statistics
- 🔍 **Search & Filter** - Find teams, filter by status (Live/Finished/Scheduled)
- 🎨 **Modern Design** - Purple gradient, card-based layout, smooth animations
- 📱 **Responsive** - Works perfectly on desktop, tablet, and mobile
- ⚡ **Interactive** - Click leagues, search matches, toggle views

### ⚽ Match & League Data
- 🏆 **Live League Tables** - Real standings for 10+ European leagues
- 📅 **Match Results** - 380+ matches per league with scores
- 🔥 **Team Form** - Recent performance tracking (W/D/L badges)
- 📊 **Team Statistics** - Goals, wins, points, goal difference
- 🔮 **Upcoming Fixtures** - Scheduled matches
- 📜 **Historical Data** - Access seasons back to 2010-11

### 👤 Player Analytics
- 🔍 **Search Functionality** - Find any player instantly
- 📸 **Player Profiles** - Photos, birthdates, complete information
- 📊 **Interactive Dashboard** - Charts, heatmaps, statistics
- 🤖 **ML Predictions** - Predict player performance ratings
- 📈 **Performance Analytics** - Trends, radar charts, detailed stats
- 🗺️ **Field Coverage Heatmaps** - Visualize player positioning

## 🚀 Quick Start (3 Commands)

```bash
cd /Users/kevsmac/football_statistics
source venv/bin/activate
python app.py
```

Then open: **http://localhost:8080**

**That's it!** Your Flashscore-style football website is ready! ⚽

> **📖 New to the project?** Read **[START_HERE.md](START_HERE.md)** for a complete walkthrough!

---

## 📁 Project Structure

```
football_statistics/
├── app.py                          # Main Flask web application
├── model.py                        # ML model (Random Forest)
├── load_data.py                    # Data loader (Transfermarkt)
├── football_json_loader.py         # OpenFootball data loader (NEW!)
├── train_model.py                  # Model training script
├── data_generator.py               # Heatmap generation
├── config.py                       # Configuration
├── test_football_json.py           # Integration test (NEW!)
├── requirements.txt                # Dependencies
├── templates/                      # HTML templates
│   ├── index.html                  # Main dashboard
│   ├── league_table.html           # League tables (NEW!)
│   ├── about.html                  # About page
│   └── base.html                   # Base template
├── static/                         # CSS & JavaScript
│   ├── css/style.css
│   └── js/main.js
├── player_data.csv                 # Player statistics (generated)
├── model.pkl                       # Trained ML model (generated)
├── OPENFOOTBALL_INTEGRATION.md     # Integration guide (NEW!)
└── IMPLEMENTATION_SUMMARY.md       # Implementation summary (NEW!)
```

---

## 🎯 Usage

### Player Analytics
1. **Search for Players**
   - Type player name in search bar (e.g., "Haaland", "Salah")
   - Or select from dropdown
   - View complete profile with photo and stats

2. **View Statistics**
   - Goals, assists, passes, tackles
   - Performance ratings over time
   - Field coverage heatmaps
   - Radar charts

3. **ML Predictions**
   - Adjust stat sliders
   - Get predicted performance rating
   - See feature importance

### League & Team Analytics (NEW!)
1. **View League Tables**
   - Visit: http://localhost:8080/leagues
   - Select league (Premier League, La Liga, etc.)
   - Choose season (2024-25 or historical)
   - See live standings with team form

2. **API Endpoints**
   ```bash
   # Get available leagues
   curl http://localhost:8080/api/leagues
   
   # Get Premier League table
   curl "http://localhost:8080/api/league/table/Premier League"
   
   # Get all matches
   curl "http://localhost:8080/api/league/matches/Premier League"
   
   # Get team form
   curl "http://localhost:8080/api/team/form/Premier League/Liverpool FC"
   ```

3. **Python API**
   ```python
   from football_json_loader import FootballJSONLoader
   
   loader = FootballJSONLoader()
   matches = loader.get_league_matches('Premier League', '2024-25')
   table = loader.get_team_statistics('Premier League', '2024-25')
   form = loader.get_team_form('Liverpool FC', 'Premier League', '2024-25')
   ```

---

## 🛠️ Technologies

- **Backend:** Python, Flask
- **ML:** Scikit-learn (Random Forest)
- **Frontend:** HTML5, CSS3, JavaScript
- **Visualizations:** Chart.js, Plotly.js
- **Data:** Pandas, NumPy

---

## 📊 Data Sources

### Player Data (Transfermarkt)
- ✅ Real player names and information
- ✅ Player photos and profiles
- ✅ Current season 2024-25
- ✅ Multiple leagues (Premier League, La Liga, Bundesliga, Serie A)

### Match Data (OpenFootball JSON) - **NEW!**
- ✅ Real match results from 10+ European leagues
- ✅ 380+ matches per season (Premier League, La Liga, Serie A)
- ✅ Historical data back to 2010-11
- ✅ Live league tables and standings
- ✅ Team statistics and form
- ✅ No API key required - Free and open data
- 📖 See `OPENFOOTBALL_INTEGRATION.md` for details

---

## 🔧 Configuration

Edit `config.py` to customize:
- Model parameters
- Feature columns
- Dashboard settings

---

## 📝 License

Open source - Educational purposes

## 🆕 What's New

### Flashscore-Style Layout (December 27, 2024) ⭐
- ✅ **Complete redesign** inspired by Flashscore.com
- ✅ **Live scores homepage** with match cards and league navigation
- ✅ **Three-column layout** - Sidebar, matches, statistics
- ✅ **Search and filter** - Find teams, toggle Live/Finished/Scheduled
- ✅ **Real-time data** - From OpenFootball JSON (380+ matches per league)
- ✅ **Beautiful UI** - Purple gradient, smooth animations, responsive
- 📖 See **[FLASHSCORE_LAYOUT_GUIDE.md](FLASHSCORE_LAYOUT_GUIDE.md)** for complete guide

### OpenFootball JSON Integration (December 2024)
- ✅ Added real match data from 10+ European leagues
- ✅ League tables with live standings
- ✅ Team statistics and form tracking
- ✅ Historical data back to 2010-11
- ✅ RESTful API endpoints for match data
- 📖 See **[OPENFOOTBALL_INTEGRATION.md](OPENFOOTBALL_INTEGRATION.md)** for technical details

### Quick Test
```bash
source venv/bin/activate
python test_football_json.py
python demo_stats.py  # See interesting statistics!
```

---

## 📖 Documentation

### Start Here 👇
- **[START_HERE.md](START_HERE.md)** ⭐ - **Read this first!** Complete overview with visual guide
- **[QUICK_START.txt](QUICK_START.txt)** - Simple 3-command start guide
- **[FLASHSCORE_LAYOUT_GUIDE.md](FLASHSCORE_LAYOUT_GUIDE.md)** - Complete Flashscore layout guide

### Technical Documentation
- **[OPENFOOTBALL_INTEGRATION.md](OPENFOOTBALL_INTEGRATION.md)** - OpenFootball JSON integration
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Implementation details
- **[QUICK_START_GUIDE.md](QUICK_START_GUIDE.md)** - OpenFootball usage guide
- **[README.md](README.md)** - This file (project overview)

---

## 🌟 Screenshots & Features

### Homepage - Live Scores (Flashscore Style)
- **Left Sidebar**: League navigation (EPL, La Liga, Bundesliga, Serie A, etc.)
- **Center**: Match cards with scores, teams, and status
- **Right Sidebar**: Top scorers, league leaders, team form
- **Top Bar**: Search, view filters (Live/Finished/Scheduled), season selector

### League Tables Page
- Interactive standings for all leagues
- Team statistics (points, goals, wins, draws, losses)
- Team form indicators (W/D/L badges)
- Season selector for historical data

### Player Stats Page
- Search any player
- Detailed statistics and charts
- ML performance predictions
- Field coverage heatmaps

---

## 🎯 Inspired By

This project's live scores interface is inspired by **[Flashscore.com](https://www.flashscore.com/)** - one of the most popular football live scores websites. We've recreated their clean, modern design while using our own real data sources.

---

**Enjoy your professional football statistics platform! ⚽📊🏆**

**Reference**: Layout inspired by [Flashscore.com](https://www.flashscore.com/)

---

## 👨‍💻 Author

Football Statistics ML Dashboard Project by Holberton School

Kevin Voka   
https://github.com/kevin10v.


Frenki Janaqi    
https://github.com/frenk1j.


Erdi Shpati    
https://github.com/Erdi-Shpati.


---
