from pyspark import SparkContext, SQLContext
from pyspark.sql import *

sc = SparkContext()
sqlContext = SQLContext(sc)

productLine = sc.textFile("hdfs://localhost:8020/user/cloudera/CCA/product")
saleLine = sc.textFile("hdfs://localhost:8020/user/cloudera/CCA/sale")

product = productLine.map(lambda x: x.split(","))
sale = saleLine.map(lambda x: x.split(","))

productSchema = product.map(lambda x:Row(
					id = int(x[0]),
					version = int(x[1]),
					brand_name = x[2], 
					category = x[3],
					price = int(x[4]),
					product_name = x[5],
					weight = x[6] ))

saleSchema = sale.map(lambda x:Row(
				id = int(x[0]),
				version = int(x[1]),
				brand_name = x[2],
				item_purchased = int(x[3]),
				product_id = int(x[4]),
				purchase_date = x[5] ))

productDF = sqlContext.createDataFrame(productSchema)
saleDF = sqlContext.createDataFrame(saleSchema)

productDF.registerTempTable("product")
saleDF.registerTempTable("sale")

joinDF = sqlContext.sql("select p.id,p.brand_name,p.price,s.item_purchased from product as p join sale as s on p.id = s.product_id")
joinDF.registerTempTable("joinTable")

outputDF = sqlContext.sql("select brand_name, sum(item_purchased) from joinTable group by brand_name")

outputDF.show()


