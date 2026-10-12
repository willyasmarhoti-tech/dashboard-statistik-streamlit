import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

st.set_page_config(page_title="Dashboard Statistik Deskriptif", page_icon="📊", layout="wide")
st.title("📊 Dashboard Statistik Deskriptif")
st.caption("Data Latihan 1 | Tugas Statistik")

file_data = Path(__file__).parent / "data1.csv"
if not file_data.exists():
    st.error("File data1.csv tidak ditemukan. Pastikan file berada satu folder dengan app.py.")
    st.stop()

try:
    df = pd.read_csv(file_data)
except Exception as e:
    st.error(f"Data tidak dapat dibaca: {e}")
    st.stop()

df = df.apply(pd.to_numeric, errors="coerce")
df = df.dropna(axis=1, how="all")
if df.empty:
    st.error("Data kosong atau tidak memiliki angka yang valid.")
    st.stop()

nilai = df.to_numpy().ravel()
nilai = nilai[~np.isnan(nilai)]
if len(nilai) == 0:
    st.error("Tidak ada nilai numerik untuk dianalisis.")
    st.stop()

rata = np.mean(nilai)
median = np.median(nilai)
std = np.std(nilai, ddof=1) if len(nilai) > 1 else 0
modus = pd.Series(nilai).mode().iloc[0]

st.subheader("Ringkasan Data")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Jumlah Data", f"{len(nilai)}")
c2.metric("Rata-rata", f"{rata:.2f}")
c3.metric("Median", f"{median:.2f}")
c4.metric("Standar Deviasi", f"{std:.2f}")
c5, c6, c7, c8 = st.columns(4)
c5.metric("Modus", f"{modus:g}")
c6.metric("Minimum", f"{np.min(nilai):g}")
c7.metric("Maksimum", f"{np.max(nilai):g}")
c8.metric("Rentang", f"{np.ptp(nilai):g}")

st.divider()
st.subheader("Statistik Deskriptif per Kelompok")
hasil = []
for kolom in df.columns:
    s = df[kolom].dropna()
    if s.empty:
        continue
    hasil.append({
        "Kelompok": kolom.replace("Column", "Kelompok "),
        "Jumlah Data": len(s),
        "Rata-rata": s.mean(),
        "Median": s.median(),
        "Modus": s.mode().iloc[0],
        "Minimum": s.min(),
        "Maksimum": s.max(),
        "Rentang": s.max() - s.min(),
        "Varians": s.var(ddof=1) if len(s) > 1 else 0,
        "Standar Deviasi": s.std(ddof=1) if len(s) > 1 else 0,
    })

tabel = pd.DataFrame(hasil)
st.dataframe(tabel.round(2), use_container_width=True, hide_index=True)
st.download_button("⬇️ Unduh Tabel Statistik (CSV)", data=tabel.to_csv(index=False).encode("utf-8"), file_name="hasil_statistik_deskriptif.csv", mime="text/csv")

st.divider()
st.subheader("Visualisasi Data")
kiri, kanan = st.columns(2)
with kiri:
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(tabel["Kelompok"], tabel["Rata-rata"])
    ax.set_title("Rata-rata Setiap Kelompok")
    ax.set_xlabel("Kelompok")
    ax.set_ylabel("Rata-rata")
    ax.tick_params(axis="x", rotation=45)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
with kanan:
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(tabel["Kelompok"], tabel["Standar Deviasi"])
    ax.set_title("Standar Deviasi Setiap Kelompok")
    ax.set_xlabel("Kelompok")
    ax.set_ylabel("Standar Deviasi")
    ax.tick_params(axis="x", rotation=45)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

st.divider()
st.subheader("💡 Insight dan Kesimpulan")
tertinggi = tabel.loc[tabel["Rata-rata"].idxmax()]
terendah = tabel.loc[tabel["Rata-rata"].idxmin()]
variasi = tabel.loc[tabel["Standar Deviasi"].idxmax()]
st.write(f"**Rata-rata tertinggi:** {tertinggi['Kelompok']} ({tertinggi['Rata-rata']:.2f}).")
st.write(f"**Rata-rata terendah:** {terendah['Kelompok']} ({terendah['Rata-rata']:.2f}).")
st.write(f"**Variasi terbesar:** {variasi['Kelompok']} (standar deviasi {variasi['Standar Deviasi']:.2f}).")
st.info("Standar deviasi yang lebih besar menunjukkan nilai lebih bervariasi, sedangkan standar deviasi lebih kecil menunjukkan nilai lebih seragam. Interpretasi akhir perlu disesuaikan dengan konteks data dari dosen.")
st.caption("Dashboard dibuat menggunakan Python, Pandas, Matplotlib, dan Streamlit.")
