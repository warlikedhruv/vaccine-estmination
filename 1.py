import pandas as pd
import warnings
from datetime import datetime, timedelta
import itertools
import numpy as np
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
plt.style.use('fivethirtyeight')
import pandas as pd
import statsmodels.api as sm

import matplotlib
matplotlib.rcParams['axes.labelsize'] = 14
matplotlib.rcParams['xtick.labelsize'] = 12
matplotlib.rcParams['ytick.labelsize'] = 12
matplotlib.rcParams['text.color'] = 'k'



dates = []
start = datetime.strptime("17-03-2021", "%d-%m-%Y")
end = datetime.strptime("31-12-2021", "%d-%m-%Y")
date_generated = [start + timedelta(days=x) for x in range(0, (end-start).days)]

for date in date_generated:
    dates.append(date.strftime("%Y-%m-%d"))

print(dates)

data = pd.DataFrame(dates)

data = data.set_index(0)





df = pd.read_csv('share-people-vaccinated-covid.csv')
print(df.Entity.unique())
world = df.loc[df['Entity'] == 'Africa']
print(world)
start = world['Day'].max()
print(world['Day'].min(), world['Day'].max())

world = world.drop(['Code','Entity'], axis=1)
world = world.sort_values('Day')
print(world)
print(world.isnull().sum())

world = world.set_index('Day')
print(world.index)
y = world['people_vaccinated_per_hundred']
y.plot(figsize=(15, 6))
plt.show()

p = d = q = range(0, 2)
pdq = list(itertools.product(p, d, q))
seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]
print('Examples of parameter combinations for Seasonal ARIMA...')
print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[1]))
print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[2]))
print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[3]))
print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[4]))


for param in pdq:
    for param_seasonal in seasonal_pdq:
        try:
            mod = sm.tsa.statespace.SARIMAX(y,
                                            order=param,
                                            seasonal_order=param_seasonal,
                                            enforce_stationarity=False,
                                            enforce_invertibility=False)
            results = mod.fit()
            print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))
        except:
            continue

mod = sm.tsa.statespace.SARIMAX(y,
                                order=(1, 1, 1),
                                seasonal_order=(1, 1, 0, 12),
                                enforce_stationarity=False,
                                enforce_invertibility=False)
results = mod.fit()
print(results.summary().tables[1])

results.plot_diagnostics(figsize=(16, 8))
plt.show()

#pred = results.get_prediction(start=pd.to_datetime('2021-03-17'), end=pd.to_datetime('2021-12-31'))
#pred_ci = pred.conf_int()
#print(pred_ci)
#print(pred)


pred = results.predict(data)
pred_ci = pred.conf_int()
print(pred_ci)
print(pred)
