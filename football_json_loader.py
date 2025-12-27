"""
Load Real Match Data from OpenFootball JSON Repository
Source: https://github.com/openfootball/football.json
Provides actual match results, fixtures, and team statistics
"""

import requests
import pandas as pd
from typing import Dict, List, Optional
from datetime import datetime
import json


class FootballJSONLoader:
    """
    Load and process real football match data from openfootball/football.json
    """
    
    BASE_URL = "https://raw.githubusercontent.com/openfootball/football.json/master"
    
    # Available leagues and their codes
    LEAGUES = {
        'Premier League': {'code': 'en.1', 'name': 'English Premier League'},
        'Championship': {'code': 'en.2', 'name': 'English Championship'},
        'Bundesliga': {'code': 'de.1', 'name': 'German Bundesliga'},
        '2. Bundesliga': {'code': 'de.2', 'name': 'German 2. Bundesliga'},
        'La Liga': {'code': 'es.1', 'name': 'Spanish La Liga'},
        'Segunda Division': {'code': 'es.2', 'name': 'Spanish Segunda Division'},
        'Serie A': {'code': 'it.1', 'name': 'Italian Serie A'},
        'Serie B': {'code': 'it.2', 'name': 'Italian Serie B'},
        'Ligue 1': {'code': 'fr.1', 'name': 'French Ligue 1'},
        'Ligue 2': {'code': 'fr.2', 'name': 'French Ligue 2'},
    }
    
    def __init__(self):
        self.cache = {}
    
    def fetch_league_data(self, league_code: str, season: str = '2024-25') -> Optional[Dict]:
        """
        Fetch league data for a specific season
        
        Args:
            league_code: League code (e.g., 'en.1' for Premier League)
            season: Season string (e.g., '2024-25')
        
        Returns:
            Dictionary with league data or None if error
        """
        cache_key = f"{league_code}_{season}"
        
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        url = f"{self.BASE_URL}/{season}/{league_code}.json"
        
        try:
            print(f"📥 Fetching {league_code} data for {season}...")
            print(f"   URL: {url}")
            
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            self.cache[cache_key] = data
            
            print(f"   ✅ Loaded {len(data.get('matches', []))} matches")
            return data
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print(f"   ⚠️  Data not available for {season}")
            else:
                print(f"   ❌ HTTP Error: {e}")
            return None
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return None
    
    def get_league_matches(self, league_name: str, season: str = '2024-25') -> pd.DataFrame:
        """
        Get all matches for a league as a DataFrame
        
        Args:
            league_name: Name of the league (e.g., 'Premier League')
            season: Season string
        
        Returns:
            DataFrame with match data
        """
        if league_name not in self.LEAGUES:
            raise ValueError(f"League '{league_name}' not supported")
        
        league_code = self.LEAGUES[league_name]['code']
        data = self.fetch_league_data(league_code, season)
        
        if not data or 'matches' not in data:
            return pd.DataFrame()
        
        matches = []
        for match in data['matches']:
            match_info = {
                'date': match.get('date'),
                'round': match.get('round'),
                'team1': match.get('team1'),
                'team2': match.get('team2'),
                'score1': None,
                'score2': None,
                'score_ht1': None,  # Half-time score
                'score_ht2': None,
            }
            
            # Extract scores if available
            if 'score' in match:
                if 'ft' in match['score']:  # Full-time
                    match_info['score1'] = match['score']['ft'][0]
                    match_info['score2'] = match['score']['ft'][1]
                if 'ht' in match['score']:  # Half-time
                    match_info['score_ht1'] = match['score']['ht'][0]
                    match_info['score_ht2'] = match['score']['ht'][1]
            
            matches.append(match_info)
        
        df = pd.DataFrame(matches)
        df['league'] = self.LEAGUES[league_name]['name']
        df['season'] = season
        
        return df
    
    def get_team_statistics(self, league_name: str, season: str = '2024-25') -> pd.DataFrame:
        """
        Calculate team statistics from match data
        
        Args:
            league_name: Name of the league
            season: Season string
        
        Returns:
            DataFrame with team statistics
        """
        df = self.get_league_matches(league_name, season)
        
        if df.empty:
            return pd.DataFrame()
        
        # Filter only completed matches (with scores)
        df = df[df['score1'].notna() & df['score2'].notna()].copy()
        
        if df.empty:
            return pd.DataFrame()
        
        teams_stats = {}
        
        for _, match in df.iterrows():
            team1, team2 = match['team1'], match['team2']
            score1, score2 = match['score1'], match['score2']
            
            # Initialize team stats if not exists
            for team in [team1, team2]:
                if team not in teams_stats:
                    teams_stats[team] = {
                        'team': team,
                        'played': 0,
                        'wins': 0,
                        'draws': 0,
                        'losses': 0,
                        'goals_for': 0,
                        'goals_against': 0,
                        'goal_difference': 0,
                        'points': 0,
                    }
            
            # Update stats for team1
            teams_stats[team1]['played'] += 1
            teams_stats[team1]['goals_for'] += score1
            teams_stats[team1]['goals_against'] += score2
            
            # Update stats for team2
            teams_stats[team2]['played'] += 1
            teams_stats[team2]['goals_for'] += score2
            teams_stats[team2]['goals_against'] += score1
            
            # Determine winner
            if score1 > score2:
                teams_stats[team1]['wins'] += 1
                teams_stats[team1]['points'] += 3
                teams_stats[team2]['losses'] += 1
            elif score1 < score2:
                teams_stats[team2]['wins'] += 1
                teams_stats[team2]['points'] += 3
                teams_stats[team1]['losses'] += 1
            else:
                teams_stats[team1]['draws'] += 1
                teams_stats[team1]['points'] += 1
                teams_stats[team2]['draws'] += 1
                teams_stats[team2]['points'] += 1
        
        # Calculate goal difference
        for team in teams_stats:
            teams_stats[team]['goal_difference'] = (
                teams_stats[team]['goals_for'] - teams_stats[team]['goals_against']
            )
        
        # Convert to DataFrame and sort by points
        stats_df = pd.DataFrame(list(teams_stats.values()))
        stats_df = stats_df.sort_values(
            ['points', 'goal_difference', 'goals_for'],
            ascending=[False, False, False]
        ).reset_index(drop=True)
        
        # Add position
        stats_df.insert(0, 'position', range(1, len(stats_df) + 1))
        
        stats_df['league'] = league_name
        stats_df['season'] = season
        
        return stats_df
    
    def get_team_form(self, team_name: str, league_name: str, 
                      season: str = '2024-25', last_n: int = 5) -> List[str]:
        """
        Get recent form for a team (e.g., ['W', 'W', 'D', 'L', 'W'])
        
        Args:
            team_name: Name of the team
            league_name: Name of the league
            season: Season string
            last_n: Number of recent matches
        
        Returns:
            List of results ('W', 'D', 'L')
        """
        df = self.get_league_matches(league_name, season)
        
        if df.empty:
            return []
        
        # Filter matches with scores for this team
        team_matches = df[
            ((df['team1'] == team_name) | (df['team2'] == team_name)) &
            (df['score1'].notna()) & (df['score2'].notna())
        ].copy()
        
        if team_matches.empty:
            return []
        
        form = []
        for _, match in team_matches.tail(last_n).iterrows():
            if match['team1'] == team_name:
                if match['score1'] > match['score2']:
                    form.append('W')
                elif match['score1'] < match['score2']:
                    form.append('L')
                else:
                    form.append('D')
            else:  # team2
                if match['score2'] > match['score1']:
                    form.append('W')
                elif match['score2'] < match['score1']:
                    form.append('L')
                else:
                    form.append('D')
        
        return form
    
    def get_upcoming_fixtures(self, league_name: str, season: str = '2024-25') -> pd.DataFrame:
        """
        Get upcoming fixtures (matches without scores)
        
        Args:
            league_name: Name of the league
            season: Season string
        
        Returns:
            DataFrame with upcoming fixtures
        """
        df = self.get_league_matches(league_name, season)
        
        if df.empty:
            return pd.DataFrame()
        
        # Filter matches without scores (upcoming)
        upcoming = df[df['score1'].isna() | df['score2'].isna()].copy()
        
        return upcoming
    
    def get_all_leagues_data(self, season: str = '2024-25') -> Dict[str, pd.DataFrame]:
        """
        Fetch data for all available leagues
        
        Args:
            season: Season string
        
        Returns:
            Dictionary mapping league names to their DataFrames
        """
        all_data = {}
        
        print(f"\n{'='*80}")
        print(f"📥 Fetching all leagues for season {season}")
        print(f"{'='*80}\n")
        
        for league_name in self.LEAGUES.keys():
            try:
                df = self.get_league_matches(league_name, season)
                if not df.empty:
                    all_data[league_name] = df
                    print(f"✅ {league_name}: {len(df)} matches")
                else:
                    print(f"⚠️  {league_name}: No data available")
            except Exception as e:
                print(f"❌ {league_name}: Error - {e}")
        
        print(f"\n{'='*80}")
        print(f"✅ Loaded {len(all_data)} leagues")
        print(f"{'='*80}\n")
        
        return all_data


def demo_usage():
    """
    Demonstrate how to use the FootballJSONLoader
    """
    loader = FootballJSONLoader()
    
    print("\n" + "="*80)
    print("⚽ OpenFootball JSON Data Loader - Demo")
    print("="*80)
    
    # Example 1: Get Premier League matches
    print("\n📊 Example 1: Premier League 2024-25 Matches")
    print("-" * 80)
    matches = loader.get_league_matches('Premier League', '2024-25')
    if not matches.empty:
        print(matches.head(10))
        print(f"\nTotal matches: {len(matches)}")
    
    # Example 2: Get team statistics (league table)
    print("\n📊 Example 2: Premier League Table")
    print("-" * 80)
    table = loader.get_team_statistics('Premier League', '2024-25')
    if not table.empty:
        print(table.head(10))
    
    # Example 3: Get team form
    print("\n📊 Example 3: Team Form (Last 5 Matches)")
    print("-" * 80)
    if not table.empty and len(table) > 0:
        team = table.iloc[0]['team']
        form = loader.get_team_form(team, 'Premier League', '2024-25')
        print(f"{team}: {' '.join(form)}")
    
    # Example 4: Get upcoming fixtures
    print("\n📊 Example 4: Upcoming Fixtures")
    print("-" * 80)
    upcoming = loader.get_upcoming_fixtures('Premier League', '2024-25')
    if not upcoming.empty:
        print(upcoming.head(10))
        print(f"\nTotal upcoming: {len(upcoming)}")
    
    print("\n" + "="*80)


if __name__ == "__main__":
    demo_usage()

