from src.spark_main import create_spark_session
from src.ingestor import download_stock_data
from src.processor import sma_ema_indicators, bollinger_bands, rsi_indicator, risk_metrics
from src.analytics import calculate_volatility
from pyspark.sql import functions as F
import os

# Ticker Listesi
TICKERS = [
    
    "THYAO.IS", "GARAN.IS", "ASELS.IS", "EREGL.IS", "KCHOL.IS", 
    "TUPRS.IS", "AKBNK.IS", "SISE.IS", "BIMAS.IS", "SAHOL.IS",
    
   
    "AAPL", "MSFT", "TSLA", "NVDA", "AMZN", 
    "GOOGL", "META", "NFLX", "AMD", "PLTR"
]
START_DATE = "2016-01-01" 

def main():
   
    download_stock_data(TICKERS, START_DATE)
    
    
    spark = create_spark_session()
    
    # csv - > df e yazma işlemi ve tüm hisseleri tek bir DataFrame'de toplama
    all_data = []
    for ticker in TICKERS:
        path = f"data/{ticker}.csv"
        if os.path.exists(path):
            temp_df = spark.read.option("header", "true").option("inferSchema", "true").csv(path)
            temp_df = temp_df.withColumn("Ticker", F.lit(ticker))
            all_data.append(temp_df)
    
    if not all_data:
        print("Veri bulunamadı")
        return

    df = all_data[0]
    for next_df in all_data[1:]:
        df = df.unionByName(next_df, allowMissingColumns=True)

    # analislzeri df e yazma
    df = sma_ema_indicators(df)
    df = bollinger_bands(df)
    df = rsi_indicator(df)
    df = risk_metrics(df) 

    # Sonuçları Tek Bir Yere Kaydet
    output_path = "data/gold_results"
    df.write.mode("overwrite").parquet(output_path)
    
    print(f"✅ İşlem başarıyla tamamlandı. Veri şuraya yazıldı: {output_path}")
    

if __name__ == "__main__":
    main()