"""
Flask App with REAL Transfermarkt Current Season Data
Includes: Search, Photos, Complete Info, Variable Matches
+ OpenFootball Real Match Data Integration
"""

from flask import Flask, render_template, request, jsonify
import pandas as pd
from model import PlayerPerformanceModel
from data_generator import generate_heatmap_data
from football_json_loader import FootballJSONLoader
from load_premier_league_matches import load_matches
import os
import json

app = Flask(__name__)

model = None
df = None
football_loader = FootballJSONLoader()
premier_league_matches = None

DATA_FILE = 'player_data.csv'
MODEL_FILE = 'model.pkl'


def load_premier_league_matches_data():
    """Load Premier League matches from local JSON file"""
    global premier_league_matches
    try:
        with open('premier_league_2024_25_matches.json', 'r') as f:
            data = json.load(f)
        
        matches = []
        for match in data['matches']:
            match_info = {
                'date': match.get('date'),
                'time': match.get('time', ''),
                'round': match.get('round'),
                'team1': match.get('team1'),
                'team2': match.get('team2'),
                'score1': None,
                'score2': None,
            }
            
            # Extract scores if available
            if 'score' in match and 'ft' in match['score']:
                match_info['score1'] = match['score']['ft'][0]
                match_info['score2'] = match['score']['ft'][1]
            
            matches.append(match_info)
        
        premier_league_matches = matches
        print(f"✅ Loaded {len(matches)} Premier League matches from local file")
    except Exception as e:
        print(f"⚠️  Could not load local matches: {e}")
        premier_league_matches = []


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
    """Default homepage - live scores"""
    return render_template('live_scores.html')


@app.route('/players')
def players():
    """Player statistics page"""
    success, message = load_app_data()
    if not success:
        return render_template('error.html', message=message)
    
    players_list = sorted(df['player_name'].unique().tolist())
    return render_template('index.html', players=players_list)


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


@app.route('/leagues')
def leagues():
    """League tables page"""
    return render_template('league_table.html')


@app.route('/live-scores')
def live_scores():
    """Live scores page - Flashscore style"""
    return render_template('live_scores.html')


# ============================================================================
# OpenFootball JSON API Endpoints - Real Match Data
# ============================================================================

@app.route('/api/league/table/<league_name>')
def get_league_table(league_name):
    """Get league standings/table"""
    try:
        season = request.args.get('season', '2024-25')
        table = football_loader.get_team_statistics(league_name, season)
        
        if table.empty:
            return jsonify({'error': 'No data available', 'league': league_name}), 404
        
        return jsonify({
            'league': league_name,
            'season': season,
            'standings': table.to_dict('records')
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/league/matches/<league_name>')
def get_league_matches_api(league_name):
    """Get all matches for a league - uses local data for Premier League"""
    try:
        season = request.args.get('season', '2024-25')
        
        # Use local Premier League data for faster loading
        if league_name == 'Premier League' and season == '2024-25':
            if premier_league_matches is None:
                load_premier_league_matches_data()
            
            return jsonify({
                'league': league_name,
                'season': season,
                'total_matches': len(premier_league_matches),
                'matches': premier_league_matches
            })
        
        # Fallback to external API for other leagues/seasons
        matches = football_loader.get_league_matches(league_name, season)
        
        if matches.empty:
            return jsonify({'error': 'No data available', 'league': league_name}), 404
        
        return jsonify({
            'league': league_name,
            'season': season,
            'total_matches': len(matches),
            'matches': matches.to_dict('records')
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/league/fixtures/<league_name>')
def get_league_fixtures(league_name):
    """Get upcoming fixtures for a league"""
    try:
        season = request.args.get('season', '2024-25')
        fixtures = football_loader.get_upcoming_fixtures(league_name, season)
        
        return jsonify({
            'league': league_name,
            'season': season,
            'upcoming_matches': len(fixtures),
            'fixtures': fixtures.to_dict('records')
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/team/form/<league_name>/<team_name>')
def get_team_form(league_name, team_name):
    """Get recent form for a team"""
    try:
        season = request.args.get('season', '2024-25')
        last_n = int(request.args.get('last_n', 5))
        
        form = football_loader.get_team_form(team_name, league_name, season, last_n)
        
        return jsonify({
            'team': team_name,
            'league': league_name,
            'season': season,
            'form': form,
            'wins': form.count('W'),
            'draws': form.count('D'),
            'losses': form.count('L')
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/leagues')
def get_available_leagues():
    """Get list of available leagues"""
    return jsonify({
        'leagues': list(football_loader.LEAGUES.keys()),
        'details': football_loader.LEAGUES
    })


if __name__ == '__main__':
    print("=" * 80)
    print("⚽ PREMIER LEAGUE STATISTICS 2024-25")
    print("=" * 80)
    print("\n✅ REAL Premier League Players & Matches")
    print("⚽ 380 Matches from 2024-25 Season")
    print("👥 21 Real Players with Accurate Stats")
    print("🏆 Top Scorers: Salah (29), Isak (23), Haaland (22)")
    print("🌓 Dark/Light Mode on All Pages")
    print("\n🚀 http://localhost:8080")
    print("=" * 80)
    
    # Load Premier League matches
    load_premier_league_matches_data()
    
    app.run(debug=True, host='0.0.0.0', port=8080)

