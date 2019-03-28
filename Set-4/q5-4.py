from pyspark import SparkContext, SQLContext
from pyspark.sql import *

sc = SparkContext()
sqlContext = SQLContext(sc)

customerFile = sc.textFile("hdfs://localhost:8020/user/cloudera/problem5/data/customers")
customer = customerFile.map(lambda x: x.split(","))
customerSchema = customer.map(lambda x: Row( customer_id= int(x[0]),
					customer_fname	= x[1],
					customer_lname	= x[2],
					customer_email	= x[3],
					customer_password= x[4],
					customer_street	= x[5],
					customer_city	= x[6],
					customer_state	= x[7],
					customer_zipcode = x[8]))

customerDF = sqlContext.createDataFrame(customerSchema)
customerDF.registerTempTable("customers")

outputDF = sqlContext.sql("select customer_city as city, customer_state as state, count(customer_id) as no_customers from customers group by city, state")
customerDF.coalesce(1).write.option("compression","GZIP").csv("hdfs://localhost:8020/user/cloudera/problem5/solution")


	
