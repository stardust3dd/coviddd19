#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from datetime import date 

# Scraping
import requests 
from bs4 import BeautifulSoup 
import numpy as np 


# In[2]:


extract_contents = lambda row: [x.text.replace('\n', '') for x in row] 
URL = 'https://www.mohfw.gov.in/'

response = requests.get(URL).content 
soup = BeautifulSoup(response, 'html.parser') 

stats = [] 
all_rows = soup.find_all('tr') 

for row in all_rows:
    stat= extract_contents(row.find_all('td'))
    if len(stat)==5:
        stats.append(stat)


# In[3]:


headers= ['Sno', 'State', 'Confirmed', 'Recovery', 'Death']


# In[4]:


df= pd.DataFrame(stats, columns= headers).set_index('State')
df.drop(['Sno'], axis= 1, inplace= True)
df= df.astype(int)
#df.rename({2: "Confirmed", 3: "Recovery", 4: "Death"}, axis= 1, inplace= True)
#df.loc['Total']= df.sum()
df


# In[26]:


summaries= df.sum()
summaries.rename({'Confirmed': 'total_confirmed', 'Recovery': 'total_recovery',
                         'Death': 'total_death'}, inplace=True, axis= 1)
summaries


# In[27]:


s = '"helps": [     { "title": "WB Helpline 1", "phone": "033-24312600",       "loc": "None", "type": "Govt. Helpline"},     { "title": "WB Helpline 2", "phone": "1800313444222",       "loc": "None", "type": "Govt. Helpline (Toll free)"},     { "title": "Beliaghata ID", "phone": "033-23032200",       "loc": "57, Beleghata Main Rd, Subhas Sarobar Park, Phool Bagan, Beleghata, Kolkata 700010",       "type": "Hospital"},     { "title": "PG Hospital", "phone": "033-22041101",       "loc": "1, Harish Mukherjee Rd, Gokhel Road, Bhowanipore, Kolkata 700020",       "type": "Hospital"},     { "title": "RG Kar", "phone": "033-25557656",       "loc": "1, Khudiram Bose Sarani, Bidhan Sarani, Shyam Bazar, Kolkata, West Bengal 700004",       "type": "Hospital"},     { "title": "North Bengal Medical College", "phone": "0353 258 5478",       "loc": "Sushruta Nagar, Siliguri, West Bengal 734012",       "type": "Hospital"}     ]'


# In[28]:


s= s + ',' + '"states":' + str(df.index.tolist())
s= s + ',' + '"confirmed":' + str(df['Confirmed'].tolist())
s= s + ',' + '"recovery":' + str(df['Recovery'].tolist())
s= s + ',' + '"death":' + str(df['Death'].tolist())


# In[29]:


s= s.replace('\'', '"')


# In[30]:


s= s + ',' + summaries.to_json()[1:-1]
s


# In[31]:


with open('t.json', 'w') as wrt:
    wrt.write('{' + s + '}')


# In[ ]:





# In[ ]:




