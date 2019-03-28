from pyspark import SparkContext, HiveContext
from pyspark.sql import *

sc = SparkContext()
hiveContext = HiveContext(sc)

table = hiveContext.table("problem3.products")
table.registerTempTable("product")

outputDF = hiveContext.sql("select * from product where product_price > 10")
outputDF.write.option("compression","SNAPPY").parquet("hdfs://localhost:8020/user/cloudera/problem3/solution")
