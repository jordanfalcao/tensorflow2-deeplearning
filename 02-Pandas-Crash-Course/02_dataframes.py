# -*- coding: utf-8 -*-
"""02-DataFrames.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NoIQ9X-yThqpld1Xd_VJPxx0AU1YmP9n

# DataFrames

DataFrames are the workhorse of pandas and are directly inspired by the R programming language. We can think of a DataFrame as a bunch of Series objects put together to share the same index. Let's use pandas to explore this topic!
"""

import pandas as pd
import numpy as np
from numpy.random import randint

# criando colunas e índices
columns = ['W', 'X', 'Y', 'Z'] # four columns
index = ['A', 'B', 'C', 'D', 'E'] # five rows

# randint retorna inteiros aleatórios de acordo com a range e o shape atribuído
np.random.seed(42)
data = randint(-100,100,(5,4))

data

# criando DF com os índices e colunas específicos
df = pd.DataFrame(data, index, columns)

df

"""# Selection and Indexing

Let's learn the various methods to grab data from a DataFrame

# COLUMNS

## Grab a single column
"""

# única coluna
df['W']

df.X

# mais de uma coluna
df[['W','Z']]

"""### Creating a new column:"""

# nova coluna sendo a soma de outras duas
df['new'] = df['W'] + df['Y']

df

"""## Removing Columns"""

# axis = 1, pq é uma coluna
df.drop('new',axis=1)

# não apaga permanentemente
df

# inserindo o inplace
df.drop('new',axis=1, inplace=True)

df

"""## Working with Rows

## Selecting one row by name
"""

df.loc['A']

"""## Selecting multiple rows by name"""

df.loc[['A','C']]

"""## Select single row by integer index location"""

df.iloc[0]

"""## Select multiple rows by integer index location"""

df.iloc[0:2]

"""## Remove row by name"""

# axis = 0 é defaltu
df.drop('C',axis=0)

# não apaga permanentemente 
df

# podemos reatribuir a remoção: método indicado, inplace cairá em desuso futuramente
df = df.drop('E',axis=0)

df

"""### Selecting subset of rows and columns at same time"""

# valor específico, inserimos a linha e a coluna
df.loc['A', 'W']

# múltiplas linhas e colunas
df.loc[['A','C'],['W','Y']]

"""# Conditional Selection

An important feature of pandas is conditional selection using bracket notation, very similar to numpy:
"""

# boolean
df>0

