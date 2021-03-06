# -*- coding: utf-8 -*-
"""01-Series.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QnvhMnSKNcRf6Gtk2dWUgzOiK5h4R-Fu

# Series
"""

import numpy as np
import pandas as pd

"""## Creating a Series

You can convert a list,numpy array, or dictionary to a Series:
"""

# criando lista, array numpy e dicionário
labels = ['a','b','c']
my_list = [10,20,30]
arr = np.array([10,20,30])
d = {'a':10,'b':20,'c':30}

"""### Using Lists

"""

pd.Series(my_list, index = labels)

"""###Using NumPy Arrays"""

pd.Series(arr, labels)

"""###Using Dictionaries"""

pd.Series(d)

"""###Using an Index"""

sales_Q1 = pd.Series(data=[250,450,200,150],index = ['USA', 'China','India', 'Brazil'])

sales_Q1

sales_Q2 = pd.Series([260,500,210,100],index = ['USA', 'China','India', 'Japan'])

# acessando um index da Serie
sales_Q2['China']

# outra forma
sales_Q2.India

# índice
sales_Q2[0]

"""Operations are then also done based off of index:"""

# retorna NaN em operações com índices diferentes
sales_Q2 + sales_Q1