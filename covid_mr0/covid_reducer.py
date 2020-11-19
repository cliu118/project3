#!/bin/python
#coding: UTF-8

import sys
import os
import time, datetime
import re

MIN_CNT = 100

# COLUMN INFO

COLUMN_DATE     = 0
COLUMN_CASES    = 1
COLUMN_DEATCH   = 2
COLUMN_CNT      = 3

# date range

date2cases_dict = {}
date_beg = '2020-07-24'
date_cnt = 35

TIME_FMT = '%Y-%m-%d %H:%M:%S'

def load_us_covid(text_file, separator):
    global date_beg, date_cnt

    last_cases = 0
    fd = open(text_file, 'r')
    for line in fd:
        # check format
        items = line.split(separator)
        if len(items) != COLUMN_CNT:
            continue

        # get date
        item_date = items[COLUMN_DATE]

        # get increment
        try:
            item_cases = int(items[COLUMN_CASES])
            date2cases_dict[item_date] = item_cases - last_cases
    
            # get first date and date total count
            last_cases = item_cases
        except:
            pass

def output_word_info(current_word, date2cnt_dict):
    global date2cases_dict, date_beg, date_cnt

    # output by date ascending, word count default value = 0
    current_list = []
    total_cnt = 0
    date_tm = datetime.datetime.strptime(date_beg, "%Y-%m-%d")
    for date_num in range(date_cnt):
        date_cur = date_tm.strftime("%Y-%m-%d")
        current_list.append(
            (
                date_cur, 
                date2cnt_dict.get(date_cur, 0), 
                date2cases_dict.get(date_cur, 0)
            )
        )

        date_tm = date_tm + datetime.timedelta(days=1)
        total_cnt += date2cnt_dict.get(date_cur, 0)
    if total_cnt >= MIN_CNT:    
        # format: word \t date1 word_cnt1 cases1 \t date2 word_cnt12 cases2 + ...
        output = current_word
        for item in current_list:
            output += '\t' + item[0] + ' ' + str(item[1]) + ' ' + str(item[2])
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
        last_word = ''
        normal_word = ''
        date2cnt_dict = {}

        for line in self:
            items = line.split(self.sep)
            if len(items) != 2:
                continue
            
            normal_word = items[0]
            tweet_date = items[1]
            if last_word != normal_word:
                # new word    
                if last_word:
                    # output last word infomation
                    output_word_info(last_word, date2cnt_dict)
                last_word = normal_word
                date2cnt_dict = {tweet_date: 1}
            else:
                # same word, update date and count
                date2cnt_dict[tweet_date] = date2cnt_dict.get(tweet_date, 0) + 1
                
        if normal_word:
            # output last word infomation
            output_word_info(normal_word, date2cnt_dict)

if __name__=='__main__':
    load_us_covid('us.csv', ',')
    reducer = TextReducer(sys.stdin)
    reducer.reduce()        
