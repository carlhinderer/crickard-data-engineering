import random

import pyspark
from pyspark.sql import SparkSession

# Create a session on the local master
spark = SparkSession.builder.appName("Pi-Estimation").master("local").getOrCreate()

# Estimate the value of pi
NUM_SAMPLES = 1

def inside(p):
    x, y = random.random(), random.random()
    return x*x + y*y < 1

count = spark.sparkContext.parallelize(range(0, NUM_SAMPLES)).filter(inside).count()

print('Pi is roughly {}'.format(4.0 * count / NUM_SAMPLES))

# Stop the session
spark.stop()