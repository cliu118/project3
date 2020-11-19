import sys
from hadoop_helper import *

if __name__=="__main__":
    hadoop_helper = HadoopHelper()
    hdfs_input_dir = '/user/covid/covid19_tweets.csv'
    hdfs_output_dir = '/user/result1'

    if hadoop_helper.existDATA(hdfs_output_dir, "HDFS"):
        hadoop_helper.delExistData(hdfs_output_dir, "HDFS")

    hadoop_cmd = "hadoop jar \
    /home/hadoop/Doc/hadoop-2.9.2/share/hadoop/tools/lib/hadoop-streaming-2.9.2.jar \
    -D stream.non.zero.exit.is.failure=false \
    -D mapred.job.name='covid_mr' \
    -D mapred.job.priority=HIGH \
    -D mapreduce.reduce.memory.mb=2048 \
    -file '/home/hadoop/covid_mr1/covid_mapper.py' \
    -file '/home/hadoop/covid_mr1/covid_reducer.py' \
    -mapper 'python covid_mapper.py' \
    -reducer 'python covid_reducer.py' " 
    job_cmd = hadoop_cmd + "-input " + hdfs_input_dir + " -output " + hdfs_output_dir
    hadoop_helper.run(job_cmd)
    
    exit (0)

