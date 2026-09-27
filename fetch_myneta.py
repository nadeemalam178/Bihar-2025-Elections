import urllib.request, re, csv, time

# All 243 MyNeta constituency IDs for Bihar 2025
IDS = list(range(1, 244))  # 1 to 243

def fetch_winner(cid):
    url = f"https://www.myneta.info/Bihar2025/index.php?action=show_candidates&constituency_id={cid}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as r:
            html = r.read().decode('utf-8', errors='ignore')
        # Extract constituency name
        name_m = re.search(r'<title>([^<]+)</title>', html)
        cname = name_m.group(1).strip() if name_m else f"ID-{cid}"
        cname = cname.replace('Candidates of ', '').replace(' - MyNeta', '').strip()
        # Find WINNER row
        win_m = re.search(r'Winner.*?<td[^>]*>([^<]+)</td>.*?<td[^>]*>([^<]+)</td>.*?<td[^>]*>([\d,]+)</td>', html, re.S|re.I)
        if win_m:
            return {
                'id': cid, 'constituency': cname,
                'winner': win_m.group(1).strip(),
                'party': win_m.group(2).strip(),
                'votes': win_m.group(3).strip().replace(',', '')
            }
        # fallback: look for row with WON badge
        won_m = re.search(r'WON.*?<td[^>]*>([^<]+)</td>.*?<td[^>]*>([^<]+)</td>.*?<td[^>]*>([\d,]+)</td>', html, re.S|re.I)
        if won_m:
            return {
                'id': cid, 'constituency': cname,
                'winner': won_m.group(1).strip(),
                'party': won_m.group(2).strip(),
                'votes': won_m.group(3).strip().replace(',', '')
            }
        return {'id': cid, 'constituency': cname, 'winner': 'N/A', 'party': 'N/A', 'votes': '0'}
    except Exception as e:
        return {'id': cid, 'constituency': f'ID-{cid}', 'winner': 'ERROR', 'party': str(e)[:40], 'votes': '0'}

results = []
for cid in IDS:
    r = fetch_winner(cid)
    results.append(r)
    if cid % 20 == 0:
        print(f"  Fetched {cid}/243 ...")
    time.sleep(0.2)

with open('myneta_winners.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['id','constituency','winner','party','votes'])
    w.writeheader()
    w.writerows(results)

print(f"\nDone! {len(results)} rows saved to myneta_winners.csv")
# Quick tally
from collections import Counter
tally = Counter(r['party'] for r in results if r['party'] not in ('N/A','ERROR'))
print("\nParty Tally from MyNeta:")
for p, c in sorted(tally.items(), key=lambda x:-x[1]):
    print(f"  {p}: {c}")
