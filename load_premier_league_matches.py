"""
Load Premier League 2024-25 Matches from Local JSON File
Creates a simplified matches dataset for faster loading
"""

import json
import pandas as pd

def load_matches():
    """Load matches from local JSON file"""
    with open('premier_league_2024_25_matches.json', 'r') as f:
        data = json.load(f)
    
    matches = []
    for match in data['matches']:
        match_info = {
            'date': match.get('date'),
            'time': match.get('time', ''),
            'round': match.get('round'),
            'team1': match.get('team1'),
            'team2': match.get('team2'),
            'score1': None,
            'score2': None,
        }
        
        # Extract scores if available
        if 'score' in match and 'ft' in match['score']:
            match_info['score1'] = match['score']['ft'][0]
            match_info['score2'] = match['score']['ft'][1]
        
        matches.append(match_info)
    
    return matches

if __name__ == "__main__":
    matches = load_matches()
    print(f"✅ Loaded {len(matches)} Premier League 2024-25 matches")
    print(f"\n📅 First match:")
    print(f"   {matches[0]['team1']} vs {matches[0]['team2']}")
    print(f"   Score: {matches[0]['score1']}-{matches[0]['score2']}")
    print(f"   Date: {matches[0]['date']}")
    
    # Count completed vs upcoming
    completed = sum(1 for m in matches if m['score1'] is not None)
    upcoming = sum(1 for m in matches if m['score1'] is None)
    
    print(f"\n📊 Status:")
    print(f"   Completed: {completed}")
    print(f"   Upcoming: {upcoming}")

