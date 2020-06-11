import pandas as pd
from itertools import count
from datetime import datetime
from matplotlib import pyplot as plt
from matplotlib import dates as mpl_dates
import json
from urllib.request import urlopen
import urllib
import ssl

def readJSON():
    req = urllib.request.Request(
        "[API_URL]")
    sslCtx = ssl.SSLContext()

    with urlopen(req, context=sslCtx) as rona_json:
        read_json = rona_json.read()

    py_json = json.loads(read_json)
    newDict = dict()

    for item in py_json['covidTimeSeries']:
        date = item['referenceDate']
        confirmedTot = item['totalConfirmed']
        deathsTot = item['totalDeaths']
        casesDay = item['dayConfirmed']
        deathsDay = item['dayDeaths']
        date_to_time = datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
        newDict[date_to_time] = confirmedTot, deathsTot, casesDay, deathsDay

    return(newDict)


plt.style.use('seaborn')

tbd = readJSON()

x_dates = []
y_cases = []
y_deaths = []
y_dayCases = []
y_dayDeaths = []


for date, cases in tbd.items():
    x_dates.append(date)
    y_cases.append(cases[0])
    y_deaths.append(cases[1])
    y_dayCases.append(cases[2])
    y_dayDeaths.append(cases[3])

print(x_dates)

fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)

ax1.plot_date(x_dates, y_cases, color='red', linestyle='solid', marker=',', linewidth='2', label='US Cases')
ax1.plot_date(x_dates, y_deaths, color='blue', linestyle='--', marker=',', linewidth='2', label='Total Deaths')
ax2.plot_date(x_dates, y_dayCases, color='orange', linestyle='solid', marker=',', linewidth='2', label='Cases per Day')
ax2.plot_date(x_dates, y_dayDeaths, color='purple', linestyle='--', marker=',', linewidth='2', label='Deaths per Day')


plt.gcf().autofmt_xdate()

date_format = mpl_dates.DateFormatter('%b, %d %Y')
plt.gca().xaxis.set_major_formatter(date_format)

ax1.set_title('Corona Cases Over Time')
ax1.set_ylabel('Corona Cases')
ax1.legend()

ax2.set_title('Corona Cases per Day')
ax2.set_ylabel('Corona Cases')
ax2.legend()

plt.tight_layout()

plt.show()