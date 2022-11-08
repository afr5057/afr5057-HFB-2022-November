#!/usr/bin/env python
# coding: utf-8

# # 2018 Harris County Poverty Estimates - US Census
# 
# This project goal is to use an API call to obtain poverty estimates from the US Census Bureau for Harris County, Texas in 2018. The data to be obtained is:
# * The estimated number of people under 18 years of age in poverty in 2018 in Harris County, Texas
# * The estimated number of individuals regardless of age in poverty in 2018 in Harris County, Texas
# * The estimated median household income in 2018 in Harris County, Texas

# In[1]:


import requests, csv
import pandas as pd


# ### US Census tool to find data
# The Small Area Income and Poverty (SAIPE) dataset will provide poverty levels and estimated houshold incomes
# https://www.census.gov/programs-surveys/saipe/data/api.html
# 
# Sample API call for Alabama in 2020
# //api.census.gov/data/timeseries/poverty/saipe?get=NAME,SAEPOVALL_PT,SAEPOVALL_MOE,SAEPOVRTALL_MOE,SAEPOVRTALL_PT&for=state:01&YEAR=2020

# ### URL to find FIPS code for Harris County, Texas
# https://www.census.gov/library/reference/code-lists/ansi.html#county
# 
# https://www2.census.gov/geo/docs/reference/codes/files/st48_tx_cou.txt

# #### Column Names 
# (https://api.census.gov/data/timeseries/poverty/saipe/variables.html)
# * NAME = State or County Name
# * YEAR = Year of data
# * SAEPOV0_17_PT = Ages 0-17 in Poverty, Count Estimate
# * SAEPOVALL_PT = All ages in Poverty, Count Estimate
# * SAEMHI_PT = Median Household Income Estimate

# In[2]:


#census data variables
year = '2018'
dsource = 'poverty'
dname = 'saipe'
cols = 'NAME,YEAR,SAEPOV0_17_PT,SAEPOVALL_PT,SAEMHI_PT'
state = 48
county = 201
#geoid = '48201'
outfile = 'harrisco_2018_census.csv'
api_key = '[your api key here]'
base_url = f'https://api.census.gov/data/timeseries/{dsource}/{dname}'


# In[3]:


# response query url
query_url = f'{base_url}?get={cols}&for=county:{county}&in=state:{state}&time={year}&key={api_key}'


# In[4]:


# response request
response = requests.get(query_url).json()


# In[5]:


# View the request response
print(response)


# In[6]:


#create dataframe
df = pd.DataFrame(response)
# view dataframe created
df


# In[7]:


# Promote first row to be used as header
df.columns=df.iloc[0]
df = df[1:]
df.head()


# In[8]:


#rename columns to readable names
df2 = df.rename(columns = {'NAME':'LOCATION', 'SAEPOV0_17_PT':'EST._CHILDREN_IN_POVERTY', 
                     'SAEPOVALL_PT':'EST_ALL_RESIDENTS_IN_POVERTY', 'SAEMHI_PT':'EST_MEDIAN_HOUSEHOLD_INCOME'})


# In[9]:


#drop redundant columns
df2 = df2.drop(columns=['time', 'state', 'county'])


# In[10]:


#view formated dataframe
df2.head()


# In[12]:


#export to csv
df2.to_csv('harrisco_2018_census.csv', index=False)


# In[13]:


#double check exported csv
import_csv = pd.read_csv('harrisco_2018_census.csv')
import_csv.head()


# #### Conclusion:
#     * The estimated number of people under 18 years of age in poverty in 2018 in Harris County, Texas was 306,893 children
#     * The estimated number of individuals regardless of age in poverty in 2018 in Harris County, Texas was 767,367 people
#     * The estimated median household income in 2018 in Harris County Texas, was $60,241

# Thank you for your time to review
