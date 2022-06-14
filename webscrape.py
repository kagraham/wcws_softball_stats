#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 10:51:57 2022

@author: kgraham

tutorials from: https://towardsdatascience.com/web-scraping-html-tables-with-python-c9baba21059
and https://oxylabs.io/blog/python-web-scraping
"""


from selenium import webdriver
import lxml.html as lh
import pandas as pd

links = ['https://soonersports.com/sports/softball/stats',
         'https://texassports.com/sports/softball/stats/2022',
         'https://uclabruins.com/sports/softball/stats/2022',
         'https://okstate.com/sports/softball/stats',
         'https://nusports.com/sports/softball/stats/2022',
         'https://arizonawildcats.com/sports/softball/stats',
         'https://osubeavers.com/sports/softball/stats/2022?path=softball',
         'https://floridagators.com/sports/softball/stats']
univ = [ 'Oklahoma', 'Texas', 'UCLA', 'Oklahoma_State', 'Northwestern', 
        'Arizona', 'Oregon_State', 'Florida' ]
driver = webdriver.Chrome(executable_path='/Users/kgraham/Downloads/chromedriver')

for z in range(0,len(links)):
    driver.get( links[z] )
    
    content = driver.page_source
    doc = lh.fromstring(content)
    doc.xpath('//tr')
    elem = doc.xpath('//tr')
    
    uni = univ[z]
    print('{}'.format(uni))
    # ------------------------------------------------ #
    # individual batting table
    print('TABLE 1')
    cols = []
    i = 0
    # For each row, store each first element (header) and an empty list
    for t in elem[0]:
        i += 1
        name=t.text_content()
        #print( '{}: {}'.format(i,name) )
        cols.append((name,[]))
    
    for j in range(1,len(elem)):
        #T is our j'th row
        T=elem[j]
        
        # needs to be size 23 each row 
        if len(T)!=23:
            next_idx = j
            break
        
        # i column index
        i=0
        
        # Iterate through each element of the row
        for t in T.iterchildren():
            data=t.text_content() 
            # Check if row is empty
            if i>0:
            # Convert any numerical value to integers
                try:
                    data=int(data)
                except:
                    pass
            # Append the data to the empty list of the i'th column
            cols[i][1].append(data)
            # Increment i for the next column
            i+=1
            
    Dict = {title:column for (title,column) in cols}
    df1 = pd.DataFrame(Dict)
    df1.to_csv('/Users/kgraham/github_build/softball_wcws/data/{}/df1.csv'.format(uni))
    
    df = {}
    for x in range(0,7): # number of data tables we want
        print('TABLE {}'.format(x+2))
        # get header info    
        i=0
        next_cols = []
        for t in elem[next_idx]:
            i += 1
            name=t.text_content()
            #print( '{}: {}'.format(i,name) )
            next_cols.append((name,[]))
    
        for j in range(next_idx+1,len(elem)):
            #T is our j'th row
            T=elem[j]
        
            # data row needs to match number of columns
            if len(T)!= len(next_cols):
                next_idx = j
                break
        
            # i column index
            i = 0
            
            # Iterate through each element of the row
            for t in T.iterchildren():
                data=t.text_content() 
                # Check if row is empty
                if i>0:
                # Convert any numerical value to integers
                    try:
                        data=int(data)
                    except:
                        pass
                # Append the data to the empty list of the i'th column
                next_cols[i][1].append(data)
                # Increment i for the next column
                i+=1
        
        Dict = {title:column for (title,column) in next_cols}
        df[x+2] = pd.DataFrame(Dict)
        df[x+2].to_csv('/Users/kgraham/github_build/softball_wcws/data/{}/df{}.csv'.format(uni, x+2))

