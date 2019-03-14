from pyspark import SparkContext, SQLContext
from pyspark.sql import *

sc = SparkContext()
sqlContext = SQLContext(sc)

orderLine = sc.textFile("hdfs://localhost:8020/user/cloudera/problem4/data/orders")
order = orderLine.map(lambda x: x.split("\t"))
orderSchema = order.map(lambda x: Row(order_id = int(x[0]),
					order_date = x[1],
					order_customer_id = int(x[2]),
					order_status = x[3]))

orderDF = sqlContext.createDataFrame(orderSchema)

orderDF.coalesce(1).write.option("compression","GZIP").parquet("hdfs://localhost:8020/user/cloudera/problem4/solution")
#orderDF.show()
