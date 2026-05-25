import streamlit as st

st.set_page_config(page_title="Peta Spasial Curah Hujan", page_icon="🌧️", layout="wide")

st.title("Beranda - Peta Spasial Curah Hujan")

st.markdown(
    """
    Aplikasi ini menampilkan peta interaktif curah hujan berdasarkan data stasiun hujan.
    Gunakan halaman **Peta Spasial** untuk melihat titik stasiun dan nilai curah hujan,
    lalu buka halaman **Grafik Curah Hujan** untuk melihat analisis grafik.
    """
)

st.markdown("#### Petunjuk penggunaan")
st.write("1. Pastikan file data berada di `data/ListPos.202605dec01_ver_20260512.csv`.")
st.write("2. Buka halaman `Peta Spasial` dari sidebar Streamlit.")
st.write("3. Gunakan filter di sidebar untuk memilih pulau dan batas minimum curah hujan.")

st.info("Jalankan aplikasi dengan: `streamlit run beranda.py`")

