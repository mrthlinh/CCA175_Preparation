from pyspark import SparkContext, HiveContext
from pyspark.sql import *

sc = SparkContext()
hiveContext = HiveContext(sc)

table = hiveContext.table("problem3.products")
table.registerTempTable("products")

outputDF = hiveContext.sql("select * from products")
outputDF.coalesce(1).write.option("compression","SNAPPY").parquet("hdfs://localhost:8020/user/cloudera/problem3/solution")
