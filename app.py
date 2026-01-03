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
import joblib
import numpy as np

# Extended Player photo URLs from Premier League official site
PLAYER_PHOTOS = {
    # Top Players with working photos
    'Mohamed Salah': 'https://img.a.transfermarkt.technology/portrait/big/148455-1694609670.jpg?lm=1',
    'Erling Haaland': 'https://img.a.transfermarkt.technology/portrait/big/418560-1694609896.jpg?lm=1',
    'Bukayo Saka': 'https://img.a.transfermarkt.technology/portrait/big/433177-1694610015.jpg?lm=1',
    'Cole Palmer': 'https://img.a.transfermarkt.technology/portrait/big/536083-1664870763.jpg?lm=1',
    'Alexander Isak': 'https://img.a.transfermarkt.technology/portrait/big/406775-1664870749.jpg?lm=1',
    'Kevin De Bruyne': 'https://img.a.transfermarkt.technology/portrait/big/88755-1682683748.jpg?lm=1',
    'Bruno Fernandes': 'https://img.a.transfermarkt.technology/portrait/big/240306-1682683483.jpg?lm=1',
    'Son Heung-min': 'https://img.a.transfermarkt.technology/portrait/big/91845-1664870616.jpg?lm=1',
    'Phil Foden': 'https://img.a.transfermarkt.technology/portrait/big/406635-1682683746.jpg?lm=1',
    'Jack Grealish': 'https://img.a.transfermarkt.technology/portrait/big/203460-1682683745.jpg?lm=1',
    'Bernardo Silva': 'https://img.a.transfermarkt.technology/portrait/big/241641-1682683746.jpg?lm=1',
    'Martin Ødegaard': 'https://img.a.transfermarkt.technology/portrait/big/316264-1664870753.jpg?lm=1',
    'Gabriel Martinelli': 'https://img.a.transfermarkt.technology/portrait/big/655488-1694610014.jpg?lm=1',
    'Darwin Núñez': 'https://img.a.transfermarkt.technology/portrait/big/546543-1664870722.jpg?lm=1',
    'Luis Díaz': 'https://img.a.transfermarkt.technology/portrait/big/480692-1682683484.jpg?lm=1',
    'Ollie Watkins': 'https://img.a.transfermarkt.technology/portrait/big/331755-1664870759.jpg?lm=1',
    'Dominic Solanke': 'https://img.a.transfermarkt.technology/portrait/big/196755-1664870736.jpg?lm=1',
    'Nicolas Jackson': 'https://img.a.transfermarkt.technology/portrait/big/534634-1693387018.jpg?lm=1',
    'Raheem Sterling': 'https://img.a.transfermarkt.technology/portrait/big/134425-1682683485.jpg?lm=1',
    'Marcus Rashford': 'https://img.a.transfermarkt.technology/portrait/big/258923-1682683483.jpg?lm=1',
    'Gabriel Jesus': 'https://img.a.transfermarkt.technology/portrait/big/363622-1694610014.jpg?lm=1',
    'William Saliba': 'https://img.a.transfermarkt.technology/portrait/big/481089-1694610015.jpg?lm=1',
    'Declan Rice': 'https://img.a.transfermarkt.technology/portrait/big/357662-1694610014.jpg?lm=1',
    'Ben White': 'https://img.a.transfermarkt.technology/portrait/big/392222-1694610015.jpg?lm=1',
    'Kai Havertz': 'https://img.a.transfermarkt.technology/portrait/big/309400-1694610014.jpg?lm=1',
    'Leandro Trossard': 'https://img.a.transfermarkt.technology/portrait/big/207498-1694610015.jpg?lm=1',
    'Virgil van Dijk': 'https://img.a.transfermarkt.technology/portrait/big/139208-1682683484.jpg?lm=1',
    'Trent Alexander-Arnold': 'https://img.a.transfermarkt.technology/portrait/big/314353-1682683483.jpg?lm=1',
    'Alisson': 'https://img.a.transfermarkt.technology/portrait/big/105470-1682683484.jpg?lm=1',
}


app = Flask(__name__)

model = None
df = None
football_loader = FootballJSONLoader()
premier_league_matches = None

# Load the prediction model
prediction_model_data = None
prediction_model = None
prediction_scaler = None
prediction_feature_columns = None

DATA_FILE = 'player_data.csv'
MODEL_FILE = 'model.pkl'

def load_prediction_model():
    """Load the player prediction model"""
    global prediction_model_data, prediction_model, prediction_scaler, prediction_feature_columns
    try:
        prediction_model_data = joblib.load('model.pkl')
        prediction_model = prediction_model_data['model']
        prediction_scaler = prediction_model_data['scaler']
        prediction_feature_columns = prediction_model_data['feature_columns']
        print("✅ Prediction model loaded successfully")
    except Exception as e:
        print(f"⚠️  Could not load prediction model: {e}")

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
    players_json = json.dumps(players_list)  # Convert to JSON string
    return render_template('index.html', players=players_list, players_json=players_json)


@app.route('/player/<player_name>')
def player_detail(player_name):
    """Individual player detail page"""
    success, message = load_app_data()
    if not success:
        return render_template('error.html', message=message)
    
    # Normalize player name
    player_name = player_name.strip()
    
    # Check if player exists (case-insensitive)
    player_exists = df[df['player_name'].str.strip().str.lower() == player_name.lower()]
    
    if player_exists.empty:
        return render_template('error.html', message=f"Player '{player_name}' not found")
    
    # Get actual player name from dataset
    actual_name = player_exists.iloc[0]['player_name']
    
    return render_template('player_detail.html', player_name=actual_name)

def get_player_photo_url(player_name):
    """Generate player photo URL - checks dictionary with fuzzy matching"""
    # Direct match
    if player_name in PLAYER_PHOTOS:
        return PLAYER_PHOTOS[player_name]
    
    # Try removing special characters for matching
    import unicodedata
    normalized_name = ''.join(c for c in unicodedata.normalize('NFD', player_name) if unicodedata.category(c) != 'Mn')
    
    for photo_key in PLAYER_PHOTOS.keys():
        normalized_key = ''.join(c for c in unicodedata.normalize('NFD', photo_key) if unicodedata.category(c) != 'Mn')
        if normalized_name.lower() == normalized_key.lower():
            return PLAYER_PHOTOS[photo_key]
    
    # Generate placeholder with initials
    return f"https://ui-avatars.com/api/?name={player_name.replace(' ', '+')}&size=200&background=5dade2&color=fff&bold=true&font-size=0.4"


@app.route('/api/player/<path:player_name>')
def get_player_stats(player_name):
    if df is None:
        return jsonify({'error': 'Not loaded'}), 500
    
    # Normalize the player name - decode URL encoding and strip whitespace
    from urllib.parse import unquote
    player_name = unquote(player_name).strip()
    
    print(f"🔍 Searching for: '{player_name}'")
    
    # Try exact match first
    player_data = df[df['player_name'].str.strip() == player_name]
    
    # If not found, try case-insensitive match
    if len(player_data) == 0:
        player_data = df[df['player_name'].str.strip().str.lower() == player_name.lower()]
    
    # Still not found? Return 404
    if len(player_data) == 0:
        print(f"❌ Player not found: '{player_name}'")
        return jsonify({'error': f'Player "{player_name}" not found'}), 404
    
    profile = player_data.iloc[0]
    actual_player_name = str(profile['player_name'])
    
    print(f"✅ Found player: '{actual_player_name}' - {len(player_data)} matches")
    
    # Helper function to safely convert values
    def safe_str(val):
        if pd.isna(val) or val is None or str(val).strip() in ['', 'nan', 'NaN', 'None']:
            return ''
        return str(val).strip()
    
    def safe_int(val):
        try:
            if pd.isna(val) or val is None or val == '':
                return 0
            return int(float(val))
        except:
            return 0
    
    def safe_float(val):
        try:
            if pd.isna(val) or val is None or val == '':
                return 0.0
            return float(val)
        except:
            return 0.0
    
    # Convert recent matches safely - replace NaN with None
    recent_matches_df = player_data.head(10).fillna('')  # Replace NaN with empty string
    recent_matches = recent_matches_df.to_dict('records')
    
    # Build response with safe conversions
    response_data = {
        'player_name': actual_player_name,
        'full_name': safe_str(profile.get('full_name')) or actual_player_name,
        'photo_url': get_player_photo_url(actual_player_name),  # Use helper function
        'birth_date': safe_str(profile.get('birth_date')),
        'age': safe_int(profile.get('age')),
        'height_cm': f"{safe_int(profile.get('height_cm'))} cm",
        'weight_kg': f"{safe_int(profile.get('weight_kg'))} kg",
        'nationality': safe_str(profile.get('nationality')) or 'Unknown',
        'position': safe_str(profile.get('position')) or 'Unknown',
        'positions_full': safe_str(profile.get('position')) or 'Unknown',
        'preferred_foot': safe_str(profile.get('preferred_foot')) or 'Unknown',
        'overall_rating': safe_int(safe_float(profile.get('market_value_euro')) / 5000000),
        'current_team': safe_str(profile.get('team')) or 'Unknown',
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
        'recent_matches': recent_matches
    }
    
    print(f"📊 Response data created successfully")
    return jsonify(response_data)

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

# ============================================================================
# Player Prediction Route
# ============================================================================

@app.route('/player-prediction', methods=['GET', 'POST'])
def player_prediction():
    prediction = None
    error_message = None
    
    # Check if model is loaded
    if prediction_model is None or prediction_scaler is None:
        error_message = "Prediction model not loaded. Please check model.pkl file."
    
    if request.method == 'POST' and error_message is None:
        try:
            # Get form data
            age = float(request.form['age'])
            position = request.form['position']
            minutes_played = float(request.form['minutes_played'])
            goals = float(request.form['goals'])
            assists = float(request.form['assists'])
            shots = float(request.form['shots'])
            shots_on_target = float(request.form['shots_on_target'])
            passes = float(request.form['passes'])
            pass_accuracy = float(request.form['pass_accuracy'])
            tackles = float(request.form['tackles'])
            interceptions = float(request.form.get('interceptions', 0))
            dribbles = float(request.form.get('dribbles', 0))
            
            # Create DataFrame with proper feature names (this fixes the warning)
            features_df = pd.DataFrame({
                'minutes_played': [minutes_played],
                'goals': [goals],
                'assists': [assists],
                'shots': [shots],
                'shots_on_target': [shots_on_target],
                'passes_completed': [passes],
                'pass_accuracy': [pass_accuracy],
                'tackles': [tackles],
                'interceptions': [interceptions],
                'dribbles_completed': [dribbles]
            })
            
            # Scale features and predict
            features_scaled = prediction_scaler.transform(features_df)
            performance_score = prediction_model.predict(features_scaled)[0]
            
            # Calculate market value estimate (simplified formula)
            # Based on age, position, and performance
            base_value = performance_score * 2
            
            # Age factor (peak at 25-28)
            if 25 <= age <= 28:
                age_factor = 1.2
            elif age < 23:
                age_factor = 1.0
            elif age > 32:
                age_factor = 0.6
            else:
                age_factor = 0.9
            
            # Position factor
            position_factors = {'FW': 1.3, 'MF': 1.0, 'DF': 0.8, 'GK': 0.7}
            position_factor = position_factors.get(position, 1.0)
            
            market_value = round(base_value * age_factor * position_factor, 1)
            
            prediction = {
                'performance_score': round(performance_score, 2),
                'market_value': market_value
            }
            
        except Exception as e:
            print(f"Error in prediction: {e}")
            import traceback
            traceback.print_exc()
            error_message = f"Prediction error: {str(e)}"
    
    return render_template('player_prediction.html', prediction=prediction, error=error_message)

if __name__ == '__main__':
    print("=" * 80)
    print("⚽ PREMIER LEAGUE STATISTICS 2024-25")
    print("=" * 80)
    print("\n✅ REAL Premier League Players & Matches")
    print("⚽ 380 Matches from 2024-25 Season")
    print("👥 562 Real Players with Accurate Stats")
    print("🏆 Top Scorers: Salah (29), Isak (23), Haaland (22)")
    print("🌓 Dark/Light Mode on All Pages")
    print("🎯 Player Performance Prediction Available")
    print(f"📸 {len(PLAYER_PHOTOS)} Player Photos Loaded")
    print("\n🚀 http://localhost:8080")
    print("=" * 80)
    
    # Load Premier League matches
    load_premier_league_matches_data()
    
    # Load prediction model
    load_prediction_model()
    
    app.run(debug=True, host='0.0.0.0', port=8080)
