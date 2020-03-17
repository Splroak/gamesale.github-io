# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 23:13:37 2020

@author: ADMIN
"""
import pandas as pd
import sqlite3

game_db = pd.read_csv('game_data_2.csv')
conn = sqlite3.connect("game_data.db")
game_db.to_sql('games', conn, if_exists='append', index=False)

c = conn.cursor()
c.execute