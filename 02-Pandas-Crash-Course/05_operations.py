# -*- coding: utf-8 -*-
"""05-Operations.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VqNVLqq789-1RXjjj5mX5Eom1WLTZXjb

# Operations

There are lots of operations with pandas that will be really useful to you, but don't fall into any distinct category. Let's show them here in this lecture:
"""

import pandas as pd

# criando DF
df_one = pd.DataFrame({'k1':['A','A','B','B','C','C'],
                      'col1':[100,200,300,300,400,500],
                      'col2':['NY','CA','WA','WA','AK','NV']})

df_one

"""### Information on Unique Values"""

# valores únicos
df_one['col2'].unique()

df_one['k1'].unique()

# quantidade de valores únicos
df_one['col2'].nunique()

# contar cada tipo
df_one['col2'].value_counts()

# removendo linhas iguais
df_one.drop_duplicates()

"""### Creating New Columns with Operations and Functions

We already know we can easily create new columns through basic arithmetic operations:
"""

df_one

# nova coluna envolvendo operações
df_one['NEW'] = df_one['col1'] * 10

df_one

"""But we can also create new columns by applying any custom function we want, as you can imagine, this could be as complex as we want, and gives us great flexibility.

Step 1: Define the function that will operate on every row entry in a column
"""

# selecionar a 1ª letra e transformar num coluna
def grab_first_letter(state):
  return state[0]

# testando
grab_first_letter('NY')

# nova coluna com a function criada
df_one['col2'].apply(grab_first_letter) # não passamos o parâmetro (), pandas passará por toda coluna

df_one['first_letter'] = df_one['col2'].apply(grab_first_letter)

df_one

"""These functions can be as complex as you want, as long as it would be able to accept the items in each row. Watch our for data type issues!"""

# função pode ser quão complexa o usuário queira
def complex_letter(state):
  if state[0] == 'W':
    return 'Washington'
  else:
    return 'Error'

# chamando a função
df_one['col2'].apply(complex_letter)

# nova coluna
df_one['State_Check'] = df_one['col2'].apply(complex_letter)

df_one

# WATCH OUT FOR DATA TYPE ERRORS!
# numéros não tem índices igual a string!

# df_one['col1'].apply(complex_letter)

"""### Mapping"""

df_one['k1']

# criando dict
my_map = {'A': 1, 'B': 2, 'C': 3}

# mapeando a coluna 'k1'
df_one['k1'].map(my_map)

# inserindo numa coluna
df_one['num'] = df_one['k1'].map(my_map)
df_one

"""### Locating Index positions of max and min values"""

df_one['col1'].max()

df_one['col1'].min()

# posição do índice do máximo
df_one['col1'].idxmax()

# posição do índice do mínimo
df_one['col1'].idxmin()

# colunas
df_one.columns

# índices
df_one.index

# renomeando colunas
df_one.columns = ['C1','C2','C3','C4','C5','C6', 'C7']

df_one

"""### Sorting and Ordering a DataFrame:"""

# reordenando de acordo com a coluna escolhida, pode ser STRING
df_one.sort_values('C3', ascending=False)

"""# Concatenating DataFrames"""

features = pd.DataFrame({'A':[100,200,300,400,500],
                        'B':[12,13,14,15,16]})
predictions = pd.DataFrame({'pred':[0,1,1,0,1]})

features

predictions

# concatenando os DF
pd.concat([features, predictions]) # axis = 0 é default

# modificando a orientação da concatenação
pd.concat([features, predictions], axis = 1)

"""## Creating Dummy Variables"""

df_one

# cria um DF com a coluna atribuida e set 1 ou 0 para cada categoria da coluna
pd.get_dummies(df_one['C1'])