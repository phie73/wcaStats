# wcaStats

just a collection of statistics I found interesting to make. As of now:
- distribution of comps in federal states in germany
- ((competitiors in event y) / (total competitors of comp)) / number of fist rounds in event y in germany
- events newcommers participate in (newcommer are ppl with a 2023 id and total comps all comps they have been to)
- gender distribution
- evulation of reg fees 2017 to 2023
- comps with most competitors
- newcommers over years
- return rate
- event combinations on comps
- average events per competitors
- registration timestamps

find everything [here](https://pad.hacknang.de/s/stats_german_cubing_community#)
 

## to get it running

- download tsv from [here](https://www.worldcubeassociation.org/export/results) safe in folder called `data`
- python virtual enviornment find out how it works for you :
- and after it is running install all requirements doing ``pip install -r requirements.txt``

for regTimestamps database is needed:
- can be found [here](https://www.worldcubeassociation.org/wst/wca-developer-database-dump.zip)
- setup local mariadb and connect to it