from pyspark import SparkContext, SQLContext
sc = SparkContext()
sqlContext = SQLContext(sc)
customerLine = sqlContext.read.parquet("hdfs://localhost:8020/user/cloudera/problem6/data/customers")
customerLine.registerTempTable("customers")
df_result = sqlContext.sql("select customer_id, customer_fname, customer_lname, concat(customer_fname,' ',customer_lname) as alias from customers")
# df_result.show()
df_result.write.option("compression","SNAPPY").parquet("hdfs://localhost:8020/user/cloudera/problem6/solution_spark")
