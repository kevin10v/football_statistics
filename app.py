"""
Flask Web Application for Football Player Statistics & Predictions
"""

from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from model import PlayerPerformanceModel
from data_generator import generate_heatmap_data
import os
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'football-stats-secret-key-2024'

# Global variables for model and data
model = None
df = None


def load_app_data():
    """Load model and data on startup"""
    global model, df
    
    # Load data
    if os.path.exists('player_statistics.csv'):
        df = pd.read_csv('player_statistics.csv')
    else:
        return False, "Data file not found. Please run train_model.py first."
    
    # Load model
    model = PlayerPerformanceModel()
    if os.path.exists('player_performance_model.pkl'):
        model.load_model()
    else:
        return False, "Model not found. Please run train_model.py first."
    
    return True, "Data and model loaded successfully"


@app.route('/')
def index():
    """Main dashboard page"""
    success, message = load_app_data()
    if not success:
        return render_template('error.html', message=message)
    
    # Get list of players
    players = sorted(df['player_name'].unique().tolist())
    
    return render_template('index.html', players=players)


@app.route('/api/players')
def get_players():
    """API endpoint to get all players"""
    if df is None:
        return jsonify({'error': 'Data not loaded'}), 500
    
    players = sorted(df['player_name'].unique().tolist())
    return jsonify({'players': players})


@app.route('/api/player/<player_name>')
def get_player_stats(player_name):
    """API endpoint to get player statistics"""
    if df is None:
        return jsonify({'error': 'Data not loaded'}), 500
    
    player_data = df[df['player_name'] == player_name]
    
    if len(player_data) == 0:
        return jsonify({'error': 'Player not found'}), 404
    
    # Calculate statistics
    stats = {
        'player_name': player_name,
        'position': player_data['position'].iloc[0],
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
        
        # For radar chart
        'radar_stats': {
            'goals': round(player_data['goals'].mean(), 2),
            'assists': round(player_data['assists'].mean(), 2),
            'shots_on_target': round(player_data['shots_on_target'].mean(), 2),
            'pass_accuracy': round(player_data['pass_accuracy'].mean(), 2),
            'tackles': round(player_data['tackles'].mean(), 2),
            'interceptions': round(player_data['interceptions'].mean(), 2),
            'dribbles_completed': round(player_data['dribbles_completed'].mean(), 2),
        },
        
        # Performance trend
        'performance_trend': {
            'matches': player_data['match_id'].tolist(),
            'ratings': player_data['performance_rating'].tolist(),
        },
        
        # Recent matches
        'recent_matches': player_data.sort_values('match_id', ascending=False).head(10).to_dict('records')
    }
    
    return jsonify(stats)


@app.route('/api/heatmap/<player_name>')
def get_heatmap(player_name):
    """API endpoint to get player heatmap data"""
    x_pos, y_pos = generate_heatmap_data(player_name, n_positions=200)
    
    return jsonify({
        'x': x_pos.tolist(),
        'y': y_pos.tolist()
    })


@app.route('/api/predict', methods=['POST'])
def predict():
    """API endpoint for ML predictions"""
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        data = request.get_json()
        
        # Create prediction dataframe
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
        
        # Make prediction
        prediction = model.predict(prediction_data)[0]
        
        return jsonify({
            'prediction': round(float(prediction), 2),
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/feature_importance')
def get_feature_importance():
    """API endpoint to get feature importance"""
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    importance_df = model.get_feature_importance()
    
    return jsonify({
        'features': importance_df['feature'].tolist(),
        'importance': importance_df['importance'].tolist()
    })


@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')


if __name__ == '__main__':
    print("=" * 60)
    print("Football Statistics Web Application")
    print("=" * 60)
    print("\nStarting server...")
    print("Open your browser and navigate to: http://localhost:8080")
    print("\nPress CTRL+C to stop the server")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=8080)

