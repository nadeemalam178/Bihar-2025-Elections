import json, re, csv
from bs4 import BeautifulSoup

def parse_wiki():
    with open(r'C:\Users\alamn\.gemini\antigravity-ide\brain\6828e211-79ea-4524-b15e-335e455a9c78\.system_generated\steps\481\content.md', 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    
    # Find the table that contains "Constituency" and "Winner"
    target_table = None
    for table in soup.find_all('table', class_='wikitable'):
        headers = [th.text.strip() for th in table.find_all('th')]
        if any('Constituency' in h for h in headers) and any('Winner' in h or 'Candidate' in h for h in headers):
            target_table = table
            break
            
    if not target_table:
        print("Could not find the constituency results table in Wikipedia.")
        return
        
    results = []
    for row in target_table.find_all('tr')[1:]: # Skip header
        cols = row.find_all(['td', 'th'])
        if len(cols) >= 5:
            # Assuming format: # | Constituency | Winner | Party | Votes | ...
            # Need to adapt based on actual columns. Let's just dump the text of the first 5 cols.
            row_data = [c.text.strip() for c in cols]
            if str(row_data[0]).isdigit() or str(row_data[1]).isdigit():
                results.append(row_data)

    print(f"Found {len(results)} rows in Wikipedia table.")
    if results:
        print("First 5 rows:", results[:5])
        
if __name__ == "__main__":
    parse_wiki()
