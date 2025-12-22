# ⚡ Quick Start Guide

## 🎯 Get Your Website Running in 3 Steps!

### Step 1: Install Dependencies (30 seconds)

Open your terminal in the project folder and run:

```bash
pip install -r requirements.txt
```

This installs all necessary Python packages.

---

### Step 2: Train the ML Model (1-2 minutes)

```bash
python train_model.py
```

**What this does:**
- ✅ Generates 1,000+ synthetic player statistics records
- ✅ Trains a Random Forest ML model
- ✅ Saves the model for predictions
- ✅ Shows you training metrics

**Expected Output:**
```
Generating synthetic player data...
Generated 1000 records for 50 players

Training ML model...

=== Training Metrics ===
train_rmse: 2.3456
test_rmse: 3.4567
train_r2: 0.9543
test_r2: 0.9321
...

Model saved to 'player_performance_model.pkl'
```

---

### Step 3: Launch the Website! (5 seconds)

```bash
python run_website.py
```

Or:

```bash
python app.py
```

**The website will start at:**
```
http://localhost:5000
```

Open this URL in your browser!

---

## 🌐 What You'll See

1. **Beautiful Dashboard** with modern UI
2. **Player Selector** - Choose from 50+ players
3. **Interactive Heatmap** - See field coverage
4. **Performance Charts** - Radar and trend charts
5. **ML Predictions** - Adjust stats and predict ratings
6. **Detailed Statistics** - Attacking, passing, defensive stats

---

## 🎨 Alternative: Streamlit Dashboard

If you prefer the Streamlit interface:

```bash
streamlit run dashboard.py
```

Opens at: `http://localhost:8501`

---

## 🛑 Stopping the Server

Press `CTRL + C` in the terminal

---

## ❓ Troubleshooting

### "Model not found" error?
👉 Run `python train_model.py` first

### Port already in use?
👉 Change port in `app.py` line: `app.run(debug=True, host='0.0.0.0', port=5001)`

### Missing packages?
👉 Make sure you ran `pip install -r requirements.txt`

---

## 📚 Project Structure

```
football_statistics/
├── app.py              ← Flask web server
├── templates/          ← HTML pages
├── static/             ← CSS & JavaScript
├── model.py            ← ML model code
├── data_generator.py   ← Creates sample data
└── train_model.py      ← Trains the model
```

---

## 🚀 Next Steps

1. **Explore Players** - Select different players and see their stats
2. **Try Predictions** - Use the sliders to predict performance
3. **View Heatmaps** - See where players spend their time on field
4. **Read About Page** - Learn about the technology

---

## 💡 Tips

- The data is synthetic but realistic
- Performance ratings range from 0-100
- Feature importance shows which stats matter most
- All visualizations are interactive!

---

**Enjoy exploring football statistics! ⚽📊**

Need help? Check `README.md` for detailed documentation.

