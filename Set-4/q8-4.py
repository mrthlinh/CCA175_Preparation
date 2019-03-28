from pyspark import SparkContext, SQLContext
from pyspark.sql import *

sc = SparkContext()
sqlContext = SQLContext(sc)

customerDF = sqlContext.read.parquet("hdfs://localhost:8020/user/cloudera/problem6/data/customers")

customerDF.registerTempTable("customers")

outputDF = sqlContext.sql("select concat(substring(customer_fname,0,1),' ',customer_lname) as fullname, concat(customer_city,'-',customer_state) as `city-state` from customers")

#outputDF.show()

outputDF.coalesce(1).write.option("delimiter","\t").csv("hdfs://localhost:8020/user/cloudera/problem8/solution")


	
