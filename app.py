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

    # --- TOP LEVEL METRICS (REVISED: 3 COLUMNS) ---
    # Hitung Total Order Gabungan (Online + Offline)
    total_orders_all = df['order_num_total_ever_online'].sum() + df['order_num_total_ever_offline'].sum()
    
    m1, m2, m3 = st.columns(3) # Menggunakan 3 Kolom
    
    # KPI 1: Total Customers
    with m1:
        st.markdown(f"""
        <div class="premium-card">
            <div class="metric-label">Total Customers</div>
            <div class="metric-value">{df2.shape[0]:,}</div>
        </div>
        """, unsafe_allow_html=True)
        
    # KPI 2: Total Orders (Online + Offline)
    with m2:
        st.markdown(f"""
        <div class="premium-card">
            <div class="metric-label">Total Orders</div>
            <div class="metric-value">{total_orders_all:,}</div>
        </div>
        """, unsafe_allow_html=True)

    # KPI 3: Total Revenue
    with m3:
        st.markdown(f"""
        <div class="premium-card">
            <div class="metric-label">Total Revenue</div>
            <div class="metric-value">₺{df['Monetary'].sum()/1000000:.1f}M</div>
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
                "customer_value_total_ever_online": st.column_config.NumberColumn("Online Spend", format="₺ %.2f"),
                "customer_value_total_ever_offline": st.column_config.NumberColumn("Offline Spend", format="₺ %.2f")
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

    # --- BAGIAN VISUAL OVERVIEW (UPDATED WITH CLEANING & FILTER) ---
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
        if start_date > end_date:
            st.error("Tanggal Mulai tidak boleh lebih besar dari Tanggal Sampai.")
            st.stop()

        mask = (df['first_order_date'].dt.date >= start_date) & (df['first_order_date'].dt.date <= end_date)
        df_filtered = df.loc[mask]
        
        st.divider()

        if df_filtered.empty:
            st.warning("⚠️ Tidak ada data transaksi pada rentang tanggal yang dipilih.")
        else:
            # === ROW 1: GROWTH & CHANNEL PIE ===
            col_viz1, col_viz2 = st.columns(2)
            
            # a. Line Chart Bulanan
            with col_viz1:
                 st.markdown("#### 📈 Pertumbuhan Pelanggan") 
                 
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

            # b. Pie Chart Order Channel
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
            
            st.divider()
            
            # === ROW 2: ORDER VOLUME & REVENUE (COMPARED) ===
            col_viz3, col_viz4 = st.columns(2)
            
            # c. Bar Chart: Volume Order (Online vs Offline)
            with col_viz3:
                st.markdown("#### 📦 Total Volume Transaksi")
                
                total_online = df_filtered['order_num_total_ever_online'].sum()
                total_offline = df_filtered['order_num_total_ever_offline'].sum()
                
                df_vol = pd.DataFrame({
                    'Channel': ['Online Order', 'Offline Order'],
                    'Total Order': [total_online, total_offline]
                })
                
                fig_vol = px.bar(
                    df_vol, x='Total Order', y='Channel', orientation='h',
                    text='Total Order', color='Channel',
                    color_discrete_map={'Online Order': '#EF8505', 'Offline Order': '#323232'}
                )
                fig_vol.update_layout(xaxis_title="Jumlah Transaksi", yaxis_title="", showlegend=False)
                st.plotly_chart(fig_vol, use_container_width=True)
            
            # d. Bar Chart: Revenue (Online vs Offline)
            with col_viz4:
                st.markdown("#### 💰 Total Revenue")
                
                # Agregasi Sum
                rev_online = df_filtered['customer_value_total_ever_online'].sum()
                rev_offline = df_filtered['customer_value_total_ever_offline'].sum()
                
                df_rev = pd.DataFrame({
                    'Source': ['Online Revenue', 'Offline Revenue'],
                    'Revenue': [rev_online, rev_offline]
                })
                
                fig_rev = px.bar(
                    df_rev, x='Revenue', y='Source', orientation='h',
                    text='Revenue', color='Source',
                    color_discrete_map={'Online Revenue': '#EF8505', 'Offline Revenue': '#323232'}
                )
                
                # Format text Lira (₺)
                fig_rev.update_traces(texttemplate='₺%{text:.2s}', textposition='inside')
                
                fig_rev.update_layout(xaxis_title="Total Revenue (₺)", yaxis_title="", showlegend=False)
                st.plotly_chart(fig_rev, use_container_width=True)

            # === ROW 3: CATEGORIES (WITH CLEANING LOGIC) ===
            st.divider()
            st.markdown("#### 🛍️ Top Kategori Peminatan")
            st.caption("Menampilkan kategori produk yang paling sering diminati pada rentang tanggal yang dipilih.")
            
            if 'interested_in_categories_12' in df_filtered.columns:
                # 1. Definisi Fungsi Cleaning
                def clean_list(x):
                    if isinstance(x, str):
                        x = x.strip("[]")
                        return [i.strip().replace("'", "") for i in x.split(",")]
                    return []

                # 2. Proses Cleaning pada Data Terfilter
                df_cat = df_filtered.copy()
                df_cat["categories"] = df_cat["interested_in_categories_12"].apply(clean_list)
                
                # 3. Explode
                df_exploded = df_cat.explode("categories")
                
                # 4. Hitung Frekuensi
                cat_counts = df_exploded["categories"].value_counts().reset_index()
                cat_counts.columns = ['Category', 'Count']
                
                # Ambil Top 5
                cat_counts = cat_counts.head(5).sort_values(by='Count', ascending=True)
                
                fig_bar = px.bar(
                    cat_counts, x='Count', y='Category', orientation='h',
                    text='Count', color='Count',
                    color_continuous_scale=px.colors.sequential.Oranges
                )
                fig_bar.update_layout(xaxis_title="Jumlah Transaksi", yaxis_title="", showlegend=False)
                st.plotly_chart(fig_bar, use_container_width=True)
            else:
                st.warning("⚠️ Kolom kategori tidak ditemukan.")
# ============================================================
# PAGE 2: DASHBOARD RFM
# ============================================================
elif page == "Dashboard RFM":
    st.markdown("<h1 style='text-align: center;'>📊 RFM Deep Dive Analysis</h1>", unsafe_allow_html=True)
    st.write("Analisis mendalam mengenai karakteristik dan perilaku belanja pelanggan antar cluster.")
    st.markdown("---")

    # --- 0. PREP DATA & CLEANING FUNCTION ---
    # Fungsi Cleaning dari User
    def clean_list(x):
        if isinstance(x, str):
            x = x.strip("[]")
            return [i.strip().replace("'", "") for i in x.split(",")] # Hapus tanda petik jika ada
        return []

    # Pastikan kolom Cluster Label tersedia
    if "Cluster" in df.columns:
        df["Cluster Label"] = df["Cluster"].map(cluster_names)
    else:
        st.error("⚠️ Kolom 'Cluster' tidak ditemukan.")
        st.stop()

    # --- 1. FILTER DROPDOWN (BERDASARKAN CLUSTER) ---
    with st.container(border=True):
        st.markdown("### 🔍 Filter Data")
        
        cluster_options = ["Semua Cluster"] + list(df["Cluster Label"].unique())
        selected_cluster = st.selectbox(
            "Pilih Kategori Pelanggan:",
            options=cluster_options,
            index=0
        )
        
        # Logic Filter
        if selected_cluster == "Semua Cluster":
            df_rfm = df.copy() 
        else:
            df_rfm = df[df["Cluster Label"] == selected_cluster] 

    # --- 2. KEY METRICS (KPI) ---
    if df_rfm.empty:
        st.warning("Data tidak ditemukan.")
    else:
        st.markdown(f"### 🚀 Key Metrics: {selected_cluster}")
        
        avg_recency = df_rfm["Recency"].mean()
        avg_freq = df_rfm["Frequency"].mean()
        avg_monetary = df_rfm["Monetary"].mean()

        kpi1, kpi2, kpi3 = st.columns(3)

        with kpi1:
            st.markdown(f"""
            <div class="premium-card">
                <div class="metric-label">Avg. Recency (Hari)</div>
                <div class="metric-value">{avg_recency:.1f}</div>
                <small>Rata-rata hari sejak order terakhir</small>
            </div>
            """, unsafe_allow_html=True)

        with kpi2:
            st.markdown(f"""
            <div class="premium-card">
                <div class="metric-label">Avg. Frequency</div>
                <div class="metric-value">{avg_freq:.1f}x</div>
                <small>Rata-rata frekuensi transaksi</small>
            </div>
            """, unsafe_allow_html=True)

        with kpi3:
            st.markdown(f"""
            <div class="premium-card">
                <div class="metric-label">Avg. Monetary</div>
                <div class="metric-value">₺{avg_monetary:,.0f}</div>
                <small>Rata-rata nilai belanja</small>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # --- 3. 3D & CATEGORY INSIGHTS ---
    # Layout: Kiri (3D Plot), Kanan (Top Categories Bar Chart)
    col_main1, col_main2 = st.columns([1.5, 1])

    with col_main1:
        st.subheader(f"🧊 3D Segmentation")
        st.caption("Sebaran pelanggan berdasarkan Recency, Frequency, Monetary.")
        
        color_map = {
            "Low Value / Inactive": "#808080", 
            "High Value / Loyal": "#EF8505",    
            "Medium / Potential": "#1E90FF"
        }

        fig_3d = px.scatter_3d(
            df_rfm,
            x='Recency',
            y='Frequency',
            z='Monetary',
            color='Cluster Label',
            color_discrete_map=color_map,
            opacity=0.7,
            height=500,
            hover_data=['master_id']
        )
        fig_3d.update_layout(margin=dict(l=0, r=0, b=0, t=0))
        st.plotly_chart(fig_3d, use_container_width=True)

    with col_main2:
        st.subheader("🛍️ Top Kategori")
        st.caption(f"Kategori paling diminati di {selected_cluster}.")
        
        # --- PROSES CLEANING & EXPLODE (Specific Syntax Request) ---
        if "interested_in_categories_12" in df_rfm.columns:
            # 1. Copy data slice agar aman
            df_cat = df_rfm.copy()
            # 2. Apply function cleaning user
            df_cat["categories"] = df_cat["interested_in_categories_12"].apply(clean_list)
            # 3. Explode
            df_exploded = df_cat.explode("categories")
            # 4. Hitung
            cat_counts = df_exploded["categories"].value_counts().reset_index()
            cat_counts.columns = ['Category', 'Count']
            
            # Visualisasi Bar Chart Horizontal
            fig_cat = px.bar(
                cat_counts.head(5).sort_values(by="Count", ascending=True), # Top 10
                x="Count",
                y="Category",
                orientation='h',
                text='Count',
                color='Count',
                color_continuous_scale=px.colors.sequential.Oranges
            )
            fig_cat.update_layout(yaxis_title="", xaxis_title="Jumlah Peminat", showlegend=False)
            st.plotly_chart(fig_cat, use_container_width=True)
        else:
            st.warning("Kolom kategori tidak ditemukan.")

    st.divider()

    # --- 4. GLOBAL CLUSTER STATS (PIE & RFM BAR) ---
    st.subheader("📊 Statistik Global Cluster")
    
    tab_g1, tab_g2, tab_g3 = st.tabs(["Distribusi Cluster (Pie)", "Perbandingan RFM (Bar)", "Channel Preference"])

    # Tab 1: Pie Chart Distribusi Cluster
    with tab_g1:
        st.markdown("#### Proporsi Jumlah Pelanggan")
        df_pie = df['Cluster Label'].value_counts().reset_index()
        df_pie.columns = ['Cluster', 'Count']
        
        fig_pie = px.pie(
            df_pie, 
            names='Cluster', 
            values='Count',
            color='Cluster',
            color_discrete_map=color_map,
            hole=0.4
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # Tab 2: Bar Chart Rata-rata RFM per Cluster
    with tab_g2:
        st.markdown("#### Perbandingan Rata-rata RFM")
        
        # Grouping Data Global
        df_grouped = df.groupby("Cluster Label")[["Recency", "Frequency", "Monetary"]].mean().reset_index()

        c_rfm1, c_rfm2 = st.columns(2)
        
        with c_rfm1:
            fig_bar_rf = px.bar(
                df_grouped,
                x="Cluster Label",
                y=["Recency", "Frequency"],
                barmode="group",
                color_discrete_sequence=["#323232", "#EF8505"],
                text_auto='.1f',
                title="Recency & Frequency"
            )
            st.plotly_chart(fig_bar_rf, use_container_width=True)
            
        with c_rfm2:
            fig_bar_m = px.bar(
                df_grouped,
                x="Cluster Label",
                y="Monetary",
                text="Monetary",
                color="Cluster Label",
                color_discrete_map=color_map,
                title="Monetary Value"
            )
            fig_bar_m.update_traces(texttemplate='₺%{text:.2s}', textposition='outside')
            st.plotly_chart(fig_bar_m, use_container_width=True)

    # Tab 3: Channel Distribution (Stacked Bar - Dari Request Sebelumnya)
    with tab_g3:
        st.markdown("#### Preferensi Channel per Cluster")
        if 'order_channel' in df.columns:
            df_channel = df.groupby(['Cluster Label', 'order_channel']).size().reset_index(name='Count')
            df_channel['Percentage'] = df_channel.groupby('Cluster Label')['Count'].transform(lambda x: x / x.sum() * 100)
            
            fig_stack = px.bar(
                df_channel,
                y="Cluster Label",
                x="Percentage",
                color="order_channel",
                orientation='h',
                text=df_channel['Percentage'].apply(lambda x: '{0:1.1f}%'.format(x)),
                color_discrete_sequence=px.colors.sequential.Oranges_r
            )
            fig_stack.update_layout(barmode='stack', xaxis=dict(range=[0, 100]))
            st.plotly_chart(fig_stack, use_container_width=True)

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
