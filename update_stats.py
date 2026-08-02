import json
import urllib.request

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
    - Passing: 0.04 pts per yard, 4 pts per TD, -2 per INT
    - Rushing: 0.1 pts per yard, 6 pts per TD
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
    # Dynamically fetch the current NFL state (season and active week)
    print("Fetching current NFL state from Sleeper API...")
    state = fetch_json("https://api.sleeper.app/v1/state/nfl")
    
    if not state:
        print("Could not fetch NFL state.")
        return

    season = str(state.get('season', '2026'))
    week = state.get('week', 1)
    season_type = state.get('season_type', 'regular')
    
    # Only run during regular season weeks (1-18)
    if season_type != 'regular' or not isinstance(week, int) or week < 1 or week > 18:
        print(f"Current state is Season: {season}, Type: {season_type}, Week: {week}. Skipping stats fetch.")
        return

    print(f"Active NFL Week Detected -> Season: {season}, Week: {week}")
    
    url_stats = f"https://api.sleeper.app/v1/stats/nfl/{season_type}/{season}/{week}"
    url_players = "https://api.sleeper.app/v1/players/nfl"
    
    weekly_stats = fetch_json(url_stats)
    players_meta = fetch_json(url_players)
    
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
            "bye": 8,
            "fpts": fpts,
            "avg": fpts
        })
    
    output_file = "updated_projections.json"
    with open(output_file, "w") as f:
        json.dump(updated_pool, f, indent=4)
        
    print(f"Successfully processed {len(updated_pool)} players for Week {week} and saved to {output_file}!")

if __name__ == "__main__":
    main()
