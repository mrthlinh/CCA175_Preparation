from pyspark import SparkContext, HiveContext

sc = SparkContext()
hiveContext = HiveContext(sc)
table = hiveContext.table("orders")
table.registerTempTable("orders")
orderDF = hiveContext.sql("select * from orders where order_status = 'PENDING'")

orderDF.coalesce(1).write.option("compression","SNAPPY").parquet("hdfs://localhost:8020/user/cloudera/CCA/TR3")

#orderDF.show()

