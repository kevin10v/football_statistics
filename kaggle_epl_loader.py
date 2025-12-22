"""
Load English Premier League Player Statistics from Kaggle
Dataset: https://www.kaggle.com/code/desalegngeb/english-premier-league-players-statistics
"""

import pandas as pd
import numpy as np
import os
from typing import Optional
import requests


def download_kaggle_dataset_instructions():
    """
    Print instructions for downloading the Kaggle dataset
    """
    print("\n" + "=" * 70)
    print("📥 KAGGLE DATASET DOWNLOAD INSTRUCTIONS")
    print("=" * 70)
    print("\n🔗 Dataset URL:")
    print("   https://www.kaggle.com/code/desalegngeb/english-premier-league-players-statistics")
    print("\n📋 How to Download:")
    print("   1. Visit the URL above")
    print("   2. Click 'Data' tab on the right side")
    print("   3. Click 'Download' button")
    print("   4. Save the CSV file to this project folder")
    print("\n💡 Or use Kaggle API:")
    print("   pip install kaggle")
    print("   kaggle datasets download -d [dataset-name]")
    print("\n" + "=" * 70 + "\n")


def find_epl_dataset() -> Optional[str]:
    """
    Search for EPL dataset file in the project directory
    
    Returns:
        Path to the dataset file if found, None otherwise
    """
    # Common file patterns for EPL datasets
    patterns = [
        'epl_players*.csv',
        'premier_league*.csv',
        'english_premier*.csv',
        'pl_players*.csv',
        'players_stats*.csv',
        'EPL*.csv',
    ]
    
    # Check current directory
    for file in os.listdir('.'):
        if file.endswith('.csv'):
            for pattern in patterns:
                if pattern.replace('*', '').lower() in file.lower():
                    print(f"✅ Found dataset: {file}")
                    return file
    
    return None


def create_sample_epl_data() -> pd.DataFrame:
    """
    Create sample EPL data with realistic 2024-2025 statistics
    Based on actual Premier League players and performance patterns
    """
    print("📊 Creating sample EPL data with real player names...")
    
    # Top 30 EPL players for 2024-2025 season
    epl_players = [
        # Manchester City
        {"name": "Erling Haaland", "team": "Manchester City", "position": "FW", "nationality": "Norway"},
        {"name": "Kevin De Bruyne", "team": "Manchester City", "position": "MF", "nationality": "Belgium"},
        {"name": "Phil Foden", "team": "Manchester City", "position": "MF", "nationality": "England"},
        {"name": "Bernardo Silva", "team": "Manchester City", "position": "MF", "nationality": "Portugal"},
        
        # Liverpool
        {"name": "Mohamed Salah", "team": "Liverpool", "position": "FW", "nationality": "Egypt"},
        {"name": "Luis Diaz", "team": "Liverpool", "position": "FW", "nationality": "Colombia"},
        {"name": "Darwin Nunez", "team": "Liverpool", "position": "FW", "nationality": "Uruguay"},
        {"name": "Alexis Mac Allister", "team": "Liverpool", "position": "MF", "nationality": "Argentina"},
        
        # Arsenal
        {"name": "Bukayo Saka", "team": "Arsenal", "position": "FW", "nationality": "England"},
        {"name": "Martin Odegaard", "team": "Arsenal", "position": "MF", "nationality": "Norway"},
        {"name": "Gabriel Martinelli", "team": "Arsenal", "position": "FW", "nationality": "Brazil"},
        {"name": "Kai Havertz", "team": "Arsenal", "position": "MF", "nationality": "Germany"},
        
        # Chelsea
        {"name": "Cole Palmer", "team": "Chelsea", "position": "MF", "nationality": "England"},
        {"name": "Nicolas Jackson", "team": "Chelsea", "position": "FW", "nationality": "Senegal"},
        {"name": "Enzo Fernandez", "team": "Chelsea", "position": "MF", "nationality": "Argentina"},
        {"name": "Raheem Sterling", "team": "Chelsea", "position": "FW", "nationality": "England"},
        
        # Manchester United
        {"name": "Bruno Fernandes", "team": "Manchester United", "position": "MF", "nationality": "Portugal"},
        {"name": "Rasmus Hojlund", "team": "Manchester United", "position": "FW", "nationality": "Denmark"},
        {"name": "Marcus Rashford", "team": "Manchester United", "position": "FW", "nationality": "England"},
        {"name": "Alejandro Garnacho", "team": "Manchester United", "position": "FW", "nationality": "Argentina"},
        
        # Tottenham
        {"name": "Son Heung-min", "team": "Tottenham", "position": "FW", "nationality": "South Korea"},
        {"name": "James Maddison", "team": "Tottenham", "position": "MF", "nationality": "England"},
        {"name": "Dejan Kulusevski", "team": "Tottenham", "position": "FW", "nationality": "Sweden"},
        {"name": "Brennan Johnson", "team": "Tottenham", "position": "FW", "nationality": "Wales"},
        
        # Newcastle
        {"name": "Alexander Isak", "team": "Newcastle", "position": "FW", "nationality": "Sweden"},
        {"name": "Anthony Gordon", "team": "Newcastle", "position": "FW", "nationality": "England"},
        {"name": "Bruno Guimaraes", "team": "Newcastle", "position": "MF", "nationality": "Brazil"},
        
        # Aston Villa
        {"name": "Ollie Watkins", "team": "Aston Villa", "position": "FW", "nationality": "England"},
        {"name": "John McGinn", "team": "Aston Villa", "position": "MF", "nationality": "Scotland"},
        {"name": "Moussa Diaby", "team": "Aston Villa", "position": "FW", "nationality": "France"},
    ]
    
    # Generate match statistics
    np.random.seed(42)
    data = []
    
    for player_info in epl_players:
        # Generate 18-20 matches (typical for mid-season)
        num_matches = np.random.randint(18, 21)
        
        for match in range(num_matches):
            # Position-based statistics
            if player_info['position'] == 'FW':
                goals = np.random.choice([0, 0, 1, 1, 2], p=[0.25, 0.35, 0.25, 0.1, 0.05])
                assists = np.random.choice([0, 0, 1], p=[0.65, 0.25, 0.1])
                shots = np.random.randint(2, 8)
                shots_on_target = np.random.randint(1, min(shots + 1, 6))
                passes = np.random.randint(20, 50)
                key_passes = np.random.randint(0, 4)
                tackles = np.random.randint(0, 3)
                interceptions = np.random.randint(0, 2)
                dribbles = np.random.randint(2, 8)
                fouls = np.random.randint(0, 3)
                
            else:  # Midfielder
                goals = np.random.choice([0, 0, 0, 1], p=[0.75, 0.15, 0.07, 0.03])
                assists = np.random.choice([0, 0, 1, 1], p=[0.55, 0.25, 0.15, 0.05])
                shots = np.random.randint(1, 5)
                shots_on_target = np.random.randint(0, min(shots + 1, 4))
                passes = np.random.randint(45, 95)
                key_passes = np.random.randint(1, 5)
                tackles = np.random.randint(2, 7)
                interceptions = np.random.randint(2, 6)
                dribbles = np.random.randint(1, 5)
                fouls = np.random.randint(0, 3)
            
            minutes = np.random.randint(70, 95)
            total_passes = passes + np.random.randint(5, 20)
            pass_accuracy = (passes / total_passes * 100) if total_passes > 0 else 0
            
            # Calculate performance rating (0-100)
            performance_rating = (
                goals * 10 + 
                assists * 7 + 
                (shots_on_target / max(shots, 1)) * 5 +
                pass_accuracy * 0.25 +
                tackles * 1.5 +
                interceptions * 1.5 +
                dribbles * 1.2 +
                key_passes * 2 +
                np.random.normal(0, 3)
            )
            performance_rating = max(0, min(100, performance_rating))
            
            data.append({
                'player_name': player_info['name'],
                'team': player_info['team'],
                'position': player_info['position'],
                'nationality': player_info['nationality'],
                'league': 'Premier League',
                'match_id': match + 1,
                'minutes_played': minutes,
                'goals': goals,
                'assists': assists,
                'shots': shots,
                'shots_on_target': shots_on_target,
                'passes_completed': passes,
                'total_passes': total_passes,
                'pass_accuracy': round(pass_accuracy, 2),
                'key_passes': key_passes,
                'tackles': tackles,
                'interceptions': interceptions,
                'dribbles_completed': dribbles,
                'fouls_committed': fouls,
                'performance_rating': round(performance_rating, 2),
            })
    
    df = pd.DataFrame(data)
    print(f"✅ Created EPL dataset: {len(df)} records for {len(epl_players)} players")
    return df


def process_kaggle_epl_data(file_path: str) -> pd.DataFrame:
    """
    Process the downloaded Kaggle EPL dataset
    
    Args:
        file_path: Path to the CSV file
        
    Returns:
        Processed DataFrame
    """
    print(f"📖 Reading dataset from: {file_path}")
    
    try:
        df = pd.read_csv(file_path)
        print(f"✅ Loaded {len(df)} rows, {len(df.columns)} columns")
        
        print("\n📋 Available columns:")
        print(df.columns.tolist())
        
        # Common EPL dataset column mappings
        column_mappings = {
            # Player info
            'Player': 'player_name',
            'Name': 'player_name',
            'player': 'player_name',
            'Team': 'team',
            'Squad': 'team',
            'Club': 'team',
            'Position': 'position',
            'Pos': 'position',
            'Nation': 'nationality',
            'Nationality': 'nationality',
            
            # Performance stats
            'Goals': 'goals',
            'Gls': 'goals',
            'Assists': 'assists',
            'Ast': 'assists',
            'Matches': 'matches_played',
            'MP': 'matches_played',
            'Minutes': 'minutes_played',
            'Min': 'minutes_played',
            '90s': 'matches_90s',
            
            # Shooting
            'Shots': 'shots',
            'Sh': 'shots',
            'SoT': 'shots_on_target',
            'SoT%': 'shot_accuracy',
            
            # Passing
            'Passes': 'passes_completed',
            'Pass%': 'pass_accuracy',
            'Cmp': 'passes_completed',
            'Att': 'total_passes',
            'KP': 'key_passes',
            
            # Defense
            'Tackles': 'tackles',
            'Tkl': 'tackles',
            'Int': 'interceptions',
            'Interceptions': 'interceptions',
            
            # Dribbling
            'Dribbles': 'dribbles_completed',
            'Succ': 'dribbles_completed',
            
            # Discipline
            'Fouls': 'fouls_committed',
            'Fls': 'fouls_committed',
            'Yellow': 'yellow_cards',
            'Red': 'red_cards',
        }
        
        # Rename columns
        df_processed = df.copy()
        for old_col, new_col in column_mappings.items():
            if old_col in df.columns:
                df_processed.rename(columns={old_col: new_col}, inplace=True)
                print(f"   ✓ Mapped: {old_col} -> {new_col}")
        
        # Ensure required columns exist
        required_columns = ['player_name', 'team', 'position']
        missing = [col for col in required_columns if col not in df_processed.columns]
        
        if missing:
            print(f"\n⚠️  Missing required columns: {missing}")
            print("   Using sample data instead...")
            return create_sample_epl_data()
        
        # Add league info
        if 'league' not in df_processed.columns:
            df_processed['league'] = 'Premier League'
        
        # Calculate performance rating if not present
        if 'performance_rating' not in df_processed.columns:
            print("\n🔄 Calculating performance ratings...")
            df_processed['performance_rating'] = calculate_performance_rating(df_processed)
        
        return df_processed
        
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        print("   Using sample data instead...")
        return create_sample_epl_data()


def calculate_performance_rating(df: pd.DataFrame) -> pd.Series:
    """
    Calculate performance rating from available stats
    """
    rating = pd.Series(0.0, index=df.index)
    
    # Add points for different contributions
    if 'goals' in df.columns:
        rating += df['goals'] * 10
    if 'assists' in df.columns:
        rating += df['assists'] * 7
    if 'pass_accuracy' in df.columns:
        rating += df['pass_accuracy'] * 0.25
    if 'tackles' in df.columns:
        rating += df['tackles'] * 1.5
    if 'interceptions' in df.columns:
        rating += df['interceptions'] * 1.5
    if 'dribbles_completed' in df.columns:
        rating += df['dribbles_completed'] * 1.2
    
    # Normalize to 0-100 range
    if rating.max() > 0:
        rating = (rating / rating.max() * 100).clip(0, 100)
    
    return rating.round(2)


def load_epl_data(save_path: str = 'player_statistics_epl.csv') -> pd.DataFrame:
    """
    Main function to load EPL data from Kaggle
    
    Args:
        save_path: Path to save the processed data
        
    Returns:
        Processed DataFrame
    """
    print("\n" + "=" * 70)
    print("⚽ LOADING ENGLISH PREMIER LEAGUE DATA (2024-2025)")
    print("=" * 70 + "\n")
    
    # Check if data file already exists
    if os.path.exists(save_path):
        print(f"✅ Found existing EPL data: {save_path}")
        df = pd.read_csv(save_path)
        print(f"   {len(df)} records, {df['player_name'].nunique()} unique players")
        return df
    
    # Try to find downloaded dataset
    dataset_file = find_epl_dataset()
    
    if dataset_file:
        df = process_kaggle_epl_data(dataset_file)
    else:
        print("⚠️  No Kaggle dataset found in project directory")
        download_kaggle_dataset_instructions()
        print("📊 Creating sample EPL data instead...")
        df = create_sample_epl_data()
    
    # Save processed data
    df.to_csv(save_path, index=False)
    print(f"\n💾 Saved EPL data to: {save_path}")
    
    # Display summary
    print("\n📊 Dataset Summary:")
    print(f"   Total Records: {len(df)}")
    print(f"   Unique Players: {df['player_name'].nunique()}")
    print(f"   Teams: {df['team'].nunique()}")
    if 'nationality' in df.columns:
        print(f"   Nationalities: {df['nationality'].nunique()}")
    
    print("\n🎯 Top Players by Performance:")
    if 'performance_rating' in df.columns:
        top_players = df.groupby('player_name')['performance_rating'].mean().sort_values(ascending=False).head(10)
        for i, (player, rating) in enumerate(top_players.items(), 1):
            print(f"   {i}. {player}: {rating:.2f}")
    
    print("\n✅ EPL data loaded successfully!")
    print("=" * 70 + "\n")
    
    return df


if __name__ == "__main__":
    # Load and display EPL data
    df = load_epl_data()
    
    print("\n📋 Sample Data:")
    print(df.head(10))
    
    print("\n🚀 Next Steps:")
    print("   1. Run: python train_model_epl.py")
    print("   2. Run: python app_epl.py")
    print("   3. Open: http://localhost:8080")

