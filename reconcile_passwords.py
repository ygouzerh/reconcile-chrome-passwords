import csv
import sys
from typing import Dict, List, Tuple, Set

def read_csv_file(filename: str) -> List[Dict[str, str]]:
    """Read CSV file and return list of records."""
    records = []
    try:
        with open(filename, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                records.append(row)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    return records

def create_record_key(record: Dict[str, str]) -> str:
    """Create a unique key from name, url, username, and note."""
    return f"{record['name']}|{record['url']}|{record['username']}|{record['note']}"

def reconcile_passwords(importing_file: str, master_file: str, output_file: str):
    """Reconcile two password CSV files."""
    print(f"Reading {importing_file}...")
    importing_records = read_csv_file(importing_file)
    
    print(f"Reading {master_file}...")
    master_records = read_csv_file(master_file)
    
    # Create dictionaries with keys for comparison
    importing_dict = {}
    master_dict = {}
    
    for record in importing_records:
        key = create_record_key(record)
        if key not in importing_dict:
            importing_dict[key] = []
        importing_dict[key].append(record)
    
    for record in master_records:
        key = create_record_key(record)
        if key not in master_dict:
            master_dict[key] = []
        master_dict[key].append(record)
    
    # Find differences and conflicts
    only_in_importing = []
    only_in_master = []
    conflicts = []
    
    all_keys = set(importing_dict.keys()) | set(master_dict.keys())
    
    for key in all_keys:
        importing_records_for_key = importing_dict.get(key, [])
        master_records_for_key = master_dict.get(key, [])
        
        if not master_records_for_key:
            only_in_importing.extend(importing_records_for_key)
        elif not importing_records_for_key:
            only_in_master.extend(master_records_for_key)
        else:
            # Check if passwords differ
            importing_passwords = {r['password'] for r in importing_records_for_key}
            master_passwords = {r['password'] for r in master_records_for_key}
            
            if importing_passwords != master_passwords:
                conflicts.append({
                    'key': key,
                    'importing': importing_records_for_key,
                    'master': master_records_for_key
                })
            else:
                # Same passwords, just add one set
                only_in_importing.extend(importing_records_for_key)
    
    # Prepare final records
    final_records = []
    final_records.extend(only_in_importing)
    final_records.extend(only_in_master)
    
    # Handle conflicts
    if conflicts:
        print(f"\nFound {len(conflicts)} conflicts to resolve:")
        print("=" * 80)
        
        for i, conflict in enumerate(conflicts, 1):
            print(f"\nConflict {i}:")
            print(f"Key: {conflict['key']}")
            print("\nImporting records:")
            for j, record in enumerate(conflict['importing']):
                print(f"  {j+1}. Password: {record['password']}")
            
            print("\nMaster records:")
            for j, record in enumerate(conflict['master']):
                print(f"  {j+1}. Password: {record['password']}")
            
            print("\nOptions:")
            print("1. Keep importing records")
            print("2. Keep master records")
            print("3. Keep both")
            print("4. Skip this conflict")
            
            while True:
                choice = input(f"Choose option for conflict {i} (1-4): ").strip()
                if choice == '1':
                    final_records.extend(conflict['importing'])
                    break
                elif choice == '2':
                    final_records.extend(conflict['master'])
                    break
                elif choice == '3':
                    final_records.extend(conflict['importing'])
                    final_records.extend(conflict['master'])
                    break
                elif choice == '4':
                    break
                else:
                    print("Invalid choice. Please enter 1, 2, 3, or 4.")
    
    # Write output CSV
    if final_records:
        fieldnames = ['name', 'url', 'username', 'password', 'note']
        with open(output_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(final_records)
        
        print(f"\nReconciliation complete! Output written to {output_file}")
        print(f"Total records in output: {len(final_records)}")
    else:
        print("\nNo records to write to output file.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python reconcile_passwords.py <importing.csv> <master.csv> <output.csv>")
        sys.exit(1)
    
    importing_file = sys.argv[1]
    master_file = sys.argv[2]
    output_file = sys.argv[3]
    
    reconcile_passwords(importing_file, master_file, output_file)
