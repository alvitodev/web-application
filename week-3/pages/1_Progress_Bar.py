import streamlit as st
import time

st.title("Progress Bar & Status Widget")

st.write("Simulasi long-running computation")

latest = st.empty()
bar = st.progress(0)

for i in range(100):
    latest.text(f"Iteration {i+1}")
    bar.progress(i + 1)
    time.sleep(0.05)

st.success("Selesai!")
st.balloons()