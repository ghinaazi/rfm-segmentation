import streamlit as st
import pandas as pd
import pickle
from datetime import datetime
import plotly.express as px
from streamlit_option_menu import option_menu  # JANGAN LUPA INSTALL INI: pip install streamlit-option-menu

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
        /* Mengatur warna background sidebar */
        [data-testid="stSidebar"] {
            background-color: #EF8505 !important;
        }
        
        /* Background utama */
        [data-testid="stAppViewContainer"] {
            background-color: #FFFFFF !important;
        }

        /* Bagian header (atas) */
        [data-testid="stHeader"] {
            background-color: #323232 !important;
        }
        
        /* Menghilangkan padding default sidebar agar menu lebih rapi */
        [data-testid="stSidebar"] .element-container {
            padding: 0px !important;
            margin: 0px !important;
        }
        
        .sidebar-images img {
            margin-bottom: 20px !important;
            margin-top: 10px !important;
        }
    </style>
""", unsafe_allow_html=True)


# ======================
# SIDEBAR MENU (YANG BARU)
# ======================

with st.sidebar:
    # Menampilkan Logo
    st.markdown('<div class="sidebar-images">', unsafe_allow_html=True)
    st.image("image/alllogo.png", width=250) 
    st.markdown('</div>', unsafe_allow_html=True)
    
    # --- NAVIGASI BARU MENGGUNAKAN OPTION MENU ---
    selected = option_menu(
        menu_title="Main Menu",  # Judul Menu
        options=["Overview", "Dashboard RFM"],  # Pilihan menu
        icons=["house", "bar-chart-fill"],  # Ikon (dari Bootstrap Icons)
        menu_icon="cast",  # Ikon menu utama
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#EF8505"}, # Background container sama dengan sidebar
            "icon": {"color": "white", "font-size": "20px"}, 
            "nav-link": {
                "font-size": "16px", 
                "text-align": "left", 
                "margin": "0px", 
                "color": "white",
                "--hover-color": "#FFC746" # Warna saat di-hover (kuning lebih terang)
            },
            "nav-link-selected": {"background-color": "#323232"}, # Warna saat dipilih (abu gelap sesuai header)
        }
    )

# ======================
# LOAD DATA
# ======================
# Pastikan path file sesuai dengan folder Anda
df = pd.read_excel("dataset/data_with_cluster.xlsx")
df2 = pd.read_csv("dataset/flo_data_20k.csv")

if "first_order_date" in df.columns:
    df["first_order_date"] = pd.to_datetime(df["first_order_date"])


# ============================================================
# ===============  HALAMAN 1 — OVERVIEW  ======================
# ============================================================
if selected == "Overview":  # Menggunakan variabel 'selected' dari option_menu
    st.markdown(
        "<h1 style='text-align: center;'>Customer Segmentation Project</h1>",
        unsafe_allow_html=True
    )

    st.header("📌 Latar Belakang")
    st.write("""
    Perubahan perilaku pasar di era digital menuntut strategi pemasaran yang lebih cerdas dan tepat sasaran. Namun, banyak perusahaan masih menggunakan promosi massal yang kurang relevan dengan karakteristik pelanggan, sehingga menimbulkan inefisiensi biaya dan rendahnya tingkat konversi. Untuk mengatasinya, diperlukan peralihan menuju pengambilan keputusan berbasis data melalui segmentasi pelanggan yang lebih actionable. Metode RFM (Recency, Frequency, Monetary) menjadi solusi efektif karena mampu mengukur nilai pelanggan secara kuantitatif. Dengan dukungan algoritma Machine Learning dan dashboard visualisasi, analisis pelanggan dapat dilakukan lebih cepat dan akurat untuk mendukung strategi personalized marketing.
    """)

    st.header("📂 Dataset")
    st.write("""
    Dataset dalam proyek berisi informasi yang diperoleh dari perilaku belanja pelanggan di masa lalu yang melakukan pembelian terakhirnya melalui OmniChannel (baik belanja online maupun offline).
    """)

    st.subheader("Preview Dataset")
    st.dataframe(df2.head())

    st.subheader("🧾 Metadata Dataset")

    metadata = {
        "Variabel": [
            "master_id", "order_channel", "last_order_channel", "first_order_date",
            "last_order_date", "last_order_date_online", "last_order_date_offline",
            "order_num_total_ever_online", "order_num_total_ever_offline",
            "customer_value_total_ever_offline", "customer_value_total_ever_online",
            "interested_in_categories_12"
        ],
        "Deskripsi": [
            "Unique client number", "Channel belanja yang digunakan", "Channel pembelian terakhir",
            "Tanggal pembelian pertama", "Tanggal pembelian terakhir", "Tanggal pembelian online terakhir",
            "Tanggal pembelian offline terakhir", "Total transaksi online", "Total transaksi offline",
            "Total nilai transaksi offline", "Total nilai transaksi online", "Kategori belanja dalam 12 bulan terakhir"
        ]
    }
    
    metadata_df = pd.DataFrame(metadata)
    st.dataframe(metadata_df, use_container_width=True)
    
    st.info("Klik **Dashboard RFM** di sidebar untuk melihat analisis.")

# ============================================================
# ===============  HALAMAN 2 — DASHBOARD RFM ==================
# ============================================================
elif selected == "Dashboard RFM": # Menggunakan variabel 'selected'

    # ======================
    # TITLE
    # ======================
    st.markdown(
        "<h1 style='text-align: center;'>📊 Customer Segmentation Dashboard</h1>",
        unsafe_allow_html=True
    )

    # ======================
    # LOAD MODELS
    # ======================
    try:
        scaler = pickle.load(open("model/scaler.pkl", "rb"))
        pca = pickle.load(open("model/pca.pkl", "rb"))
        kmeans = pickle.load(open("model/kmeans.pkl", "rb"))
    except FileNotFoundError:
        st.error("Model file not found. Pastikan folder 'model' dan isinya sudah benar.")
        st.stop()

    cluster_reco = {
        0: "Prioritas Marketing",
        1: "Loyal Customers",
        2: "Hibernating",
    }

    # ======================
    # KPI CARDS
    # ======================

    total_customer = df.shape[0]
    total_monetary = df["Monetary"].sum()
    total_frequency = df["Frequency"].sum()

    kpi1, kpi2, kpi3 = st.columns(3)

    with kpi1:
        with st.container(border=True):
            st.metric("Total Customers", total_customer)

    with kpi2:
        with st.container(border=True):
            st.metric("Total Monetary", f"{total_monetary:,.0f}")

    with kpi3:
        with st.container(border=True):
            st.metric("Total Frequency", f"{total_frequency:,}")

    # ======================
    # PIE + BAR
    # ======================
    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.markdown("<h3 style='text-align: center;'>Order Channel Distribution</h3>", unsafe_allow_html=True)
            fig_pie = px.pie(
                df,
                names="order_channel",
                color="order_channel",
                color_discrete_sequence= ["#E05F00", "#FAAD00", "#FFC746", "#FFE169"]
            )
            st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        with st.container(border=True):
            st.markdown("<h3 style='text-align: center;'>Order Count by First Order Date</h3>", unsafe_allow_html=True)
            fig_bar = px.bar(
                df.groupby("first_order_date").size().reset_index(name="count"),
                x="first_order_date",
                y="count",
                color_discrete_sequence=["#323232"]
            )
            st.plotly_chart(fig_bar, use_container_width=True)

    # ======================
    # DISTRIBUSI RFM PER CLUSTER
    # ======================

    st.markdown("<h3 style='text-align: center;'>Distribusi RFM Berdasarkan Cluster</h3>", unsafe_allow_html=True)

    colA, colB, colC = st.columns(3)

    cluster_names = {
        0: "Low Value Inactive Customer",
        1: "High Value Customer",
        2: "Medium Customer"
    }
    
    # Pastikan kolom Cluster ada
    if "Cluster" in df.columns:
        df["Cluster_Name"] = df["Cluster"].map(cluster_names)
    else:
        st.error("Kolom 'Cluster' tidak ditemukan di dataset.")
        st.stop()

    with colA:
        with st.container(border=True):
            fig_r = px.histogram(
                df, x="Recency", color="Cluster_Name",
                title="Recency Distribution",
                color_discrete_sequence= ["#F8A91F", "#EC6426", "#632713"]
            )
            fig_r.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.5, xanchor="center", x=0.5), legend_title_text="", xaxis_title="")
            st.plotly_chart(fig_r, use_container_width=True)

    with colB:
        with st.container(border=True):
            fig_f = px.histogram(
                df, x="Frequency", color="Cluster_Name",
                title="Frequency Distribution",
                color_discrete_sequence=["#F8A91F", "#EC6426", "#632713"]
            )
            fig_f.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.5, xanchor="center", x=0.5), legend_title_text="", xaxis_title="")
            st.plotly_chart(fig_f, use_container_width=True)

    with colC:
        with st.container(border=True):
            fig_m = px.histogram(
                df, x="Monetary", color="Cluster_Name",
                title="Monetary Distribution",
                color_discrete_sequence=["#F8A91F", "#EC6426", "#632713"]
            )
            fig_m.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.5, xanchor="center", x=0.5), legend_title_text="", xaxis_title="")
            st.plotly_chart(fig_m, use_container_width=True)
    
    # ======================
    # CLUSTER DISTRIBUTION + CHANNEL DISTRIBUTION
    # ======================
    
    st.markdown("<h3 style='text-align: center;'>Distribusi Cluster & Order Channel</h3>", unsafe_allow_html=True)

    colA, colB = st.columns(2)

    with colA:
        with st.container(border=True):
            fig_cluster_pie = px.pie(
                df, names="Cluster_Name", title="Proporsi Pelanggan per Cluster",
                color="Cluster_Name",
                color_discrete_sequence= ["#E05F00", "#FAAD00", "#FFC746"]
            )
            st.plotly_chart(fig_cluster_pie, use_container_width=True)

    with colB:
        with st.container(border=True):
            fig_channel = px.bar(
                df.groupby(["Cluster_Name", "order_channel"]).size().reset_index(name="count"),
                x="Cluster_Name", y="count", color="order_channel",
                barmode="group", title="Distribusi Order Channel per Cluster",
                color_discrete_sequence=px.colors.sequential.YlOrRd
            )
            st.plotly_chart(fig_channel, use_container_width=True)

    # ======================
    # FORM PREDIKSI
    # ======================
    
    recommendation_dict = {
        0: "Reaktivasi agresif: promosi besar, 'We miss you', voucher singkat.",
        1: "Retensi jangka panjang: program loyalitas, reward eksklusif, referral.",
        2: "Engagement: reminder berkala, promo ringan, poin tambahan."
    }

    left, right = st.columns(2)

    with left:
        st.markdown("<h3 style='text-align: center;'>Input Nilai RFM</h3>", unsafe_allow_html=True)
        start_date = st.date_input("Tanggal terakhir transaksi")
        end_date = st.date_input("Tanggal analisis", datetime.today())

        if start_date > end_date:
            st.error("❌ Tanggal transaksi tidak boleh > tanggal analisis.")
            recency = None
        else:
            recency = (end_date - start_date).days

        freq = st.number_input("Frequency", min_value=0)
        mon = st.number_input("Monetary", min_value=0)
        btn = st.button("Prediksi Cluster")

    with right:
        st.markdown("<h3 style='text-align: center;'>Hasil Prediksi</h3>", unsafe_allow_html=True)

        if btn and recency is not None:
            # Pastikan urutan fitur sama dengan saat training (Recency, Frequency, Monetary)
            X_scaled = scaler.transform([[recency, freq, mon]])
            X_pca = pca.transform(X_scaled)
            cluster_pred = kmeans.predict(X_pca)[0]

            cluster_name_res = cluster_names[cluster_pred]
            reco_res = recommendation_dict[cluster_pred]

            st.success(f"Cluster: **{cluster_name_res}**")
            st.info(f"Rekomendasi: {reco_res}")
