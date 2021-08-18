#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests


# In[2]:


flower_example = {
"sepal_length":5.1,
"sepal_width":3.5,
"petal_length":1.4,
"petal_width":0.2
}


# In[3]:


r = requests.post("http://localhost:5000/api/flower",json=flower_example)


# In[4]:


r.status_code


# In[6]:


print(r.text)


# In[7]:


if r.status_code == 200:
    print(f"Success: {r.text}")
else:
    print(f"Failure: {r.text}")

