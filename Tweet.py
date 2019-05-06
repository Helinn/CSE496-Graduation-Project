#!/usr/bin/env python
# coding: utf-8

# In[1]:


class Tweet:
    num = 0
    def __init__(self, user, text, date, *args):
        self.user = user
        self.text = text
        self.date = date
        self.data = args
        self.num = Tweet.num
        Tweet.num += 1
    def __repr__(self):
        return ' '.join([self.user,self.text,self.date.strftime("%d.%m.%Y"),str(self.num)])


# In[ ]:




