# To run this in spark-submit
# spark-submit --packages com.databricks:spark-avro_2.11:3.2.0 q8.py

from pyspark import SparkContext, SQLContext
from pyspark.sql import *

sc = SparkContext()
sqlContext = SQLContext(sc)

customerLine = sc.textFile("hdfs://localhost:8020/user/cloudera/CCA/customers")
customer = customerLine.map(lambda x: x.split("\t"))

customerSchema = customer.map(lambda x: Row(customer_id=int(x[0]),
					customer_fname = x[1],
					customer_lname = x[2],
					customer_email = x[3],
					customer_password = x[4],
					customer_street = x[5],
					customer_city = x[6],
					customer_state= x[7],
					customer_zipcode= x[8]))

customerDF = sqlContext.createDataFrame(customerSchema)


orderLine = sc.textFile("hdfs://localhost:8020/user/cloudera/CCA/orders")
order = orderLine.map(lambda x: x.split(","))

orderSchema = order.map(lambda x: Row(order_id = int(x[0]),
					order_date = x[1],
					order_customer_id = int(x[2]),
					order_status = x[3]))

orderDF = sqlContext.createDataFrame(orderSchema)

orderItemLine = sc.textFile("hdfs://localhost:8020/user/cloudera/CCA/order_items")
orderItem = orderItemLine.map(lambda x: x.split(","))

orderItemSchema = orderItem.map(lambda x: Row(order_item_id = int(x[0]),
					order_item_order_id = int(x[1]),
					order_item_product_id = int(x[2]),
					order_item_quantity = int(x[3]),
					order_item_subtotal = float(x[4]),
					order_item_product_price = float(x[5])))

orderItemDF = sqlContext.createDataFrame(orderItemSchema)

orderDF.registerTempTable("order")
orderItemDF.registerTempTable("orderItem")
customerDF.registerTempTable("customer")


joinDF = sqlContext.sql("select customer_id, customer_city, customer_state, order_id, order_item_subtotal from customer join order on customer_id = order_customer_id join orderItem on order_id = order_item_order_id")

joinDF.registerTempTable("joinTable")

outputDF = sqlContext.sql("select customer_city as City, customer_state as State, count(order_id) as total_no_of_orders, sum(order_item_subtotal) as revenue from joinTable group by City, State")

#outputDF.show()

outputDF.write.option("compression","GZIP").format("com.databricks.spark.avro").save("hdfs://localhost:8020/user/cloudera/CCA/TR8")





