from pyspark.sql import functions as F
from pyspark.sql.window import Window

def calculate_volatility(df):
    window_spec = Window.partitionBy("Ticker").orderBy("Date")
    
    df = df.withColumn("Daily_Return", 
                       (F.col("Close") - F.lag("Close").over(window_spec)) / F.lag("Close").over(window_spec))
    
    # Yıllıklandırılmış Volatilite (Standart Sapma * kök(252))
    stats = df.groupBy("Ticker").agg(F.stddev("Daily_Return").alias("StdDev"))
    df = df.join(stats, "Ticker").withColumn("Annual_Volatility", F.col("StdDev") * F.sqrt(F.lit(252)))
    
    return df