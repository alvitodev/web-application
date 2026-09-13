import streamlit as st

st.write("Halo dunia, Halo streamlit!")
st.write("Saya sekarang berada di Sidoagung, Godean")

st.title("Hello Streamlit")
st.header("ini adalah Header st.header()")
st.subheader("ini adalah Subheader st.subheader()")
st.text("ini adalah Text st.text()")
st.caption("ini adalah Caption st.caption()")
st.write("ini adalah Write st.write()")

st.metric(label="Harga pertamax", value=4, delta=-0.5)
st.metric(label="Harga Pertamax turbo", value=7, delta=0.5)
st.metric(label="Jumlah anak kucing", value=123, delta=123, delta_color="off")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Temperature", "25 ℃", "1.2 °C")
col2.metric("Humidity", "60%", "5%")
col3.metric("Pressure", "1013 hPa", "10 hPa")
col4.metric("Wind", "5 km/h", "2 km/h")