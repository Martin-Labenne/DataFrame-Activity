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

date = pd.DataFrame(date)   # date is now df so we can merge 

births_transformed = pd.merge(births.copy()[['gender','births']], date,
                              left_on=births.index, right_on = date.index)

del births_transformed['key_0']

gb = births_transformed.groupby('date')['births'].sum()