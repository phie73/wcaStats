import matplotlib.pyplot as plt
from mysql.connector import connect, Error
import pandas as pd


def executeQuery(query):
    ret = []
    with connect(host="localhost", user="user", password="password", database="test") as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            column_names = [tup[0] for tup in cursor.description]
            result = cursor.fetchall()
            ret.append(column_names)
            ret.append(result)
        return ret


query = "select count(distinct id) as number, extract(year from start_date) as year from Competitions where countryId = 'Germany' and extract(year from start_date) in (select distinct extract(year from start_date) from Competitions where countryId = 'Germany') group by year order by year"
res = executeQuery(query)

df = pd.DataFrame(res[1])
for ix in range(len(res[0])):
    df.rename(columns = {ix:res[0][ix]}, inplace=True)


years = df['year'].tolist()
comps = df['number'].tolist()

plt.rcParams["figure.figsize"] = (12, 6)
# fig = plt.figure()
# ax = fig.add_subplot(111)

plt.plot(years, comps, 'x-', color="green")
plt.title("number of comps in germany")
plt.xlabel("years")
plt.ylabel("comps")
plt.xticks(years[::2])

for i, v in enumerate(comps):
    plt.annotate(str(v), xy=(years[i],comps[i]), xytext=(-7,7), textcoords='offset points')


plt.savefig("compCount.png")