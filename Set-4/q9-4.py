from pyspark import SparkContext, SQLContext
from pyspark.sql import *

sc = SparkContext()
sqlContext = SQLContext(sc)

productLine = sc.textFile("hdfs://localhost:8020/user/cloudera/problem9/data/products")
product = productLine.map(lambda x: x.split("\t"))
productSchema = product.map(lambda x: Row( product_id=int(x[0]),
					product_category_id=int(x[1]),
					product_name=x[2],
					product_description=x[3],
					product_price=float(x[4]),
					product_image=x[5]))

productDF = sqlContext.createDataFrame(productSchema)

productDF.registerTempTable("products")

outputDF = sqlContext.sql("select product_category_id, avg(product_price) as avg_product_price from products group by product_category_id")

outputDF.coalesce(1).write.option("delimiter","\t").csv("hdfs://localhost:8020/user/cloudera/problem9/solution")


	
