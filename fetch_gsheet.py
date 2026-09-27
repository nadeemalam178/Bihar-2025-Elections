import urllib.request, csv, io

SHEET_ID = "1tnLhUze3WciXohkB9P0S-dsMZtvnyfbdB3Sc_iqNZqI"

# Try to get all sheets — first export the first sheet (default)
# Google Sheets CSV export: sheet 0 = first sheet
def fetch_sheet(sheet_id, gid=0):
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode('utf-8', errors='ignore')

# Fetch main (first) sheet first
print("Fetching Sheet 1 (default)...")
try:
    raw = fetch_sheet(SHEET_ID)
    reader = csv.reader(io.StringIO(raw))
    rows = list(reader)
    print(f"  Rows: {len(rows)}")
    print(f"  Headers: {rows[0] if rows else 'none'}")
    print(f"  First 5 data rows:")
    for r in rows[1:6]:
        print(f"    {r}")
    # Save it
    with open('sheet1.csv', 'w', newline='', encoding='utf-8') as f:
        csv.writer(f).writerows(rows)
    print("  Saved: sheet1.csv")
except Exception as e:
    print(f"  ERROR: {e}")

# Try common gids for other sheets
KNOWN_GIDS = {
    'Sheet1': 0,
    'Assembly': 1234567890,  # unknown, will try
    'Lok Sabha': 0,
}

# Try to detect sheet GIDs from the HTML page
print("\nFetching sheet list from main page...")
try:
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=15) as r:
        html = r.read().decode('utf-8', errors='ignore')
    import re
    # Find gid patterns
    gids = re.findall(r'"gid":"?(\d+)"?', html)
    names = re.findall(r'"name":"([^"]+)"', html[:5000])
    print(f"  Found GIDs: {list(set(gids))[:10]}")
    print(f"  Found names: {names[:10]}")
except Exception as e:
    print(f"  Could not get sheet list: {e}")
