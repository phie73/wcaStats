# wcaStats

just a collection of statistics I found interesting to make. As of now:
- distribution of comps in federal states in germany [plot](foo.png)
- ((competitiors in event y) / (total competitors of comp)) / number of fist rounds in event y in germany

event | factor | num comps | total rounds |
------------- | ------------- | ---- | --- |
333 | 0.97 | 23 | 67 |
222 | 0.86  | 15 | 44 |
pyram | 0.75 | 14 | 28 |
444 | 0.74 | 20 | 38 |
333oh | 0.66 | 14 | 27 |
555 | 0.64 | 23 | 43 |
skewb | 0.63 | 15 | 29 |
clock | 0.55 | 13 | 25 |
666 | 0.52 | 15 | 24 |
777 | 0.50 | 15 | 26 |
minx | 0.49 | 12 | 18 |
sq1 | 0.48 | 9 | 20 |
333fm | 0.38 | 9 | 9 |
333bf | 0.37 | 15 | 24 |
333mfb | 0.29 | 4 | 4 |
444bf | 0.22 | 10 | 10 |
555bf | 0.11 | 9 | 9 |

- events newcommers participate in (newcommer are ppl with a 2023 id and total comps all comps they have been to)
    - newcommers: 513
    - comps: 785
    - newcommers been to more than one comp: 150
      
event | total comps | first comp |
--- | --- | --- |
333 | 753 | 500 |
222 | 467 | 197 |
pyram | 315 | 113 |
444 | 303 | 104 |
skewb | 198 | 62 |
555 | 160 | 43 |
333oh | 140 | 42 |
clock | 77 | 18 |
minx | 75 | 25 |
666 | 46 | 12 |
777 | 46 | 9 |
sq1 | 38 | 11 |
333bf | 34 | 7 |
333fm | 25 | 8 |
444bf | 5 | 0 |
333mbf | 2 | 0 |
555bf | 0 | 0 |
 

## to get it running

- download tsv from [here](https://www.worldcubeassociation.org/export/results) safe in folder called `data`
- python virtual enviornment find out how it works for you :)
- and after it is running install all requirements doing ``pip install -r requirements.txt``
