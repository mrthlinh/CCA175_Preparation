from pyspark import SparkContext, SQLContext
from pyspark.sql import *

sc = SparkContext()
sqlContext = SQLContext(sc)
orderitemLine = sc.textFile("hdfs://localhost:8020/user/cloudera/problem7/data/orderItems")
orderLine = sc.textFile("hdfs://localhost:8020/user/cloudera/problem7/data/orders")

orderItem = orderitemLine.map(lambda x: x.split(","))
order = orderLine.map(lambda x: x.split("\t"))

orderItemSchema = orderItem.map(lambda x: Row( order_item_id	= int(x[0]),
					order_item_order_id	= int(x[1]),
					order_item_product_id	= int(x[2]),
					order_item_quantity	= int(x[3]),
					order_item_subtotal	= float(x[4]),
					order_item_product_price= float(x[5]) ))

orderSchema = order.map(lambda s: Row(order_id = int(s[0]),
                                   order_date = s[1],
                                   order_customer_id =  int(s[2]),
                                   order_status =  s[3]))

orderItemDF = sqlContext.createDataFrame(orderItemSchema)
orderDF = sqlContext.createDataFrame(orderSchema)


orderItemDF.registerTempTable("orderItems")
orderDF.registerTempTable("orders")

df_output = sqlContext.sql("select concat(order_item_id,' ',order_id) as col1, order_status from orders join orderItems on order_id = order_item_order_id")

#df_output.show()

df_output.coalesce(1).write.option("delimiter","\t").csv("hdfs://localhost:8020/user/cloudera/problem7/solution")

