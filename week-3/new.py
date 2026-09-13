import streamlit as st
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


DATE_COLUMN = 'date/time'
DATA_URL = 'https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz'

'Starting a long computation...'
# Add a placeholder
latest_iteration = st.empty()
bar = st.progress(0)
for i in range(100):
# Update the progress bar with each iteration.
  latest_iteration.text(f'Iteration {i+1}')
  bar.progress(i + 1)
  time.sleep(0.1)
'...and now we\'re done!'
st.balloons()
with st.spinner("Tunggu sebentar..."):
    time.sleep(5)
st.success("Selesai! 🥶")
st.snow()
data = pd.read_csv(DATA_URL, nrows=500)
data
lowercas = lambda x: str(x).lower()
data.rename(lowercas, axis='columns', inplace=True)

data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
data
np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
hist_values
plt.plot(hist_values)
plt.bar(x=[i for i in range(24)], height=hist_values)

st.title("Uber pickups in NYC")
@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Done! (using st.cache)")

if st.checkbox('Show raw data'):
  st.subheader('Raw data')
  st.write(data)

st.subheader('Number of pickups by hour')
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

hour_to_filter = st.slider('hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
hour_to_filter

st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)
  