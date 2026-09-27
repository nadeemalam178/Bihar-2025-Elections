import urllib.request, csv, io

SHEET_ID = "1tnLhUze3WciXohkB9P0S-dsMZtvnyfbdB3Sc_iqNZqI"

for gid in [0, 1, 2, 3, 4, 1705706559, 1334386899, 123456789]:
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&gid={gid}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = r.read().decode("utf-8", errors="ignore")
        lines = data.strip().split("\n")
        header = lines[0][:100] if lines else "empty"
        print(f"GID {gid}: {len(lines)} rows | Header: {header}")
        if len(lines) > 2:
            fname = f"sheet_gid_{gid}.csv"
            with open(fname, "w", encoding="utf-8") as f:
                f.write(data)
            print(f"  => Saved {fname}")
    except Exception as e:
        print(f"GID {gid}: ERROR - {str(e)[:80]}")
