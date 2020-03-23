# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 23:13:37 2020

@author: ADMIN
"""
import pandas as pd
import json
import numpy as np

df = pd.read_csv('game_data_2.csv')
df = df.replace({np.nan:None})
df= df.to_dict('records')
with open('game_db.json', 'w') as game_data:
    json.dump(df, game_data)