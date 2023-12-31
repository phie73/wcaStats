import pandas as pd
from tabulate import tabulate

# reading data and drop not needed colums
Results = pd.read_csv('data/WCA_export_Results.tsv', sep='\t')
Results = Results.loc[:,  ['eventId', 'personId', 'roundTypeId', 'competitionId']]
Competitions = pd.read_csv('data/WCA_export_Competitions.tsv', sep='\t')
Competitions = Competitions.loc[:,['countryId', 'id', 'year']]

# results
results = {
    '333' : [0,0,0],
    '222' : [0,0,0],
    '444' : [0,0,0],
    '555' : [0,0,0],
    '666' : [0,0,0],
    '777' : [0,0,0],
    '333oh' : [0,0,0],
    '333fm' : [0,0,0],
    '333bf' : [0,0,0],
    '444bf' : [0,0,0],
    '555bf' : [0,0,0],
    '333mbf' : [0,0,0],
    'minx' : [0,0,0],
    'pyram' : [0,0,0],
    'clock' : [0,0,0],
    'skewb' : [0,0,0],
    'sq1' : [0,0,0]
}

table = []

# german comps only - merging on comps because results tabel no country
df = Results.merge(Competitions, how='left', left_on='competitionId', right_on='id', validate = "m:1")
df = df.drop('id', 1)
dfG = df[df['countryId'] == 'Germany']

# group by comps
grouped = dfG.groupby(dfG['competitionId'])

for comp in dfG['competitionId'].unique():
    temp = grouped.get_group(comp)
    # year of interest
    if (temp['year'] != 2023).any():
        continue

    # total number of competitor on a comp
    competitors = grouped['personId'].nunique()
    tempE = temp.groupby(temp['eventId'])

    for event in temp['eventId'].unique():
        if event == "333mbo" or event == "magic" or event == "mmagic" or event == "333ft":
            continue

        ev = tempE.get_group(event)
        evR = ev.groupby(ev['roundTypeId'])
        roundTypes = ev['roundTypeId'].nunique()

        for roundType in ev['roundTypeId'].unique():
            rr = evR.get_group(roundType)
            results[event][2] = results[event][2] + 1 # total rounds of event y 
            if (roundType == "1" or roundType == "d" or roundType == "c") or (roundTypes == 1 and roundType == "f"):
                results[event][0] = results[event][0] + rr['personId'].count()/competitors[comp] # (competitiors in event y) / (total competitors of comp)
                results[event][1] = results[event][1] + 1 # number of first rounds = number of comps with event y
            

# jeder gute code braucht eine HILFE funktion
# mehr habe ich in 6sem und einem info bachelor auch nicht gelehrnt
def hilfe(h):
    return h[1]

for key,element in results.items():
    factor = element[0]/element[1]
    table.append([key, factor, element[1], element[2]])

table.sort(key=hilfe, reverse=True)
print(type(table))

for col in table:
    col[1] = col[1]*100

table.insert(0, ['event', 'percentage competing in event', 'num comps', 'total rounds'])
print(tabulate(table, headers='firstrow', tablefmt='github'))