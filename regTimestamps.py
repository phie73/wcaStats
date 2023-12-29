import datetime
from mysql.connector import connect, Error
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os 


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
    with connect(host="localhost", user="user", password="password", database="test") as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        return result

def fillDB():
    for file in sorted(os.listdir('data_sql/splited')):
        filename = os.fsdecode(file)
        print(filename)
        db(filename)

def label(ax, data):
    for label in ax.get_xticklabels(which='major'):
        label.set(rotation=30, horizontalalignment='right')
    if len(data) >= compLimit:
        ax.plot(timestamps[compLimit - 1], compLimit, 'go', label='marker only') 
        ax.text(timestamps[compLimit - 1], compLimit, timestamps[compLimit - 1])
        ax.axvline(x=timestamps[compLimit - 1], color='r', linestyle='-')

def fixDateLines(ax):
    ax.axhline(y=compLimit, color='r', linestyle='-')

def plotStuff(ax, data, title, secs, format):
    ax.hist(data)
    ax.set_title(title)
    ax.xaxis.set_major_locator(mdates.SecondLocator(interval=secs))
    ax.xaxis.set_major_formatter(mdates.DateFormatter(format))
    if len(data) >= compLimit:
        fixDateLines(ax)
    label(ax, data)

# fill db with data (takes long don't to it if filled already)
# fillDB()

#Competition IDs
comps = []
qc = "select id from Competitions where countryId = 'Germany' and extract(year from start_date) = 2023;"
res = executeQuery(qc)
for comp in res:
    comps.append(comp[0])

for comp in comps:
    q = "select r.competition_id, c.competitor_limit, r.created_at, c.registration_open from registrations r join Competitions c on c.id = r.competition_id where c.countryId = 'Germany' and extract(year from c.start_date) = 2023 and r.competition_id = '" + comp + "' order by r.created_at asc;"
    r = executeQuery(q)

    compName = r[0][0]
    compLimit = r[0][1]
    regOpen = r[0][3]

    timestamps = []
    firstDay = []
    firstH = []
    first10Min = []
    first5Min = []
    firstMin = []

    # 24h
    d1 = regOpen + datetime.timedelta(days=1)
    # first 1h
    d2 = regOpen + datetime.timedelta(hours=1)
    # first 10min
    d3 = regOpen + datetime.timedelta(minutes=10)
    # first 5min
    d4 = regOpen + datetime.timedelta(minutes=5)
    # first 1min
    d5 = regOpen + datetime.timedelta(minutes=1)

    orgaCount = 0

    for row in r:
        timestamps.append(row[2])
        if row[2] < regOpen:
            orgaCount = orgaCount + 1
        if row[2] > regOpen and row[2] < d1:
            firstDay.append(row[2])
        if row[2] > regOpen and row[2] < d2:
            firstH.append(row[2])
        if row[2] > regOpen and row[2] < d3:
            first10Min.append(row[2])
        if row[2] > regOpen and row[2] < d4:
            first5Min.append(row[2])
        if row[2] > regOpen and row[2] < d5:
            firstMin.append(row[2])

    # figure settings
    plt.rcParams["figure.figsize"] = (16, 12)
    fig, axs = plt.subplots(3, 2)
    fig.tight_layout(pad=4.0) 
    fig.suptitle("registration timeline " + compName + " (opened: " + str(regOpen) + ", limit: " + str(compLimit) + ")")
    # Set common labels
    fig.supylabel('registrations')
    fig.supxlabel('time')
    ax1, ax2, ax3, ax4, ax5, ax6 = axs.flatten()

    plotStuff(ax1, timestamps, "total (" + str(len(timestamps)) + ")", 604800, '%D')
    plotStuff(ax2, firstDay, "first day (" + str(len(firstDay)) + " + " + str(orgaCount) + " (orga))", 3600, '%H:%M')
    plotStuff(ax3, firstH, "first hour( " + str(len(firstH)) + " + " + str(orgaCount) + " (orga))", 180, '%M:%S')
    plotStuff(ax4, first10Min, "first 10 min (" + str(len(first10Min)) + " + " + str(orgaCount) + " (orga))", 30, '%M:%S')
    plotStuff(ax5, first5Min, "first 5 min (" + str(len(first5Min)) + " + " + str(orgaCount) + " (orga))", 15, '%M:%S')
    plotStuff(ax6, firstMin, "first min (" + str(len(firstMin)) + " + " + str(orgaCount) + " (orga))", 3, '%M:%S')

    plt.savefig("fig/regTimeline" + compName + ".png")
