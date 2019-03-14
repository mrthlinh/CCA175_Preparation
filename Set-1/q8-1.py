from pyspark import SparkContext, SQLContext
from pyspark.sql.types import *
from pyspark.sql import *
from pyspark.sql.functions import *
import pyspark.sql.functions as sf


sc = SparkContext()
sqlContext = SQLContext(sc)
orderLine = sc.textFile("hdfs://localhost:8020/user/cloudera/problem8/data/orders")
order = orderLine.map(lambda x: x.split(","))
orderSchema = order.map(lambda s: Row(order_id = int(s[0]),
                                   order_date = s[1],
                                   order_customer_id =  int(s[2]),
                                   order_status =  s[3]))
orderDF = sqlContext.createDataFrame(orderSchema)
# orderDF.show()
df_output = orderDF.select(concat(orderDF.order_id, sf.lit(' '),orderDF.order_customer_id).alias("fullname"),
                           date_format(orderDF.order_date,'MM/dd').alias("date"))

df_output.show()
# output.coalesce(1).write.text("/user/cloudera/problem8/solution")
