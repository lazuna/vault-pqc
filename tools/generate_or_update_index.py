import os
import yaml
import re
from collections import OrderedDict

INDEX_FILENAME = "_index.yaml"

def read_existing_index(path):
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            return data if isinstance(data, list) else []
    except Exception as e:
        print(f"Warning: Failed to parse existing index — {e}")
        return []

def extract_title_from_md(md_path):
    try:
        with open(md_path, "r", encoding="utf-8") as f:
            for line in f:
                match = re.match(r"^#\s+(.*)", line)
                if match:
                    return match.group(1).strip()
    except Exception as e:
        print(f"Error reading {md_path}: {e}")
    # Fallback to filename title-case
    return os.path.splitext(os.path.basename(md_path))[0].replace("_", " ").title()

def generate_index_entries(md_files):
    entries = []
    for md_file in md_files:
        title = extract_title_from_md(md_file)
        entries.append({'title': title, 'file': md_file})
    return entries

def merge_indices(existing, new):
    existing_map = {item['file']: item for item in existing}
    for entry in new:
        if entry['file'] in existing_map:
            # Update title if changed
            existing_map[entry['file']]['title'] = entry['title']
        else:
            existing_map[entry['file']] = entry
    # Return sorted by file
    return sorted(existing_map.values(), key=lambda x: x['file'])

def write_index(path, entries):
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(entries, f, sort_keys=False, allow_unicode=True)

def main():
    cwd = os.getcwd()
    md_files = sorted(f for f in os.listdir(cwd) if f.endswith(".md"))
    
    if not md_files:
        print("No markdown files found.")
        return
    
    existing_index = read_existing_index(INDEX_FILENAME)
    new_entries = generate_index_entries(md_files)
    merged = merge_indices(existing_index, new_entries)
    write_index(INDEX_FILENAME, merged)
    print(f"Updated: {INDEX_FILENAME} with {len(merged)} entries.")

if __name__ == "__main__":
    main()

