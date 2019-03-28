from pyspark import SparkContext, HiveContext
from pyspark.sql import *

sc = SparkContext()
hiveContext = HiveContext(sc)

table = hiveContext.table("problem3.payments")

table.registerTempTable("payments")

outputDF = hiveContext.sql("select * from payments where amount > 2000")

outputDF.coalesce(1).write.option("compression","GZIP").parquet("hdfs://localhost:8020/user/cloudera/problem3/solution")
