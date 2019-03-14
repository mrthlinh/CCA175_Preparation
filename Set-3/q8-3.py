from pyspark import SparkContext, SQLContext
from pyspark.sql import *

sc = SparkContext()
sqlContext = SQLContext(sc)

orderLine = sc.textFile("hdfs://localhost:8020/user/cloudera/problem8/data/orders")
order = orderLine.map(lambda x: x.split(","))

orderSchema = order.map(lambda s: Row(order_id = int(s[0]),
                                   order_date = s[1],
                                   order_customer_id = int(s[2]),
                                   order_status =  s[3]))

orderDF = sqlContext.createDataFrame(orderSchema)

orderItemDF = sqlContext.read.parquet("hdfs://localhost:8020/user/cloudera/problem8/data/orderItems")
productDF = sqlContext.read.parquet("hdfs://localhost:8020/user/cloudera/problem8/data/products")

orderDF.registerTempTable("orders")
orderItemDF.registerTempTable("orderItems")
productDF.registerTempTable("products")

# df_output = sqlContext.sql("select order_id, order_date, order_customer_id, order_item_id,order_item_quantity, order_item_subtotal, product_id, product_category_id, product_name, product_price from orders join orderItems on order_id = order_item_order_id join products on order_item_product_id = product_id where product_price <= 100.00 and order_status = 'COMPLETE' ")

df_output = orderDF.join(orderItemDF,orderDF.order_id == orderItemDF.order_item_order_id).join(productDF, productDF.product_id == orderItemDF.order_item_product_id).where("product_price <= 100.00 and order_status = 'COMPLETE'").select("order_id", "order_date", "order_customer_id", "order_item_id","order_item_quantity", "order_item_subtotal", "product_id", "product_category_id", "product_name", "product_price")

# df_output.show()

df_output.coalesce(1).write.option("compression", "GZIP").parquet("hdfs://localhost:8020/user/cloudera/problem8/solution")

