"""
Train model on Transfermarkt current season data
"""

from load_data import create_transfermarkt_based_database
from model import train_and_save_model
import os


def main():
    print("=" * 80)
    print("⚽ Training with TRANSFERMARKT DATA")
    print("=" * 80)
    
    if not os.path.exists('player_data.csv'):
        print("\n📊 Creating player database...")
        df = create_transfermarkt_based_database()
    else:
        print("\n✅ Database exists")
    
    print("\n🤖 Training model...")
    model, metrics = train_and_save_model('player_data.csv')
    
    model.save_model('model.pkl')
    
    print("\n✅ Training complete!")
    print("🚀 Run: python app.py")


if __name__ == "__main__":
    main()

