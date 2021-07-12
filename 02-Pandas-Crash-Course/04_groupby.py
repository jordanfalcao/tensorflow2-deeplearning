# -*- coding: utf-8 -*-
"""04-Groupby.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1k6rNNOKPo1ga8lLf1Tue8--o--sZidkf

# Groupby

The groupby method allows you to group rows of data together and call aggregate functions
"""

import pandas as pd

df = pd.read_csv('Universities.csv')

df.head()

"""Now you can use the .groupby() method to group rows together based off of a **categorical** column. This column will then be reassigned to be the index.

Notice we have 2 steps:

1. Choose a categorical column to group by
2. Choose your aggregation function. Recall an aggregation function should take multiple values and return a single value (e.g. max,min, mean, std, etc...)
"""

# primeiramente escolhemos a feature que iremos agrupar
df.groupby('Year') # neste caso retorna aoenas um DataFrameGroupBy object

# inserindo a aggregate function
df.groupby('Year').sum() # retorna apenas as colunas com soma possível

# média de conclusões por ano
df.groupby('Year').mean().sort_index(ascending = False)

"""-----
## Other Aggregate Functions

<table><td><tt
><span
>count</span></tt></td><td>Number of non-null observations</td></tr><tr
><td><tt
><span
>sum</span></tt></td><td>Sum of values</td></tr><tr
><td><tt
><span
>mean</span></tt></td><td>Mean of values</td></tr><tr
><td><tt
><span
>mad</span></tt></td><td>Mean absolute deviation</td></tr><tr
><td><tt
><span
>median</span></tt></td><td>Arithmetic median of values</td></tr><tr
><td><tt
><span
>min</span></tt></td><td>Minimum</td></tr><tr
><td><tt
><span
>max</span></tt></td><td>Maximum</td></tr><tr
><td><tt
><span
>mode</span></tt></td><td>Mode</td></tr><tr
><td><tt
><span
>abs</span></tt></td><td>Absolute Value</td></tr><tr
><td><tt
><span
>prod</span></tt></td><td>Product of values</td></tr><tr
><td><tt
><span
>std</span></tt></td><td>Unbiased standard deviation</td></tr><tr
><td><tt
><span
>var</span></tt></td><td>Unbiased variance</td></tr><tr
><td><tt
><span
>sem</span></tt></td><td>Unbiased standard error of the mean</td></tr><tr
><td><tt
><span
>skew</span></tt></td><td>Unbiased skewness (3rd moment)</td></tr><tr
><td><tt
><span
>kurt</span></tt></td><td>Unbiased kurtosis (4th moment)</td></tr><tr
><td><tt
><span
>quantile</span></tt></td><td>Sample quantile (value at %)</td></tr><tr
><td><tt
><span
>cumsum</span></tt></td><td>Cumulative sum</td></tr><tr
><td><tt
><span
>cumprod</span></tt></td><td>Cumulative product</td></tr><tr
><td><tt
><span
>cummax</span></tt></td><td>Cumulative maximum</td></tr><tr
><td><tt
><span
>cummin</span></tt></td><td>Cumulative minimum</td></tr></tbody></table>

## Grouping By multiple columns
"""

# agrupando por ano e Setor e tirando a média
df.groupby(['Year', 'Sector']).mean() # outer group: year, inner group: sector

# describe já retorna várias aggregate functions 
df.groupby('Year').describe()

# transpondo o DF
df.groupby('Year').describe().transpose()