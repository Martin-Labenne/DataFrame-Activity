# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 15:18:38 2019

@author: marti
"""

import pandas as pd

births = pd.read_csv('births.csv')
births = births.dropna() 
date = {'date':[]}
for i in range(len(births)):    # create date Serie  
    date['date'].append(pd.to_datetime([births['year'][i],
                                       births['month'][i],
                                       births['day'][i]], yearfirst = True))

date = pd.DataFrame(date)

