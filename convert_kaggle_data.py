"""
Convert Kaggle EPL Player Stats to Our Format
Real Premier League 2024-25 Season Data
"""

import pandas as pd
import numpy as np

def convert_kaggle_to_our_format():
    """Convert Kaggle dataset to our application format"""
    
    # Load Kaggle dataset
    kaggle_df = pd.read_csv('epl_player_stats_24_25.csv')
    
    print(f"📥 Loaded {len(kaggle_df)} players from Kaggle dataset")
    
    # Convert to our format
    converted_data = []
    
    for _, player in kaggle_df.iterrows():
        # Calculate pass accuracy (handle string percentages)
        try:
            pass_acc = player['Passes%']
            if pd.isna(pass_acc):
                pass_accuracy = 75.0
            elif isinstance(pass_acc, str):
                pass_accuracy = float(pass_acc.replace('%', '').strip())
            else:
                pass_accuracy = float(pass_acc)
        except:
            pass_accuracy = 75.0
        
        # Calculate performance rating
        goals = int(player['Goals']) if not pd.isna(player['Goals']) else 0
        assists = int(player['Assists']) if not pd.isna(player['Assists']) else 0
        minutes = int(player['Minutes']) if not pd.isna(player['Minutes']) else 0
        tackles = int(player['Tackles']) if not pd.isna(player['Tackles']) else 0
        interceptions = int(player['Interceptions']) if not pd.isna(player['Interceptions']) else 0
        
        performance_rating = (
            goals * 10 +
            assists * 7 +
            pass_accuracy * 0.3 +
            tackles * 1.5 +
            interceptions * 1.5
        )
        performance_rating = min(100, max(0, performance_rating))
        
        # Create match records (one summary record per player)
        converted_data.append({
            'player_name': player['Player Name'],
            'full_name': player['Player Name'],
            'photo_url': '',  # Will need to add separately
            'team': player['Club'],
            'position': player['Position'] if not pd.isna(player['Position']) else 'Unknown',
            'nationality': player['Nationality'] if not pd.isna(player['Nationality']) else 'Unknown',
            'age': 25,  # Default age
            'birth_date': '1999-01-01',
            'height_cm': 180,
            'weight_kg': 75,
            'preferred_foot': 'Right',
            'league': 'Premier League',
            'season': '2024-2025',
            'match_id': 1,
            'minutes_played': int(minutes) if not pd.isna(minutes) else 0,
            'goals': int(goals),
            'assists': int(assists),
            'shots': int(player['Shots']) if not pd.isna(player['Shots']) else 0,
            'shots_on_target': int(player['Shots On Target']) if not pd.isna(player['Shots On Target']) else 0,
            'passes_completed': int(player['Successful Passes']) if not pd.isna(player['Successful Passes']) else 0,
            'total_passes': int(player['Passes']) if not pd.isna(player['Passes']) else 0,
            'pass_accuracy': round(pass_accuracy, 2),
            'tackles': int(player['Tackles']) if not pd.isna(player['Tackles']) else 0,
            'interceptions': int(player['Interceptions']) if not pd.isna(player['Interceptions']) else 0,
            'dribbles_completed': int(player['Progressive Carries']) if not pd.isna(player['Progressive Carries']) else 0,
            'performance_rating': round(performance_rating, 2),
            'market_value_euro': 1000000,
            'number': 0,
        })
    
    df = pd.DataFrame(converted_data)
    
    # Save to CSV
    df.to_csv('player_data.csv', index=False)
    
    print(f"\n✅ Converted dataset saved!")
    print(f"📊 Total players: {len(df)}")
    print(f"⚽ Top 10 scorers:")
    top_scorers = df.nlargest(10, 'goals')[['player_name', 'team', 'goals']]
    for i, row in top_scorers.iterrows():
        print(f"   {row['goals']:2d} goals - {row['player_name']} ({row['team']})")
    
    return df


if __name__ == "__main__":
    df = convert_kaggle_to_our_format()
    print(f"\n✅ Real Premier League 2024-25 data ready!")
    print(f"💾 Saved to: player_data.csv")
