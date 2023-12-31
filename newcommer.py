import pandas as pd

#considering everyone with a 2023ABCDxx id as a newcommer

# reading data and drop not needed colums
Results = pd.read_csv('data/WCA_export_Results.tsv', sep='\t')
Results = Results.loc[:,  ['eventId', 'personId', 'roundTypeId', 'competitionId']]
Competitions = pd.read_csv('data/WCA_export_Competitions.tsv', sep='\t')
Competitions = Competitions.loc[:,['countryId', 'id', 'year', 'endMonth', 'endDay']]
Persons = pd.read_csv('data/WCA_export_Persons.tsv', sep='\t')
Persons = Persons.loc[:, ['id']]

events = {
    '333' : [0,0],
    '222' : [0,0],
    '444' : [0,0],
    '555' : [0,0],
    '666' : [0,0],
    '777' : [0,0],
    '333oh' : [0,0],
    '333fm' : [0,0],
    '333bf' : [0,0],
    '444bf' : [0,0],
    '555bf' : [0,0],
    '333mbf' : [0,0],
    'minx' : [0,0],
    'pyram' : [0,0],
    'clock' : [0,0],
    'skewb' : [0,0],
    'sq1' : [0,0]
}

newcommers = 0
compsBeenTo = 0
moreThanOne = 0

# german comps only 
df = Results.merge(Competitions, how='left', left_on='competitionId', right_on='id', validate = "m:1")
df = df.drop('id', 1)
dfG = df[df['countryId'] == 'Germany']
dfG = dfG[dfG['year'] == 2023]

# group by comps
grouped = dfG.groupby(dfG['personId'])

for persom in dfG['personId'].unique():
    temp = grouped.get_group(persom)
    if (temp.personId.str.contains('^2023').any()):
        newcommers = newcommers + 1
        comps = temp['competitionId'].nunique()
        compsBeenTo = compsBeenTo + comps
        groupedComps = temp.groupby(temp['competitionId'])

        if comps > 1:
            first = True
            moreThanOne = moreThanOne + 1
            for comp in temp['competitionId'].unique():
                t = groupedComps.get_group(comp)
                for event in t['eventId'].unique():
                    events[event][0] = events[event][0] + 1
                    if first:
                        events[event][1] = events[event][1] + 1
                        first = False 

        elif comps == 1:
            t = groupedComps.get_group(temp['competitionId'].values[0])
            for event in t['eventId'].unique():
                events[event][0] = events[event][0] + 1
                events[event][1] = events[event][1] + 1


eventsSorted = sorted(events.items(), key=lambda x:x[1], reverse=True)

dfp = pd.DataFrame(eventsSorted)
dfp.fillna(0, inplace=True)
print("newcommers: ", newcommers)
print("comps: ", compsBeenTo)
print("newcommers been to more than one comp: ", moreThanOne)
print("return rate: ", (moreThanOne/newcommers)*100)
print(dfp.to_markdown())
