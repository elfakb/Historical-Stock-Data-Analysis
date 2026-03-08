import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os



st.set_page_config(layout="wide", page_title="Hisse Analizi")

#@st.cache_data
def load_data():
    path = "data/gold_results" 
    if os.path.exists(path):
        df = pd.read_parquet(path)
        # Sayısal sütunları zorla float yap, hata verenleri NaN yap ve sonra sil
        numeric_cols = ['Close', 'upper_band', 'lower_band', 'rsi', 'volatility', 'sharpe_ratio']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        return df.dropna(subset=numeric_cols)
    return None

df = load_data()

if df is None:
    st.error("VERİ YÜKLENEMEDİ .")
    st.stop()

# --- SIDEBAR ---
st.sidebar.title("Portföy Analizi")
ticker = st.sidebar.selectbox("Hisse Seçin", df['Ticker'].unique())
st.write(f"Seçilen Ticker: {ticker}")


# Filtreleme
hisse_df = df[df['Ticker'] == ticker].sort_values("Date")
current_trend = hisse_df['Trend'].iloc[-1]
st.write(hisse_df[['Ticker', 'volatility', 'sharpe_ratio']].tail(1))

# --- ANA PANEL ---
st.title(f"{ticker} Hissesinin 10 Yıllık Veri Analiz Paneli")

tab1, tab2, tab3 = st.tabs(["📈 Teknik Analiz", "🛡️ Risk Metrikleri", "📘Bilgi"])

with tab1:
    st.subheader(f"{ticker} Teknik İndikatörleri")
    

    latest_data = hisse_df.iloc[-1]
    
    current_trend = latest_data['Trend']
    last_rsi = latest_data['rsi']
    last_close = latest_data['Close']
    upper_b = latest_data['upper_band']
    lower_b = latest_data['lower_band']

    # --- 1. DİNAMİK TREND BİLGİSİ ---
    if current_trend == "BULL":
        st.success(f"**Güncel Durum: BOĞA (BULL)** 🐂 | SMA 50 > SMA 200. Yükseliş trendi aktif.")
    else:
        st.error(f"**Güncel Durum: AYI (BEAR)** 🐻 | SMA 50 < SMA 200. Düşüş baskısı hakim.")

    col_chart, col_info = st.columns([3, 1])
    
    with col_chart:
        # Fiyat ve Bollinger Grafiği
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=hisse_df['Date'], y=hisse_df['Close'], name='Fiyat', line=dict(color='white')))
        fig.add_trace(go.Scatter(x=hisse_df['Date'], y=hisse_df['upper_band'], name='Üst Bant', line=dict(dash='dash', color='gray')))
        fig.add_trace(go.Scatter(x=hisse_df['Date'], y=hisse_df['lower_band'], name='Alt Bant', line=dict(dash='dash', color='gray')))
        fig.update_layout(template="plotly_dark", height=500, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig, use_container_width=True)

        # RSI Grafiği
        fig_rsi = go.Figure()
        fig_rsi.add_trace(go.Scatter(x=hisse_df['Date'], y=hisse_df['rsi'], name='RSI', line=dict(color='orange')))
        fig_rsi.add_hline(y=70, line_dash="dot", line_color="red")
        fig_rsi.add_hline(y=30, line_dash="dot", line_color="green")
        fig_rsi.update_layout(template="plotly_dark", height=250, title=f"RSI: {last_rsi:.2f}")
        st.plotly_chart(fig_rsi, use_container_width=True)
    
    with col_info:
        st.info("**Hızlı Strateji:**")
        
        # --- 2. DİNAMİK RSI STRATEJİSİ ---
        if last_rsi > 70:
            st.warning(f"⚠️ **SAT SİNYALİ**")
            st.write(f"RSI ({last_rsi:.1f}) aşırı alımda. Kâr realizasyonu düşünülebilir.")
        elif last_rsi < 30:
            st.success(f"✅ **AL SİNYALİ**")
            st.write(f"RSI ({last_rsi:.1f}) aşırı satımda. Tepki alımı gelebilir.")
        else:
            st.write(f"⚖️ **NÖTR / İZLE**")
            st.write("Fiyat dengeli bölgede. Trendi takip etmeye devam edin.")

        st.divider()

        # --- 3. EKSTRA: BOLLINGER SİNYALİ ---
        st.write("**Fiyat Konumu:**")
        if last_close >= upper_b:
            st.error("DİRENÇ: Fiyat üst banda çarptı.")
        elif last_close <= lower_b:
            st.success("DESTEK: Fiyat alt banda çarptı.")
        else:
            st.write("Üst- Alt içinde normal seyir.")
with tab2:
    st.subheader("Risk ve Performans Özeti")
    
    c1, c2, c3 = st.columns(3)
    current_vol = hisse_df['volatility'].iloc[-1]
    current_sharpe = hisse_df['sharpe_ratio'].iloc[-1]
    
    c1.metric("Yıllık Volatilite", f"%{current_vol*100:.2f}", help="Hissenin yıllık bazda fiyat oynaklığını gösterir.")
    
    sharpe_delta = "Güçlü Getiri" if current_sharpe > 1 else "Düşük Getiri"
    c2.metric("Sharpe Ratio", f"{current_sharpe:.2f}", delta=sharpe_delta, help="Bir birim riske karşılık elde edilen fazla getiriyi ölçer.")
    
    c3.metric("Trend Durumu", current_trend, delta="Bullish" if current_trend == "BULL" else "Bearish")

    st.divider()

    # Getiri Dağılımı
    fig_dist = px.histogram(hisse_df, x="daily_return", 
                            title="Günlük Getiri Dağılımı", 
                            nbins=100, 
                            template="plotly_dark",
                            color_discrete_sequence=['#636EFA'])
    st.plotly_chart(fig_dist, use_container_width=True)
    st.caption("Not: Dağılımın merkezden sağa veya sola kayması, hissenin getiri karakteristiğini (pozitif/negatif skewness) gösterir.")

with tab3:
    st.header("📘 Finansal Metrikler ve Teknik Analiz Bilgileri")
    st.markdown("""

    * **Market Regime ve Trend Analizi:**
        * **Bull Market (Boğa):** 50 günlük **Simple Moving Average** (SMA 50) değerinin, 200 günlük ortalamayı (SMA 200) yukarı yönlü kesmesiyle oluşur; yapısal bir yükseliş trendini işaret eder.
        * **Bear Market (Ayı):** Kısa vadeli momentumun uzun vadeli trendin altına sarkmasıdır; piyasada satış baskısının ve negatif **Market Sentiment**'in hakim olduğunu temsil eder.
    * **Bollinger Bands:** Fiyatın, 20 günlük hareketli ortalamadan $\pm 2$ **Standard Deviation** uzaklığını ölçen istatistiksel bir göstergedir. Fiyatın **Upper Band** teması "teknik aşırı değerlenme", **Lower Band** teması ise "aşırı düşüş" (ucuzluk) olasılığını simgeler.
    * **Relative Strength Index (RSI 14):** Fiyat hareketlerinin hızını ve değişimini ölçen bir **Momentum Oscillator**'dür. 
        * **Overbought (70+ Seviyesi):** Piyasanın doygunluğa ulaştığını ve **Profit-Taking** (Kâr Satışı) ihtimalinin arttığını gösterir.
        * **Oversold (30- Seviyesi):** Fiyatın dip arayışında olduğunu ve teknik tepki alımlarının (**Buy Signals**) başlayabileceğini işaret eder.
    * **Sharpe Ratio (Risk-Adjusted Return):** Portföyün veya varlığın, alınan birim risk başına ürettiği **Excess Return**'ü ölçer. 1.0 üzerindeki değerler, yatırımın riskine oranla verimli ve sürdürülebilir bir getiri sunduğunu kanıtlar.
    * **Annualized Volatility:** Günlük getirilerin standart sapmasının yıllıklandırılarak ($\sqrt{252}$) sunulmuş halidir. Hissenin fiyat oynaklığını ve maruz kalınan toplam **Market Risk**'i temsil eder.
    """)
# Sayfa Altı
st.sidebar.markdown("---")
st.sidebar.info(f"Elif Akbaş")