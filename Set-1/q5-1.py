from pyspark import SparkContext, SQLContext
from pyspark.sql import *
from pyspark.sql.functions import *

sc = SparkContext()
sqlContext = SQLContext(sc)
customerLine = sc.textFile("hdfs://localhost:8020/user/cloudera/problem5/data/customers")
customer = customerLine.map(lambda x: x.split("|"))
customerSchema = customer.map(lambda s: Row(customer_id=int(s[0]),
                                           customer_fname = s[1],
                                           customer_lname = s[2],
                                           customer_email = s[3],
                                           customer_password = s[4],
                                           customer_street = s[5],
                                           customer_city  = s[6],
                                           customer_state =  s[7],
                                           customer_zipcode = s[8]))

customerDF = sqlContext.createDataFrame(customerSchema)
customerDF.registerTempTable("customers")

df_output = sqlContext.sql("select customer_city, customer_state, count(customer_id) as no_customer from customers group by customer_city, customer_state")

# df_output = customerDF.groupby("customer_city", "customer_state").agg(count(customerDF.customer_id).alias("no.of customers"))

# df_output.show()

df_output.coalesce(1).write.option("delimiter","\t").csv("hdfs://localhost:8020/user/cloudera/problem5/solution")

