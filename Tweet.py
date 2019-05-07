#!/usr/bin/env python
# coding: utf-8

class Tweet:
    num = 0
    def __init__(self,Id, user, text, date, *args):
        self.user = user
        self.text = text
        self.date = date
        self.data = args
        self.Id = Id
    def __repr__(self):
        return ' '.join([self.Id,self.user,self.text,self.date.strftime("%d.%m.%Y")])



