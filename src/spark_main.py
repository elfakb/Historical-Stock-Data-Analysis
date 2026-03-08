from pyspark.sql import SparkSession

def create_spark_session():
    return SparkSession.builder \
        .appName("Historical_stock_analysis") \
        .master("local[*]") \
        .config("spark.driver.memory", "4g") \
        .getOrCreate()