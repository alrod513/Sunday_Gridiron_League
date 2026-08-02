import csv
import json
import os

def main():
    filename = "FantasyPros_Fantasy_Football_Projections_QB.csv"
    
    if not os.path.exists(filename):
        print(f"ERROR: Could not find {filename}!")
        return

    updated_pool = []
    print(f"Reading players and correct positions from {filename}...")

    with open(filename, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            name = row.get('Player') or row.get('Player Name') or row.get('Name', '')
            name = name.strip()
            if not name:
                continue
            
            team = row.get('Team', 'FA').strip().upper()
            
            # Dynamically read the actual position from the CSV (POS or Position column)
            pos = row.get('POS') or row.get('Position')
            if not pos:
                # Fallback check based on filename if column is missing
                if 'QB' in filename: pos = 'QB'
                elif 'RB' in filename: pos = 'RB'
                elif 'WR' in filename: pos = 'WR'
                elif 'TE' in filename: pos = 'TE'
                else: pos = 'QB'
            pos = pos.strip().upper()
            
            fpts_str = row.get('FPTS') or row.get('PTS') or row.get('Fantasy Points') or '0'
            try:
                fpts = float(fpts_str.replace(',', ''))
            except ValueError:
                fpts = 0.0

            updated_pool.append({
                "id": name.lower().replace(' ', '_').replace('.', ''),
                "name": name,
                "pos": pos,
                "team": team if team else 'FA',
                "bye": 8,
                "fpts": fpts,
                "avg": round(fpts / 17.0, 1)
            })

    output_file = "updated_projections.json"
    with open(output_file, "w", encoding='utf-8') as f:
        json.dump(updated_pool, f, indent=4)
        
    print(f"Successfully processed {len(updated_pool)} players with correct positions!")

if __name__ == "__main__":
    main()
