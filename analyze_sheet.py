import pandas as pd

df = pd.read_csv('user_sheet_data.csv')

df_2025 = df[df['Year'].astype(str) == '2025'].copy()

# Filter for winners
winners = df_2025[df_2025['Status'].astype(str).str.contains('Winner', case=False, na=False)].copy()

print(f"Total 2025 winners found: {len(winners)}")

print("\n=== PARTY TALLY ===")
tally = winners['Party'].value_counts()
for p, c in tally.items():
    print(f"  {p}: {c}")

print("\n=== SUSPICIOUS PARTIES ===")
suspicious = winners[winners['Party'].isin(['Muslim', 'Rajput', 'Yadav', 'Rishi', 'TIGER'])]
for _, row in suspicious.iterrows():
    print(f"  {row['Constituency']} | {row['Candidate']} | Party: {row['Party']} | Votes: {row['Votes']}")

print("\n=== 0 VOTES ===")
winners['Votes_Num'] = pd.to_numeric(winners['Votes'], errors='coerce').fillna(0)
zero_votes = winners[winners['Votes_Num'] == 0]
for _, row in zero_votes.iterrows():
    print(f"  {row['Constituency']} | {row['Candidate']} | Party: {row['Party']} | Votes: {row['Votes']}")
    
# Let's save the sorted 2025 winner data to a CSV so I can easily compare it later
winners.to_csv('user_2025_winners.csv', index=False)
