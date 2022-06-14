#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 14:11:33 2022

@author: kgraham
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

univ = [ 'Oklahoma', 'Texas', 'UCLA', 'Oklahoma_State', 'Northwestern', 
        'Arizona', 'Oregon_State', 'Florida' ]

path = '/Users/kgraham/github_build/softball_wcws/data/'

for i in range( 0, len(univ) ):
    uni = univ[i]
    
    #for i in range(0,8):
    df1 = pd.read_csv(path + '{}/df1.csv'.format(uni) ) # individual hitting
    df2 = pd.read_csv(path + '{}/df2.csv'.format(uni) ) # individual pitching
    df3 = pd.read_csv(path + '{}/df3.csv'.format(uni) ) # individual fielding
    df4 = pd.read_csv(path + '{}/df4.csv'.format(uni) ) # conference hitting
    df5 = pd.read_csv(path + '{}/df5.csv'.format(uni) ) # conference pitching
    df6 = pd.read_csv(path + '{}/df6.csv'.format(uni) ) # conference fielding
    df7 = pd.read_csv(path + '{}/df7.csv'.format(uni) ) # game by game hitting
    df8 = pd.read_csv(path + '{}/df8.csv'.format(uni) ) # game by game pitching
    
    # df1,2,3 (not using 4,5,6 for now)
    df1.drop(['Unnamed: 0', 'Player', 'Bio Link'], axis=1, inplace=True)
    df1.dropna(axis=0, inplace=True)
    df1['#'] = df1['#'].astype(int)
    df1.to_pickle( path + '{}/ind_hitting.pkl'.format(uni))    
    
    df2.drop(['Unnamed: 0', 'Player', 'Bio Link'], axis=1, inplace=True)
    df2.dropna(axis=0, inplace=True)
    df2['#'] = df2['#'].astype(int)
    df2.to_pickle( path + '{}/ind_pitching.pkl'.format(uni))    
    
    df3.drop(['Unnamed: 0', 'Player', 'Bio Link'], axis=1, inplace=True)
    df3.dropna(axis=0, inplace=True)
    df3['#'] = df3['#'].astype(int)
    df3.to_pickle( path + '{}/ind_fielding.pkl'.format(uni))    
    
    # df7
    df7.Date = pd.to_datetime(df7.Date, infer_datetime_format=True, errors='coerce')
    df7.drop(['Unnamed: 0'], axis=1, inplace=True)
    df7.Loc = df7.Loc.astype(str)
    df7.Loc[df7.Loc == ' at '] = 'visitor'
    df7.Loc[df7.Loc == ' vs '] = 'home'
    df7.Loc[df7.Loc == ' nan '] = 'neutral'
    df7.dropna(axis=0, inplace=True)
    df7.to_pickle( path + '{}/gbg_hitting.pkl'.format(uni))    
    
    # df8
    df8.Date = pd.to_datetime(df8.Date, infer_datetime_format=True, errors='coerce')
    df8.drop(['Unnamed: 0'], axis=1, inplace=True)
    df8.Loc = df8.Loc.astype(str)
    df8.Loc[df8.Loc == ' at '] = 'visitor'
    df8.Loc[df8.Loc == ' vs '] = 'home'
    df8.Loc[df8.Loc == ' nan '] = 'neutral'
    df8.dropna(axis=0, inplace=True)
    df8.to_pickle( path + '{}/gbg_pitching.pkl'.format(uni))    