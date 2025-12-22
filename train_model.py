"""
Script to train the ML model
"""

from data_generator import generate_player_data
from model import train_and_save_model
import os


def main():
    """Generate data and train model"""
    
    print("=" * 60)
    print("Football Player Performance Prediction - Model Training")
    print("=" * 60)
    
    # Check if data exists, if not generate it
    if not os.path.exists('player_statistics.csv'):
        print("\n📊 Generating synthetic player data...")
        df = generate_player_data(n_players=50, n_matches=20)
        df.to_csv('player_statistics.csv', index=False)
        print(f"✅ Generated {len(df)} records for {df['player_name'].nunique()} players")
    else:
        print("\n✅ Data file already exists")
    
    # Train model
    print("\n🤖 Training ML model...")
    model, metrics = train_and_save_model('player_statistics.csv')
    
    print("\n" + "=" * 60)
    print("✅ Training Complete!")
    print("=" * 60)
    print("\nYou can now run the dashboard with: streamlit run dashboard.py")


if __name__ == "__main__":
    main()

