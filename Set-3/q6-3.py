from pyspark import SparkContext, SQLContext
from pyspark.sql import *
from pyspark.sql.functions import *

sc = SparkContext()
sqlContext = SQLContext(sc)

customerLine = sc.textFile("hdfs://localhost:8020/user/cloudera/problem5/data/customers")
customer = customerLine.map(lambda x: x.split("|"))
customerSchema = customer.map(lambda x: Row(customer_id=int(x[0]),
                                            customer_fname=x[1],
                                            customer_lname=x[2],
                                            customer_email=x[3],
                                            customer_password=x[4],
                                            customer_street=x[5],
                                            customer_city=x[6],
                                            customer_state=x[7],
                                            customer_zipcode=x[8]))
customerDF = sqlContext.createDataFrame(customerSchema)

# customerDF.registerTempTable("customer")
# df_output = sqlContext.sql("select customer_id, concat(substring(customer_lname,0,1),customer_fname) as customer_name, customer_email,customer_city from customer where customer_state='CA'")

df_output = customerDF.select("customer_id",concat(substring("customer_lname",0,1),"customer_fname").alias("customer_name"),"customer_email","customer_city").where("customer_state = 'CA'")

# df_output.show()
df_output.coalesce(1).write.csv("hdfs://localhost:8020/user/cloudera/problem6/solution")
