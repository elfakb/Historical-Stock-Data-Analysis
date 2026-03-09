

# Historical Stock Analytics with Apache Spark

This project is an end-to-end data pipeline designed to perform financial analysis on 10-year historical stock market data using **Big Data** principles. Leveraging the distributed computing power of **Apache Spark**, the system calculates technical indicators and risk metrics, visualizing the results through an interactive **Streamlit** dashboard.


## Dataset 

The engine performs high-performance analytics on 10 years of historical daily price action (**OHLCV**) for a diverse portfolio:

* **Borsa Istanbul (BIST 30):** High-volume Turkish equities including **THYAO**, **GARAN**, **ASELS**, **EREGL**, and **TUPRS**.
* **Global Equities:** Major US Tech giants and growth stocks such as **AAPL**, **MSFT**, **TSLA**, **NVDA**, **AMZN**, and **META**.
* **Scope:** 10-year historical time horizon for robust long-term trend and risk evaluation.


The project is built with a focus on scalability and performance:

* **Data Ingestion:** Raw stock data in CSV format is loaded into the Spark environment.
* **Processing (Spark):** Distributed computation of RSI, Bollinger Bands, SMA, and Sharpe Ratio using `Window Functions`.
* **Storage (Gold Layer):** Processed data is stored in **Parquet** format to optimize read performance for the dashboard.
* **Visualization:** Real-time generation of Buy/Sell signals and risk profiles using Streamlit and Plotly.


## Quant Metrics and Indicators

* **Market Regime Analysis:** Detection of **Bull** or **Bear** markets based on 50/200 day **Simple Moving Average (SMA)** crossovers.
* **Volatility Channels:** Statistical analysis of price action using **Bollinger Bands** ($\pm 2$ standard deviations).
* **Momentum Tracking:** **Relative Strength Index (RSI 14)** implementation to identify Overbought and Oversold conditions.
* **Risk Management:** Calculation of **Sharpe Ratio** (Risk-Adjusted Return) and **Annualized Volatility** ($\sqrt{252}$) for portfolio optimization.
* **Actionable Insights:** Dynamic "Buy", "Sell", or "Hold" strategy recommendations based on technical triggers.
## Visuals & Demo

### Dashboard Overview
<img width="1524" height="773" alt="image" src="https://github.com/user-attachments/assets/4cff76c7-a314-4514-99c6-c03fc0fe8221" />



### Interface Walkthrough

<img width="1464" height="830" alt="image" src="https://github.com/user-attachments/assets/d551434f-104e-459a-aefd-0b51891a3ab2" />

<img width="1464" height="830" alt="image" src="https://github.com/user-attachments/assets/d85a8f32-b9c1-4823-adea-1447d11d3c9a" />
<img width="1464" height="830" alt="image" src="https://github.com/user-attachments/assets/dba94158-1f92-4db3-a0be-9ab6a9ecc706" />

<img width="1464" height="830" alt="image" src="https://github.com/user-attachments/assets/2d1b9ef2-2cd9-4cba-b664-b11f2bb67094" />

### Project Demo


https://github.com/user-attachments/assets/ffcd9710-9bf5-4859-a378-81f9ebc7edff



https://github.com/user-attachments/assets/194770b2-2a60-489c-b4c4-fe3b4fc914cb






# Apache Spark ile Hisse Senedi AnaliZİ

Bu proje, 10 yıllık geçmiş borsa verileri üzerinde finansal analizler gerçekleştirmek için tasarlanmış uçtan uca bir veri hattıdır. Apache Spark ile teknik göstergeleri ve risk metriklerini hesaplar, sonuçları ise etkileşimli bir Streamlit paneli aracılığıyla görselleştirir.

## Veri Seti

Analiz motoru, çeşitlendirilmiş bir portföy için 10 yıllık geçmiş günlük fiyat hareketleri (OHLCV) üzerinde yüksek performanslı analizler gerçekleştirir:

* **Borsa İstanbul (BIST 30):** THYAO, GARAN, ASELS, EREGL ve TUPRS gibi yüksek hacimli Türk hisselerini içerir.
* **Küresel Hisseler:** AAPL, MSFT, TSLA, NVDA, AMZN ve META gibi büyük ABD teknoloji devlerini ve büyüme hisselerini kapsar.
* **Kapsam:** Güçlü uzun vadeli trend ve risk değerlendirmesi için 10 yıllık geçmiş zaman dilimi baz alınmıştır.


* **Veri Alımı:** CSV formatındaki ham hisse senedi verileri Spark ortamına yüklenir.
* **İşleme (Spark):** Pencere Fonksiyonları (Window Functions) kullanılarak RSI, Bollinger Bantları, SMA ve Sharpe Oranı gibi metriklerin dağıtık hesaplaması yapılır.
* **Depolama (Gold Layer):** İşlenen veriler, panel okuma performansını optimize etmek için Parquet formatında saklanır.
* **Görselleştirme:** Streamlit ve Plotly kullanılarak gerçek zamanlı Al/Sat sinyalleri ve risk profilleri oluşturulur.

## Kantitatif Metrikler ve Göstergeler

* **Piyasa Rejimi Analizi:** 50/200 günlük Basit Hareketli Ortalama (SMA) kesişimlerine dayalı Boğa veya Ayı piyasası tespiti.
* **Volatilite Kanalları:** Bollinger Bantları (+/- 2 standart sapma) kullanılarak fiyat hareketlerinin istatistiksel analizi.
* **Momentum Takibi:** Aşırı alım ve aşırı satım koşullarını belirlemek için Göreceli Güç Endeksi (RSI 14) uygulaması.
* **Risk Yönetimi:** Portföy optimizasyonu için Sharpe Oranı (Risk Ayarlı Getiri) ve Yıllıklandırılmış Volatilite (kök 252) hesaplamaları.
* **Uygulanabilir Analizler:** Teknik tetikleyicilere dayalı dinamik "Al", "Sat" veya "Bekle" strateji önerileri.



### Panel Genel Bakış
![Dashboard](screenshots/dashboard.png)

## Görseller ve Demo
<img width="1464" height="830" alt="image" src="https://github.com/user-attachments/assets/d551434f-104e-459a-aefd-0b51891a3ab2" />

<img width="1464" height="830" alt="image" src="https://github.com/user-attachments/assets/d85a8f32-b9c1-4823-adea-1447d11d3c9a" />
<img width="1464" height="830" alt="image" src="https://github.com/user-attachments/assets/dba94158-1f92-4db3-a0be-9ab6a9ecc706" />

<img width="1464" height="830" alt="image" src="https://github.com/user-attachments/assets/2d1b9ef2-2cd9-4cba-b664-b11f2bb67094" />




