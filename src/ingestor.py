import os 
import yfinance as yf 

def download_stock_data(tickers , start_date , output = "data"):
    # klasçr bulunmuyosa oluştur 
    if not os.path.exists(output):
        os.makedirs(output)
    
    for ticker in tickers:
        print(f"Downloading data for : {ticker}")
        data = yf.download(ticker , start = start_date  ,auto_adjust = True)

        data.reset_index(inplace = True) # sadece date sütünu kalsın diye indexi sıfırlıyoruz
        file_path = os.path.join(output, f"{ticker}.csv")
        data.to_csv(file_path, index=False)
    
    print("Download completed!")
