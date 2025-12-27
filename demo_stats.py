"""
Demo Script - Interesting Football Statistics
Shows what you can do with the OpenFootball JSON integration
"""

from football_json_loader import FootballJSONLoader
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 120)


def print_header(title):
    """Print a nice header"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80)


def demo_interesting_stats():
    """Show some interesting football statistics"""
    
    loader = FootballJSONLoader()
    
    print_header("⚽ INTERESTING FOOTBALL STATISTICS - 2024-25 Season")
    
    # Load data for multiple leagues
    leagues = ['Premier League', 'La Liga', 'Bundesliga', 'Serie A']
    all_tables = {}
    
    print("\n📥 Loading data for all major leagues...")
    for league in leagues:
        table = loader.get_team_statistics(league, '2024-25')
        if not table.empty:
            all_tables[league] = table
            print(f"  ✅ {league}: {len(table)} teams")
    
    # 1. Champions of each league
    print_header("🏆 CURRENT LEAGUE LEADERS")
    for league, table in all_tables.items():
        leader = table.iloc[0]
        print(f"\n{league}:")
        print(f"  🥇 {leader['team']}")
        print(f"     Points: {leader['points']} | Wins: {leader['wins']} | "
              f"Goal Diff: +{leader['goal_difference']}")
    
    # 2. Most goals scored
    print_header("⚡ MOST PROLIFIC ATTACK (Goals Scored)")
    all_teams = []
    for league, table in all_tables.items():
        table['league'] = league
        all_teams.append(table)
    
    combined = pd.concat(all_teams, ignore_index=True)
    top_scorers = combined.nlargest(10, 'goals_for')[['team', 'league', 'goals_for', 'played']]
    top_scorers['gpg'] = (top_scorers['goals_for'] / top_scorers['played']).round(2)
    
    print("\nTop 10 teams by goals scored:")
    for i, row in top_scorers.iterrows():
        print(f"  {i+1:2d}. {row['team']:30s} ({row['league']:20s}) "
              f"- {int(row['goals_for']):3d} goals ({row['gpg']} per game)")
    
    # 3. Best defense
    print_header("🛡️ BEST DEFENSE (Fewest Goals Conceded)")
    best_defense = combined.nsmallest(10, 'goals_against')[
        ['team', 'league', 'goals_against', 'played']
    ]
    best_defense['gpg'] = (best_defense['goals_against'] / best_defense['played']).round(2)
    
    print("\nTop 10 teams by defense:")
    for i, row in best_defense.iterrows():
        print(f"  {i+1:2d}. {row['team']:30s} ({row['league']:20s}) "
              f"- {int(row['goals_against']):3d} conceded ({row['gpg']} per game)")
    
    # 4. Most wins
    print_header("💪 MOST WINS")
    most_wins = combined.nlargest(10, 'wins')[['team', 'league', 'wins', 'played']]
    most_wins['win_pct'] = ((most_wins['wins'] / most_wins['played']) * 100).round(1)
    
    print("\nTop 10 teams by wins:")
    for i, row in most_wins.iterrows():
        print(f"  {i+1:2d}. {row['team']:30s} ({row['league']:20s}) "
              f"- {int(row['wins']):2d} wins ({row['win_pct']}%)")
    
    # 5. Best goal difference
    print_header("📊 BEST GOAL DIFFERENCE")
    best_gd = combined.nlargest(10, 'goal_difference')[
        ['team', 'league', 'goal_difference', 'goals_for', 'goals_against']
    ]
    
    print("\nTop 10 teams by goal difference:")
    for i, row in best_gd.iterrows():
        print(f"  {i+1:2d}. {row['team']:30s} ({row['league']:20s}) "
              f"- +{int(row['goal_difference']):2d} ({int(row['goals_for'])}-{int(row['goals_against'])})")
    
    # 6. Team form comparison
    print_header("🔥 CURRENT FORM (Last 5 Matches)")
    
    print("\nTop team from each league:")
    for league, table in all_tables.items():
        top_team = table.iloc[0]['team']
        form = loader.get_team_form(top_team, league, '2024-25', last_n=5)
        wins = form.count('W')
        draws = form.count('D')
        losses = form.count('L')
        form_str = ' '.join(form)
        
        # Color indicators
        if wins >= 4:
            indicator = "🔥 HOT"
        elif wins >= 3:
            indicator = "✅ Good"
        else:
            indicator = "⚠️  Mixed"
        
        print(f"\n{league}:")
        print(f"  {top_team}")
        print(f"  Form: {form_str} (W:{wins} D:{draws} L:{losses}) {indicator}")
    
    # 7. Historical comparison (if available)
    print_header("📜 HISTORICAL COMPARISON: 2023-24 vs 2024-25")
    
    try:
        pl_current = loader.get_team_statistics('Premier League', '2024-25')
        pl_last = loader.get_team_statistics('Premier League', '2023-24')
        
        if not pl_last.empty and not pl_current.empty:
            print("\nPremier League Champions:")
            
            current_leader = pl_current.iloc[0]
            last_champion = pl_last.iloc[0]
            
            print(f"\n2023-24 Champion: {last_champion['team']}")
            print(f"  Points: {last_champion['points']} | Wins: {last_champion['wins']} | "
                  f"Goals: {last_champion['goals_for']}")
            
            print(f"\n2024-25 Leader: {current_leader['team']}")
            print(f"  Points: {current_leader['points']} | Wins: {current_leader['wins']} | "
                  f"Goals: {current_leader['goals_for']}")
            
            # Check if same team
            if current_leader['team'] == last_champion['team']:
                print(f"\n  🏆 {current_leader['team']} defending their title!")
            else:
                print(f"\n  ⚡ New leader! {current_leader['team']} looking to dethrone "
                      f"{last_champion['team']}")
    except Exception as e:
        print(f"\n  ⚠️  Historical data not available: {e}")
    
    # 8. League statistics
    print_header("📈 LEAGUE STATISTICS SUMMARY")
    
    print("\nComparative league stats:")
    print(f"{'League':<20} {'Avg Goals/Game':<15} {'Highest Pts':<12} {'Most Competitive'}")
    print("-" * 80)
    
    for league, table in all_tables.items():
        total_goals = table['goals_for'].sum()
        total_matches = table['played'].sum() / 2  # Divide by 2 (each match counted twice)
        avg_goals = total_goals / total_matches if total_matches > 0 else 0
        highest_pts = table.iloc[0]['points']
        pts_range = table.iloc[0]['points'] - table.iloc[-1]['points']
        
        competitiveness = "Very" if pts_range < 40 else "Moderate" if pts_range < 50 else "Less"
        
        print(f"{league:<20} {avg_goals:<15.2f} {highest_pts:<12} {competitiveness} "
              f"(range: {pts_range} pts)")
    
    # 9. Interesting facts
    print_header("💡 INTERESTING FACTS")
    
    # Find teams with most draws
    most_draws = combined.nlargest(5, 'draws')[['team', 'league', 'draws', 'played']]
    print("\nMost Draw-Happy Teams:")
    for i, row in most_draws.iterrows():
        draw_pct = (row['draws'] / row['played'] * 100)
        print(f"  • {row['team']} ({row['league']}): {int(row['draws'])} draws "
              f"({draw_pct:.1f}% of matches)")
    
    # Find biggest underachievers (good GF but low position)
    print("\nUnlucky Teams (Great Attack, Lower Position):")
    struggling = combined[combined['position'] > 10].nlargest(5, 'goals_for')[
        ['team', 'league', 'position', 'goals_for', 'goals_against']
    ]
    for i, row in struggling.iterrows():
        print(f"  • {row['team']} ({row['league']}): "
              f"#{int(row['position'])} despite {int(row['goals_for'])} goals scored "
              f"(conceded {int(row['goals_against'])})")
    
    print("\n" + "="*80)
    print("✅ DEMO COMPLETE - Explore more with the API!")
    print("="*80)
    print("\n💡 Try these in your code:")
    print("  • loader.get_league_matches('Premier League', '2024-25')")
    print("  • loader.get_team_form('Liverpool FC', 'Premier League', '2024-25')")
    print("  • loader.get_upcoming_fixtures('La Liga', '2024-25')")
    print("\n🌐 Or use the web interface:")
    print("  • http://localhost:8080/leagues")
    print("  • http://localhost:8080/api/league/table/Premier League")
    print("\n")


if __name__ == "__main__":
    demo_interesting_stats()

