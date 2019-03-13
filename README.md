# Mock test and revision for CCA175 Cloudera Certificate

CCA175 is performance-based (hands-on) exam conducted on Cloudera CDH
to test candidate skills on Apache Spark (1.6 / 2.3), Scala / Python, Hive, HDFS
and Sqoop.

Out of 9 problems, you get:

1. Sqoop Import
2. Sqoop Export
3. Hive (In some cases, can solve it using spark)
4. Spark (changing file format and compression)
5. Spark (count and groupby function)
6. Spark(concat)
7. Spark (concat, substring and order by)
8. Spark(join)
9. Spark (find avg or count, groupby functions)

## Problems:
1. Sqoop Import – In this problem, the data is stored in MySQL table and should
be imported to HDFS using Sqoop. The conditions may vary, for example:
Only few columns in customer table, who live in particular city must be
imported.\
__Note: No need to write in .sh file. Run the command directly on the
terminal.__

2. Sqoop Export – In this problem, the data is in HDFS and should be exported
to MySQL table.\
Always remember to check the format of data in HDFS location. Mostly, it is
tab separated data. Don’t forget to use --input-fields-terminated-by ‘ \t’.\
__Note: No need to write in .sh file. Run the command directly on the
terminal.__

3. Hive – This can be asked in two different types
  - If the question says that a hive table is present in hive metastore and
you need to save that data in the HDFS location using the given
compression and file format.\
Do it in spark using enableHiveSupport() which is easy and saves a lot
of time.\
__Note: You don’t need to create a database and table for this.__

  - If you’re asked to create a database and table in hive, then you need
to do it using hive. (For Impala, the procedure is same, do everything
in hive and use INVALIDATE METADATA command in impala-shell)

4. Spark – To execute any spark program, use spark2-submit ‘/path’
In this question, the data needs to be converted from one file format to
another. For example: the data should be converted in parquet GZIP
compression.

5,6,7,8,9 problems are based on different functions like Concat of first name and
last name, Concat of first letter of first name and last name, one question on Join
(two tables join), Substring of date to take only month&year, count, average, max,
min, group by, order by functions.
In spark, you will be asked to save the data in text format using tab or comma as
columnar delimiter. Make sure you’ve learned how to write using different file
formats and compression techniques.

## Important things to be noted
- MacOS is recommended instead of windows as this helps us to copy/paste
in easier way and saves a lot of time.
- For all the ‘.py files’, make sure to save the file before execution because
Ctrl+S will not work in the exam (if you are using windows). You can do it by
clicking on the file which is on top left corner and click save.
- It is always a good practice to check the source data format (csv, tab
separated columns etc.)
- During the exam once you have executed your solution, make sure to check
the target folder and the data content in the folder using cat command.
- Time management plays a vital role in the examination. Skip the problem and
proceed with the next problem if you get stuck anywhere.
- Spark – There are two versions of spark,1.6 and 2.3. To execute any spark
program with SparkSession (or you want to use spark 2.3 version to solve
spark problems), use spark2-submit ‘/path’.
  - Spark 1.6 – spark-Submit (for .py files)
  - Spark 1.6 – pyspark (to open terminal)
  - Spark 2.3 – spark2-submit (for .py files)
  - Spark 2.3 – pyspark2 (to open terminal) \
__NOTE: Be aware of the version you are using to execute spark programs.__
- There are no specific ways mentioned to solve spark problems. SparkSQL is
easier.
- Make sure you don’t use ‘hdfs://localhost:8020’ in the path during
exam(because we generally use ‘hdfs://localhost:8020’ in our virtual
machine to read or save data in spark to hdfs).
The path given in the problem can be used directly.
- In spark, it’s better to check the data if it is loaded by typing .show() after
creating the data frame.
- Don’t be nervous because you have all the tips now.
