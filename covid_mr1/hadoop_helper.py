#coding=utf8
#!/usr/bin/env python

import os
import sys
import time
import datetime
import subprocess

class LogHelper():
    def printLog(self, LEVEL, log_info):
        str_log = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\t" + LEVEL + "\t" + log_info
        print(str_log)

class HadoopHelper():
    def __init__(self):
        self.log = LogHelper()
        self.hadoop = "hadoop"

    def existDATA(self, file_path, _type):
        if _type=="HDFS":
            test_cmd = self.hadoop + " fs -test -e " + file_path
            res = subprocess.call(test_cmd, shell=True)
            if res!=0:
                log_info = file_path + " not exist"
                self.log.printLog("INFO", log_info)
                return 0

        if _type=="LOCAL":
            if os.path.exists(file_path):
                test_cmd = "ls -l " + file_path + "|wc -l"
                res = subprocess.call(test_cmd, shell=True)
                if res==0:
                    log_info = file_path + " not exist"
                    self.log.printLog("INFO", log_info)
                    return 0
        return 1    

    def delExistData(self, file_path, _type):
        if _type=="HDFS":
            rm_cmd = self.hadoop + " fs -rm -r " + file_path
            res = subprocess.call(rm_cmd, shell=True)
            if res!=0:
                log_info = file_path + " not exist"
                self.log.printLog("FATAL", log_info)
                return -1

        if _type=="LOCAL":
            if os.path.exists(file_path):
                rm_cmd = "rm -rf " + file_path
                res = subprocess.call(rm_cmd, shell=True)
                if res!=0:
                    log_info = file_path + " not exist"
                    self.log.printLog("FATAL", log_info)
                    return -1
        return 0
        
    def mkdirHdfs(self, file_path):
        mkdir_cmd = self.hadoop + " fs -mkdir -p " + file_path
        res = subprocess.call(mkdir_cmd, shell=True)
        if res!=0:
            log_info = file_path + " mkdir failed"
            self.log.printLog("FATAL", log_info)
            return -1

    def getMergeHdfsData(self, hdfs_path, result):
        hadoop_cmd = self.hadoop + " fs -getmerge " + hdfs_path + " " + result
        res = subprocess.call(hadoop_cmd, shell=True)
        if res!=0:
            log_info = "getmerge " + hdfs_path + " failed"
            self.log.printLog("ERROR", log_info)
            return -1

        return 0

    def putLocalData2Hdfs(self, local_path, hdfs_path):
        hadoop_cmd = self.hadoop + " fs -put " + local_path + " " + hdfs_path
        res = subprocess.call(hadoop_cmd, shell=True)
        if res!=0:
            log_info = "put " + local_path + " failed"
            return -1

        return 0

    def run(self, hadoop_cmd):
        self.log.printLog("INFO", hadoop_cmd)
        res = subprocess.call(hadoop_cmd, shell=True)
        if res!=0:
            self.log.printLog("ERROR", "hadoop run failed")
            exit(-1)

        return 0

if __name__=="__main__":
    hp = HadoopHelper()
