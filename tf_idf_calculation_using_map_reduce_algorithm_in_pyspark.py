# -*- coding: utf-8 -*-
"""TF-IDF Calculation Using Map-Reduce Algorithm in PySpark.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14yhxdTRqQZBU4Genwu463vgaaDeEQSRE
"""

!apt-get update

!apt-get install openjdk-11-jdk-headless -qq > /dev/null
!wget -q https://dlcdn.apache.org/spark/spark-3.3.0/spark-3.3.0-bin-hadoop3.tgz
!tar xf spark-3.3.0-bin-hadoop3.tgz
!rm -rf spark-3.3.0-bin-hadoop3.tgz*

import os

os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-11-openjdk-amd64"
os.environ["SPARK_HOME"] = "/content/spark-3.3.0-bin-hadoop3"

# Install library for finding Spark
!pip install -q findspark
# Import the libary
import findspark
# Initiate findspark
findspark.init()
# Check the location for Spark
findspark.find()

# Import SparkSession
from pyspark.sql import SparkSession

# Create a Spark Session
spark = SparkSession.builder.master("local[*]").getOrCreate()
spark.conf.set("spark.sql.repl.eagerEval.enabled", True) # Property used to format output tables better
# Check Spark Session Information
spark

sc = spark.sparkContext

text1 = open('first.txt','r')
text2 = open('second.txt','r')
text3 = open('third.txt','r')

data=[(1,text1.read()),(2,text2.read()),(3,text3.read())]
data

#data=[(1,'i love dogs'),(2,"i hate dogs and knitting"),(3,"knitting is my hobby and my passion")]
lines=sc.parallelize(data)
lines.collect()

map1=lines.flatMap(lambda x: [((x[0],word),1) for word in x[1].split()])
map1.collect()

reduce=map1.reduceByKey(lambda x,y:x+y)
reduce.collect()

tf=reduce.map(lambda x: (x[0][1],(x[0][0],x[1])))
tf.collect()

map3=reduce.map(lambda x: (x[0][1],(x[0][0],x[1],1)))
map3.collect()

map4=map3.map(lambda x:(x[0],x[1][2]))
map4.collect()

reduce2=map4.reduceByKey(lambda x,y:x+y)
reduce2.collect()

import math
from pyspark.sql.functions import *
idf=reduce2.map(lambda x: (x[0],math.log10(len(data)/x[1])))
idf.collect()

rdd=tf.join(idf)
rdd.collect()

rdd=rdd.map(lambda x: (x[1][0][0],(x[0],x[1][0][1],x[1][1],x[1][0][1]*x[1][1]))).sortByKey()
rdd.collect()

rdd=rdd.map(lambda x: (x[0],x[1][0],x[1][1],x[1][2],x[1][3]))
rdd.toDF(["DocumentId","Word","TF","IDF","TF-IDF"]).show()