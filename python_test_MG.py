import pandas as pd
import numpy as np
import datetime


tab = pd.read_csv('tab1.csv')     #Считываем таблицу
tab['created'] = pd.to_datetime(tab['created']).dt.floor('D')      #Отбрасываем часы-минуты-секунды

dates = tab.groupby('user_id').agg(min_date = ('created', np.min), max_date = ('created', np.max))   #Первый и последний вход#
dates['week_start'] = dates['min_date'].dt.to_period('W').apply(lambda r: r.start_time)  #Разница между первым и последним входом в днях

dates['user_id'] = dates.index
df = dates.drop(['min_date','max_date'], axis = 1)

gm = df.groupby(by=['week_start'])
count = gm['user_id'].count()
count = count.to_frame()
count = count.rename(columns={"user_id": "day_1"})

n = 9            # За сколько дней смотрим Retention

for i in range(1, n):
    name = 'day_' + str(i + 1)
    name_prev = 'day_' + str(i)
    
    gm = df[df['diff'] == i].groupby(by=['week_start'])  # Сколько пользователей "отвалилось на i-й день"
    temp = gm['user_id'].count()
    temp = temp.to_frame()
    temp = temp.rename(columns={"user_id": 'temporary'})
    
    count = pd.merge(count, temp, left_on = 'week_start', right_index=True)
    count[name] = count[name_prev] - count['temporary']  # Сколько пользователей осталось
    count = count.drop('temporary',axis = 1)

display(count)
