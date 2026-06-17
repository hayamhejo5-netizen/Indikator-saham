import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# Pengaturan halaman agar pas di layar HP
st.set_page_config(page_title="Indikator Saham Pintar", layout="centered")

st.title("📊 Indikator Saham Pintar")
st.write("Tinggal masukkan kode saham untuk melihat grafik otomatis.")

# Input kode saham (Otomatis huruf besar)
ticker_input = st.text_input("Masukkan Kode Ticker Saham (Contoh: BBCA, TLKM, ASII):", "BBCA").strip().upper()

# Otomatis menambahkan '.JK' jika pengguna memasukkan saham Indonesia tanpa akhiran .JK
if ticker_input and not ticker_input.endswith('.JK') and len(ticker_input) <= 4:
    ticker = f"{ticker_input}.JK"
else:
    ticker = ticker_input

# Pilihan Rentang Waktu Grafik
periode = st.selectbox("Pilih Rentang Waktu:", ("1 Bulan", "3 Bulan", "6 Bulan", "1 Tahun"), index=2)
periode_map = {"1 Bulan": "1m", "3 Bulan": "3m", "6 Bulan": "6m", "1 Tahun": "1y"}

# Ambil data otomatis dari Yahoo Finance
if ticker:
    with st.spinner("Mengambil data..."):
        data_raw = yf.download(ticker, period=periode_map[periode], interval="1d")

    if not data_raw.empty:
        # Perbaikan Struktur Kolom agar Kebal Eror AttributeError
        df = data_raw.copy()
        
        # Jika kolom bertingkat (MultiIndex), kita ratakan dahulu
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
            
        df.index.name = 'date'
        df = df.reset_index()
        df.columns = [str(col).lower() for col in df.columns]
        
        st.success(f"✅ Menampilkan grafik untuk kode: {ticker}")
        
        # Membuat Grafik Candlestick Interaktif
        fig = go.Figure(data=[go.Candlestick(
            x=df['date'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name="Harga Saham"
        )])
        
        # Mempercantik visual grafik di HP
        fig.update_layout(
            xaxis_rangeslider_visible=True,
            template="plotly_dark",
            margin=dict(l=10, r=10, t=10, b=10)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Menampilkan Tabel Data 5 hari terakhir
        st.subheader("📋 Riwayat Data Harga (5 Hari Terakhir)")
        st.dataframe(df.tail(5), use_container_width=True)

    else:
        st.error(f"❌ Data untuk '{ticker}' tidak ditemukan. Jika mencari saham luar negeri, pastikan kodenya benar (Contoh: AAPL).")
