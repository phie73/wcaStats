import pandas as pd
import numpy as np
import datetime
import time
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import LinearSegmentedColormap
import copy


# read in and sort data
plt.rcParams["figure.figsize"] = (12, 6)

Results = pd.read_csv('data/WCA_export_Results.tsv', sep='\t', low_memory = False)
Competitions = pd.read_csv('data/WCA_export_Competitions.tsv', sep='\t')

df = Results.merge(Competitions, how='left', left_on='competitionId', right_on='id', validate = "m:1")
df = df.drop('id', 1)

df = df.rename(columns = {'name':'competitionName'})

rounds = pd.read_csv('data/WCA_export_RoundTypes.tsv', sep='\t', low_memory = False)

df = df.merge(rounds[['id','rank']], how='left', left_on='roundTypeId', right_on='id')
df = df.drop('id',1)

persons = pd.read_csv('data/WCA_export_Persons.tsv', sep='\t')

events = pd.read_csv('data/WCA_export_Events.tsv', sep='\t')

# file to write marktown tables in
FILE = "tables_markdown.txt"

# Truncates a number to the nth digit. 
def truncate(num, n):
    if np.isnan(num) == True:
        return np.nan
    
    integer = int(num * (10**n))/(10**n)
    return float(integer)

def writeToFile(title, data):
    f = open(FILE, "a")
    f.write(title)
    f.write(data.to_markdown())
    f.close()

## most competitors
def mostCompetitor(queryCond):
    competiors = df.query(queryCond).groupby("competitionId")['personId'].nunique()

    competiors = pd.DataFrame(competiors
            ).rename(columns = {"personId":"competitors"}
            ).sort_values(by = "competitors", ascending = False
            ).reset_index(drop = False)

    competiors.index += 1
    writeToFile("\nmost competitors: " + queryCond + "\n", competiors.head(15))


def createPersonDf():
    newcomer = df.query("personCountryId == 'Germany'")
    femaleCompetors = list(persons.query("gender == 'f'")['id'])

    dict_new = {}

    for year in range(2003,1+int(datetime.datetime.now().year)):
        buff = newcomer[newcomer['personId'].str.contains(str(year))] 
        buff2 = newcomer.query("year == @year")
        dict_new[year] = (buff['personId'].nunique(),
                       buff2.groupby('personId')['competitionId'].nunique().sum(),
                       buff2.query("countryId == 'Germany'")['competitionId'].nunique(),
                       buff.query("personId in @femaleCompetors")['personId'].nunique(),
                    buff2.query("personId in @femaleCompetors")['personId'].nunique())
    
    
    new = pd.DataFrame.from_dict(dict_new, orient="index"
                        ).reset_index(drop=False
                        ).rename(columns={"index":"year", 0:"newcomers", 1:"competitors", 2:"competitions", 3:"female newcomers", 4:"female competitors"}
                        ).sort_values(by = 'year', ascending = True
                        ).reset_index(drop = True)

    new.index += 1

    return new

## newcommers and competitors over yeras
def personYears(new):
    plt.figure(1)
    plt.grid(visible = True, which='major', axis='y', alpha = 0.5, zorder = 1)
    plt.bar(new['year'], new['competitors'], color = '#9acd32', zorder = 2);
    plt.bar(new['year'], new['newcomers'], zorder = 3, color = '#008000');
    plt.title('German Cubers', fontsize = 14);
    plt.legend(['competitors','newcomers'], fontsize = 14)
    plt.xticks(new['year']);
    plt.xticks(rotation=45);

    plt.savefig("newcommer.png")


## female competitors
def fmale(new):
    plt.figure(2)
    plt.title('female competitors', fontsize = 14)

    plt.grid(visible = True, which='major', axis='y', alpha = 0.5, zorder = 1)
    plt.bar(new['year'], new['competitors'], color = '#9acd32', zorder = 2)
    plt.bar(new['year'], new['female competitors'], zorder = 3, color = '#556b2f')
    plt.legend(['male','female'], fontsize = 14)
    plt.tick_params(axis = 'x', bottom=False)

    plt.savefig("fmale.png")


## newcommers and female competitors
def newCommerFemale(new):
    plt.figure(3)
    fig, (ax1,ax2) = plt.subplots(2, sharex=True, figsize=(10, 10))
    fig.suptitle('male and female german newcommers', fontsize = 14)

    ax1.grid(visible = True, which='major', axis='y', alpha = 0.5, zorder = 1)
    ax1.bar(new['year'], new['competitors'] - new['female competitors'], color = '#9acd32', zorder = 2);
    ax1.bar(new['year'], new['newcomers'] - new['female newcomers'], zorder = 3, color = '#556b2f');
    ax1.legend(['male competitors','male newcomers'], fontsize = 14)
    ax1.tick_params(axis = 'x', bottom=False)
               
    ax2.figure
    ax2.grid(visible = True, which='major', axis='y', alpha = 0.5, zorder = 1)
    ax2.bar(new['year'], new['female competitors'], color = '#adff2f', zorder = 2);
    ax2.bar(new['year'], new['female newcomers'], zorder = 3, color = '#006400');
    ax2.legend(['female competitors','female newcomers'], fontsize = 14)
    ax2.set_xticks(new['year'])
    ax2.tick_params(axis = 'x', labelrotation=45)

    fig.tight_layout()
    fig.subplots_adjust(top=0.95)

    plt.savefig("fmnewcommer.png")


## return rate
def retRate():
    d = df.groupby('countryId')['competitionId'].nunique()
    countries2 = pd.DataFrame(d).reset_index(drop = False)
    countries2 = list(countries2.query("competitionId >= 2")['countryId'])

    dict_retrate = {}

    for country in countries2:
        solve = df.query("personCountryId == @country") 
        comps = list(solve.groupby('personId')['competitionId'].nunique()) 
    
        competitors = len(comps) 
        returners = len([x for x in comps if x >= 2])
    
        if competitors > 25: 
            dict_retrate[country] = (competitors, returners, truncate(100*returners / competitors , 2))
        else:
            dict_retrate[country] = (-1,-1,-1)

    retrate = pd.DataFrame.from_dict(dict_retrate, orient="index").reset_index(drop=False)
    retrate = retrate.rename(columns={"index":"Country", 0:"Competitors", 1:"Returners", 2:"Return Rate"})
    retrate = retrate[retrate['Return Rate'] >= 0]

    retrate = retrate.sort_values(by = 'Return Rate', ascending = False).reset_index(drop = True)
    retrate.index += 1
    # print(retrate.query("Country == 'Germany'"))
    writeToFile("\nreturn rate:\n", retrate.head(20))

# ## event combination
def eventCombi(queryCond):
    pd.set_option('display.max_colwidth', None)

    event_comb = df.query(queryCond
        )[['competitionId','eventSpecs']
        ].groupby('eventSpecs', as_index=False
        )['competitionId'].nunique(
        ).rename(columns = {'competitionId':'competitions'}
        ).sort_values(['competitions', 'eventSpecs'], ascending=[False, True]
        ).reset_index(drop=True)

    event_comb.index +=1
    writeToFile("\nevent combi (" + queryCond + "):\n", event_comb.head(15))

## average events per competitor
def eventsPerCompetitor(queryCond):
    compz = df.query(queryCond)

    gare = list(set(compz['competitionId']))

    dict_avgevents = {}

    for c in gare:
        subset = compz.query("competitionId == @c")
        count = subset['eventId'].nunique()
        count2 = subset.groupby('personId')['eventId'].nunique().mean()
    
        dict_avgevents[c] = (count, count2)
    
    avgevents = pd.DataFrame.from_dict(dict_avgevents, orient="index"
                            ).reset_index(drop=False
                            ).rename(columns={"index":"competition", 0:"events", 1:"avg events per competitor"}
                            ).sort_values(by = 'avg events per competitor', ascending = False
                            ).reset_index(drop = True)

    avgevents.index += 1
    writeToFile("\nevents per competitor (" + queryCond + "):\n", avgevents.head(15))

## average rounds per competitor
def roundsPerCompetitor():
    compz = df.query("countryId == 'Germany' and year == 2023")

    gare = list(set(compz['competitionId']))

    dict_avgevents = {}

    for c in gare:
        subset = compz.query("competitionId == @c")
        count = subset.groupby('eventId')['roundTypeId'].nunique().sum()
        tmp = subset.groupby('personId')['eventId']
        count2 = tmp.count().mean()
    
        dict_avgevents[c] = (count, count2)
    
    avgevents = pd.DataFrame.from_dict(dict_avgevents, orient="index"
                            ).reset_index(drop=False
                            ).rename(columns={"index":"competition", 0:"rounds", 1:"avg rounds per competitor"}
                            ).sort_values(by = 'avg rounds per competitor', ascending = False
                            ).reset_index(drop = True)

    avgevents.index += 1
    writeToFile("\nrounds per competitor\n", avgevents.head(15))


# calling all the stuff
mostCompetitor("countryId == 'Germany' and year == 2023")
mostCompetitor("countryId == 'Germany'")
retRate()

data = createPersonDf()
personYears(data)
fmale(data)
newCommerFemale(data)

eventCombi("countryId == 'Germany' and year == 2023")
eventCombi("countryId == 'Germany'")

eventsPerCompetitor("countryId == 'Germany' and year == 2023")
eventsPerCompetitor("countryId == 'Germany'")

roundsPerCompetitor()


