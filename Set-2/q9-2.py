from pyspark import SparkContext, SQLContext
from pyspark.sql import *

sc = SparkContext()
sqlContext = SQLContext(sc)

orderItemLine = sc.textFile("hdfs://localhost:8020/user/cloudera/problem9/data/orderItems")
orderItem = orderItemLine.map(lambda x: x.split("|"))
orderItemSchema = orderItem.map(lambda x: Row(order_item_id=int(x[0]),
                                              order_item_order_id=int(x[1]),
                                              order_item_product_id=int(x[2]),
                                              order_item_quantity=int(x[3]),
                                              order_item_subtotal=float(x[4]),
                                              order_item_product_price=float(x[5])))

orderDF = sqlContext.createDataFrame(orderItemSchema)
# orderDF.show()
orderDF.registerTempTable("orders")
df_output = sqlContext.sql("select order_item_product_id, order_item_product_price, sum(order_item_quantity) as total_quantity from orders group by order_item_product_id, order_item_product_price")
# df_output.show()
df_output.coalesce(1).write.option("compression","SNAPPY").parquet("hdfs://localhost:8020/user/cloudera/problem9/solution")


