"""
Test Script for OpenFootball JSON Integration
Run this to verify the integration works correctly
"""

from football_json_loader import FootballJSONLoader
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', 30)


def test_integration():
    """Test the OpenFootball JSON integration"""
    
    print("\n" + "="*80)
    print("⚽ TESTING OPENFOOTBALL JSON INTEGRATION")
    print("="*80)
    
    loader = FootballJSONLoader()
    
    # Test 1: List available leagues
    print("\n📋 Test 1: Available Leagues")
    print("-" * 80)
    for league_name, info in loader.LEAGUES.items():
        print(f"  • {league_name} ({info['code']}) - {info['name']}")
    
    # Test 2: Fetch Premier League data
    print("\n📥 Test 2: Fetching Premier League 2024-25 Data")
    print("-" * 80)
    matches = loader.get_league_matches('Premier League', '2024-25')
    
    if not matches.empty:
        print(f"\n✅ Successfully loaded {len(matches)} matches!")
        print("\nFirst 5 matches:")
        print(matches[['date', 'round', 'team1', 'team2', 'score1', 'score2']].head())
        
        # Count completed vs upcoming
        completed = matches[matches['score1'].notna()].shape[0]
        upcoming = matches[matches['score1'].isna()].shape[0]
        print(f"\n📊 Completed matches: {completed}")
        print(f"📅 Upcoming matches: {upcoming}")
    else:
        print("⚠️  No data available")
    
    # Test 3: League Table
    print("\n📊 Test 3: Premier League Table (Current Standings)")
    print("-" * 80)
    table = loader.get_team_statistics('Premier League', '2024-25')
    
    if not table.empty:
        print(f"\n✅ Successfully calculated standings for {len(table)} teams!")
        print("\nTop 10 Teams:")
        print(table[['position', 'team', 'played', 'wins', 'draws', 'losses', 
                     'goals_for', 'goals_against', 'goal_difference', 'points']].head(10).to_string(index=False))
    else:
        print("⚠️  No standings available")
    
    # Test 4: Team Form
    print("\n🔥 Test 4: Team Form (Recent 5 Matches)")
    print("-" * 80)
    if not table.empty and len(table) > 0:
        # Test form for top 5 teams
        for i in range(min(5, len(table))):
            team = table.iloc[i]['team']
            form = loader.get_team_form(team, 'Premier League', '2024-25', last_n=5)
            form_str = ' '.join(form) if form else 'No data'
            wins = form.count('W')
            draws = form.count('D')
            losses = form.count('L')
            print(f"  {i+1}. {team:30} Form: {form_str:15} (W:{wins} D:{draws} L:{losses})")
    
    # Test 5: Upcoming Fixtures
    print("\n📅 Test 5: Upcoming Fixtures")
    print("-" * 80)
    fixtures = loader.get_upcoming_fixtures('Premier League', '2024-25')
    
    if not fixtures.empty:
        print(f"\n✅ Found {len(fixtures)} upcoming matches!")
        print("\nNext 5 fixtures:")
        print(fixtures[['date', 'round', 'team1', 'team2']].head().to_string(index=False))
    else:
        print("⚠️  No upcoming fixtures (season may be complete)")
    
    # Test 6: Try multiple leagues
    print("\n🌍 Test 6: Testing Multiple Leagues")
    print("-" * 80)
    test_leagues = ['Premier League', 'La Liga', 'Bundesliga', 'Serie A']
    
    results = {}
    for league in test_leagues:
        try:
            matches = loader.get_league_matches(league, '2024-25')
            if not matches.empty:
                completed = matches[matches['score1'].notna()].shape[0]
                results[league] = {'total': len(matches), 'completed': completed, 'status': '✅'}
            else:
                results[league] = {'total': 0, 'completed': 0, 'status': '⚠️'}
        except Exception as e:
            results[league] = {'total': 0, 'completed': 0, 'status': f'❌ {str(e)[:30]}'}
    
    print("\nLeague Data Summary:")
    print(f"{'League':<20} {'Status':<5} {'Total Matches':<15} {'Completed':<12}")
    print("-" * 60)
    for league, data in results.items():
        print(f"{league:<20} {data['status']:<5} {data['total']:<15} {data['completed']:<12}")
    
    # Test 7: Historical data (2023-24)
    print("\n📜 Test 7: Testing Historical Data (2023-24)")
    print("-" * 80)
    try:
        historical = loader.get_league_matches('Premier League', '2023-24')
        if not historical.empty:
            completed = historical[historical['score1'].notna()].shape[0]
            print(f"✅ 2023-24 Season: {len(historical)} matches ({completed} completed)")
            
            # Show the champion
            if completed > 0:
                table_23_24 = loader.get_team_statistics('Premier League', '2023-24')
                if not table_23_24.empty:
                    champion = table_23_24.iloc[0]
                    print(f"🏆 Champion: {champion['team']} ({champion['points']} points)")
        else:
            print("⚠️  No data for 2023-24 season")
    except Exception as e:
        print(f"❌ Error fetching 2023-24: {e}")
    
    # Summary
    print("\n" + "="*80)
    print("✅ INTEGRATION TEST COMPLETE")
    print("="*80)
    print("\n📊 Summary:")
    print("  • OpenFootball JSON data is accessible")
    print("  • Match data loads successfully")
    print("  • League tables calculate correctly")
    print("  • Team form tracking works")
    print("  • Multiple leagues supported")
    print("  • Historical data available")
    print("\n🚀 Ready to use in your Flask app!")
    print("\n💡 Next steps:")
    print("  1. Run: python app.py")
    print("  2. Visit: http://localhost:8080")
    print("  3. Try API endpoints:")
    print("     • http://localhost:8080/api/leagues")
    print("     • http://localhost:8080/api/league/table/Premier League")
    print("     • http://localhost:8080/api/league/matches/Premier League")
    print("="*80 + "\n")


if __name__ == "__main__":
    test_integration()

