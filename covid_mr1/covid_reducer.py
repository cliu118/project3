#!/bin/python
#coding: UTF-8

import sys
import os
import time, datetime
import re

TOP_K = 10

def output_word_info(word_date, date2name_list):

    # sort by followers descending, by user name descending
    date2name_list = sorted(date2name_list,  key=lambda x:(x[1], x[0]), 
        reverse=True)

    # format: word_date1 \t name1 followers1 \t date2 name2 followers2 + ...
    cnt = 0
    output = word_date
    last = ''
    for item in date2name_list:
        if last == item[0]:
            continue
        output += '\t' + item[0] + '\t' + str(item[1])
        last = item[0]

        cnt += 1
        if cnt >= TOP_K:
            break

    print(output)

# class TextReducer

class TextReducer():

    def __init__(self, infile=sys.stdin, separator='\t'):
        self.infile = infile
        self.sep = separator

    def read(self):
        for line in self.infile:
            yield line.rstrip()

    def __iter__(self):
        for line in self.read():
            yield line

    def reduce(self):
        last_word_date = ''
        cur_word_date = ''
        date2name_list = []

        for line in self:
            items = line.split(self.sep)
            if len(items) != 3:
                continue
            
            cur_word_date = items[0]
            user_name = items[1]
            followers = int(items[2])
            if last_word_date != cur_word_date:
                # new word_date   
                if last_word_date:
                    # output last word_date infomation
                    output_word_info(last_word_date, date2name_list)
                last_word_date = cur_word_date
                date2name_list = [(user_name, followers)]
            else:
                # same word, update date info
                date2name_list.append((user_name, followers))    
                
        if last_word_date:
            # output last word_date infomation
            output_word_info(last_word_date, date2name_list)

if __name__=='__main__':
    reducer = TextReducer(sys.stdin)
    reducer.reduce()        
