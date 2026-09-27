import urllib.request, json, csv, re

url = "https://script.google.com/macros/s/AKfycbw3h4ZkxAcvB_ox6_3OvW9iNTgFtAsuXqyaEsCBckK5_1yGHGGU3_9v8-P4M7D_wTDrlQ/exec"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=30) as r:
    data = json.loads(r.read().decode('utf-8'))

assembly = data.get('assembly', [])
loksabha = data.get('loksabha', [])

# ── Parse assembly data ──────────────────────────────────────────
def parse_votes(details):
    m = re.search(r'Votes\s*[-–]\s*([\d,]+)', details, re.I)
    if m: return int(m.group(1).replace(',',''))
    return 0

def parse_runner(details):
    m = re.search(r'Runner[- ]?Up[-–\s]+(.+?)(?:\(|$)', details, re.I)
    if m: return m.group(1).strip()
    return 'N/A'

def parse_runner_party(details):
    m = re.search(r'Runner[- ]?Up[-–\s]+.*?\(([^)]+)\)', details, re.I)
    if m: return m.group(1).strip()
    return 'N/A'

rows = []
for r in assembly:
    details = r.get('details','')
    mla_m = re.search(r'MLA[-–\s]+([^(|]+)', details, re.I)
    mla_name = mla_m.group(1).strip() if mla_m else 'N/A'
    party_m = re.search(r'MLA[-–\s]+[^(]+\(\s*([^)]+)\s*\)', details, re.I)
    party = party_m.group(1).strip() if party_m else 'N/A'
    caste_m = re.search(r'Caste\s*[-–]\s*([^|]+)', details, re.I)
    caste = caste_m.group(1).strip() if caste_m else 'N/A'
    votes = parse_votes(details)
    runner = parse_runner(details)
    runner_party = parse_runner_party(details)
    rows.append({
        'zone': r.get('zone',''),
        'loksabha': r.get('loksabha',''),
        'assembly': r.get('assembly',''),
        'mla': mla_name,
        'party': party,
        'caste': caste,
        'votes': votes,
        'runner': runner,
        'runner_party': runner_party,
    })

# Write assembly CSV
with open('assembly_data.csv','w',newline='',encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['zone','loksabha','assembly','mla','party','caste','votes','runner','runner_party'])
    w.writeheader()
    w.writerows(rows)

# ── Parse Lok Sabha data ──────────────────────────────────────────
ls_rows = []
for r in loksabha:
    raw = r.get('loksabha','') or r.get('zone','') or ''
    # Parse "Winner: Name (Party) votes | Runner-up: Name (Party) votes"
    win_m = re.search(r'Winner:\s*(.+?)\s*\(([^)]+)\)\s*([\d,]+)', raw, re.I)
    run_m = re.search(r'Runner-up:\s*(.+?)\s*\(([^)]+)\)\s*([\d,]+)', raw, re.I)
    ls_rows.append({
        'constituency': r.get('zone',''),
        'winner': win_m.group(1).strip() if win_m else 'N/A',
        'winner_party': win_m.group(2).strip() if win_m else 'N/A',
        'winner_votes': win_m.group(3).replace(',','') if win_m else '0',
        'runner': run_m.group(1).strip() if run_m else 'N/A',
        'runner_party': run_m.group(2).strip() if run_m else 'N/A',
        'runner_votes': run_m.group(3).replace(',','') if run_m else '0',
    })

with open('loksabha_data.csv','w',newline='',encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['constituency','winner','winner_party','winner_votes','runner','runner_party','runner_votes'])
    w.writeheader()
    w.writerows(ls_rows)

# ── Summary stats ────────────────────────────────────────────────
print(f"Total assembly rows: {len(rows)}")
print(f"Total Lok Sabha rows: {len(ls_rows)}")

# Party tally
from collections import Counter
party_count = Counter(r['party'] for r in rows)
print("\n=== ASSEMBLY PARTY TALLY ===")
for p, c in sorted(party_count.items(), key=lambda x:-x[1]):
    print(f"  {p}: {c} seats")

# Check for suspicious entries
print("\n=== SUSPICIOUS ENTRIES (party=N/A or votes=0) ===")
bad = [r for r in rows if r['party']=='N/A' or r['votes']==0]
for b in bad:
    print(f"  {b['assembly']} | party={b['party']} | votes={b['votes']}")

# Check Lok Sabha
print("\n=== LOK SABHA PARTY TALLY ===")
ls_party = Counter(r['winner_party'] for r in ls_rows)
for p, c in sorted(ls_party.items(), key=lambda x:-x[1]):
    print(f"  {p}: {c} seats")

print("\nCSV files written: assembly_data.csv, loksabha_data.csv")
