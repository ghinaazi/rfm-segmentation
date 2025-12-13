import streamlit as st
import pandas as pd
import pickle
from datetime import datetime
import plotly.express as px

# ======================
# CONFIG PAGE
# ======================
st.set_page_config(
    page_title="Customer Segmentation App",
    page_icon="📊",
    layout="wide"
)

# ======================
# SIDEBAR COLOR & STYLE
# ======================
st.markdown("""
    <style>
        /* Mengubah warna background sidebar */
        [data-testid="stSidebar"] {
            background-color: #EF8505 !important;
        }

        /* Mengubah warna background utama */
        [data-testid="stAppViewContainer"] {
            background-color: #FFFFFF !important;
        }

        /* Mengubah warna header atas */
        [data-testid="stHeader"] {
            background-color: #323232 !important;
        }

        /* Menghilangkan padding agar layout lebih rapat */
        [data-testid="stSidebar"] .element-container {
            padding: 0px !important;
            margin: 0px !important;
        }

        /* Mengatur margin gambar di sidebar */
        .sidebar-images img {
            margin-bottom: 0px !important;
            margin-top: 0px !important;
        }
        
        /* Styling khusus untuk kotak hasil prediksi */
        .prediction-box {
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
            border-left: 5px solid #EF8505;
            margin-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)


# ======================
# SIDEBAR MENU (3 OPSI)
# ======================
with st.sidebar:
    st.markdown('<div class="sidebar-images">', unsafe_allow_html=True)
    # Pastikan file gambar ada di folder image
    st.image("image/alllogo.png", width=250)
    st.markdown('</div>', unsafe_allow_html=True)

st.sidebar.title("📘 Navigation")

# --- NAVIGASI BARU: 3 OPSI ---
page = st.sidebar.radio(
    "Pilih Halaman",
    ["Overview", "Dashboard RFM", "Prediksi & Insight"],
    index=0
)
# -----------------------------

# ======================
# LOAD DATA & MODELS
# ======================
# Load Dataset
try:
    df = pd.read_excel("dataset/data_with_cluster.xlsx")
    df2 = pd.read_csv("dataset/flo_data_20k.csv")
    if "first_order_date" in df.columns:
        df["first_order_date"] = pd.to_datetime(df["first_order_date"])
except FileNotFoundError:
    st.error("File dataset tidak ditemukan. Cek folder 'dataset'.")
    st.stop()

# Load Models
try:
    scaler = pickle.load(open("model/scaler.pkl", "rb"))
    pca = pickle.load(open("model/pca.pkl", "rb"))
    kmeans = pickle.load(open("model/kmeans.pkl", "rb"))
except FileNotFoundError:
    st.error("File model tidak ditemukan. Cek folder 'model'.")
    st.stop()

# Definisi Cluster & Rekomendasi
cluster_names = {
    0: "Low Value / Inactive",
    1: "High Value / Loyal",
    2: "Medium / Potential"
}

recommendation_text = {
    0: "🔍 **Strategi: Reaktivasi.** Pelanggan ini sudah lama tidak transaksi. Kirimkan pesan 'We Miss You' dengan voucher diskon besar yang memiliki masa berlaku singkat (urged action). Lakukan survei kepuasan pelanggan.",
    1: "💎 **Strategi: Retensi VIP.** Ini adalah aset berharga. Berikan akses eksklusif ke produk baru, reward poin ganda, atau layanan prioritas. Ajak masuk ke program referral.",
    2: "📈 **Strategi: Nurturing.** Pelanggan ini aktif tapi belum maksimal. Tawarkan paket bundling atau rekomendasi produk pelengkap (cross-selling) untuk meningkatkan nilai belanja mereka."
}


# ============================================================
# ===============  HALAMAN 1 — OVERVIEW  ======================
# ============================================================
if page == "Overview":
    st.markdown(
        "<h1 style='text-align: center;'>Customer Segmentation Project</h1>",
        unsafe_allow_html=True
    )

    st.header("📌 Latar Belakang")
    st.write("""
    Perubahan perilaku pasar di era digital menuntut strategi pemasaran yang lebih cerdas dan tepat sasaran. Aplikasi ini membantu perusahaan beralih dari promosi massal ke **Personalized Marketing** berbasis data menggunakan metode RFM (Recency, Frequency, Monetary) dan Machine Learning.
    """)

    st.header("📂 Dataset")
    st.write("Dataset ini mencakup perilaku belanja pelanggan OmniChannel (Online & Offline).")

    st.subheader("Preview Dataset")
    st.dataframe(df2.head())

    st.subheader("🧾 Metadata Variabel")
    metadata = {
        "Variabel": ["Recency", "Frequency", "Monetary"],
        "Deskripsi": [
            "Jumlah hari sejak pembelian terakhir (Semakin kecil semakin baik)",
            "Total jumlah transaksi yang dilakukan (Semakin besar semakin baik)",
            "Total uang yang dihabiskan pelanggan (Semakin besar semakin baik)"
        ]
    }
    st.table(pd.DataFrame(metadata))


# ============================================================
# ===============  HALAMAN 2 — DASHBOARD RFM ==================
# ============================================================
elif page == "Dashboard RFM":

    st.markdown(
        "<h1 style='text-align: center;'>📊 Executive Dashboard</h1>",
        unsafe_allow_html=True
    )
    st.markdown("---")

    # --- KPI CARDS ---
    total_customer = df.shape[0]
    total_monetary = df["Monetary"].sum()
    avg_trans = df["Frequency"].mean()

    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Total Customers", f"{total_customer:,}", "Active")
    kpi2.metric("Total Revenue", f"Rp {total_monetary:,.0f}", "+5% vs last month")
    kpi3.metric("Avg Transaction", f"{avg_trans:.1f}x", "per User")

    st.markdown("---")

    # --- ROW 1: CHARTS ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Distribusi Channel Belanja")
        fig_pie = px.pie(
            df, names="order_channel",
            color="order_channel",
            color_discrete_sequence= ["#E05F00", "#FAAD00", "#FFC746", "#FFE169"]
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        st.subheader("Jumlah Order per Tanggal")
        fig_bar = px.bar(
            df.groupby("first_order_date").size().reset_index(name="count"),
            x="first_order_date", y="count",
            color_discrete_sequence=["#323232"]
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # --- ROW 2: CLUSTER INSIGHT ---
    st.subheader("Distribusi Cluster Pelanggan")
    
    # Pastikan nama cluster ter-update
    if "Cluster" in df.columns:
        df["Cluster_Name"] = df["Cluster"].map(cluster_names)

    colA, colB = st.columns([1, 2])
    
    with colA:
        # Pie Chart Cluster
        fig_c_pie = px.pie(
            df, names="Cluster_Name",
            color="Cluster_Name",
            hole=0.4,
            color_discrete_sequence= ["#F8A91F", "#EC6426", "#632713"]
        )
        st.plotly_chart(fig_c_pie, use_container_width=True)

    with colB:
        # Bar Chart Channel per Cluster
        fig_channel = px.bar(
            df.groupby(["Cluster_Name", "order_channel"]).size().reset_index(name="count"),
            x="Cluster_Name", y="count", color="order_channel",
            barmode="group",
            title="Preferensi Channel per Cluster",
            color_discrete_sequence=px.colors.sequential.YlOrRd
        )
        st.plotly_chart(fig_channel, use_container_width=True)


# ============================================================
# ===============  HALAMAN 3 — PREDIKSI & INSIGHT ===========
# ============================================================
elif page == "Prediksi & Insight":

    st.markdown(
        "<h1 style='text-align: center;'>🤖 Customer Predictor</h1>",
        unsafe_allow_html=True
    )
    st.write("Masukkan data pelanggan terbaru untuk mengetahui segmen dan strategi yang tepat.")
    st.markdown("---")

    # Membagi layout menjadi 2 kolom: Input (Kiri) & Hasil (Kanan)
    col_input, col_result = st.columns([1, 1.5], gap="large")

    with col_input:
        st.subheader("📝 Input Data Pelanggan")
        with st.container(border=True):
            # Input Tanggal
            start_date = st.date_input("Tanggal Terakhir Transaksi")
            end_date = st.date_input("Tanggal Analisis (Hari ini)", datetime.today())

            # Hitung Recency otomatis
            if start_date > end_date:
                st.error("⚠️ Tanggal transaksi tidak boleh lebih dari hari ini.")
                recency = None
            else:
                recency = (end_date - start_date).days
                st.caption(f"**Recency (Hari sejak transaksi terakhir): {recency} hari**")

            # Input Frequency & Monetary
            freq = st.number_input("Frequency (Total Transaksi)", min_value=1, value=5)
            mon = st.number_input("Monetary (Total Belanja)", min_value=0, value=1000000, step=50000)

            predict_btn = st.button("🔍 Analisis Pelanggan", type="primary")

    with col_result:
        st.subheader("💡 Hasil Analisis & Insight")
        
        if predict_btn and recency is not None:
            # 1. Preprocessing & Prediksi
            X_input = [[recency, freq, mon]]
            X_scaled = scaler.transform(X_input)
            X_pca = pca.transform(X_scaled)
            cluster_pred = kmeans.predict(X_pca)[0]

            # 2. Ambil Label & Rekomendasi
            res_name = cluster_names[cluster_pred]
            res_desc = recommendation_text[cluster_pred]

            # 3. Tampilkan Hasil dengan Style Kartu
            st.markdown(f"""
            <div class="prediction-box">
                <h2 style="color: #323232; margin-top: 0;">Segmen: {res_name}</h2>
                <hr>
                <p style="font-size: 16px;">{res_desc}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # 4. Detail Data
            st.markdown("")
            with st.expander("Lihat Detail Data Input"):
                st.json({
                    "Recency (Hari)": recency,
                    "Frequency (Kali)": freq,
                    "Monetary (IDR)": mon
                })

        else:
            # Tampilan default sebelum tombol ditekan
            st.info("👈 Silakan masukkan data di panel kiri dan klik tombol 'Analisis Pelanggan'.")
            st.image("https://cdn-icons-png.flaticon.com/512/1087/1087815.png", width=100)
