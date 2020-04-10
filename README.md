# Creating an Extended dataset of Covid-19 Epidemic in Bangladesh and showing them in some basic visualizations

Covid-19 has taken an epidemic form all over the world. Producing a fair dataset of all the informations will give a closer look to the dynamics of the current situation. But, in Bangladesh, it is very hard to get an extended database. All I found on the internet are Cumulative dataset of Confirmed, Recovered and Deaths only. So, I decided to make one myself. I am a very very beginner in this arena. So, this is actually my practice pad.

I got a dataset on the Internet only containing the cumulative Confirmed, Recovered and Deaths counts. I happen to find some press releases regarding covid-19 on these sources, [Here](https://iedcr.gov.bd/index.php/component/content/article/11-others/227-pressrelease) and [Here](https://corona.gov.bd/press-release). But they contain inconsistant
and ambiguous informations. Yet, I checked my downloaded dataset, made some edits and collected the information of tests per day.

So, The data collection is over, now it's time to accumalate them and producing some more facts outta them. I am using Python to code and pandas to sort things out. Okay, then start with importing sum modules that will help us in rest of the parts. I imported `chdir` from `OS` to change my working directory. I also explecitly imported the matplotlib converters because in future the program will erroneous except it.

```python
from os import chdir
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
%matplotlib inline
```

The edited csv file is read using pandas' built in `read_csv` method which directly converts the csv file into pandas dataframe. Let's see what's inside the file and what are the data types. The data types I may have to be changed according to my need.

```python
chdir('E:\\Projects\\Jupyter\\Covid-19BD')
dataset = pd.read_csv('covid-19_bd_cumu_cleaned.csv')
print(dataset)
print(dataset.dtypes)
```

```{.json .output n=2}
          Date  Confirmed  Deaths  Recovered
0   2020-03-08          3       0          0
1   2020-03-09          3       0          0
2   2020-03-10          3       0          0
3   2020-03-11          3       0          0
4   2020-03-12          3       0          0
5   2020-03-13          3       0          0
6   2020-03-14          3       0          0
7   2020-03-15          5       0          0
8   2020-03-16          8       0          0
9   2020-03-17         10       0          0
10  2020-03-18         14       1          3
11  2020-03-19         17       1          3
12  2020-03-20         20       1          3
13  2020-03-21         24       1          3
14  2020-03-22         28       2          3
15  2020-03-23         33       2          3
16  2020-03-24         39       3          5
17  2020-03-25         39       5          7
18  2020-03-26         44       5         11
19  2020-03-27         48       5         11
20  2020-03-28         48       5         15
21  2020-03-29         48       5         15
22  2020-03-30         49       5         19
23  2020-03-31         51       5         25
24  2020-04-01         54       6         26
25  2020-04-02         56       6         26
26  2020-04-03         61       6         26
27  2020-04-04         70       8         30
28  2020-04-05         88       9         30
29  2020-04-06        123      12         33
30  2020-04-07        164      17         33
31  2020-04-08        218      20         33
32  2020-04-09        330      21         33
33  2020-04-10        424      27         33
Date         object
Confirmed     int64
Deaths        int64
Recovered     int64
dtype: object
```

So, the dataset is in cumulative form which I have already mentioned. It's a good thing that the numbers are already in `int64` type, so they don't need to be changed. But in case of the `Date` column, I will turn it into datetime object. I will print  a portion of the dataframe and data types to be sure if this is working fine.

```python
dataset['Date'] = pd.to_datetime(dataset['Date'], format='%Y-%m-%d')
print(dataset.head())
print(dataset.dtypes)

```

```{.json .output n=3}
        Date  Confirmed  Deaths  Recovered
0 2020-03-08          3       0          0
1 2020-03-09          3       0          0
2 2020-03-10          3       0          0
3 2020-03-11          3       0          0
4 2020-03-12          3       0          0
Date         datetime64[ns]
Confirmed             int64
Deaths                int64
Recovered             int64
dtype: object
```
```

I am going to change all the cumulative data to a non-cumulative form. So, let
me keep a copy of the original dataset. I will need this later. I will give the
columns of `cumu_data` some new names.

```python
cumu_data = dataset.copy()
cumu_data.columns = ['Date','Total Cases','Total Deaths','Total Recovered']
```

Now,I will turn the dataset in a non-cumulative form. Then I manually created a list named `tests` which contains the information about how many tests are taken each day. I will add this list as a new column to my `dataset` dataframe and save it to csv format. It will help if I try to reproduce the whole thing again. Also take a look at a portion of dataset to make sure everything is fine.

```python
for i in range(len(dataset)-1,0,-1):
    dataset.loc[i,'Confirmed':'Recovered'] -= dataset.loc[i-1,'Confirmed':'Recovered']
tests = [120,7,10,10,16,24,24,30,27,49,49,46,36,36,65,56,92,82,126,106,47,109,153,140,157,141,203,434,367,468,679,981,905,1184]
dataset['New Tests'] = tests
dataset.columns = ['Date','New Cases','New Deaths','New Recovered','New Tests']
dataset.to_csv('covid-19_bd_cleaned.csv',index=False)
print(dataset.tail())
```

```python
         Date  New Cases  New Deaths  New Recovered  New Tests
29 2020-04-06         35           3              3        468
30 2020-04-07         41           5              0        679
31 2020-04-08         54           3              0        981
32 2020-04-09        112           1              0        905
33 2020-04-10         94           6              0       1184
```

But the test data were for each day, we also need to turn it to cumulative form. Lets do it.

```python
cumu_tests = []
cumu_tests = tests[:]
for i in range(1,len(tests)):
    cumu_tests[i] += cumu_tests[i-1]
print(cumu_tests)
print(tests)
```

```{.json .output n=6}
[120, 127, 137, 147, 163, 187, 211, 241, 268, 317, 366, 412, 448, 484, 549, 605, 697, 779, 905, 1011, 1058, 1167, 1320, 1460, 1617, 1758, 1961, 2395, 2762, 3230, 3909, 4890, 5795, 6979]
[120, 7, 10, 10, 16, 24, 24, 30, 27, 49, 49, 46, 36, 36, 65, 56, 92, 82, 126, 106, 47, 109, 153, 140, 157, 141, 203, 434, 367, 468, 679, 981, 905, 1184]
```

Add this list to my cumulative dataset which is `cumu_data`.

```python
cumu_data['Total Tests'] = cumu_tests
print(cumu_data.tail())
```

```{.json .output n=7}
         Date  Total Cases  Total Deaths  Total Recovered  Total Tests
29 2020-04-06          123            12               33         3230
30 2020-04-07          164            17               33         3909
31 2020-04-08          218            20               33         4890
32 2020-04-09          330            21               33         5795
33 2020-04-10          424            27               33         6979
```

Now, this is time for the most interesting  part. Lets produce more data from what we have. I am calculing number of total active cases each day first in `active`. And then I will save percentage of death per confirmed case to `death_by_confirmed`, number of death divided by number of recovered to `death_by_recovered`, percentage of confirmed cases per total tests each day to `cases_by_tests`, number of confirmed cases per 1 million population in `cases_per_1m` and number of deaths per 1 million population to `deaths_per_1m`. Each of them is a series. Of course, I will print a portion of all of them to make sure they are calculated correctly.

```python
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
```

```{.json .output n=8}
29     78
30    114
31    165
32    276
33    364
dtype: int64
29     9.756098
30    10.365854
31     9.174312
32     6.363636
33     6.367925
dtype: float64
29    0.363636
30    0.515152
31    0.606061
32    0.636364
33    0.818182
dtype: float64
29    0.683333
30    0.911111
31    1.211111
32    1.833333
33    2.355556
Name: Total Cases, dtype: float64
```

Now I will append all the series from previous part to the `dataset` dataframe. This is our complete extended dataset. Check wheather nothing is miscalculated.

```python
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
```

```{.json .output n=9}
        Date  New Cases  New Deaths  New Recovered  New Tests  Total Cases  \
0 2020-03-08          3           0              0        120            3   
1 2020-03-09          0           0              0          7            3   
2 2020-03-10          0           0              0         10            3   
3 2020-03-11          0           0              0         10            3   
4 2020-03-12          0           0              0         16            3   

   Total Deaths  Total Recovered  Total Active  Total Tests  Death/Cases (%)  \
0             0                0             3          120              0.0   
1             0                0             3          127              0.0   
2             0                0             3          137              0.0   
3             0                0             3          147              0.0   
4             0                0             3          163              0.0   

   Death/Recovered  Cases/Tests(%)  Cases/1M Pop.  Deaths/1M Pop.  
0              0.0        2.500000       0.016667             0.0  
1              0.0        2.362205       0.016667             0.0  
2              0.0        2.189781       0.016667             0.0  
3              0.0        2.040816       0.016667             0.0  
4              0.0        1.840491       0.016667             0.0  
```

So the complete extended dataset will be saved to csv. For convenience, I would like to store one of it each day with the date when I created them. It will be very helpful in future if I need to use them again.

```python
dataset.to_csv('covid-19_bd_extended_' + str(date.today()) + '.csv',index=False,float_format='%.3f')
```

```python
bars = dataset['Total Deaths'] + dataset['Total Recovered']
plt.bar(dataset['Date'],dataset['Total Deaths'] , color=(0.8,0,0,0.8), label='Deaths')
plt.bar(dataset['Date'], dataset['Total Recovered'], bottom=dataset['Total Deaths'], color=(0,0.8,0,0.5), label='Recovered')
plt.bar(dataset['Date'], dataset['Total Active'], bottom=bars,color='#ffea00',alpha=0.7,label='Active')
plt.xticks(rotation=90)
plt.xlabel("Date")
plt.ylabel("Total Cases")
plt.legend(loc="upper left")
plt.show()
```

```{.json .output n=11}
![alt text](https://github.com/promitbasak/Covid-19_bd_extended/raw/master/assests/2020-04-10/Figure_1.png "Fig_1")
```

Okay. So the dataset has been built. Now it's time to do some visualization. I will use pyplot to obtain curves and bartcharts. These charts will give a very good idea of the current situation of Covid-19 epidemic in Bangladesh. I will use different colors for different kind of data.

```python
plt.plot(dataset['Date'],dataset['Total Cases'],alpha=0.8)
plt.fill_between(dataset['Date'], dataset['Total Cases'], 0,alpha=0.3)
plt.xticks(rotation=90)
plt.xlabel("Date")
plt.ylabel("Total Cases")
plt.title("Curve of Covid-19 Total Cases Each Day in Bangladesh")
plt.grid(True)
plt.show()
```

```{.json .output n=12}
[
 {
  "data": {
   "image/png": "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
