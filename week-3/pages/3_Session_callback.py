import streamlit as st

st.title("Session State & Callback")

if "counter" not in st.session_state:
    st.session_state.counter = 0

def increment():
    st.session_state.counter += 1

st.button("Tambah", on_click=increment)
st.write(f"Counter: {st.session_state.counter}")