from pyspark import SparkContext, SQLContext
from pyspark.sql import *
import pyspark.sql.functions as func

sc = SparkContext()
sqlContext = SQLContext(sc)

customerLine = sc.textFile("hdfs://localhost:8020/user/cloudera/problem5/data/customers")
customer = customerLine.map(lambda x: x.split("|"))
customerSchema = customer.map(lambda x: Row(customer_id=int(x[0]),
                                            customer_fname=x[1],
                                            customer_lname=x[2],
                                            customer_email=x[3],
                                            customer_password=x[4],
                                            customer_street=x[5],
                                            customer_city=x[6],
                                            customer_state=x[7],
                                            customer_zipcode=x[8]))
customerDF = sqlContext.createDataFrame(customerSchema)

# customerDF.registerTempTable("customer")
# df_output = sqlContext.sql("select customer_city as city, customer_state as state, count(customer_id) as no_customers from customer group by customer_city, customer_state")

df_output = customerDF.select("customer_id","customer_city","customer_state").groupBy('customer_city','customer_state').agg(func.countDistinct("customer_id").alias("no.of customers"))

#df_output.show()
df_output.coalesce(1).write.option("delimiter","\t").csv("hdfs://localhost:8020/user/cloudera/problem5/solution")
