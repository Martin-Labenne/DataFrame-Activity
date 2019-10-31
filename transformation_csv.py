# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 15:18:38 2019

@author: marti
"""

import pandas as pd
import datetime as dt 

births = pd.read_csv('births.csv')
births = births.dropna() # drop na data 

def is_leap(year) : #test whether or not year is leap
    return (year%4==0)

###### drop non sens data from biths df ########
    
labels = [] # labels to drop from the dataset
thirty_one = [1,3,5,7,8,10,12]
thirty = [4,6,9,11]
for i in range(len(births)) : 
    if births['month'][i] == 2 : #in february
        if is_leap(births['year'][i]) : # in leap_year
            if births['day'][i] > 29 : 
                labels.append(i)
        else :
            if births['day'][i] > 28 : 
                labels.append(i)
            
    if births['month'][i] in thirty : # in 30 days' months
        if births['day'][i] > 30 : 
            labels.append(i)
            
    if births['month'][i] in thirty_one : # in 31 days' months
        if births['day'][i] > 31 : 
            labels.append(i)
            
births = births.drop(labels, axis='index') # drop non sens data

##### transform year, month, day colones to a date one ######

date = {'date':[]}
for index in births.index:    # create date Serie  
    date['date'].append(dt.date(births['year'][index],
                            births['month'][index],
                            int(births['day'][index])))
    # date is now a datetime Series 

date = pd.DataFrame(date)   # date is now df so we can merge 

births_transformed = pd.merge(births.copy()[['gender','births']], date,
                              left_on=births.index, right_on = date.index)

del births_transformed['key_0']

## group the data by date and agregate male and female birhts by date ##
gb = births_transformed.groupby('date')['births'].sum()
gb = pd.DataFrame(gb)

##### extact 3 dataframes : 60s, 70s, 80s  ######

# before 1970, January, the 1st
sixties = gb[gb.index.values < dt.date(1970, 1, 1)]

# between before 1970, January, the 1st and 1980, January, the 1st
seventies = gb[~(dt.date(1970, 1, 1) <= gb.index.values) ^  
               (gb.index.values < dt.date(1980, 1, 1))] 
# not xor to achieve bool Array conjontion

# after 1980, January, the 1st
heighties = gb[gb.index.values >= dt.date(1980, 1, 1)]

#### add a new column 'weekDay' in each DataFrame ####

weekDays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
            'Friday', 'Saturday', 'Sunday']

dfs = [sixties, seventies, heighties]

for i in range(len(dfs)) : 
    temp = {'weekDay' : []}
    for date in dfs[i].index : # we fill temp with weekDay values
        temp['weekDay'].append(weekDays[date.weekday()]) # date.weekday()
    temp_df = pd.DataFrame(temp)                  # retourne un int (0 -> 6)
    dfs[i] = pd.merge(dfs[i], temp_df, on=dfs[i].index)

#### groupe by weekDay the aggregate by 'birth' (sum) #####
    
dfs[0] = pd.DataFrame(dfs[0].groupby('weekDay')['births'].sum())
dfs[1] = pd.DataFrame(dfs[1].groupby('weekDay')['births'].sum())
dfs[2] = pd.DataFrame(dfs[2].groupby('weekDay')['births'].sum())

#### sorting the data by weekDay ####
for i in range(len(dfs)) : 
    df = dfs[i].copy()
    df.index = weekDays
    for day in weekDays : 
        df['births'][day] = dfs[i]['births'][day]
    dfs[i] = df    
    
sixties = dfs[0]
seventies = dfs[1]
heighties = dfs[2]

####### extract DataFarme to CSV ##########
sixties.to_csv(path_or_buf = '60s.csv')
seventies.to_csv(path_or_buf = '70s.csv')
heighties.to_csv(path_or_buf = '80s.csv')