import csv
import glob
import json
import os

def parse_csvs():
    updated_pool = []
    # Find any FantasyPros projection CSVs in the repository
    csv_files = [f for f in glob.glob("*.csv") if "Projections" in f or "FantasyPros" in f]
    
    if not csv_files:
        csv_files = [f for f in glob.glob("*.csv")] # Fallback to any CSV

    for csv_filename in csv_files:
        print(f"Reading custom projections from {csv_filename}...")
        try:
            with open(csv_filename, mode='r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    name = row.get('Player') or row.get('Player Name') or row.get('Name', '')
                    name = name.strip()
                    if not name:
                        continue
                    
                    team = row.get('Team', 'FA').strip().upper()
                    
                    fpts_str = row.get('FPTS') or row.get('PTS') or row.get('Fantasy Points') or '0'
                    try:
                        fpts = float(fpts_str)
                    except ValueError:
                        fpts = 0.0

                    # Infer position from filename or row data
                    pos = row.get('POS') or row.get('Position')
                    if not pos:
                        if 'QB' in csv_filename: pos = 'QB'
                        elif 'RB' in csv_filename: pos = 'RB'
                        elif 'WR' in csv_filename: pos = 'WR'
                        elif 'TE' in csv_filename: pos = 'TE'
                        else: pos = 'QB'
                    pos = pos.strip().upper()

                    updated_pool.append({
                        "id": name.lower().replace(' ', '_').replace('.', ''),
                        "name": name,
                        "pos": pos,
                        "team": team if team else 'FA',
                        "bye": 8,
                        "fpts": fpts,
                        "avg": round(fpts / 17.0, 1)
                    })
        except Exception as e:
            print(f"Error reading {csv_filename}: {e}")

    return updated_pool

def main():
    pool = parse_csvs()
    if not pool:
        print("No valid player data found in CSV files.")
        return

    output_file = "updated_projections.json"
    with open(output_file, "w", encoding='utf-8') as f:
        json.dump(pool, f, indent=4)
        
    print(f"Successfully processed {len(pool)} players from CSV and saved to {output_file}!")

if __name__ == "__main__":
    main()
