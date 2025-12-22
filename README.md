# Football Player Statistics & Predictions Dashboard ⚽

A comprehensive Machine Learning project that predicts football player performance and visualizes statistics through an interactive dashboard.

## 🎯 Features

- **ML Model**: Random Forest Regressor to predict player performance ratings
- **Interactive Dashboard**: Built with Streamlit for real-time visualization
- **Player Statistics**: Comprehensive stats including goals, assists, passes, tackles, and more
- **Field Coverage Heatmap**: Visualize player movement and positioning on the field
- **Performance Radar Chart**: Multi-dimensional view of player capabilities
- **Trend Analysis**: Track performance over multiple matches
- **Real-time Predictions**: Adjust stats and see predicted performance ratings

## 📁 Project Structure

```
football_statistics/
├── README.md                          # Project documentation
├── requirements.txt                   # Python dependencies
├── config.py                         # Configuration settings
├── data_generator.py                 # Generate synthetic player data
├── model.py                          # ML model implementation
├── train_model.py                    # Script to train the model
├── run_website.py                    # Quick start script for Flask app
├── app.py                            # Flask web application
├── dashboard.py                      # Streamlit dashboard (alternative)
├── templates/                        # HTML templates
│   ├── base.html                     # Base template
│   ├── index.html                    # Main dashboard
│   ├── about.html                    # About page
│   └── error.html                    # Error page
├── static/                           # Static assets
│   ├── css/
│   │   └── style.css                 # Custom CSS styling
│   └── js/
│       └── main.js                   # JavaScript functionality
├── player_statistics.csv             # Generated data (after running)
└── player_performance_model.pkl      # Trained model (after training)
```

## 🚀 Getting Started

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Generate Data and Train Model

```bash
python train_model.py
```

This will:
- Generate synthetic player statistics data (1000+ records)
- Train the ML model with Random Forest
- Save the trained model to disk
- Display training metrics and feature importance

### 3. Run the Web Application

#### Option A: Flask Web Application (Recommended for Production)

```bash
python run_website.py
```

Or directly:

```bash
python app.py
```

The website will open at `http://localhost:5000`

**Features:**
- Beautiful, responsive web interface
- Interactive charts with Chart.js and Plotly
- Real-time ML predictions
- Professional dashboard design
- Mobile-friendly layout

#### Option B: Streamlit Dashboard (Quick Prototyping)

```bash
streamlit run dashboard.py
```

The dashboard will open at `http://localhost:8501`

**Features:**
- Rapid prototyping interface
- Streamlit's built-in widgets
- Quick data exploration

## 📊 Web Application Features

### 🏠 Main Dashboard

1. **Player Selection Dropdown**
   - Browse 50+ players
   - Instant stats loading

2. **Key Stats Cards**
   - Position, Total Matches, Avg Performance, Total Goals
   - Beautiful gradient backgrounds
   - Hover animations

3. **Field Coverage Heatmap** 🗺️
   - Interactive football field visualization
   - Real field dimensions (105m x 68m)
   - Density heatmap showing player positioning
   - Built with Plotly.js

4. **Performance Radar Chart** 📊
   - 7-dimensional performance view
   - Normalized statistics (0-100 scale)
   - Interactive tooltips
   - Built with Chart.js

5. **Performance Trend Line Chart** 📈
   - Match-by-match rating progression
   - Smooth animations
   - Identify consistency patterns

6. **Detailed Statistics Breakdown**
   - **⚽ Attacking Stats**: Goals, assists, shots, accuracy
   - **🎯 Passing Stats**: Total passes, accuracy, avg per match
   - **🛡️ Defensive Stats**: Tackles, interceptions, dribbles
   - Color-coded categories

7. **ML Prediction Interface** 🤖
   - 10 interactive sliders for stat adjustment
   - Real-time value display
   - Large prediction display (0-100)
   - Calculate button with smooth animations

8. **Feature Importance Chart**
   - Horizontal bar chart
   - Shows which stats matter most
   - Based on trained model

9. **Recent Matches Table** 📋
   - Last 10 matches detailed view
   - Sortable columns
   - Hover effects

### 📄 About Page
- Full project documentation
- Technology stack details
- Model information
- Quick start guide

## 🤖 Model Details

### Algorithm
- **Random Forest Regressor** with 100 estimators
- Features: 10 key player statistics
- Target: Performance rating (0-100)

### Features Used
1. Minutes played
2. Goals
3. Assists
4. Shots
5. Shots on target
6. Passes completed
7. Pass accuracy
8. Tackles
9. Interceptions
10. Dribbles completed

### Performance Metrics
- R² Score: ~0.95+ on test set
- RMSE: Low error rate
- Cross-validation: 5-fold CV for robustness

## 🎨 Visualizations

- **Plotly**: Interactive charts and heatmaps
- **Matplotlib/Seaborn**: Statistical visualizations
- **Custom Football Field**: Accurate field dimensions (105m x 68m)

## 📝 Data

The project uses synthetic data that mimics realistic football statistics:
- 50 players across 4 positions (Forward, Midfielder, Defender, Goalkeeper)
- 20 matches per player (1000 total records)
- Position-specific statistical distributions
- Realistic performance ratings based on multiple factors

## 🔧 Configuration

Edit `config.py` to customize:
- Model hyperparameters
- Feature columns
- Dashboard settings
- Field dimensions

## 🎓 Use Cases

- **Player Analysis**: Evaluate player performance comprehensively
- **Scouting**: Predict potential based on statistics
- **Team Strategy**: Understand player strengths and weaknesses
- **Performance Tracking**: Monitor improvement over time
- **Educational**: Learn ML and data visualization techniques

## 🛠️ Technologies Used

- **Python 3.8+**
- **Pandas & NumPy**: Data manipulation
- **Scikit-learn**: Machine learning
- **Streamlit**: Web dashboard
- **Plotly**: Interactive visualizations
- **Matplotlib & Seaborn**: Statistical plots

## 📈 Future Enhancements

- Real football data integration (API)
- Player comparison features
- Team-level analytics
- Advanced ML models (XGBoost, Neural Networks)
- Historical data analysis
- Export reports functionality

## 📄 License

This project is open source and available for educational purposes.

## 👨‍💻 Author

Created as a demonstration of ML and data visualization capabilities in sports analytics.

---

**Enjoy exploring football statistics! ⚽📊**