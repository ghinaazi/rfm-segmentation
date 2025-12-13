import streamlit as st
import pandas as pd
import pickle
from datetime import datetime
import plotly.express as px

# ======================
# 1. CONFIG PAGE
# ======================
st.set_page_config(
    page_title="Customer Segmentation Pro",
    page_icon="💎",
    layout="wide"
)

# ======================
# 2. PREMIUM CSS STYLING
# ======================
st.markdown("""
    <style>
        /* --- Sidebar Style --- */
        [data-testid="stSidebar"] {
            background-color: #EF8505 !important;
        }
        [data-testid="stSidebar"] * {
            color: white !important;
        }
        
        /* --- Header Style --- */
        [data-testid="stHeader"] {
            background-color: #323232 !important;
        }

        /* --- Main Background --- */
        .stApp {
            background-color: #FAFAFA;
        }

        /* --- Custom Cards (Kotak Mewah) --- */
        .premium-card {
            background-color: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            border-left: 5px solid #EF8505;
            margin-bottom: 20px;
        }
        
        .metric-label {
            font-size: 14px;
            color: #666;
            font-weight: 500;
        }
        
        .metric-value {
            font-size: 26px;
            color: #323232;
            font-weight: bold;
        }

        /* --- Navigation Clean Up --- */
        [data-testid="stSidebar"] .element-container {
            padding: 0px !important;
            margin: 0px !important;
        }
    </style>
""", unsafe_allow_html=True)


# ======================
# 3. SIDEBAR NAVIGATION
# ======================
with st.sidebar:
    st.markdown('<div style="margin-bottom: 20px;">', unsafe_allow_html=True)
    # Pastikan file alllogo.png ada di folder image/
    try:
        st.image("image/alllogo.png", width=220) 
    except:
        st.caption("Logo not found")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("### 🧭 Main Menu")
    
    # Navigasi menggunakan Radio Button (Terpisah & Jelas)
    page = st.sidebar.radio(
        "",
        ["Executive Overview", "Dashboard RFM", "Prediksi & Insight"],
        index=0
    )
    
    st.markdown("---")
    st.caption("© 2025 Data Science Team\nCustomer Intelligence System")

# ======================
# 4. LOAD DATA & MODELS
# ======================
try:
    df = pd.read_excel("dataset/data_with_cluster.xlsx")
    df2 = pd.read_csv("dataset/flo_data_20k.csv")
    if "first_order_date" in df.columns:
        df["first_order_date"] = pd.to_datetime(df["first_order_date"])
except Exception as e:
    st.error(f"Terjadi kesalahan saat memuat data: {e}")
    st.warning("Pastikan file 'data_with_cluster.xlsx' dan 'flo_data_20k.csv' ada di dalam folder 'dataset' di GitHub Anda.")
    st.stop()

# Load Models
try:
    scaler = pickle.load(open("model/scaler.pkl", "rb"))
    pca = pickle.load(open("model/pca.pkl", "rb"))
    kmeans = pickle.load(open("model/kmeans.pkl", "rb"))
except Exception:
    st.warning("⚠️ Model (scaler.pkl, pca.pkl, kmeans.pkl) belum ditemukan di folder 'model'. Fitur prediksi tidak akan berjalan.")

# Mapping Nama Cluster
cluster_names = {
    0: "Low Value / Inactive",
    1: "High Value / Loyal",
    2: "Medium / Potential"
}
recommendation_text = {
    0: "🔍 *Reaktivasi:* Kirim voucher 'We Miss You', diskon urgensi tinggi.",
    1: "💎 *Retensi VIP:* Reward eksklusif, early access, layanan prioritas.",
    2: "📈 *Upselling:* Tawarkan bundling produk, program poin loyalty."
}


# ============================================================
# PAGE 1: EXECUTIVE OVERVIEW 
# ============================================================
if page == "Executive Overview":
    
    # --- HERO SECTION ---
    st.title("💎 Customer Intelligence Hub")
    st.markdown("### Transformation from Mass Marketing to Personalized Strategy")
    st.write("Selamat datang di panel analitik pelanggan. Platform ini menggunakan *Machine Learning* untuk mengelompokkan pelanggan berdasarkan perilaku belanja mereka (RFM Analysis).")
    
    st.markdown("---")

    # --- TOP LEVEL METRICS ---
    m1, m2, m3, m4 = st.columns(4)
    
    with m1:
        st.markdown(f"""
        <div class="premium-card">
            <div class="metric-label">Total Data Points</div>
            <div class="metric-value">{df2.shape[0]:,}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with m2:
        st.markdown(f"""
        <div class="premium-card">
            <div class="metric-label">Online Orders</div>
            <div class="metric-value">{df['order_num_total_ever_online'].sum():,}</div>
        </div>
        """, unsafe_allow_html=True)

    with m3:
        st.markdown(f"""
        <div class="premium-card">
            <div class="metric-label">Offline Orders</div>
            <div class="metric-value">{df['order_num_total_ever_offline'].sum():,}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with m4:
        st.markdown(f"""
        <div class="premium-card">
            <div class="metric-label">Total Revenue</div>
            <div class="metric-value">£{df['Monetary'].sum()/1000000:.1f}M</div>
        </div>
        """, unsafe_allow_html=True)

    # --- TABS FOR ORGANIZED CONTENT ---
    tab1, tab2, tab3 = st.tabs(["🎯 Business Objectives", "📂 Dataset Explorer", "📈 Visual Overview"])

    with tab1:
        st.subheader("Mengapa Segmentasi Itu Penting?")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.info("**1. Efisiensi Biaya**\n\nHentikan promosi massal yang mahal. Fokuskan budget hanya pada pelanggan yang berpotensi tinggi.")
        with c2:
            st.warning("**2. Personalisasi**\n\nPelanggan loyal butuh *reward*, pelanggan pasif butuh diskon. Berikan apa yang mereka butuhkan.")
        with c3:
            st.success("**3. Tingkatkan ROI**\n\nStrategi yang tepat sasaran terbukti meningkatkan konversi penjualan hingga 2-3x lipat.")
            
        st.markdown("#### 🔑 The RFM Concept")
        try:
            st.image("image/rfmanalysisdiagram.png", caption="Recency, Frequency, Monetary Model Concept", width=600)
        except Exception:
             st.warning("Gambar 'rfmanalysisdiagram.png' tidak ditemukan. Cek folder image.")

    with tab2:
        st.subheader("Data Source Overview")
        st.markdown("Dataset ini menggabungkan perilaku transaksi dari *OmniChannel* (Aplikasi, Website, dan Toko Fisik).")
        
        # Interactive DataFrame
        st.dataframe(
            df2.head(10),
            use_container_width=True,
            column_config={
                "master_id": "Customer ID",
                "first_order_date": st.column_config.DateColumn("First Join"),
                "customer_value_total_ever_online": st.column_config.NumberColumn("Online Spend", format="£ %.2f"),
                "customer_value_total_ever_offline": st.column_config.NumberColumn("Offline Spend", format="£ %.2f")
            }
        )
        
        with st.expander("Lihat Metadata Lengkap (Kamus Data)"):
             metadata = {
                "Variabel": [
                    "master_id",
                    "order_channel",
                    "last_order_channel",
                    "first_order_date",
                    "last_order_date",
                    "last_order_date_online",
                    "last_order_date_offline",
                    "order_num_total_ever_online",
                    "order_num_total_ever_offline",
                    "customer_value_total_ever_offline",
                    "customer_value_total_ever_online",
                    "interested_in_categories_12"
                ],
                "Deskripsi": [
                    "Unique client number",
                    "Channel belanja yang digunakan",
                    "Channel pembelian terakhir",
                    "Tanggal pembelian pertama",
                    "Tanggal pembelian terakhir",
                    "Tanggal pembelian online terakhir",
                    "Tanggal pembelian offline terakhir",
                    "Total transaksi online",
                    "Total transaksi offline",
                    "Total nilai transaksi offline",
                    "Total nilai transaksi online",
                    "Kategori belanja dalam 12 bulan terakhir"
                ]
            }
             st.table(pd.DataFrame(metadata))

    # --- BAGIAN VISUAL OVERVIEW (UPDATED) ---
    with tab3:
        st.subheader("Visualisasi Data Utama")
        
        # 1. PENGATUR TANGGAL (DATE FILTER)
        st.markdown("##### 🗓️ Filter Periode Data")
        
        # Ambil min dan max tanggal dari data untuk default value
        min_date_available = df['first_order_date'].min().date()
        max_date_available = df['first_order_date'].max().date()
        
        col_filter1, col_filter2 = st.columns(2)
        
        with col_filter1:
            start_date = st.date_input(
                "Mulai Tanggal", 
                value=min_date_available, 
                min_value=min_date_available, 
                max_value=max_date_available
            )
        
        with col_filter2:
            end_date = st.date_input(
                "Sampai Tanggal", 
                value=max_date_available, 
                min_value=min_date_available, 
                max_value=max_date_available
            )
            
        # 2. FILTER DATA BERDASARKAN TANGGAL
        # Mengubah kolom 'first_order_date' menjadi date object untuk perbandingan
        mask = (df['first_order_date'].dt.date >= start_date) & (df['first_order_date'].dt.date <= end_date)
        df_filtered = df.loc[mask]
        
        st.divider()

        if df_filtered.empty:
            st.warning("⚠️ Tidak ada data transaksi pada rentang tanggal yang dipilih.")
        else:
            col_viz1, col_viz2 = st.columns(2)
            
            # a. Line Chart Bulanan (Menggunakan df_filtered)
            with col_viz1:
                 # [REQUEST] Judul diubah
                 st.markdown("#### 📈 Pertumbuhan Pelanggan") 
                 
                 # Resample Data Filtered
                 df_trend = df_filtered.copy()
                 if 'first_order_date' in df_trend.columns:
                     df_trend = df_trend.set_index('first_order_date')
                     monthly_counts = df_trend.resample('MS').size().reset_index(name='count')
                     
                     fig_line = px.line(
                        monthly_counts,
                        x='first_order_date',
                        y='count',
                        markers=True,
                        labels={'first_order_date': 'Bulan', 'count': 'Jumlah Pelanggan Baru'},
                        color_discrete_sequence=["#EF8505"]
                     )
                     
                     fig_line.update_layout(
                         title_text="",
                         margin=dict(t=20),
                         xaxis_title="Periode",
                         yaxis_title="Total Customer"
                     )
                     
                     st.plotly_chart(fig_line, use_container_width=True)
                 else:
                     st.error("Kolom 'first_order_date' tidak ditemukan.")

            # b. Pie Chart Order Channel (Menggunakan df_filtered)
            with col_viz2:
                 st.markdown("#### 🥧 Distribusi Channel")
                 fig_pie = px.pie(
                    df_filtered, 
                    names='order_channel', 
                    color='order_channel', 
                    color_discrete_sequence=px.colors.sequential.Oranges_r, 
                    hole=0.4
                 )
                 st.plotly_chart(fig_pie, use_container_width=True)


# ============================================================
# PAGE 2: DASHBOARD RFM
# ============================================================
elif page == "Dashboard RFM":
    st.markdown("<h1 style='text-align: center;'>📊 Performance Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("---")

    # --- KPI SUMMARY ---
    total_cust = df.shape[0]
    avg_monetary = df["Monetary"].mean()
    
    k1, k2, k3 = st.columns(3)
    k1.metric("Active Customers", f"{total_cust:,}", "User Base")
    k2.metric("Average Spending", f"£ {avg_monetary:,.0f}", "per User")
    k3.metric("Clustering Confidence", "Silhouette 0.65", "High Quality")

    st.markdown("---")

    # --- VISUALIZATION ROW 1 ---
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Channel Preference")
        fig = px.pie(df, names='order_channel', color='order_channel', 
                     color_discrete_sequence=px.colors.sequential.Oranges_r, hole=0.4)
        st.plotly_chart(fig, use_container_width=True)
    
    with c2:
        st.subheader("Transaction Volume Timeline")
        daily_counts = df.groupby('first_order_date').size().reset_index(name='counts')
        fig = px.area(daily_counts, x='first_order_date', y='counts', 
                      color_discrete_sequence=['#EF8505'])
        st.plotly_chart(fig, use_container_width=True)

    # --- VISUALIZATION ROW 2 (CLUSTERS) ---
    st.subheader("🔎 Deep Dive: Customer Clusters")
    if "Cluster" in df.columns:
        df["Cluster_Name"] = df["Cluster"].map(cluster_names)
        
        col_cl1, col_cl2 = st.columns([2, 1])
        with col_cl1:
             fig = px.bar(df.groupby("Cluster_Name").mean(numeric_only=True).reset_index(), 
                          x="Cluster_Name", y=["Recency", "Frequency"], barmode="group",
                          color_discrete_sequence=["#323232", "#EF8505"])
             st.plotly_chart(fig, use_container_width=True)
             
        with col_cl2:
            st.markdown("#### Insight:")
            st.markdown("""
            - **Loyal:** Frequency tinggi, Recency rendah.
            - **Inactive:** Recency sangat tinggi (sudah lama tidak belanja).
            - **Potential:** Perlu didorong agar frekuensi naik.
            """)


# ============================================================
# PAGE 3: PREDIKSI & INSIGHT (ACTIONABLE)
# ============================================================
elif page == "Prediksi & Insight":
    st.markdown("<h1 style='text-align: center;'>🤖 AI Predictor</h1>", unsafe_allow_html=True)
    st.write("Simulasi pelanggan baru untuk menentukan strategi marketing yang tepat secara Real-Time.")
    
    col_input, col_res = st.columns([1, 1.5], gap="large")
    
    with col_input:
        with st.container(border=True):
            st.subheader("Input Data")
            start_date = st.date_input("Tanggal Transaksi Terakhir")
            end_date = st.date_input("Tanggal Hari Ini", datetime.today())
            
            recency = (end_date - start_date).days
            if recency < 0: st.error("Tanggal tidak valid")
            
            freq = st.number_input("Frequency (Total Transaksi)", 1, 100, 5)
            mon = st.number_input("Monetary (Total Belanja)", 0, 100000000, 500000)
            
            st.write("")
            run_btn = st.button("Analisis Sekarang", type="primary", use_container_width=True)

    with col_res:
        if run_btn:
            # Prediksi
            try:
                X = [[recency, freq, mon]]
                X_scaled = scaler.transform(X)
                X_pca = pca.transform(X_scaled)
                pred = kmeans.predict(X_pca)[0]
                
                label = cluster_names[pred]
                desc = recommendation_text[pred]
                
                # Tampilan Hasil Mahal (HTML Injection)
                st.markdown(f"""
                <div class="premium-card" style="border-left: 10px solid #EF8505;">
                    <h3 style="margin:0; color:#EF8505;">Hasil Analisis AI</h3>
                    <h1 style="font-size: 40px; margin: 10px 0;">{label}</h1>
                    <hr>
                    <p style="font-size:18px;">{desc}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Show Metrics Recency calculated
                c_a, c_b = st.columns(2)
                c_a.metric("Recency (Hari)", f"{recency} Hari")
                # Logic sederhana untuk menentukan potential value
                mean_monetary = df['Monetary'].mean() if not df.empty else 0
                c_b.metric("Potential Value", "High" if mon > mean_monetary else "Standard")
            except Exception as e:
                st.error(f"Terjadi kesalahan saat prediksi: {e}. Cek apakah model sudah dimuat dengan benar.")
            
        else:
            st.info("👈 Masukkan data di panel kiri untuk melihat hasil prediksi.")
            try:
                st.image("image/alllogo.png", width=100) # Placeholder image
            except:
                pass
