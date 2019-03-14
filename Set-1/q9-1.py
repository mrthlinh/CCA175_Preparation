from pyspark import SparkContext, SQLContext
from pyspark.sql.types import *
from pyspark.sql import *
from pyspark.sql.functions import *
import pyspark.sql.functions as f
sc = SparkContext()
sqlContext = SQLContext(sc)
productLine = sc.textFile("hdfs://localhost:8020/user/cloudera/problem9/data/products")
product = productLine.map(lambda x: x.split("\t"))
productSchema = product.map(lambda s: Row(product_id = int(s[0]),
                                          product_category_id = int(s[1]),
                                          product_name =  s[2],
                                          product_description =  s[3],
                                          product_price = float(s[4]),
                                          product_image = s[5]))
productDF = sqlContext.createDataFrame(productSchema)
# productDF.show()
productDF.registerTempTable("product")
df_output = sqlContext.sql("select product_category_id,avg(product_price) as avg_product_price "
                           "from product group by product_category_id")
# df_output = productDF.groupBy("product_category_id").agg(f.avg(productDF.product_price).alias("avg_product_price"))

# df_output.show()
df_output.coalesce(1).write.csv("hdfs://localhost:8020/user/cloudera/problem9/solution")
