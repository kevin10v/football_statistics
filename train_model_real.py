"""
Train ML model using real 2024-2025 season data
"""

from real_data_loader import load_real_data
from model import train_and_save_model
import os


def main():
    """Load real data and train model"""
    
    print("=" * 60)
    print("⚽ Training Model with REAL 2024-2025 Season Data")
    print("=" * 60)
    
    # Load real data
    if not os.path.exists('player_statistics_real.csv'):
        print("\n📥 Loading real 2024-2025 season data...")
        df = load_real_data('player_statistics_real.csv')
    else:
        print("\n✅ Real data file already exists")
        print("   Using: player_statistics_real.csv")
    
    # Train model with real data
    print("\n🤖 Training ML model with real data...")
    model, metrics = train_and_save_model('player_statistics_real.csv')
    
    # Save model with different name
    print("\n💾 Saving model trained on real data...")
    model.save_model('player_performance_model_real.pkl')
    
    print("\n" + "=" * 60)
    print("✅ Training Complete with Real Data!")
    print("=" * 60)
    print("\n🎯 Next Steps:")
    print("   1. The model is now trained on real 2024-2025 season data")
    print("   2. Run: python app_real.py")
    print("   3. Or update app.py to use 'player_statistics_real.csv'")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()

