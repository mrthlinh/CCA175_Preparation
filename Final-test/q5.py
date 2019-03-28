# To run this in spark-submit
# spark-submit --packages com.databricks:spark-avro_2.11:3.2.0 q5.py

from pyspark import SparkContext, SQLContext
from pyspark.sql import *

sc = SparkContext()
sqlContext = SQLContext(sc)

productDF = sqlContext.read.format("com.databricks.spark.avro").load("hdfs://localhost:8020/user/cloudera/CCA/problem1/products/")

productDF.registerTempTable("product")

outputDF = sqlContext.sql("select max(price) as max, min(price) as min, avg(price) as avg from product group by product_name")

outputDF.coalesce(1).write.option("compression","GZIP").parquet("hdfs://localhost:8020/user/cloudera/CCA/TR5")
#productDF.show()
