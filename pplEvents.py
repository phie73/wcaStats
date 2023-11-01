import pandas as pd

# reading data and drop not needed colums
Results = pd.read_csv('data/WCA_export_Results.tsv', sep='\t')
Results = Results.loc[:,  ['eventId', 'personId', 'roundTypeId', 'competitionId']]

Competitions = pd.read_csv('data/WCA_export_Competitions.tsv', sep='\t')
Competitions = Competitions.loc[:,['countryId', 'id']]

# german comps only - merging on comps because results tabel no country
df = Results.merge(Competitions, how='left', left_on='competitionId', right_on='id', validate = "m:1")
df = df.drop('id', 1)
dfG = df[df['countryId'] == 'Germany']

# group by comps
grouped = dfG.groupby(dfG['competitionId'])


for comp in dfG['competitionId'].unique():
    temp = grouped.get_group(comp)
    print(comp)
    competitors = grouped['personId'].nunique()
    print(competitors)

# for index, row in dfG.iterrows():
#     print(row['competitionId'])