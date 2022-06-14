#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 14:04:33 2022

@author: kgraham
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

univ = [ 'Oklahoma', 'Texas', 'UCLA', 'Oklahoma_State', 'Northwestern', 
        'Arizona', 'Oregon_State', 'Florida' ]

uni_colors = ['crimson', 'peru', 'dodgerblue', 'black', 'darkviolet', 
              'firebrick', 'orange', 'blue' ]

uni_colors2 = ['floralwhite', 'antiquewhite', 'gold', 'orange', 'whitesmoke',
               'navy', 'black', 'orangered']

path = '/Users/kgraham/github_build/softball_wcws/data/'

data_collections = ['ind_hitting', 'ind_pitching', 'ind_fielding',
                    'gbg_hitting', 'gbg_pitching']

# function to obtain regular and post-season dataframes // post season began 20 May 2022
def gbg_separate_season( df ):
    df.index = df.Date      # set datetime to df index
    reg_season = df[df.index < '2022-05-20']    # select games before 5/20
    post_season = df[df.index >= '2022-05-20']  # select games on and after 5/20
    return reg_season, post_season

# function to average games per month
def monthly_means( df ):
    if (type(df.index) == pd.DatetimeIndex):
        monthly_means = df.groupby( by= df.index.month ).mean() # group by month
        return monthly_means
    else:
        raise ValueError( 'dataframe index is not datetime' )

# function to calculate win/loss percentage 
def win_loss_pct_calc( df ):
    df.index = range(0,len(df))
    df['winloss'] = np.nan
    df['winlosspct'] = np.nan
    df.winloss[ df['W/L'] == 'W' ] = int(1)
    df.winloss[ df['W/L'] == 'L' ] = int(0)
    df.winlosspct = (df.winloss.cumsum() / (df.index+1)) * 100
    return df

# Win Loss Percentage Figure
fig, ax = plt.subplots(1,1)
for i in range(0,8):
   # university formatters
   uni = univ[i]
   uni_color = uni_colors[i]
   uni_color2 = uni_colors2[i]
   
   # calls proper df corresponding with university
   df_uni = pd.read_pickle(path + '{}/gbg_hitting.pkl'.format(uni) ) 
   
   # calculate win loss percentage & regular vs post season games
   df_uni_wlp = win_loss_pct_calc( df_uni )
   df_uni_reg_wlp, df_uni_post_wlp = gbg_separate_season( df_uni_wlp )
   df_uni_reg_wlp.index = range(0, len(df_uni_reg_wlp) )    # resets index
   df_uni_post_wlp.index = range(df_uni_reg_wlp.index.max()+1, df_uni_reg_wlp.index.max()+len(df_uni_post_wlp)+1 ) # resets index
   
   # plots entire season win percentage
   plt.plot(df_uni_reg_wlp.winlosspct, 'o-', label='{}'.format(uni), color=uni_color, markeredgecolor=uni_color2)
   plt.plot(df_uni_post_wlp.winlosspct, 'X-', color=uni_color, markeredgecolor=uni_color2)

# matplotlib formatters
#plt.legend()
plt.grid()
ax.set_facecolor('whitesmoke')
plt.ylabel('Win Percentage %', fontsize=18)
plt.title('Win Percentage During Complete Season', fontsize=18)
plt.xlabel('Game number', fontsize=18)
ax.tick_params(axis='x', labelsize=16)
ax.tick_params(axis='y', labelsize=16)
   

    
# Monthly mean stats per game figure
fig, ax = plt.subplots(nrows=3, ncols=2, sharex=True)
for i in range(0,8):
    # university formatters
   uni = univ[i]
   uni_color = uni_colors[i]
   uni_color2 = uni_colors2[i]
   
   #print(uni)
   df_gbg_hitting = pd.read_pickle(path + '{}/gbg_hitting.pkl'.format(uni) ) 
   df_gbg_pitching = pd.read_pickle(path + '{}/gbg_pitching.pkl'.format(uni) )
   hitting = gbg_separate_season( df_gbg_hitting )[0]   # only calling reg season df
   pitching = gbg_separate_season( df_gbg_pitching )[0] # only calling reg season df
   hitting_monthly_means = monthly_means(hitting)
   pitching_monthly_means = monthly_means(pitching)   
   
   # hitting stats
   avg = hitting_monthly_means.AVG
   runs = hitting_monthly_means.R
   sb = hitting_monthly_means.SB
   
   # pitching stats
   era = pitching_monthly_means.ERA
   walks = pitching_monthly_means.BB
   runs_def = pitching_monthly_means.R
   
   # plot values in each subplot
   # offensive vals
   ax00 = ax[0,0].plot(avg, 'o-', label=uni, color=uni_color, markeredgecolor=uni_color2)
   ax10 = ax[1,0].plot(runs, 'o-', label=uni, color=uni_color, markeredgecolor=uni_color2)
   ax20 = ax[2,0].plot(sb, 'o-', label=uni, color=uni_color, markeredgecolor=uni_color2)
   # pitching vals
   ax01 = ax[0,1].plot(era, 'o-', color=uni_color, markeredgecolor=uni_color2)
   ax11 = ax[1,1].plot(runs_def, 'o-', color=uni_color, markeredgecolor=uni_color2)
   ax21 = ax[2,1].plot(walks, 'o-', color=uni_color, markeredgecolor=uni_color2)

# figure formatting
plt.suptitle('Stats Per Game, Averaged Monthly', fontsize=20)   
ax[0,0].set_ylim( [.2, .42] )
ax[0,0].yaxis.set_major_formatter(FormatStrFormatter('%.3f'))
ax[0,0].set_xticks( [2,3,4,5] )
ax[0,0].set_xticklabels( ['Feb', 'Mar', 'Apr', 'May'] )
ax[2,0].tick_params(axis='x', labelsize=14)
ax[2,1].tick_params(axis='x', labelsize=14)
ax[0,0].tick_params(axis='y', labelsize=14)
ax[1,0].tick_params(axis='y', labelsize=14)
ax[2,0].tick_params(axis='y', labelsize=14)
ax[0,1].tick_params(axis='y', labelsize=14)
ax[1,1].tick_params(axis='y', labelsize=14)
ax[2,1].tick_params(axis='y', labelsize=14)

ax[0,0].set_title('Offense', fontsize=18)
ax[0,1].set_title('Pitching', fontsize=18)

ax[1,0].set_ylim( [0, 11] )
ax[1,1].set_ylim( [0, 11] )

ax[0,0].set_ylabel('Batting Average', fontsize=16)
ax[1,0].set_ylabel('Runs Scored', fontsize=16)
ax[2,0].set_ylabel('Stolen Bases', fontsize=16)
ax[0,1].set_ylabel('Earned Run Average', fontsize=16)
ax[1,1].set_ylabel('Runs Allowed', fontsize=16)
ax[2,1].set_ylabel('Walks Allowed', fontsize=16)

ax[0,0].set_facecolor('whitesmoke')
ax[1,0].set_facecolor('whitesmoke')
ax[2,0].set_facecolor('whitesmoke')
ax[0,1].set_facecolor('whitesmoke')
ax[1,1].set_facecolor('whitesmoke')
ax[2,1].set_facecolor('whitesmoke')
   
ax[0,0].grid()
ax[1,0].grid()
ax[2,0].grid()
ax[0,1].grid()
ax[1,1].grid()
ax[2,1].grid()