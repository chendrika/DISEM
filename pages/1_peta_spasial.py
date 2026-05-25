import os

import folium
import pandas as pd
import streamlit as st
from branca.colormap import linear

from data_loader import load_rainfall_data

st.set_page_config(page_title="Peta Spasial", page_icon="🗺️", layout="wide")
st.title("Peta Spasial Curah Hujan")

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "ListPos.202605dec01_ver_20260512.csv")

@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    return load_rainfall_data(path)

df = pd.DataFrame()

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
min_rain = int(df["curah_hujan"].min())
max_rain = int(df["curah_hujan"].max())
threshold = st.sidebar.slider("Curah hujan minimum (mm)", min_rain, max_rain, min_rain)

filtered = df[(df["pulau"].isin(selected_pulau)) & (df["curah_hujan"] >= threshold)]

st.markdown(
    f"Menampilkan **{len(filtered)}** stasiun dari total **{len(df)}** stasiun setelah filter."
)

if filtered.empty:
    st.info("Tidak ada stasiun yang memenuhi filter. Silakan sesuaikan pilihan pulau atau batas curah hujan.")
    st.stop()

center_lat = float(filtered["latitude"].mean())
center_lon = float(filtered["longitude"].mean())
map_object = folium.Map(location=[center_lat, center_lon], zoom_start=5, tiles="OpenStreetMap")

colormap = getattr(linear, "YlOrRd_09").scale(df["curah_hujan"].min(), df["curah_hujan"].max())
colormap.caption = "Curah Hujan (mm)"
colormap.add_to(map_object)

for _, row in filtered.iterrows():
    popup_html = (
        f"<strong>{row['station_name']}</strong><br>"
        f"Kode: {row['station_id']}<br>"
        f"Pulau: {row['pulau']}<br>"
        f"Provinsi: {row['provinsi']}<br>"
        f"Kab/Kota: {row['kabkota']}<br>"
        f"Elevasi: {row['elevasi']} m<br>"
        f"Curah hujan: {row['curah_hujan']} mm"
    )
    radius = 4 + (row["curah_hujan"] / df["curah_hujan"].max()) * 10
    folium.CircleMarker(
        location=[row["latitude"], row["longitude"]],
        radius=radius,
        color=colormap(row["curah_hujan"]),
        fill=True,
        fill_color=colormap(row["curah_hujan"]),
        fill_opacity=0.7,
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=row["station_name"],
    ).add_to(map_object)

map_html = map_object.get_root().render()
st.iframe(map_html, height=700)
