import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Pengaturan halaman agar pas di layar HP
st.set_page_config(page_title="Indikator Saham Instan", layout="centered")

st.title("📈 Indikator Saham Pintar")
st.write("Cukup upload file data saham (`.csv`), dapatkan sinyal beli instan!")

# 1. Fitur Upload File
uploaded_file = st.file_uploader("Upload file CSV saham Anda di sini", type=["csv"])

if uploaded_file is not None:
    try:
        # Membaca data
        df = pd.read_csv(uploaded_file)
        
        # Membersihkan nama kolom (mengantisipasi perbedaan format)
        df.columns = [col.strip().lower() for col in df.columns]
        
        # Memastikan kolom yang dibutuhkan ada
        required_cols = ['date', 'close']
        if not all(col in df.columns for col in required_cols):
            st.error("Pastikan file CSV memiliki kolom 'Date' dan 'Close'!")
        else:
            # Mengurutkan tanggal dari lama ke baru
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date').reset_index(drop=True)
            
            # --- Perhitungan Indikator ---
            # 1. Moving Average (MA 20 & MA 50)
            df['ma20'] = df['close'].rolling(window=20).mean()
            df['ma50'] = df['close'].rolling(window=50).mean()
            
            # 2. RSI (14)
            delta = df['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df['rsi'] = 100 - (100 / (1 + rs))
            
            # Ambil data hari terakhir (paling update)
            latest_data = df.iloc[-1]
            prev_data = df.iloc[-2]
            
            latest_price = latest_data['close']
            latest_rsi = latest_data['rsi']
            
            # --- Logika Sinyal Pembelian ---
            # Kriteria Beli: RSI < 35 (Oversold/Murah) ATAU MA20 memotong ke atas MA50 (Golden Cross)
            is_oversold = latest_rsi < 35
            is_golden_cross = (prev_data['ma20'] <= prev_data['ma50']) and (latest_data['ma20'] > latest_data['ma50'])
            
            if is_oversold or is_golden_cross:
                status = "🟢 REKOMENDASI: BELI (BUY)"
                warna = "green"
                alasan = "RSI menunjukkan harga sudah jenuh jual (murah) atau terjadi tren pembalikan arah ke atas (Golden Cross)."
            elif latest_rsi > 70:
                status = "🔴 REKOMENDASI: JUAL (SELL)"
                warna = "red"
                alasan = "RSI sudah di atas 70 (Overbought), harga sudah terlalu mahal dan rawan koreksi turun."
            else:
                status = "🟡 REKOMENDASI: TAHAN (HOLD)"
                warna = "orange"
                alasan = "Harga bergerak stabil. Belum ada momentum kuat untuk beli atau jual."

            # --- Tampilan di HP ---
            st.markdown("---")
            st.subheader("📊 Hasil Analisis Hari Ini")
            
            # Menampilkan Harga terakhir & RSI dengan Box menarik
            col1, col2 = st.columns(2)
            col1.metric(label="Harga Terakhir", value=f"Rp {latest_price:,.0f}")
            col2.metric(label="Nilai RSI", value=f"{latest_rsi:.2f}")
            
            # Tampilan Sinyal Utama
            st.markdown(f"<h3 style='color:{warna}; text-align:center;'>{status}</h3>", unsafe_allow_html=True)
            st.info(f"**Analisis:** {alasan}")
            
            # --- Grafik Interaktif (Bisa di-zoom di HP) ---
            st.subheader("📈 Grafik Tren Harga")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df['date'], y=df['close'], name='Harga Close', line=dict(color='blue', width=2)))
            fig.add_trace(go.Scatter(x=df['date'], y=df['ma20'], name='MA 20 (Tren Pendek)', line=dict(color='orange', dash='dash')))
            fig.add_trace(go.Scatter(x=df['date'], y=df['ma50'], name='MA 50 (Tren Menengah)', line=dict(color='green', dash='dot')))
            
            fig.update_layout(
                margin=dict(l=10, r=10, t=10, b=10),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                xaxis_title="Tanggal",
                yaxis_title="Harga"
            )
            st.plotly_chart(fig, use_container_width=True)
            
    except Exception as e:
        st.error(f"Gagal membaca file. Pastikan format file sesuai. Error: {e}")
