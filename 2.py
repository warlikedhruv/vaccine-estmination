import pandas as pd
import datetime

dates = []
start = datetime.datetime.strptime("17-03-2021", "%d-%m-%Y")
end = datetime.datetime.strptime("17-03-2022", "%d-%m-%Y")
date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]

for date in date_generated:
    dates.append(date.strftime("%Y-%m-%d"))

print(dates)

data = pd.DataFrame(dates)

data = data.set_index(0)
print(data.index)
df = pd.read_csv('share-people-vaccinated-covid.csv')
world= df.loc[df['Entity'] == 'World']
world = world.drop(['Code','Entity'], axis=1)

print(world)