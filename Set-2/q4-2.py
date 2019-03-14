from pyspark import SparkContext, SQLContext
from pyspark.sql import *


sc = SparkContext()
sqlContext = SQLContext(sc)

orderLine = sc.textFile("hdfs://localhost:8020/user/cloudera/problem4/data/orders")

order = orderLine.map(lambda x: x.split("|"))
orderSchema = order.map(lambda s: Row(order_id = int(s[0]),
                                   order_date = s[1],
                                   order_customer_id =  int(s[2]),
                                   order_status =  s[3]))
orderDF = orderSchema.createDateFrame(orderSchema)
orderDF.write.option("compression","GZIP").parquet("hdfs://localhost:8020/user/cloudera/problem4/solution")
