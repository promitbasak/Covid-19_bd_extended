#!/usr/bin/env python
# coding: utf-8

# # Creating an Extended dataset of Covid-19 Epidemic in Bangladesh and showing them in some basic visualizations

# Covid-19 has taken an epidemic form all over the world. Producing a fair dataset of all the informations will give a closer look to the dynamics of the current situation. But, in Bangladesh, it is very hard to get an extended database. All I found on the internet are Cumulative dataset of Confirmed, Recovered and Deaths only. So, I decided to make one myself. I am a very very beginner in this arena. So, this is actually my practice pad.

# I got a dataset on the Internet only containing the cumulative Confirmed, Recovered and Deaths counts. I happen to find some press releases regarding covid-19 on these sources, [Here](https://iedcr.gov.bd/index.php/component/content/article/11-others/227-pressrelease) and [Here](https://corona.gov.bd/press-release). But they contain inconsistant and ambiguous informations. Yet, I checked my downloaded dataset, made some edits and collected the information of tests per day. 

# So, The data collection is over, now it's time to accumalate them and producing some more facts outta them. I am using Python to code and pandas to sort things out. Okay, then start with importing sum modules that will help us in rest of the parts. I imported `chdir` from `OS` to change my working directory. I also explecitly imported the matplotlib converters because in future the program will erroneous except it.

# In[1]:


from os import chdir
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
# get_ipython().run_line_magic('matplotlib', 'inline')


# The edited csv file is read using pandas' built in `read_csv` method which directly converts the csv file into pandas dataframe. Let's see what's inside the file and what are the data types. The data types I may have to be changed according to my need.

# In[2]:


chdir('E:\\Projects\\Jupyter\\Covid-19BD')
dataset = pd.read_csv('covid-19_bd_cumu_cleaned.csv')
print(dataset)
print(dataset.dtypes)


# So, the dataset is in cumulative form which I have already mentioned. It's a good thing that the numbers are already in `int64` type, so they don't need to be changed. But in case of the `Date` column, I will turn it into datetime object. I will print  aportion of the dataframe and data types to be sure if this is working fine.

# In[3]:


dataset['Date'] = pd.to_datetime(dataset['Date'], format='%Y-%m-%d')
print(dataset.head())
print(dataset.dtypes)


# I am going to change all the cumulative data to a non-cumulative form. So, let me keep a copy of the original dataset. I will need this later. I will give the columns of `cumu_data` some new names.

# In[4]:


cumu_data = dataset.copy()
cumu_data.columns = ['Date','Total Cases','Total Deaths','Total Recovered']


# Now,I will turn the dataset in a non-cumulative form. Then I manually created a list named `tests` which contains the information about how many tests are taken each day. I will add this list as a new column to my `dataset` dataframe and save it to csv format. It will help if I try to reproduce the whole thing again. Also take a look at a portion of dataset to make sure everything is fine.

# In[5]:


for i in range(len(dataset)-1,0,-1):
    dataset.loc[i,'Confirmed':'Recovered'] -= dataset.loc[i-1,'Confirmed':'Recovered']
tests = [120,7,10,10,16,24,24,30,27,49,49,46,36,36,65,56,92,82,126,106,47,109,153,140,157,141,203,434,367,468,679,981,905,1184]
dataset['New Tests'] = tests
dataset.columns = ['Date','New Cases','New Deaths','New Recovered','New Tests']
dataset.to_csv('covid-19_bd_cleaned.csv',index=False)
print(dataset.tail())


# But the test data were for each day, we also need to turn it to cumulative form. Lets do it.

# In[6]:


cumu_tests = []
cumu_tests = tests[:]
for i in range(1,len(tests)):
    cumu_tests[i] += cumu_tests[i-1]
print(cumu_tests)
print(tests)


# Add this list to my cumulative dataset which is `cumu_data`.

# In[7]:


cumu_data['Total Tests'] = cumu_tests
print(cumu_data.tail())


# Now, this is time for the most interesting  part. Lets produce more data from what we have. I am calculing number of total active cases each day first in `active`. And then I will save percentage of death per confirmed case to `death_by_confirmed`, number of death divided by number of recovered to `death_by_recovered`, percentage of confirmed cases per total tests each day to `cases_by_tests`, number of confirmed cases per 1 million population in `cases_per_1m` and number of deaths per 1 million population to `deaths_per_1m`. Each of them is a series. Of course, I will print a portion of all of them to make sure they are calculated correctly.

# In[8]:


active = cumu_data['Total Cases'] - cumu_data['Total Deaths'] - cumu_data['Total Recovered']
death_by_confirmed = cumu_data['Total Deaths']*100/cumu_data['Total Cases']
death_by_recovered = cumu_data['Total Deaths']/cumu_data['Total Recovered']
cases_by_tests = cumu_data['Total Cases']*100/cumu_data['Total Tests']
cases_per_1m = cumu_data['Total Cases']/180
deaths_per_1m = cumu_data['Total Deaths']/180
print(active.tail())
print(death_by_confirmed.tail())
print(death_by_recovered.tail())
print(cases_per_1m.tail())


# Now I will append all the series from previous part to the `dataset` dataframe. This is our complete extended dataset. Check wheather nothing is miscalculated.

# In[9]:


dataset['Total Cases'] = cumu_data['Total Cases']
dataset['Total Deaths'] = cumu_data['Total Deaths']
dataset['Total Recovered'] = cumu_data['Total Recovered']
dataset['Total Active'] = active
dataset['Total Tests'] = cumu_data['Total Tests']
dataset['Death/Cases (%)'] = death_by_confirmed
dataset['Death/Recovered'] = death_by_recovered.fillna(0)
dataset['Cases/Tests(%)'] = cases_by_tests
dataset['Cases/1M Pop.'] = cases_per_1m
dataset['Deaths/1M Pop.'] = deaths_per_1m
print(dataset.head())


# So the complete extended dataset will be saved to csv. For convenience, I would like to store one of it each day with the date when I created them. It will be very helpful in future if I need to use them again.

# In[10]:


dataset.to_csv('covid-19_bd_extended_' + str(date.today()) + '.csv',index=False,float_format='%.3f')


# In[11]:


bars = dataset['Total Deaths'] + dataset['Total Recovered']
plt.bar(dataset['Date'],dataset['Total Deaths'] , color=(0.8,0,0,0.8), label='Deaths')
plt.bar(dataset['Date'], dataset['Total Recovered'], bottom=dataset['Total Deaths'], color=(0,0.8,0,0.5), label='Recovered')
plt.bar(dataset['Date'], dataset['Total Active'], bottom=bars,color='#ffea00',alpha=0.7,label='Active')
plt.xticks(rotation=90)
plt.xlabel("Date")
plt.ylabel("Total Cases")
plt.legend(loc="upper left")
plt.show()


# Okay. So the dataset has been built. Now it's time to do some visualization. I will use pyplot to obtain curves and bartcharts. These charts will give a very good idea of the current situation of Covid-19 epidemic in Bangladesh. I will use different colors for different kind of data.

# In[12]:


plt.plot(dataset['Date'],dataset['Total Cases'],alpha=0.8)
plt.fill_between(dataset['Date'], dataset['Total Cases'], 0,alpha=0.3)
plt.xticks(rotation=90)
plt.xlabel("Date")
plt.ylabel("Total Cases")
plt.title("Curve of Covid-19 Total Cases Each Day in Bangladesh")
plt.grid(True)
plt.show()


# In[13]:


plt.bar(dataset['Date'],dataset['Total Cases'],alpha=0.5)
plt.xticks(rotation=90)
plt.xlabel("Date")
plt.ylabel("Total Cases")
plt.title("Covid-19 Total Cases Each Day in Bangladesh")
plt.show()


# In[14]:


plt.plot(dataset['Date'],dataset['New Cases'],alpha=0.8)
plt.xticks(rotation=90)
plt.xlabel("Date")
plt.ylabel("New Cases")
plt.title("Curve of Covid-19 New Cases Each Day in Bangladesh")
plt.grid(True)
plt.show()


# In[15]:


plt.bar(dataset['Date'],dataset['New Cases'],align='center',alpha=0.5)
plt.xticks(rotation=90)
plt.xlabel("Date")
plt.ylabel("Confirmed Cases")
plt.title("Covid-19 New Cases Each Day in Bangladesh")
plt.show()


# In[16]:


plt.plot(dataset['Date'],dataset['New Deaths'],color=(0.8,0,0,0.5))
plt.xticks(rotation=90)
plt.xlabel("Date")
plt.ylabel("New Deaths")
plt.title("Curve of Covid-19 New Deaths Each Day in Bangladesh")
plt.grid(True)
plt.show()


# In[17]:


plt.bar(dataset['Date'],dataset['New Deaths'],align='center',color=(0.8,0,0,0.5))
plt.xticks(rotation=90)
plt.xlabel("Date")
plt.ylabel("New Deaths")
plt.title("Covid-19 New Deaths Each Day in Bangladesh")
plt.show()


# In[18]:


plt.plot(dataset['Date'],dataset['Total Deaths'],color=(0.8,0,0,0.5))
plt.fill_between(dataset['Date'], dataset['Total Deaths'], 0,color=(0.8,0,0,0.3))
plt.xticks(rotation=90)
plt.xlabel("Date")
plt.ylabel("Total Deaths")
plt.title("Curve of Covid-19 Total Deaths Each Day in Bangladesh")
plt.grid(True)
plt.show()


# In[19]:


plt.bar(dataset['Date'],dataset['Total Deaths'],align='center',color=(0.8,0,0,0.5))
plt.xticks(rotation=90)
plt.xlabel("Date")
plt.ylabel("Total Deaths")
plt.title("Covid-19 Total Deaths Each Day in Bangladesh")
plt.show()


# In[20]:


plt.plot(dataset['Date'],dataset['New Recovered'],color=(0,0.8,0.4,0.8))
plt.xticks(rotation=90)
plt.xlabel("Date")
plt.ylabel("New Recovered")
plt.title("Curve of Covid-19 New Recovered Each Day in Bangladesh")
plt.grid(True)
plt.show()


# In[21]:


plt.bar(dataset['Date'],dataset['New Recovered'],align='center',color=(0,0.8,0.4,0.8))
plt.xticks(rotation=90)
plt.xlabel("Date")
plt.ylabel("New Recovered")
plt.title("Covid-19 New Recovered Each Day in Bangladesh")
plt.show()


# In[22]:


plt.plot(dataset['Date'],dataset['Total Recovered'],color=(0,0.8,0.4,0.8))
plt.fill_between(dataset['Date'], dataset['Total Recovered'], 0,color=(0,0.8,0.4,0.3))
plt.xticks(rotation=90)
plt.xlabel("Date")
plt.ylabel("Total Recovered")
plt.title("Curve of Covid-19 Total Recovered Each Day in Bangladesh")
plt.grid(True)
plt.show()


# In[23]:


plt.bar(dataset['Date'],dataset['Total Recovered'],align='center',color=(0,0.8,0.4,0.8))
plt.xticks(rotation=90)
plt.xlabel("Date")
plt.ylabel("Total Recovered")
plt.title("Covid-19 Total Recovered Each Day in Bangladesh")
plt.show()


# In[24]:


plt.plot(dataset['Date'],dataset['Total Active'],color='#ffea00',alpha=1)
plt.fill_between(dataset['Date'], dataset['Total Active'], 0,color='#ffea00', alpha=0.3)
plt.xticks(rotation=90)
plt.xlabel("Date")
plt.ylabel("Total Active Cases")
plt.title("Curve of Covid-19 Total Active Cases Each Day in Bangladesh")
plt.grid(True)
plt.show()


# In[25]:


plt.bar(dataset['Date'],dataset['Total Active'],align='center',color='#ffea00',alpha=0.7,)
plt.xticks(rotation=90)
plt.xlabel("Date")
plt.ylabel("Total Active Casess")
plt.title("Covid-19 Total Active Cases Each Day in Bangladesh")
plt.show()


# In[26]:


plt.plot(dataset['Date'],dataset['Death/Cases (%)'],color=(0.5,0.5,0.9,1))
plt.xticks(rotation=90)
plt.xlabel("Date")
plt.ylabel("Percentage of Deaths Per Cases")
plt.title("Curve of Covid-19 Percentage of Deaths Per Cases each day in Bangladesh")
plt.grid(True)
plt.show()


# In[27]:


plt.bar(dataset['Date'],dataset['Death/Cases (%)'],align='center',color=(0.5,0.5,0.9,1))
plt.xticks(rotation=90)
plt.xlabel("Date")
plt.ylabel("Percentage of Deaths Per Cases")
plt.title("Covid-19 Percentage of Deaths Per Cases Each Day in Bangladesh")
plt.show()


# In[28]:


plt.plot(dataset['Date'],dataset['Cases/Tests(%)'],color=(0.7,0.3,0.9,1))
plt.xticks(rotation=90)
plt.xlabel("Date")
plt.ylabel("Percentage of Confirmed Cases per Tests")
plt.title("Curve of Covid-19 Percentage of Confirmed Cases per Tests each day in Bangladesh")
plt.grid(True)
plt.show()


# In[29]:


plt.bar(dataset['Date'],dataset['Cases/Tests(%)'],align='center',color=(0.7,0.3,0.9,0.5))
plt.xticks(rotation=90)
plt.xlabel("Date")
plt.ylabel("Percentage of Confirmed Cases per Tests")
plt.title("Covid-19 Percentage of Confirmed Cases per Tests Each Day in Bangladesh")
plt.show()


# I think this is a good practice for today. It's pretty late to sleep. So I finish it here. I will do some more work on it, if something comes to my mind.
