from pyspark.sql import functions as f 
from pyspark.sql.window import Window

def sma_ema_indicators(df):
    win = Window.partitionBy("Ticker").orderBy("Date")

    # sma 50 - 200-20
    df = df.withColumn("SMA_50", f.avg("Close").over(win.rowsBetween(-49, 0)))
    df = df.withColumn("SMA_200", f.avg("Close").over(win.rowsBetween(-199, 0)))
    df = df.withColumn("EMA_20", f.avg("Close").over(win.rowsBetween(-19, 0)))

    # trend bear ot bull bulma
    df = df.withColumn("Trend", 
                       f.when(f.col("SMA_50") > f.col("SMA_200"), "BULL")
                       .otherwise("BEAR"))
    return df


def bollinger_bands(df):
    win = Window.partitionBy("Ticker").orderBy("Date").rowsBetween(-19, 0)
    
    df = df.withColumn("SMA_20", f.avg("Close").over(win))
    df = df.withColumn("stddev_20", f.stddev("Close").over(win))
    
    df = df.withColumn("upper_band", f.col("SMA_20") + (f.col("stddev_20") * 2))
    df = df.withColumn("lower_band", f.col("SMA_20") - (f.col("stddev_20") * 2))

    return df

def rsi_indicator(df):
     win = Window.partitionBy("Ticker").orderBy("Date")

     df = df.withColumn("diff" , f.col("Close") - f.lag("Close", 1).over(win))

     df = df.withColumn("gain" , f.when(f.col("diff") > 0, f.col("diff")).otherwise(0)).withColumn("loss" , f.when(f.col("diff") < 0, f.abs(f.col("diff") )).otherwise(0))
     window_rsi = Window.partitionBy("Ticker").orderBy("Date").rowsBetween(-13, 0)
     df = df.withColumn("avg_gain" , f.avg("gain").over(window_rsi)).withColumn("avg_loss" , f.avg("loss").over(window_rsi))

     df = df.withColumn("rs" , f.col("avg_gain") / f.col("avg_loss")).withColumn("rsi" , 100 - (100 / (1 + f.col("rs"))))
     return df


def risk_metrics(df):
    win_all = Window.partitionBy("Ticker").orderBy("Date")
    win_full = Window.partitionBy("Ticker") 

    df = df.withColumn("daily_return",(f.col("Close") - f.lag("Close", 1).over(win_all)) / f.lag("Close", 1).over(win_all))
    

    df = df.withColumn("volatility", f.stddev("daily_return").over(win_full) * (252 ** 0.5))
    
    avg_ret = f.avg("daily_return").over(win_full)
    std_ret = f.stddev("daily_return").over(win_full)
    df = df.withColumn("sharpe_ratio", (avg_ret - (0.05/252)) / std_ret)
    
    return df