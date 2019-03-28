from pyspark import SparkContext, HiveContext
from pyspark.sql import *

sc = SparkContext()
hiveContext = HiveContext(sc)

table = hiveContext.table("orders")
table.registerTempTable("orders")

outputDF = hiveContext.sql("select * from orders where order_status = 'PENDING'")
outputDF.coalesce(1).write.option("compression","SNAPPY").parquet("hdfs://localhost:8020/user/cloudera/problem3/solution")
