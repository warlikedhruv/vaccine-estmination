import pandas as pd
from people_left import count_people_left, add_years_to_data, predict_values
import datetime


df = pd.read_csv('share-people-vaccinated-covid.csv')
df_country= df.loc[df['Entity'] == 'Africa']
df_country = df_country.drop(['Code','Entity'], axis=1)


population_africa = 1363973822



updated_df = df_country.set_index('Day')
print(updated_df)


#data1 = predict_values(updated_df)
#print(data1)
#data2 = predict_values(data1)
#print(data2)


#df_population_africa_left = count_people_left('Africa', population_africa, data)
temp_data = updated_df.copy()
while True:
    try:
        data1 = predict_values(pd.DataFrame(temp_data))
    #del temp_data
        temp_data = data1.copy()
    except:
        pass
    df_population_africa_left = count_people_left('Africa', population_africa, data1)


    if df_population_africa_left['remaining_population'].iloc[-1] <= 0:
        break
    else:
        df_population_africa_left.to_csv('final.csv')


df_population_africa_left = df_population_africa_left[::-1]
print(df_population_africa_left)

for index, row in df_population_africa_left.iterrows():
    if row['remaining_population'] > 0:
        last_day = index
        break
print("the vaccination in Africa will be completed in :",last_day)