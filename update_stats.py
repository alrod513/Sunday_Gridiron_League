import csv
import json
import os

def main():
    filename = "FantasyPros_Fantasy_Football_Projections_QB.csv"
    
    # Base pool keeping RBs, WRs, TEs, Ks, and DSTs intact
    full_pool = [
        {"id": "christian_mccaffrey", "name": "Christian McCaffrey", "pos": "RB", "team": "SF", "bye": 8, "fpts": 332.8, "avg": 20.8},
        {"id": "breece_hall", "name": "Breece Hall", "pos": "RB", "team": "NYJ", "bye": 13, "fpts": 280.0, "avg": 17.5},
        {"id": "bijan_robinson", "name": "Bijan Robinson", "pos": "RB", "team": "ATL", "bye": 11, "fpts": 289.6, "avg": 18.1},
        {"id": "justin_jefferson", "name": "Justin Jefferson", "pos": "WR", "team": "MIN", "bye": 6, "fpts": 302.4, "avg": 18.9},
        {"id": "ceedee_lamb", "name": "CeeDee Lamb", "pos": "WR", "team": "DAL", "bye": 14, "fpts": 310.4, "avg": 19.4},
        {"id": "tyreek_hill", "name": "Tyreek Hill", "pos": "WR", "team": "MIA", "bye": 6, "fpts": 305.6, "avg": 19.1},
        {"id": "travis_kelce", "name": "Travis Kelce", "pos": "TE", "team": "KC", "bye": 5, "fpts": 227.2, "avg": 14.2},
        {"id": "sam_laporta", "name": "Sam LaPorta", "pos": "TE", "team": "DET", "bye": 6, "fpts": 204.8, "avg": 12.8},
        {"id": "justin_tucker", "name": "Justin Tucker", "pos": "K", "team": "BAL", "bye": 13, "fpts": 136.0, "avg": 8.5},
        {"id": "san_francisco_dst", "name": "San Francisco DST", "pos": "DST", "team": "SF", "bye": 8, "fpts": 140.8, "avg": 8.8}
    ]

    if os.path.exists(filename):
        print(f"Reading QBs from {filename}...")
        with open(filename, mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row.get('Player') or row.get('Player Name') or row.get('Name', '')
                name = name.strip()
                if not name:
                    continue
                
                team = row.get('Team', 'FA').strip().upper()
                fpts_str = row.get('FPTS') or row.get('PTS') or row.get('Fantasy Points') or '0'
                try:
                    fpts = float(fpts_str.replace(',', ''))
                except ValueError:
                    fpts = 0.0

                full_pool.append({
                    "id": name.lower().replace(' ', '_').replace('.', ''),
                    "name": name,
                    "pos": "QB",
                    "team": team if team else 'FA',
                    "bye": 8,
                    "fpts": fpts,
                    "avg": round(fpts / 17.0, 1)
                })

    output_file = "updated_projections.json"
    with open(output_file, "w", encoding='utf-8') as f:
        json.dump(full_pool, f, indent=4)
        
    print(f"Successfully saved {len(full_pool)} total players to {output_file}!")

if __name__ == "__main__":
    main()
