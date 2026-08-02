import json
import os
import urllib.request

# Configuration
SEASON = "2026"
WEEK = 1  # Change or automate this to match the current active week
URL_STATS = f"https://api.sleeper.app/v1/stats/nfl/regular/{SEASON}/{WEEK}"
URL_PLAYERS = "https://api.sleeper.app/v1/players/nfl"

def fetch_json(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"Error fetching data from {url}: {e}")
        return {}

def calculate_ppr_points(stats):
    """
    Calculates 1.0 PPR Fantasy Points based on standard scoring:
    - Passing: 0.04 pts per yard (1 pt per 25 yds), 4 pts per TD, -2 per INT
    - Rushing: 0.1 pts per yard (1 pt per 10 yds), 6 pts per TD
    - Receiving: 1.0 pt per reception, 0.1 pts per yard, 6 pts per TD
    - Fumbles Lost: -2 pts
    """
    passing_yards = stats.get('pass_yd', 0)
    passing_tds = stats.get('pass_td', 0)
    passing_ints = stats.get('pass_int', 0)
    
    rushing_yards = stats.get('rush_yd', 0)
    rushing_tds = stats.get('rush_td', 0)
    
    receptions = stats.get('rec', 0)
    receiving_yards = stats.get('rec_yd', 0)
    receiving_tds = stats.get('rec_td', 0)
    
    fumbles_lost = stats.get('fum_lost', 0)
    
    points = (
        (passing_yards * 0.04) + (passing_tds * 4.0) - (passing_ints * 2.0) +
        (rushing_yards * 0.1) + (rushing_tds * 6.0) +
        (receptions * 1.0) + (receiving_yards * 0.1) + (receiving_tds * 6.0) -
        (fumbles_lost * 2.0)
    )
    
    return round(points, 1)

def main():
    print(f"Fetching NFL stats for Season {SEASON}, Week {WEEK}...")
    weekly_stats = fetch_json(URL_STATS)
    players_meta = fetch_json(URL_PLAYERS)
    
    if not weekly_stats:
        print("No stats returned for this week yet.")
        return

    updated_pool = []
    
    for player_id, stats in weekly_stats.items():
        if player_id not in players_meta:
            continue
            
        meta = players_meta[player_id]
        name = f"{meta.get('first_name', '')} {meta.get('last_name', '')}".strip()
        pos = meta.get('position', 'FLEX')
        team = meta.get('team', 'FA')
        
        if not name or pos not in ['QB', 'RB', 'WR', 'TE', 'K', 'DST']:
            continue
            
        fpts = calculate_ppr_points(stats)
        
        updated_pool.append({
            "id": player_id,
            "name": name,
            "pos": pos,
            "team": team if team else 'FA',
            "bye": 8, # Default or map via nflByeWeeks dictionary if needed
            "fpts": fpts,
            "avg": fpts # Simplified to weekly score or season average tracker
        })
    
    # Save processed stats into a json file that your app can load
    output_file = "updated_projections.json"
    with open(output_file, "w") as f:
        json.dump(updated_pool, f, indent=4)
        
    print(f"Successfully processed {len(updated_pool)} players and saved to {output_file}!")

if __name__ == "__main__":
    main()