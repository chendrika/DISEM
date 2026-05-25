import os

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Grafik Curah Hujan", page_icon="📈", layout="wide")
st.title("Grafik Curah Hujan")

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "ListPos.202605dec01_ver_20260512.csv")

@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    column_names = [
        "station_id",
        "station_name",
        "pulau",
        "provinsi",
        "kabkota",
        "longitude",
        "latitude",
        "elevasi",
        "curah_hujan",
    ]
    df = pd.read_csv(path, header=None, names=column_names, dtype=str)

    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["elevasi"] = pd.to_numeric(df["elevasi"], errors="coerce")
    df["curah_hujan"] = pd.to_numeric(df["curah_hujan"], errors="coerce")

    df = df.dropna(subset=["longitude", "latitude", "curah_hujan"])
    return df

try:
    df = load_data(DATA_PATH)
except FileNotFoundError:
    st.error(f"File data tidak ditemukan: {DATA_PATH}")
    st.stop()

if df.empty:
    st.warning("Data tidak tersedia atau semua baris invalid setelah pembersihan.")
    st.stop()

with st.expander("Preview data (20 baris pertama)"):
    st.dataframe(df.head(20))

pulau_options = df["pulau"].dropna().unique().tolist()
selected_pulau = st.sidebar.multiselect("Pilih Pulau", options=pulau_options, default=pulau_options)

filtered = df[df["pulau"].isin(selected_pulau)]

st.markdown(f"Menampilkan **{len(filtered)}** stasiun dari total **{len(df)}** stasiun setelah filter.")

if filtered.empty:
    st.info("Tidak ada stasiun yang memenuhi filter. Silakan pilih pulau lain.")
    st.stop()

st.subheader("Rata-rata Curah Hujan per Pulau")
avg_by_pulau = (
    filtered.groupby("pulau", as_index=False)["curah_hujan"].mean().sort_values("curah_hujan", ascending=False)
)
avg_by_pulau["curah_hujan"] = avg_by_pulau["curah_hujan"].round(2)
st.bar_chart(data=avg_by_pulau.set_index("pulau"))

st.subheader("Top 20 Stasiun dengan Curah Hujan Tertinggi")
top20 = filtered.sort_values("curah_hujan", ascending=False).head(20)
st.dataframe(top20[["station_id", "station_name", "pulau", "provinsi", "kabkota", "elevasi", "curah_hujan"]])
st.bar_chart(data=top20.set_index("station_name")["curah_hujan"])

st.subheader("Distribusi Curah Hujan")
bins = pd.cut(filtered["curah_hujan"], bins=10)
histogram = filtered["curah_hujan"].groupby(bins).count().rename("count")
st.bar_chart(histogram)
