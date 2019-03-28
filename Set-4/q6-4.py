from pyspark import SparkContext, SQLContext
from pyspark.sql import *

sc = SparkContext()
sqlContext = SQLContext(sc)

customerDF = sqlContext.read.parquet("hdfs://localhost:8020/user/cloudera/problem6/data/customers")

customerDF.registerTempTable("customers")

outputDF = sqlContext.sql("select customer_id, customer_fname, customer_lname, concat(customer_fname,customer_lname) as alias from customers")
outputDF.coalesce(1).write.option("compression","SNAPPY").parquet("hdfs://localhost:8020/user/cloudera/problem6/solution")


	
