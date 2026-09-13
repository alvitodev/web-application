import streamlit as st
import pandas as pd

df = pd.DataFrame({
    'nama': ['Deterjen', 'Sampo', 'Sabun', 'Baju', 'Kemeja'],
    'stok': [100, 50, 20, 30, 40]
})

st.write(df)

