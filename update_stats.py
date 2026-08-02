import csv
import json
import os

def main():
    # Updated to look for the comprehensive file across all positions
    filename = "FantasyPros_Fantasy_Football_Projections.csv"
    
    if not os.path.exists(filename):
        print(f"ERROR: Could not find {filename} in the repository!")
        print("Available files in directory:", os.listdir('.'))
        return

    updated_pool = []
    print(f"Reading multi-position projections from {filename}...")

    with open(filename, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            # Clean up keys for case-insensitivity
            row_clean = {k.strip().lower(): v for k, v in row.items() if k}
            
            name = row_clean.get('player') or row_clean.get('player name') or row_clean.get('name', '')
            name = name.strip()
            if not name:
                continue
            
            team = row_clean.get('team', 'FA').strip().upper()
            
            # Read the exact position from the CSV (POS or Position)
            pos = row_clean.get('pos') or row_clean.get('position', 'QB')
            pos = pos.strip().upper()
            
            fpts_str = row_clean.get('fpts') or row_clean.get('pts') or row_clean.get('fantasy points') or '0'
            try:
                fpts = float(str(fpts_str).replace(',', ''))
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
        
    print(f"Successfully processed {len(updated_pool)} players across all positions!")

if __name__ == "__main__":
    main()
