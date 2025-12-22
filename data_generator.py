"""
Generate synthetic football player statistics data for demonstration
"""

import pandas as pd
import numpy as np
from typing import Tuple

np.random.seed(42)


def generate_player_data(n_players: int = 100, n_matches: int = 10) -> pd.DataFrame:
    """
    Generate synthetic player statistics data
    
    Args:
        n_players: Number of players to generate
        n_matches: Number of matches per player
    
    Returns:
        DataFrame with player statistics
    """
    data = []
    
    player_names = [f"Player_{i+1}" for i in range(n_players)]
    positions = ['Forward', 'Midfielder', 'Defender', 'Goalkeeper']
    
    for player_id, player_name in enumerate(player_names):
        position = np.random.choice(positions)
        
        for match in range(n_matches):
            # Base stats depending on position
            if position == 'Forward':
                minutes = np.random.randint(60, 95)
                goals = np.random.poisson(0.5)
                assists = np.random.poisson(0.3)
                shots = np.random.randint(2, 8)
                shots_on_target = np.random.randint(1, shots + 1)
                passes_completed = np.random.randint(20, 50)
                total_passes = np.random.randint(passes_completed, passes_completed + 20)
                tackles = np.random.randint(0, 3)
                interceptions = np.random.randint(0, 3)
                dribbles_completed = np.random.randint(2, 8)
                
            elif position == 'Midfielder':
                minutes = np.random.randint(70, 95)
                goals = np.random.poisson(0.2)
                assists = np.random.poisson(0.4)
                shots = np.random.randint(1, 5)
                shots_on_target = np.random.randint(0, shots + 1)
                passes_completed = np.random.randint(40, 80)
                total_passes = np.random.randint(passes_completed, passes_completed + 25)
                tackles = np.random.randint(2, 6)
                interceptions = np.random.randint(2, 6)
                dribbles_completed = np.random.randint(1, 5)
                
            elif position == 'Defender':
                minutes = np.random.randint(75, 95)
                goals = np.random.poisson(0.05)
                assists = np.random.poisson(0.1)
                shots = np.random.randint(0, 2)
                shots_on_target = np.random.randint(0, shots + 1)
                passes_completed = np.random.randint(30, 60)
                total_passes = np.random.randint(passes_completed, passes_completed + 20)
                tackles = np.random.randint(4, 10)
                interceptions = np.random.randint(3, 8)
                dribbles_completed = np.random.randint(0, 2)
                
            else:  # Goalkeeper
                minutes = np.random.randint(85, 95)
                goals = 0
                assists = 0
                shots = 0
                shots_on_target = 0
                passes_completed = np.random.randint(20, 40)
                total_passes = np.random.randint(passes_completed, passes_completed + 15)
                tackles = 0
                interceptions = np.random.randint(0, 2)
                dribbles_completed = 0
            
            pass_accuracy = (passes_completed / total_passes * 100) if total_passes > 0 else 0
            
            # Calculate performance rating based on stats
            performance_rating = (
                goals * 10 + 
                assists * 7 + 
                (shots_on_target / max(shots, 1)) * 5 +
                pass_accuracy * 0.3 +
                tackles * 2 +
                interceptions * 2 +
                dribbles_completed * 1.5 +
                np.random.normal(0, 5)  # Add some noise
            )
            performance_rating = max(0, min(100, performance_rating))  # Clamp between 0-100
            
            data.append({
                'player_id': player_id,
                'player_name': player_name,
                'position': position,
                'match_id': match,
                'minutes_played': minutes,
                'goals': goals,
                'assists': assists,
                'shots': shots,
                'shots_on_target': shots_on_target,
                'passes_completed': passes_completed,
                'total_passes': total_passes,
                'pass_accuracy': round(pass_accuracy, 2),
                'tackles': tackles,
                'interceptions': interceptions,
                'dribbles_completed': dribbles_completed,
                'performance_rating': round(performance_rating, 2),
            })
    
    return pd.DataFrame(data)


def generate_heatmap_data(player_name: str, n_positions: int = 200) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate synthetic heatmap data for a player's field coverage
    
    Args:
        player_name: Name of the player
        n_positions: Number of position points to generate
    
    Returns:
        Tuple of (x_positions, y_positions) arrays
    """
    # Use player name hash for reproducibility
    seed = hash(player_name) % (2**32)
    np.random.seed(seed)
    
    # Generate positions with some clustering (realistic player movement)
    # Center of activity
    center_x = np.random.uniform(30, 75)
    center_y = np.random.uniform(20, 48)
    
    # Generate positions around the center with some spread
    x_positions = np.random.normal(center_x, 15, n_positions)
    y_positions = np.random.normal(center_y, 10, n_positions)
    
    # Clip to field boundaries
    x_positions = np.clip(x_positions, 0, 105)
    y_positions = np.clip(y_positions, 0, 68)
    
    return x_positions, y_positions


if __name__ == "__main__":
    # Generate and save sample data
    df = generate_player_data(n_players=50, n_matches=20)
    df.to_csv('player_statistics.csv', index=False)
    print(f"Generated {len(df)} records for {df['player_name'].nunique()} players")
    print(f"\nSample data:\n{df.head()}")
    print(f"\nData info:\n{df.describe()}")

