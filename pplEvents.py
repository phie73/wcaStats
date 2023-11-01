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

# ich bin ja fan von dingen leer schonmal haben, weil haben ist besser als nicht haben oder so ähnlich
table = [ 
    ['333', 0,0,0], 
    ['222', 0,0,0], 
    ['444', 0,0,0], 
    ['555', 0,0,0], 
    ['666', 0,0,0], 
    ['777', 0,0,0], 
    ['333oh', 0,0,0], 
    ['333fm', 0,0,0], 
    ['333bf', 0,0,0], 
    ['444bf', 0,0,0], 
    ['555bf', 0,0,0], 
    ['333mbf', 0,0,0], 
    ['minx', 0,0,0], 
    ['pyram', 0,0,0], 
    ['clock', 0,0,0], 
    ['skewb', 0,0,0], 
    ['sq1', 0,0,0]]


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

count = 0
for i in results:
    table[(count)][1] = results[i][0]/results[i][1] # ((competitiors in event y) / (total competitors of comp)) / number of fist rounds in event y
    table[(count)][2] = results[i][1]
    table[(count)][3] = results[i][2]
    count = count + 1

table.sort(key=hilfe, reverse=True)
table.insert(0, ['event', 'factor (res/com)', 'num comps', 'total rounds'])
print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))