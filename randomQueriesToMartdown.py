import datetime
from mysql.connector import connect, Error
import pandas as pd

def db(filename):
    try:
        with connect(
            host="localhost",
            user="user",
            password="password",
            database="test",
        ) as connection:
            print(connection)
            with connection.cursor() as cursor:
                with open('data_sql/splited/'+filename, 'r') as f:
                    cursor.execute(f.read(), multi=True)
    except Error as e:
        print(e)


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

def fillDB():
    for file in sorted(os.listdir('data_sql/splited')):
        filename = os.fsdecode(file)
        print(filename)
        db(filename)

# read random queries and save every query to list
queries = []
f = open('randomQueries.sql', 'r')
currentq = ""
FILE = "randomQueries.txt"

# Iterate over lines.
for line in f:
    if line.startswith('--- '):
        continue
    elif len(line.strip()) == 0:
        queries.append(currentq)
        currentq = ""
    else:
        currentq = currentq.replace("\n", "")
        currentq = currentq + line 

f.close()

for query in queries:
    r = executeQuery(query)
    df = pd.DataFrame(r[1])
    for ix in range(len(r[0])):
        df.rename(columns = {ix:r[0][ix]}, inplace=True)
    
    f = open(FILE, "a")
    f.write("\n\n")
    f.write((df.head(18)).to_markdown())
    f.close()