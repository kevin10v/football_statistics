"""
Train ML model using English Premier League 2024-2025 data
"""

from kaggle_epl_loader import load_epl_data
from model import train_and_save_model
import os


def main():
    """Load EPL data and train model"""
    
    print("=" * 70)
    print("⚽ Training Model with EPL 2024-2025 Season Data")
    print("=" * 70)
    
    # Load EPL data
    if not os.path.exists('player_statistics_epl.csv'):
        print("\n📥 Loading EPL 2024-2025 season data...")
        df = load_epl_data('player_statistics_epl.csv')
    else:
        print("\n✅ EPL data file already exists")
        print("   Using: player_statistics_epl.csv")
    
    # Train model with EPL data
    print("\n🤖 Training ML model with EPL data...")
    model, metrics = train_and_save_model('player_statistics_epl.csv')
    
    # Save model
    print("\n💾 Saving EPL-trained model...")
    model.save_model('player_performance_model_epl.pkl')
    
    print("\n" + "=" * 70)
    print("✅ Training Complete with EPL Data!")
    print("=" * 70)
    print("\n🎯 Next Steps:")
    print("   Run: python app_epl.py")
    print("   Open: http://localhost:8080")
    print("\n📊 Players available:")
    print("   • Erling Haaland (Manchester City)")
    print("   • Mohamed Salah (Liverpool)")
    print("   • Bukayo Saka (Arsenal)")
    print("   • Cole Palmer (Chelsea)")
    print("   • Son Heung-min (Tottenham)")
    print("   ...and 25 more EPL stars!")
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()

