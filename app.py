"""
Flask App with REAL Transfermarkt Current Season Data
Includes: Search, Photos, Complete Info, Variable Matches
"""

from flask import Flask, render_template, request, jsonify
import pandas as pd
from model import PlayerPerformanceModel
from data_generator import generate_heatmap_data
import os

app = Flask(__name__)

model = None
df = None

DATA_FILE = 'player_data.csv'
MODEL_FILE = 'model.pkl'


def load_app_data():
    global model, df
    
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        print(f"✅ TRANSFERMARKT DATA: {df['player_name'].nunique()} players")
        print(f"   Season: 2024-2025 (CURRENT)")
    else:
        return False, "Run: python train_model_transfermarkt.py"
    
    model = PlayerPerformanceModel()
    if os.path.exists(MODEL_FILE):
        model.load_model(MODEL_FILE)
    else:
        return False, "Run: python train_model_transfermarkt.py"
    
    return True, "OK"


@app.route('/')
def index():
    success, message = load_app_data()
    if not success:
        return render_template('error.html', message=message)
    
    players = sorted(df['player_name'].unique().tolist())
    return render_template('index.html', players=players)


@app.route('/api/player/<player_name>')
def get_player_stats(player_name):
    if df is None:
        return jsonify({'error': 'Not loaded'}), 500
    
    player_data = df[df['player_name'] == player_name]
    if len(player_data) == 0:
        return jsonify({'error': 'Not found'}), 404
    
    profile = player_data.iloc[0]
    
    return jsonify({
        'player_name': player_name,
        'full_name': profile.get('full_name', player_name),
        'photo_url': profile.get('photo_url', ''),
        'birth_date': profile.get('birth_date', ''),
        'age': int(profile.get('age', 0)),
        'height_cm': f"{int(profile.get('height_cm', 0))} cm",
        'weight_kg': f"{int(profile.get('weight_kg', 0))} kg",
        'nationality': profile.get('nationality', ''),
        'position': profile.get('position', ''),
        'positions_full': profile.get('position', ''),
        'preferred_foot': profile.get('preferred_foot', ''),
        'overall_rating': int(profile.get('market_value_euro', 0) / 5000000),  # Approximate rating
        'current_team': profile.get('team', ''),
        'total_matches': len(player_data),
        'avg_performance': round(player_data['performance_rating'].mean(), 2),
        'total_goals': int(player_data['goals'].sum()),
        'total_assists': int(player_data['assists'].sum()),
        'avg_shots': round(player_data['shots'].mean(), 2),
        'shot_accuracy': round((player_data['shots_on_target'].sum() / max(player_data['shots'].sum(), 1) * 100), 1),
        'total_passes': int(player_data['passes_completed'].sum()),
        'avg_pass_accuracy': round(player_data['pass_accuracy'].mean(), 1),
        'avg_passes_per_match': round(player_data['passes_completed'].mean(), 1),
        'total_tackles': int(player_data['tackles'].sum()),
        'total_interceptions': int(player_data['interceptions'].sum()),
        'avg_dribbles': round(player_data['dribbles_completed'].mean(), 2),
        'radar_stats': {
            'goals': round(player_data['goals'].mean(), 2),
            'assists': round(player_data['assists'].mean(), 2),
            'shots_on_target': round(player_data['shots_on_target'].mean(), 2),
            'pass_accuracy': round(player_data['pass_accuracy'].mean(), 2),
            'tackles': round(player_data['tackles'].mean(), 2),
            'interceptions': round(player_data['interceptions'].mean(), 2),
            'dribbles_completed': round(player_data['dribbles_completed'].mean(), 2),
        },
        'performance_trend': {
            'matches': player_data['match_id'].tolist(),
            'ratings': player_data['performance_rating'].tolist(),
        },
        'recent_matches': player_data.head(10).to_dict('records')
    })


@app.route('/api/heatmap/<player_name>')
def get_heatmap(player_name):
    x_pos, y_pos = generate_heatmap_data(player_name, n_positions=200)
    return jsonify({'x': x_pos.tolist(), 'y': y_pos.tolist()})


@app.route('/api/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Not loaded'}), 500
    
    try:
        data = request.get_json()
        prediction_data = pd.DataFrame({
            'minutes_played': [data.get('minutes_played', 90)],
            'goals': [data.get('goals', 0)],
            'assists': [data.get('assists', 0)],
            'shots': [data.get('shots', 0)],
            'shots_on_target': [data.get('shots_on_target', 0)],
            'passes_completed': [data.get('passes_completed', 50)],
            'pass_accuracy': [data.get('pass_accuracy', 85.0)],
            'tackles': [data.get('tackles', 3)],
            'interceptions': [data.get('interceptions', 3)],
            'dribbles_completed': [data.get('dribbles_completed', 2)],
        })
        
        prediction = model.predict(prediction_data)[0]
        return jsonify({'prediction': round(float(prediction), 2), 'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/feature_importance')
def get_feature_importance():
    if model is None:
        return jsonify({'error': 'Not loaded'}), 500
    
    importance_df = model.get_feature_importance()
    return jsonify({
        'features': importance_df['feature'].tolist(),
        'importance': importance_df['importance'].tolist()
    })


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    print("=" * 80)
    print("⚽ TRANSFERMARKT - Current 2024-2025 Season")
    print("=" * 80)
    print("\n✅ REAL Players with Photos & Complete Info")
    print("🔍 Search Feature Enabled")
    print("📅 Current Rosters & Transfers")
    print("\n🚀 http://localhost:8080")
    print("=" * 80)
    
    app.run(debug=True, host='0.0.0.0', port=8080)

