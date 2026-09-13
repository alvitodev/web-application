import streamlit as st
import pandas as pd
import numpy as np
import time

st.set_page_config(page_title="Earthquake Dashboard", page_icon="🌋", layout="wide")

st.title("🌋 Earthquake Dashboard - USGS Data")
st.markdown("Data gempa bumi 1 bulan terakhir dari USGS (menggantikan Uber pickups)")

DATE_COLUMN = "time"
DATA_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.csv"

@st.cache_data(show_spinner=False)
def load_data(nrows=None):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    # pastikan kolom lat/lon ada
    data = data.rename(columns={"latitude": "lat", "longitude": "lon"})
    return data

# Progress bar saat loading
data_load_state = st.empty()
progress_bar = st.progress(0)

data_load_state.text("Loading data...")
for i in range(100):
    time.sleep(0.01)
    progress_bar.progress(i + 1)

data = load_data()
data_load_state.text("Done! (using st.cache_data)")
progress_bar.empty()

# Checkbox raw data
if st.checkbox("Show raw data"):
    st.subheader("Raw data")
    st.write(data)

# Histogram jumlah gempa per jam
st.subheader("Jumlah gempa per jam (0-23)")
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0, 24))[0]
st.bar_chart(hist_values)

# Filter magnitude dengan slider
min_mag, max_mag = float(data["mag"].min()), float(data["mag"].max())
mag_filter = st.slider("Filter magnitude minimum", min_mag, max_mag, 4.0, 0.1)

filtered = data[data["mag"] >= mag_filter]

st.subheader(f"Peta gempa magnitude ≥ {mag_filter}")
st.map(filtered[["lat", "lon"]])

st.caption(f"Total gempa yang ditampilkan: {len(filtered)}")