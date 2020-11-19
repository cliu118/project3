#!/bin/python
#coding: UTF-8

import sys
import os
import csv
import jieba
import jieba.analyse
import re

MIN_FOLLOWERS = 5000

# const value

WORD_EXPRESSION='(^\w+$)'
REG_EXPRESSION = re.compile(r"%s" %WORD_EXPRESSION)

# column define

COLUMN_USER_NAME        = 0
COLUMN_USER_LOCATION    = 1
COLUMN_USER_DESC        = 2
COLUMN_USER_CREATED     = 3
COLUMN_USER_FOLLOWERS   = 4
COLUMN_USER_FRIENDS     = 5
COLUMN_USER_FAV         = 6
COLUMN_USER_VERIFIED    = 7
COLUMN_DATE             = 8
COLUMN_TEXT             = 9
COLUMN_CNT              = 13

# class TextMapper

class TextMapper():

    def __init__(self, infile=sys.stdin, separator='\t'):
        self.infile = infile
        self.sep = separator

    def map(self): 
            lines = csv.reader(self.infile, delimiter=',')
            for line in lines:
                # check line columns
                cnt = len(line)
                if cnt != COLUMN_CNT:
                    continue
                  
                # skip header

                text = line[COLUMN_TEXT]
                if text == "text":
                    continue
                followers = int(line[COLUMN_USER_FOLLOWERS])
                dt = line[COLUMN_DATE].split(' ', -1)[0]
                name = line[COLUMN_USER_NAME]

                # skip when followers too few
                if followers < MIN_FOLLOWERS:
                    continue
                
                # text parse
                try:
                    words = jieba.analyse.extract_tags(text, topK=10, withWeight=False, allowPOS=())
                    for word in words:
                        # skip empty
                        if not word:
                            continue
                           
                        # alpha or digit only
                        reg_item = REG_EXPRESSION.search(word)
                        if not reg_item:
                            # print("no reg")
                            continue   
                                                      
                        # to lower
                        for item in reg_item.groups():
                            # skip short word
                            if len(item) < 3:
                                # print("too short")
                                continue
                           
                            # output "word_date \t user name \t followers"
                            print(
                                self.sep.join([
                                    item.lower() + '_' + dt,
                                    name,
                                    str(followers)
                                ])
                            ) 
                except:
                        pass                            

if __name__=='__main__':
    mapper = TextMapper(sys.stdin, '\t')
    mapper.map()

            
            
            
            
                