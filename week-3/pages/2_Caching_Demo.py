import streamlit as st
import time

@st.cache_data
def slow_function(x):
    time.sleep(2)
    return x * 2

st.title("Caching Demo")
num = st.number_input("Masukkan angka", 1, 100, 5)
st.write(f"Hasil (cached): {slow_function(num)}")