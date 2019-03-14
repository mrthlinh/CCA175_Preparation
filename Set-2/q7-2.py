from pyspark import SparkContext, SQLContext
from pyspark.sql import *

sc = SparkContext()
sqlContext = SQLContext(sc)
customerLine = sc.textFile("hdfs://localhost:8020/user/cloudera/problem7/data/customers")
orderLine = sc.textFile("hdfs://localhost:8020/user/cloudera/problem7/data/orders")
customer = customerLine.map(lambda x: x.split("\t"))
order = orderLine.map(lambda x: x.split("\t"))
customerSchema = customer.map(lambda s: Row(customer_id=int(s[0]),
                                           customer_fname = s[1],
                                           customer_lname = s[2],
                                           customer_email = s[3],
                                           customer_password = s[4],
                                           customer_street = s[5],
                                           customer_city  = s[6],
                                           customer_state =  s[7],
                                           customer_zipcode = s[8]))
orderSchema = order.map(lambda s: Row(order_id = int(s[0]),
                                   order_date = s[1],
                                   order_customer_id =  int(s[2]),
                                   order_status =  s[3]))

customerDF = sqlContext.createDataFrame(customerSchema)
orderDF = sqlContext.createDataFrame(orderSchema)
customerDF.registerTempTable("customers")
orderDF.registerTempTable("orders")

df_output = sqlContext.sql("select customer_id, customer_fname, customer_lname, customer_email, count(o.order_id) as total_orders from customers as c inner join orders as o on c.customer_id = o.order_customer_id group by customer_id,customer_fname, customer_lname, customer_email")

# df_output.show()
df_output.coalesce(1).write.option("compression", "GZIP").csv("hdfs://localhost:8020/user/cloudera/problem7/solution")

