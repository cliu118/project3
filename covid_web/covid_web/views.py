# -*- coding: utf-8 -*-
import datetime
import time
import json

from django.shortcuts import render
from django.conf import settings

def word2cases_option(request):
    try:
        start_date = request.GET['start_date']
    except:
        start_date = '2020-07-25'
    try:
        date_interval = int(request.GET['date_interval'])
    except:
         date_interval = 7   
    try:
        word = request.GET['word']
    except:
        word = 'covid19'             

    return (start_date, date_interval, word)

# 2.2 
word2cases_dict = {}
def load_word2cases(input_file, separator = '\t'):
    global word2cases_dict
    fd = open(input_file, 'r')
    for line in fd:
        items = line.split('\t', -1)
        word = items[0]
        dtlist = []
        for i in range(1, len(items)):
            dtinfo = items[i].split(' ', -1)
            dt = dtinfo[0]
            freq = int(dtinfo[1])
            increment = int(dtinfo[2])
            dtlist.append([dt, freq, increment])
        word2cases_dict[word] = dtlist

load_word2cases(settings.INPUT_WORD2CASES)

def word2cases_table_and_chart(start_date, date_interval, word_info):
    chart_dict = {}
    chart_dict['date'] = []
    chart_dict['value'] = []

    table_data = []
    total_freq = 0
    total_increment = 0

    if start_date >= word_info[0][0] and start_date <= word_info[-1][0]:
    
        # locate start date
        date_index = 0
        for info in word_info:
            dt = info[0]
            if dt == start_date:
                break
            date_index += 1

        # pack date list, chart points
        for i in range(date_index, min(len(word_info), date_index + date_interval)):
            info = word_info[i]
            dt = info[0]
            freq = info[1]
            increment = info[2]  

            chart_dict['date'].append(dt)
            chart_dict['value'].append(((increment * 1.0 / freq) if freq else 0))
            table_data.append(info)
            total_freq += freq
            total_increment += increment

    chart_data = json.dumps([chart_dict])

    return (table_data, chart_data, total_freq, total_increment)

def word2cases(request):
    # parse url parameters
    (start_date, date_interval, word) = word2cases_option(request)
    total_freq = total_increment = 0
    table_data = []
    chart_data = ''

    # search word information: date and word frequency
    word_info = []
    if word in word2cases_dict:
        word_info = word2cases_dict[word]
        (table_data, chart_data, total_freq, total_increment) = word2cases_table_and_chart(
            start_date, date_interval, word_info)

    # return response
    return render(request, 'word2cases.html', {
        'selected_start_date': start_date,
        'selected_date_interval': date_interval, 
        'selected_word': word,    
        'fields_list': ['increment / frequency'],             
        'total_freq': total_freq,        
        'total_increment': total_increment,
        'fields_data': ['date', 'word frequency', 'case increment'],
        'table_data': table_data,
        'chart_data': chart_data
        })

# 2.3

def word_date2user_option(request):
    try:
        start_date = request.GET['start_date']
    except:
        start_date = '2020-07-25'
    try:
        word = request.GET['word']
    except:
        word = 'covid19'             

    return (start_date, word)

def load_word_date2user(input_file, word_date2user_dict, separator = '\t'):
    fd = open(input_file, 'r')
    for line in fd:
        items = line.split('\t', -1)
        word_date = items[0]
        user_list = []
        user_cnt = int(len(items) / 2)
        for i in range(user_cnt):
            user_name = items[1 + 2 * i]
            user_info = items[2 + 2 * i]
            user_list.append([user_name, user_info])
        word_date2user_dict[word_date] = user_list

def word_date2user_chart(start_date, word, word_date2user_dict):
    table_data = []
    word_date = word + '_' + start_date
    if word_date in word_date2user_dict:
        table_data = word_date2user_dict[word_date]
    return table_data

word_date2follower_dict = {}      
load_word_date2user(settings.INPUT_WORD_DATE2FOLLOWER, word_date2follower_dict)

def word_date2follower(request):
    # parse url parameters
    (start_date, word) = word_date2user_option(request)
    table_data = []

    # search word date information: user and follower count
    table_data = word_date2user_chart(start_date, word, word_date2follower_dict)

    # return response
    return render(request, 'word_date2user.html', {
        'selected_start_date': start_date,
        'selected_word': word,              
        'fields_data': ['user', 'followers'],
        'table_data': table_data,
        })

# 2.4

word_date2desc_dict = {}      
load_word_date2user(settings.INPUT_WORD_DATE2DESC, word_date2desc_dict)

def word_date2desc(request):
    # parse url parameters
    (start_date, word) = word_date2user_option(request)
    table_data = []

    # search word date information: user and follower count
    table_data = word_date2user_chart(start_date, word, word_date2desc_dict)

    # return response
    return render(request, 'word_date2user.html', {
        'selected_start_date': start_date,
        'selected_word': word,              
        'fields_data': ['user', 'desc'],
        'table_data': table_data,
        })

# 2.5

word_date2friend_dict = {}      
load_word_date2user(settings.INPUT_WORD_DATE2FRIEND, word_date2friend_dict)

def word_date2friend(request):
    # parse url parameters
    (start_date, word) = word_date2user_option(request)
    table_data = []

    # search word date information: user and friend count
    table_data = word_date2user_chart(start_date, word, word_date2friend_dict)

    # return response
    return render(request, 'word_date2user.html', {
        'selected_start_date': start_date,
        'selected_word': word,              
        'fields_data': ['user', 'friend'],
        'table_data': table_data,
        })