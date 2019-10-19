# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 15:18:38 2019

@author: marti
"""

import pandas as pd
import datetime as dt 

births = pd.read_csv('births.csv')
#births = births.dropna() 

date = {'date':[]}
for i in range(len(births)):    # create date Serie  
    date['date'].append(dt.date(births['year'][i],
                            births['month'][i],
                            int(births['day'][i])))

date = pd.DataFrame(date)

del births['year']
del births['month']
del births['day']

births_transformed = pd.merge(births, date, left_on=births.index,
                              right_on = date.index)

del births_transformed['key_0']
