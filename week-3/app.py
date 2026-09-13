import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ====================== CONFIG ======================
st.set_page_config(
    page_title="Anak Krakatau Monitoring",
    page_icon="🌋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ====================== LOAD DATA ======================
@st.cache_data
def load_data():
    df = pd.read_csv("anak_krakatau_seismic.csv")
    df["tanggal"] = pd.to_datetime(df["tanggal"])
    df["datetime"] = df["tanggal"].astype(str) + " " + df["periode"].str.split("-").str[0]
    return df

df = load_data()

# ====================== SIDEBAR ======================
st.sidebar.title("🌋 Anak Krakatau")
st.sidebar.markdown("**Status terkini: Level III (Siaga)**")
st.sidebar.markdown("Radius bahaya: **3 km** dari kawah aktif")
st.sidebar.markdown("---")

# Filter tanggal
min_date = df["tanggal"].min().date()
max_date = df["tanggal"].max().date()
date_range = st.sidebar.date_input(
    "Filter Tanggal",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if len(date_range) == 2:
    start_date, end_date = date_range
    mask = (df["tanggal"].dt.date >= start_date) & (df["tanggal"].dt.date <= end_date)
    filtered = df.loc[mask].copy()
else:
    filtered = df.copy()

st.sidebar.markdown("---")
st.sidebar.info(
    """
    **Sumber data**  
    Sample berdasarkan laporan MAGMA Indonesia / PVMBG  
    (erupsi 4–6 September 2026 + beberapa data sebelumnya)
    
    Untuk data real-time kunjungi:  
    [magma.esdm.go.id](https://magma.esdm.go.id)
    """
)

# ====================== HEADER ======================
st.title("🌋 Dashboard Aktivitas Gunung Anak Krakatau")
st.caption("Latihan Streamlit • Data sample erupsi September 2026")

# ====================== METRICS ======================
col1, col2, col3, col4 = st.columns(4)

total_letusan = int(filtered["gempa_letusan"].sum())
max_amp = filtered["amplitudo_max_mm"].max()
total_hembusan = int(filtered["gempa_hembusan"].sum())
latest_level = filtered.iloc[-1]["level"] if len(filtered) > 0 else "-"

col1.metric("Total Gempa Letusan", f"{total_letusan}")
col2.metric("Amplitudo Maks (mm)", f"{max_amp:.0f}" if pd.notna(max_amp) else "-")
col3.metric("Total Gempa Hembusan", f"{total_hembusan}")
col4.metric("Status Terakhir", latest_level)

st.markdown("---")

# ====================== CHARTS ======================
tab1, tab2, tab3, tab4 = st.tabs(["📈 Time Series", "📊 Perbandingan Tipe Gempa", "🗺️ Lokasi & Radius", "📋 Data Tabel"])

with tab1:
    st.subheader("Jumlah Gempa Letusan & Amplitudo Maksimum")
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=filtered["tanggal"],
        y=filtered["gempa_letusan"],
        name="Gempa Letusan",
        marker_color="#e74c3c",
        opacity=0.8
    ))
    
    fig.add_trace(go.Scatter(
        x=filtered["tanggal"],
        y=filtered["amplitudo_max_mm"],
        name="Amplitudo Max (mm)",
        mode="lines+markers",
        yaxis="y2",
        line=dict(color="#f39c12", width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title="Aktivitas Seismik Anak Krakatau",
        xaxis_title="Tanggal",
        yaxis=dict(title="Jumlah Gempa Letusan", side="left"),
        yaxis2=dict(title="Amplitudo Maksimum (mm)", side="right", overlaying="y"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        height=450,
        template="plotly_white"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Highlight erupsi besar
    st.info("📌 **4–6 September 2026**: Erupsi menerus (lava fountain) tercatat dengan amplitudo hingga 70 mm dan durasi sangat panjang. Erupsi menerus berhenti sekitar 00:04 WIB tanggal 6 September.")

with tab2:
    st.subheader("Distribusi Tipe Gempa")
    
    # Aggregate
    tipe_cols = ["gempa_letusan", "gempa_hembusan", "gempa_low_freq", "gempa_hybrid", "gempa_vulkanik_dangkal"]
    tipe_sum = filtered[tipe_cols].sum().reset_index()
    tipe_sum.columns = ["Tipe Gempa", "Jumlah"]
    tipe_sum["Tipe Gempa"] = tipe_sum["Tipe Gempa"].str.replace("gempa_", "").str.replace("_", " ").str.title()
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        fig_pie = px.pie(
            tipe_sum, 
            values="Jumlah", 
            names="Tipe Gempa",
            color_discrete_sequence=px.colors.sequential.Reds_r,
            hole=0.4
        )
        fig_pie.update_layout(title="Proporsi Tipe Gempa", height=400)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col_b:
        fig_bar = px.bar(
            tipe_sum.sort_values("Jumlah", ascending=True),
            x="Jumlah",
            y="Tipe Gempa",
            orientation="h",
            color="Jumlah",
            color_continuous_scale="Reds"
        )
        fig_bar.update_layout(title="Jumlah per Tipe Gempa", height=400, showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)

with tab3:
    st.subheader("Lokasi Gunung Anak Krakatau")
    
    # Koordinat resmi
    lat, lon = -6.102, 105.423
    
    map_df = pd.DataFrame({
        "lat": [lat],
        "lon": [lon],
        "nama": ["Anak Krakatau"],
        "status": ["Level III (Siaga)"],
        "radius_km": [3]
    })
    
    st.map(map_df, latitude="lat", longitude="lon", size=100, color="#e74c3c", zoom=9)
    
    st.markdown("""
    **Informasi Lokasi**
    - **Koordinat**: 6.102° LS, 105.423° BT  
    - **Lokasi**: Selat Sunda, Kabupaten Lampung Selatan, Provinsi Lampung  
    - **Ketinggian saat ini**: ±157 mdpl  
    - **Radius bahaya (Level III)**: 3 km dari kawah aktif  
    - Masyarakat & wisatawan dilarang mendekati dalam radius tersebut.
    """)
    
    st.warning("⚠️ Data peta di atas hanya menunjukkan titik lokasi. Radius 3 km adalah rekomendasi resmi PVMBG.")

with tab4:
    st.subheader("Data Mentah")
    
    # Format tampilan
    display_df = filtered.copy()
    display_df["tanggal"] = display_df["tanggal"].dt.strftime("%Y-%m-%d")
    display_df = display_df.rename(columns={
        "tanggal": "Tanggal",
        "periode": "Periode",
        "gempa_letusan": "Letusan",
        "amplitudo_max_mm": "Amp Max (mm)",
        "durasi_detik": "Durasi (detik)",
        "gempa_hembusan": "Hembusan",
        "gempa_low_freq": "Low Freq",
        "gempa_hybrid": "Hybrid",
        "gempa_vulkanik_dangkal": "Vulkanik Dangkal",
        "tremor_menerus": "Tremor",
        "amplitudo_tremor_dominan": "Amp Tremor",
        "level": "Level",
        "catatan": "Catatan"
    })
    
    st.dataframe(
        display_df.drop(columns=["datetime"], errors="ignore"),
        use_container_width=True,
        height=400
    )
    
    # Download button
    csv = filtered.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download CSV",
        data=csv,
        file_name="anak_krakatau_filtered.csv",
        mime="text/csv"
    )

# ====================== FOOTER ======================
st.markdown("---")
st.caption(
    "Dashboard latihan Streamlit • Data sample disusun berdasarkan laporan publik MAGMA Indonesia / PVMBG & berita resmi September 2026. "
    "Bukan data resmi real-time. Untuk informasi akurat kunjungi magma.esdm.go.id atau situs Badan Geologi."
)