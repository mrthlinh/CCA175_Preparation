from pyspark import SparkContext, SQLContext
from pyspark.sql import *

sc = SparkContext()
sqlContext = SQLContext(sc)

orderLine = sc.textFile("hdfs://localhost:8020/user/cloudera/CCA/orders")
order = orderLine.map(lambda x: x.split(","))

orderSchema = order.map(lambda x: Row(order_id = int(x[0]),order_date = x[1],order_customer_id = int(x[2]),order_status = x[3]))

orderDF = sqlContext.createDataFrame(orderSchema)

orderItemLine = sc.textFile("hdfs://localhost:8020/user/cloudera/CCA/order_items")
orderItem = orderItemLine.map(lambda x: x.split(","))

orderItemSchema = orderItem.map(lambda x: Row(order_item_id = int(x[0]),order_item_order_id = int(x[1]),order_item_product_id = int(x[2]),order_item_quantity = int(x[3]),order_item_subtotal = float(x[4]),order_item_product_price = float(x[5])))

orderItemDF = sqlContext.createDataFrame(orderItemSchema)

orderDF.registerTempTable("order")
orderItemDF.registerTempTable("orderItem")

joinDF = sqlContext.sql("select * from order join orderItem on order.order_id = orderItem.order_item_order_id")

joinDF.registerTempTable("joinTable")

outputDF = sqlContext.sql("select order_date, count(order_id) as total_order from joinTable group by order_date")

outputDF.coalesce(1).write.option("compression","SNAPPY").parquet("hdfs://localhost:8020/user/cloudera/CCA/TR4")
# outputDF.show()


