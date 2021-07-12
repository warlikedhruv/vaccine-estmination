import pandas as pd
import statsmodels.api as sm
import itertools
from statsmodels.tsa.arima.model import ARIMA
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings("ignore")
def count_people_left(country,population , data_pop):
    vaccinated_ratio = data_pop['people_vaccinated_per_hundred'].to_list()
    population_remaining = population
    remaining_list = []
    #print(vaccinated_ratio)
    for ratio in vaccinated_ratio:
        if population_remaining < 0:
            remaining_list.append(-100)
        else:
            one_day_people_count =  int((population_remaining * ratio ) // 100)
            if population_remaining < 100:
                population_remaining -= int(ratio)
            else:
                population_remaining -= one_day_people_count
            remaining_list.append(population_remaining)#print(one_day_people_count)
    data_pop['remaining_population'] = remaining_list
    return data_pop

def add_years_to_data(data):
    start = datetime.strptime("18-03-2021", "%d-%m-%Y")
    end = datetime.strptime("17-03-2022", "%d-%m-%Y")
    date_generated = [start + timedelta(days=x) for x in range(0, (end - start).days)]
    for date in date_generated:
        data = data.append(pd.Series([date.strftime("%Y-%m-%d"), 0.0], index=['Day','people_vaccinated_per_hundred']), ignore_index=True)
    return data

def predict_values(data):
    y = data[:'2021-03-17']
    test = data
    """
    model = ARIMA(y, order=(1, 1, 1))
    model_fit = model.fit()
    """
    p = d = q = range(0, 2)
    pdq = list(itertools.product(p, d, q))
    seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]
    #print('Examples of parameter combinations for Seasonal ARIMA...')
    #print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[1]))
    #print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[2]))
    #print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[3]))
    #print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[4]))

    for param in pdq:
        for param_seasonal in seasonal_pdq:
            try:
                mod = sm.tsa.statespace.SARIMAX(y,
                                                order=param,
                                                seasonal_order=param_seasonal,
                                                enforce_stationarity=False,
                                                enforce_invertibility=False)
                results = mod.fit()
                #print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))
            except:
                continue

    mod = sm.tsa.statespace.SARIMAX(y,
                                    order=(1, 1, 1),
                                    seasonal_order=(1, 1, 0, 12),
                                    enforce_stationarity=False,
                                    enforce_invertibility=False)
    results = mod.fit()
    print(results.summary().tables[1])



    yhat = results.predict(start=len(data)+1, end=len(data)+365)
    y  = yhat.to_list()
    start = datetime.strptime(data.index[-1], "%Y-%m-%d")
    print(start)
    end = datetime.strptime("2021-03-17", "%Y-%m-%d")
    print(end)
    date_generated = [start + timedelta(days=x) for x in range(0, 365)]
    print(date_generated)


    new_data = pd.DataFrame()
    for i in range(len(date_generated)):
        new_data = new_data.append(pd.Series([date_generated[i].strftime("%Y-%m-%d"),y[i] ], index=['Day', 'people_vaccinated_per_hundred']),
                           ignore_index=True)
    new_data = new_data.set_index('Day')
    print(new_data)
    data = data.append(new_data)
    return data
