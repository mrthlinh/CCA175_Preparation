from pyspark import SparkContext, SQLContext
from pyspark.sql import *
from pyspark.sql.functions import *

sc = SparkContext()
sqlContext = SQLContext(sc)

orderLine = sc.textFile("hdfs://localhost:8020/user/cloudera/problem7/data/orders")
order = orderLine.map(lambda x: x.split("\t"))
orderSchema = order.map(lambda s: Row(order_id = int(s[0]),
                                   order_date = s[1],
                                   order_customer_id = int(s[2]),
                                   order_status =  s[3]))

orderDF = sqlContext.createDataFrame(orderSchema)


customerLine = sc.textFile("hdfs://localhost:8020/user/cloudera/problem7/data/customers")
customer = customerLine.map(lambda x: x.split("\t"))
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

customerDF.registerTempTable("customer")
orderDF.registerTempTable("order")

df_output = sqlContext.sql("select customer_id,customer_fname, customer_lname, customer_email, customer_city, count(order_id) as total_orders from customer outer join order on customer_id=order_customer_id group by customer_id,customer_fname, customer_lname, customer_email, customer_city")

# df_output = customerDF.join(orderDF,customerDF.customer_id == orderDF.order_customer_id,"outer")\
#     .groupBy("customer_id","customer_fname","customer_lname","customer_email","customer_city").count().withColumnRenamed('count','total_orders')

# df_output.show()

df_output.coalesce(1).write.option("compression","GZIP").csv("hdfs://localhost:8020/user/cloudera/problem7/solution")


