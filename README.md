# Password CSV Reconciliation Tool

A Python script to reconcile two Chrome password CSV files by comparing records and handling conflicts interactively.

## Overview

This tool compares two password CSV files (`importing.csv` and `master.csv`) and generates a consolidated output file (`new.csv`). It handles three scenarios:

1. **Records only in importing file** → Added to output
2. **Records only in master file** → Added to output  
3. **Conflicting records** → Presented for manual resolution

## CSV Format

Both input files must have the following header format:
```
name,url,username,password,note
```

Example:
```
10.0.0.1,https://10.0.0.1/,john,P@ssw0rd,
Gmail,https://gmail.com,john@email.com,mypass123,Personal email
```

## Matching Logic

Records are considered the same if they have identical:
- name
- url  
- username
- note

If any of these fields differ, they are treated as separate records. Only password differences trigger conflict resolution.

## Usage

```bash
python reconcile_passwords.py <importing.csv> <master.csv> <output.csv>
```

Example:
```bash
python reconcile_passwords.py importing.csv master.csv new.csv
```

## Conflict Resolution

When conflicts are found, you'll see an interactive prompt:

```
Conflict 1:
Key: Gmail|https://gmail.com|john@email.com|Personal email

Importing records:
  1. Password: oldpass123

Master records:
  1. Password: newpass456

Options:
1. Keep importing records
2. Keep master records
3. Keep both
4. Skip this conflict

Choose option for conflict 1 (1-4):
```

### Resolution Options

- **Option 1**: Keep only the importing file's version
- **Option 2**: Keep only the master file's version
- **Option 3**: Keep both versions (creates duplicate entries)
- **Option 4**: Skip entirely (neither version included)

## Output

The script generates:
- A new CSV file with reconciled records
- Console output showing the reconciliation summary
- Total count of records in the final output

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)

## Notes

- The tool preserves all original CSV formatting
- Multiple records can exist for the same name/url combination
- Empty fields are handled gracefully
- File encoding is UTF-8

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
