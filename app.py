import streamlit as st
import pandas as pd
import pickle
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go # Ditambahkan untuk kustomisasi lebih detail
import streamlit as st
from PIL import Image  # Tambahkan library PIL untuk loading gambar lebih aman

# ======================
# 1. CONFIG PAGE
# ======================
import streamlit as st
from PIL import Image # Kita butuh bantuan "PIL" buat baca gambar

# ======================
# 1. LOAD GAMBAR & CONFIG (Wajib Paling Atas)
# ======================
try:
    img = Image.open("flo.png")
except:
    img = "💎" # Kalau flo.png gak ketemu, otomatis balik ke diamond biar gak error

st.set_page_config(
    page_title="Customer Segmentation Pro",
    page_icon=img,  # Masukkan variabel gambar di sini
    layout="wide"
)

# ... baru lanjut kode tema warna di bawah sini ...
THEME_ORANGE = "#EF8505"
# Warna Tema Utama (Dark Orange)
THEME_ORANGE = "#EF8505"
THEME_ORANGE_LIGHT = "#FF9F43"
THEME_DARK_TEXT = "#2C3E50"
THEME_GRAY_TEXT = "#7F8C8D"

# ======================
# 2. PREMIUM CSS STYLING (VISUAL ENHANCEMENT)
# ======================
st.markdown(f"""
    <style>
        /* --- Global Font & Background --- */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

        html, body, [class*="css"] {{
            font-family: 'Inter', sans-serif;
        }}

        .stApp {{
            background-color: #F8F9FA; /* Latar belakang sedikit lebih cerah dan bersih */
        }}

        /* --- Sidebar Style --- */
        [data-testid="stSidebar"] {{
            background-color: {THEME_ORANGE} !important;
            background-image: linear-gradient(180deg, {THEME_ORANGE} 0%, #d35400 100%); /* Tambah gradien halus agar tidak flat */
        }}
        [data-testid="stSidebar"] * {{
            color: white !important;
        }}
        /* Mempercantik radio button di sidebar */
        .stRadio > div[role="radiogroup"] > label > div:first-child {{
            background-color: rgba(255, 255, 255, 0.2);
            border-color: rgba(255, 255, 255, 0.5);
        }}


        /* --- Header Style --- */
        [data-testid="stHeader"] {{
            background-color: #FFFFFF !important; /* Header putih agar bersih */
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.05); /* Shadow halus di bawah header */
        }}

        /* --- Custom Cards (Kotak Mewah v2.0 - Lebih Dalam & Menonjol) --- */
        .premium-card {{
            background-color: white;
            padding: 25px 20px;
            border-radius: 15px;
            /* Shadow ganda untuk efek melayang (floating effect) */
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.05);
            border-left: 6px solid {THEME_ORANGE};
            margin-bottom: 25px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}

        .premium-card:hover {{
             transform: translateY(-3px); /* Efek naik sedikit saat di-hover */
             box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        }}

        .metric-label {{
            font-size: 15px;
            color: {THEME_GRAY_TEXT};
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .metric-value {{
            font-size: 32px;
            color: {THEME_DARK_TEXT};
            font-weight: 800;
            margin-top: 5px;
        }}

        /* Penekanan warna pada angka tertentu */
        .highlight-orange {{
            color: {THEME_ORANGE} !important;
        }}

        /* --- Tab Styling Enhancement --- */
        /* Mencoba mengubah warna garis bawah tab aktif menjadi oranye */
        button[data-baseweb="tab"] > div[data-testid="stMarkdownContainer"] > p {{
            font-weight: 600;
        }}
        [data-baseweb="tab-highlight"] {{
            background-color: {THEME_ORANGE} !important;
        }}

        /* --- Navigation Clean Up --- */
        [data-testid="stSidebar"] .element-container {{
            padding: 0px !important;
            margin: 0px !important;
        }}
        h1, h2, h3 {{
            color: {THEME_DARK_TEXT};
            font-weight: 700;
        }}
    </style>
""", unsafe_allow_html=True)

# ======================

# ======================
# 1. CONFIG PAGE
# ======================
st.set_page_config(
    page_title="Customer Segmentation Pro",
    page_icon="🔑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================
# 2. CSS SUPER AESTHETIC (Orange Theme)
# ======================
st.markdown("""
    <style>
        /* Import Font yang Estetik */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800&display=swap');

        /* 1. SIDEBAR BACKGROUND: Gradasi Dibalik (Kuning ke Oranye) */
        [data-testid="stSidebar"] {
            /* Warna dibalik: #FDC830 (Kuning) di atas, #F37335 (Oranye) di bawah */
            background: linear-gradient(180deg, #FDC830 0%, #F37335 100%);
            border-right: 1px solid rgba(255,255,255,0.2);
        }

        /* 2. HEADER MAIN MENU ESTETIK */
        .sidebar-header {
            font-family: 'Outfit', sans-serif;
            font-size: 24px;              /* Ukuran font lebih besar */
            font-weight: 800;             /* Sangat tebal */
            color: white;
            text-align: center;           /* Posisi Tengah */
            margin-bottom: 20px;
            margin-top: 10px;
            text-transform: uppercase;    /* Huruf Kapital semua biar estetik */
            letter-spacing: 2px;          /* Jarak antar huruf renggang */
            text-shadow: 0 2px 4px rgba(0,0,0,0.1);
            display: flex;
            justify-content: center;      /* Pastikan benar-benar di tengah */
            align-items: center;
        }

        /* 3. MENU ITEM STYLING ("Dikotakin & Seragam") */
        .stRadio div[role='radiogroup'] > label {
            background-color: rgba(255, 255, 255, 0.2); /* Transparan kaca */
            border: 1px solid rgba(255, 255, 255, 0.3);
            padding: 12px 20px;
            border-radius: 15px;          /* Lebih bulat sedikit */
            margin-bottom: 12px;
            transition: all 0.3s ease;
            cursor: pointer;
            color: white !important;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            
            /* KUNCI AGAR KOTAK SAMA BESAR */
            width: 100%;                  
            display: flex;
            justify-content: flex-start;  /* Teks rata kiri di dalam kotak */
            align-items: center;
        }

        /* Efek Hover */
        .stRadio div[role='radiogroup'] > label:hover {
            background-color: rgba(255, 255, 255, 0.5);
            transform: scale(1.02);       /* Efek membesar sedikit */
            box-shadow: 0 8px 15px rgba(0,0,0,0.1);
        }

        /* Teks di dalam Radio Button */
        .stRadio div[role='radiogroup'] label p {
            font-family: 'Outfit', sans-serif;
            font-size: 16px !important;
            font-weight: 600 !important;
            color: white !important;
            margin: 0 !important;
        }

        /* Hapus bulatan radio button default */
        .stRadio div[role='radiogroup'] label div[data-testid="stMarkdownContainer"] {
            display: flex;
            align-items: center;
            width: 100%;
        }
        
        /* Hapus elemen lingkaran default Streamlit */
        div[data-testid="stRadio"] > div {
             gap: 0px;
        }

    </style>
""", unsafe_allow_html=True)

# ======================
# 3. SIDEBAR NAVIGATION
# ======================
with st.sidebar:
    # --- LOGO SECTION ---
    # Container logo dibuat agak tinggi sesuai request sebelumnya
    st.markdown('<div style="text-align: center; margin-bottom: 20px; margin-top: 30px;">', unsafe_allow_html=True)
    try:
        st.image("image/alllogo.png", width=220) 
    except:
        # Fallback Logo
        st.markdown("""
            <h1 style='color: white; font-size: 50px; text-align: center; margin: 0;'>🍊</h1>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- CUSTOM HEADER (CENTERED & AESTHETIC) ---
    st.markdown("""
        <div class="sidebar-header">
            Main Menu
        </div>
    """, unsafe_allow_html=True)

    # --- NAVIGATION MENU ---
    # Spasi di dalam string ditambahkan agar teks tidak terlalu mepet ke kiri kotak
    selected_page = st.sidebar.radio(
        "",
        [
            "Executive Overview", 
            "Dashboard RFM", 
            "Prediksi & Insight"
        ],
        index=0,
        label_visibility="collapsed"
    )

    # Logika Page
    if "Executive" in selected_page:
        page = "Executive Overview"
    elif "RFM" in selected_page:
        page = "Dashboard RFM"
    else:
        page = "Prediksi & Insight"

    # --- FOOTER ---
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; background: rgba(255,255,255,0.15); padding: 20px; border-radius: 15px; margin-top: 10px;">
            <p style="font-family: 'Outfit'; font-size: 12px; color: white; margin: 0; font-weight: 800; letter-spacing: 1px;">
                CUSTOMER INTELLIGENCE
            </p>
            <p style="font-family: 'Outfit'; font-size: 10px; color: rgba(255,255,255,0.8); margin: 5px 0 0 0;">
                © 2025 Team A25-CS254
            </p>
        </div>
    """, unsafe_allow_html=True)

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
    st.warning("⚠ Model (scaler.pkl, pca.pkl, kmeans.pkl) belum ditemukan di folder 'model'. Fitur prediksi tidak akan berjalan.")

# Mapping Nama Cluster
cluster_names = {
    0: "Low Value / Inactive",
    1: "High Value / Loyal",
    2: "Medium / Potential"
}
recommendation_text = {
    0: "🔍 <b>Strategi Reaktivasi:</b> Pelanggan ini sudah lama tidak aktif. Segera picu minat mereka kembali dengan kampanye 'Win-Back' personal. Berikan voucher diskon dengan urgensi tinggi (limited time) untuk mendorong transaksi instan.",
    1: "💎 <b>Retensi Prioritas (VIP):</b> Ini adalah aset berharga bisnis Anda. Fokus pada eksklusivitas dengan memberikan akses awal (Early Access) ke produk baru, layanan prioritas, dan reward khusus yang tidak dimiliki pelanggan lain.",
    2: "📈 <b>Peluang Pertumbuhan:</b> Pelanggan ini memiliki potensi besar untuk menjadi loyal. Dorong nilai transaksi (Average Order Value) mereka melalui teknik Upselling, penawaran paket bundling menarik, atau insentif poin loyalitas."
}

# --- FUNGSI BANTUAN VISUAL UNTUK PLOTLY ---
def update_plotly_layout(fig, title="", show_grid=False):
    """Fungsi untuk menyeragamkan tampilan chart Plotly"""
    fig.update_layout(
        title={
            'text': title,
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=18, color=THEME_DARK_TEXT, family="Inter")
        },
        paper_bgcolor='rgba(0,0,0,0)', # Transparan agar menyatu dengan card
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter", color=THEME_GRAY_TEXT),
        margin=dict(t=40, l=20, r=20, b=20),
    )
    if not show_grid:
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)
    return fig

# ============================================================
# PAGE 1: EXECUTIVE OVERVIEW
# ============================================================
if page == "Executive Overview":

    # --- HERO SECTION ---
    st.title("💎 Customer Intelligence Hub")
    st.markdown(f"<h3 style='color: {THEME_ORANGE};'>Transformation from Mass Marketing to Personalized Strategy</h3>", unsafe_allow_html=True)
    st.write("Selamat datang di panel analitik pelanggan. Platform ini menggunakan Machine Learning untuk mengelompokkan pelanggan berdasarkan perilaku belanja mereka (RFM Analysis).")

    st.markdown("---")

    # --- TOP LEVEL METRICS (REVISED VISUALS) ---
    total_orders_all = df['order_num_total_ever_online'].sum() + df['order_num_total_ever_offline'].sum()
    revenue_juta = df['Monetary'].sum()/1000000

    m1, m2, m3 = st.columns(3)

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

    # KPI 3: Total Revenue (Dengan penekanan warna oranye pada nilai uang)
    with m3:
        st.markdown(f"""
        <div class="premium-card" style="border-left-color: {THEME_ORANGE_LIGHT};">
            <div class="metric-label">Total Revenue</div>
            <div class="metric-value highlight-orange">₺{revenue_juta:.1f}M</div>
        </div>
        """, unsafe_allow_html=True)

    # --- TABS FOR ORGANIZED CONTENT ---
    tab1, tab2, tab3 = st.tabs(["🎯 Business Objectives", "📂 Dataset Explorer", "📈 Visual Overview"])

    with tab1:
        st.subheader("Mengapa Segmentasi Itu Penting?")
        # Menggunakan container dengan border untuk visualisasi yang lebih rapi
        with st.container(border=True):
            c1, c2, c3 = st.columns(3)
            with c1:
                st.info("**1. Efisiensi Biaya**\n\nHentikan promosi massal yang mahal. Fokuskan budget hanya pada pelanggan yang berpotensi tinggi.")
            with c2:
                st.warning("**2. Personalisasi**\n\nPelanggan loyal butuh *reward*, pelanggan pasif butuh diskon. Berikan apa yang mereka butuhkan.")
            with c3:
                # Mengubah success menjadi warna tema jika memungkinkan, atau biarkan hijau untuk semantik positif
                st.success("**3. Tingkatkan ROI**\n\nStrategi yang tepat sasaran terbukti meningkatkan konversi penjualan hingga 2-3x lipat.")

        st.markdown("#### 🔑 The RFM Concept")
        try:
            # Menambahkan border halus dan shadow pada gambar diagram
            st.image("image/rfmanalysisdiagram.jpeg", caption="Recency, Frequency, Monetary Model Concept", width=600)
        except Exception:
             st.warning("Gambar 'rfmanalysisdiagram.jpeg' tidak ditemukan. Cek folder image.")
            
    with tab2:
        st.subheader("Data Source Overview")
        st.markdown("Dataset ini menggabungkan perilaku transaksi dari OmniChannel (Aplikasi, Website, dan Toko Fisik).")

        # Interactive DataFrame dengan border
        with st.container(border=True):
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
                    "Total nilai transaksi offline", "Total nilai transaksi online",
                    "Kategori belanja dalam 12 bulan terakhir"
                ]
            }
             st.table(pd.DataFrame(metadata))

    # --- BAGIAN VISUAL OVERVIEW (UPDATED VISUALS) ---
    with tab3:
        st.subheader("Visualisasi Data Utama")

        # 1. PENGATUR TANGGAL (DATE FILTER) dalam Container
        with st.container(border=True):
            st.markdown(f"<h5 style='color:{THEME_ORANGE};'>🗓 Filter Periode Data</h5>", unsafe_allow_html=True)

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
            st.warning("⚠ Tidak ada data transaksi pada rentang tanggal yang dipilih.")
        else:
            # === ROW 1: GROWTH & CHANNEL PIE ===
            col_viz1, col_viz2 = st.columns(2)

            # a. Line Chart Bulanan (Visual Enhancement)
            with col_viz1:
                 with st.container(border=True): # Bungkus chart dalam container ber-border halus
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
                            color_discrete_sequence=[THEME_ORANGE] # Menggunakan warna tema
                         )
                         # Kustomisasi Line Chart agar lebih bersih
                         fig_line.update_traces(line=dict(width=3), marker=dict(size=8, line=dict(width=2, color='white')))
                         fig_line = update_plotly_layout(fig_line, show_grid=True) # Tampilkan grid tipis untuk line chart
                         fig_line.update_xaxes(showgrid=False) # Hapus grid vertikal saja

                         st.plotly_chart(fig_line, use_container_width=True)
                     else:
                         st.error("Kolom 'first_order_date' tidak ditemukan.")

            # b. Pie Chart Order Channel (Visual Enhancement)
            with col_viz2:
                 with st.container(border=True):
                     st.markdown("#### 🥧 Distribusi Channel")
                     fig_pie = px.pie(
                        df_filtered,
                        names='order_channel',
                        color='order_channel',
                        # Menggunakan palet sequential oranye yang konsisten
                        color_discrete_sequence=px.colors.sequential.Oranges_r,
                        hole=0.5 # Donut chart yang lebih modern
                     )
                     fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                     fig_pie = update_plotly_layout(fig_pie)
                     st.plotly_chart(fig_pie, use_container_width=True)

            st.divider()

            # === ROW 2: ORDER VOLUME & REVENUE (COMPARED) ===
            col_viz3, col_viz4 = st.columns(2)

            # c. Bar Chart: Volume Order (Visual Enhancement)
            with col_viz3:
                with st.container(border=True):
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
                        # Kontras: Online = Oranye Terang, Offline = Oranye Gelap/Coklat
                        color_discrete_map={'Online Order': THEME_ORANGE, 'Offline Order': '#A04000'}
                    )
                    fig_vol.update_traces(texttemplate='%{text:.2s}', textposition='outside')
                    fig_vol = update_plotly_layout(fig_vol)
                    fig_vol.update_layout(xaxis_title="Jumlah Transaksi", yaxis_title="", showlegend=False)
                    st.plotly_chart(fig_vol, use_container_width=True)

            # d. Bar Chart: Revenue (Visual Enhancement)
            with col_viz4:
                with st.container(border=True):
                    st.markdown("#### 💰 Total Revenue")

                    rev_online = df_filtered['customer_value_total_ever_online'].sum()
                    rev_offline = df_filtered['customer_value_total_ever_offline'].sum()

                    df_rev = pd.DataFrame({
                        'Source': ['Online Revenue', 'Offline Revenue'],
                        'Revenue': [rev_online, rev_offline]
                    })

                    fig_rev = px.bar(
                        df_rev, x='Revenue', y='Source', orientation='h',
                        text='Revenue', color='Source',
                        # Kontras yang sama
                        color_discrete_map={'Online Revenue': THEME_ORANGE, 'Offline Revenue': '#A04000'}
                    )

                    fig_rev.update_traces(texttemplate='₺%{text:.2s}', textposition='outside')
                    fig_rev = update_plotly_layout(fig_rev)
                    fig_rev.update_layout(xaxis_title="Total Revenue (₺)", yaxis_title="", showlegend=False)
                    st.plotly_chart(fig_rev, use_container_width=True)

            # === ROW 3: CATEGORIES (Visual Enhancement) ===
            st.divider()
            with st.container(border=True):
                st.markdown("#### 🛍 Top Kategori Peminatan")
                st.caption("Menampilkan kategori produk yang paling sering diminati pada rentang tanggal yang dipilih.")

                if 'interested_in_categories_12' in df_filtered.columns:
                    # 1. Definisi Fungsi Cleaning
                    def clean_list(x):
                        if isinstance(x, str):
                            x = x.strip("[]")
                            return [i.strip().replace("'", "") for i in x.split(",")]
                        return []

                    # 2. Proses Cleaning
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
                        # Menggunakan skala warna oranye yang konsisten
                        color_continuous_scale=px.colors.sequential.Oranges
                    )
                    fig_bar.update_traces(textposition='outside')
                    fig_bar = update_plotly_layout(fig_bar)
                    fig_bar.update_layout(xaxis_title="Jumlah Transaksi", yaxis_title="", showlegend=False, coloraxis_showscale=False)
                    st.plotly_chart(fig_bar, use_container_width=True)
                else:
                    st.warning("⚠ Kolom kategori tidak ditemukan.")
# ============================================================
# PAGE 2: DASHBOARD RFM
# ============================================================
elif page == "Dashboard RFM":
    st.markdown(f"<h1 style='text-align: center; color: {THEME_DARK_TEXT};'>📊 RFM Deep Dive Analysis</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Analisis mendalam mengenai karakteristik dan perilaku belanja pelanggan antar cluster.</p>", unsafe_allow_html=True)
    st.markdown("---")

    # --- 0. PREP DATA & CLEANING FUNCTION ---
    def clean_list(x):
        if isinstance(x, str):
            x = x.strip("[]")
            return [i.strip().replace("'", "") for i in x.split(",")]
        return []

    if "Cluster" in df.columns:
        df["Cluster Label"] = df["Cluster"].map(cluster_names)
    else:
        st.error("⚠ Kolom 'Cluster' tidak ditemukan.")
        st.stop()

    # --- 1. FILTER DROPDOWN (VISUAL ENHANCEMENT) ---
    # Menggunakan st.container dengan border agar area filter terdefinisi jelas
    with st.container(border=True):
        st.markdown(f"### 🔍 Filter Data Cluster")
        col_f1, col_f2 = st.columns([1, 3])
        with col_f1:
             st.write("") # Spasi kosong untuk alignment vertical
             st.markdown(f"**Pilih Segmen:**", help="Pilih salah satu segmen untuk melihat detail metriknya.")
        with col_f2:
            cluster_options = ["Semua Cluster"] + list(df["Cluster Label"].unique())
            selected_cluster = st.selectbox(
                "", # Label dikosongkan karena sudah ada di col_f1
                options=cluster_options,
                index=0,
                label_visibility="collapsed"
            )

        # Logic Filter
        if selected_cluster == "Semua Cluster":
            df_rfm = df.copy()
        else:
            df_rfm = df[df["Cluster Label"] == selected_cluster]

    # --- 2. KEY METRICS (KPI) - VISUAL ENHANCEMENT ---
    if df_rfm.empty:
        st.warning("Data tidak ditemukan.")
    else:
        st.markdown(f"### 🚀 Key Metrics: <span style='color:{THEME_ORANGE}'>{selected_cluster}</span>", unsafe_allow_html=True)

        avg_recency = df_rfm["Recency"].mean()
        avg_freq = df_rfm["Frequency"].mean()
        avg_monetary = df_rfm["Monetary"].mean()

        kpi1, kpi2, kpi3 = st.columns(3)

        # Penggunaan class highlight-orange untuk angka agar menonjol
        with kpi1:
            st.markdown(f"""
            <div class="premium-card">
                <div class="metric-label">Avg. Recency (Hari)</div>
                <div class="metric-value highlight-orange">{avg_recency:.1f}</div>
                <small style="color: {THEME_GRAY_TEXT};">Rata-rata hari sejak order terakhir</small>
            </div>
            """, unsafe_allow_html=True)

        with kpi2:
            st.markdown(f"""
            <div class="premium-card">
                <div class="metric-label">Avg. Frequency</div>
                <div class="metric-value highlight-orange">{avg_freq:.1f}x</div>
                <small style="color: {THEME_GRAY_TEXT};">Rata-rata frekuensi transaksi</small>
            </div>
            """, unsafe_allow_html=True)

        with kpi3:
            st.markdown(f"""
            <div class="premium-card">
                <div class="metric-label">Avg. Monetary</div>
                <div class="metric-value highlight-orange">₺{avg_monetary:,.0f}</div>
                <small style="color: {THEME_GRAY_TEXT};">Rata-rata nilai belanja</small>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # --- 3. 3D & CATEGORY INSIGHTS (MAJOR VISUAL OVERHAUL ON 3D COLORS) ---
    col_main1, col_main2 = st.columns([1.5, 1])

    with col_main1:
        with st.container(border=True):
            st.subheader(f"🧊 3D Segmentation")
            st.caption("Sebaran pelanggan berdasarkan Recency, Frequency, Monetary.")

            # === PENTING: Pemetaan Warna Baru untuk 3D Chart agar Sesuai Tema ===
            # Low Value (Inactive) -> Abu-abu netral
            # Medium (Potential) -> Kuning/Amber (Antara)
            # High Value (Loyal) -> Oranye Gelap (Warna Utama Brand)
            color_map_3d = {
                "Low Value / Inactive": "#95A5A6",  # Concrete Gray
                "Medium / Potential": "#F1C40F",    # Amber/Gold
                "High Value / Loyal": THEME_ORANGE  # Brand Orange
            }

            fig_3d = px.scatter_3d(
                df_rfm,
                x='Recency',
                y='Frequency',
                z='Monetary',
                color='Cluster Label',
                color_discrete_map=color_map_3d,
                opacity=0.8, # Sedikit lebih solid
                height=500,
                hover_data=['master_id']
            )
            # Update layout 3D untuk menghilangkan background abu-abu default Plotly
            fig_3d.update_layout(
                margin=dict(l=0, r=0, b=0, t=0),
                scene = dict(
                    xaxis = dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="white", showbackground=True, zerolinecolor="white"),
                    yaxis = dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="white", showbackground=True, zerolinecolor="white"),
                    zaxis = dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="white", showbackground=True, zerolinecolor="white"),
                    bgcolor = "rgba(0,0,0,0)"
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                legend=dict(
                    yanchor="top",
                    y=0.99,
                    xanchor="left",
                    x=0.01,
                    bgcolor="rgba(255,255,255,0.8)" # Legenda semi-transparan
                )
            )
            st.plotly_chart(fig_3d, use_container_width=True)

    with col_main2:
        with st.container(border=True):
            st.subheader("🛍 Top Kategori")
            st.caption(f"Kategori paling diminati di {selected_cluster}.")

            if "interested_in_categories_12" in df_rfm.columns:
                df_cat = df_rfm.copy()
                df_cat["categories"] = df_cat["interested_in_categories_12"].apply(clean_list)
                df_exploded = df_cat.explode("categories")
                cat_counts = df_exploded["categories"].value_counts().reset_index()
                cat_counts.columns = ['Category', 'Count']

                fig_cat = px.bar(
                    cat_counts.head(5).sort_values(by="Count", ascending=True),
                    x="Count",
                    y="Category",
                    orientation='h',
                    text='Count',
                    color='Count',
                    # Konsisten dengan skala warna oranye
                    color_continuous_scale=px.colors.sequential.Oranges
                )
                fig_cat.update_traces(textposition='outside')
                fig_cat = update_plotly_layout(fig_cat)
                fig_cat.update_layout(yaxis_title="", xaxis_title="Jumlah Peminat", showlegend=False, coloraxis_showscale=False)
                st.plotly_chart(fig_cat, use_container_width=True)
            else:
                st.warning("Kolom kategori tidak ditemukan.")

    st.divider()

    # --- 4. GLOBAL CLUSTER STATS (VISUAL ENHANCEMENT) ---
    st.subheader("📊 Statistik Global Cluster")

    tab_g1, tab_g2, tab_g3 = st.tabs(["Distribusi Cluster (Pie)", "Perbandingan RFM (Bar)", "Channel Preference"])

    # Tab 1: Pie Chart Distribusi Cluster
    with tab_g1:
        with st.container(border=True):
            st.markdown("#### Proporsi Jumlah Pelanggan")
            df_pie = df['Cluster Label'].value_counts().reset_index()
            df_pie.columns = ['Cluster', 'Count']

            # Gunakan color map yang sama dengan 3D chart agar konsisten
            fig_pie_global = px.pie(
                df_pie,
                names='Cluster',
                values='Count',
                color='Cluster',
                color_discrete_map=color_map_3d, # PENTING: Konsistensi warna
                hole=0.5
            )
            fig_pie_global.update_traces(textposition='inside', textinfo='percent+label')
            fig_pie_global = update_plotly_layout(fig_pie_global)
            st.plotly_chart(fig_pie_global, use_container_width=True)

    # Tab 2: Bar Chart Rata-rata RFM per Cluster
    with tab_g2:
        st.markdown("#### Perbandingan Rata-rata RFM")
        df_grouped = df.groupby("Cluster Label")[["Recency", "Frequency", "Monetary"]].mean().reset_index()

        c_rfm1, c_rfm2 = st.columns(2)

        with c_rfm1:
            with st.container(border=True):
                # R & F menggunakan warna kontras Oranye vs Abu gelap
                fig_bar_rf = px.bar(
                    df_grouped,
                    x="Cluster Label",
                    y=["Recency", "Frequency"],
                    barmode="group",
                    color_discrete_sequence=[THEME_DARK_TEXT, THEME_ORANGE], # Recency=Gelap, Freq=Oranye
                    text_auto='.1f',
                    title="Recency & Frequency (Grouped)"
                )
                fig_bar_rf.update_traces(textposition='outside')
                fig_bar_rf = update_plotly_layout(fig_bar_rf)
                st.plotly_chart(fig_bar_rf, use_container_width=True)

        with c_rfm2:
            with st.container(border=True):
                # Monetary menggunakan warna cluster yang konsisten
                fig_bar_m = px.bar(
                    df_grouped,
                    x="Cluster Label",
                    y="Monetary",
                    text="Monetary",
                    color="Cluster Label",
                    color_discrete_map=color_map_3d, # Konsistensi warna
                    title="Monetary Value (Average)"
                )
                fig_bar_m.update_traces(texttemplate='₺%{text:.2s}', textposition='outside')
                fig_bar_m = update_plotly_layout(fig_bar_m)
                fig_bar_m.update_layout(showlegend=False) # Hide legend karena sudah jelas di sumbu X
                st.plotly_chart(fig_bar_m, use_container_width=True)

    # Tab 3: Channel Distribution
    with tab_g3:
        with st.container(border=True):
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
                    # Palet Oranye yang konsisten
                    color_discrete_sequence=px.colors.sequential.Oranges_r
                )
                fig_stack = update_plotly_layout(fig_stack)
                fig_stack.update_layout(barmode='stack', xaxis=dict(range=[0, 100]), xaxis_title="Persentase (%)", yaxis_title="")
                st.plotly_chart(fig_stack, use_container_width=True)

# ============================================================
# PAGE 3: PREDIKSI & INSIGHT (ACTIONABLE)
# ============================================================
elif page == "Prediksi & Insight":
    st.markdown(f"<h1 style='text-align: center; color:{THEME_DARK_TEXT};'>🤖 AI Predictor</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Simulasi pelanggan baru untuk menentukan strategi marketing yang tepat secara Real-Time.</p>", unsafe_allow_html=True)

    st.divider()

    col_input, col_res = st.columns([1, 1.5], gap="large")

    with col_input:
        # Container Input dengan border tebal di atas berwarna oranye
        with st.container():
            st.markdown(f"""
                <div style="background-color: white; padding: 20px; border-radius: 10px; border-top: 5px solid {THEME_ORANGE}; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                    <h3 style="color: {THEME_DARK_TEXT}; margin-top:0;">Input Data Pelanggan</h3>
            """, unsafe_allow_html=True)

            start_date = st.date_input("Tanggal Transaksi Terakhir")
            end_date = st.date_input("Tanggal Hari Ini", datetime.today())

            recency = (end_date - start_date).days
            if recency < 0: st.error("Tanggal tidak valid")

            freq = st.number_input("Frequency (Total Transaksi)", 1, 100, 5)
            mon = st.number_input("Monetary (Total Belanja ₺)", 0, 100000000, 500000)

            st.write("")
            # Tombol diletakkan di luar div HTML kustom agar berfungsi normal
            run_btn = st.button("Analisis Sekarang 🚀", type="primary", use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True) # Penutup div container input

    with col_res:
        if run_btn:
            # Prediksi (Logika Tetap Sama)
            try:
                X = [[recency, freq, mon]]
                X_scaled = scaler.transform(X)
                X_pca = pca.transform(X_scaled)
                pred = kmeans.predict(X_pca)[0]

                label = cluster_names[pred]
                desc = recommendation_text[pred]

                # Tampilan Hasil Lebih Premium dengan Gradien Halus sebagai latar belakang
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, #FFFFFF 0%, #FFF3E0 100%);
                    padding: 30px;
                    border-radius: 15px;
                    box-shadow: 0 10px 25px -5px rgba(239, 133, 5, 0.2); /* Shadow oranye */
                    border-left: 10px solid {THEME_ORANGE};
                    animation: fadeIn 0.8s;
                ">
                    <h4 style="margin:0; color:{THEME_ORANGE_LIGHT}; text-transform: uppercase; letter-spacing: 1px;">Hasil Analisis AI</h4>
                    <h1 style="font-size: 48px; margin: 15px 0; color: {THEME_DARK_TEXT};">{label}</h1>
                    <hr style="border-top: 2px solid {THEME_ORANGE_LIGHT}; opacity: 0.3;">
                    <p style="font-size:20px; color: {THEME_DARK_TEXT}; font-weight: 500;"><span style="font-size: 24px;">💡</span> {desc}</p>
                </div>
                <style>@keyframes fadeIn {{ from {{ opacity:0; transform: translateY(10px); }} to {{ opacity:1; transform: translateY(0); }} }}</style>
                """, unsafe_allow_html=True)

                st.write("") # Spasi

                # Show Metrics Recency calculated dalam container kecil
                with st.container(border=True):
                    c_a, c_b = st.columns(2)
                    with c_a:
                        st.metric("Recency yang Dihitung", f"{recency} Hari")
                    with c_b:
                        mean_monetary = df['Monetary'].mean() if not df.empty else 0
                        val_status = "Above Average 📈" if mon > mean_monetary else "Below Average 📉"
                        st.metric("Status Monetary Value", val_status)

            except Exception as e:
                st.error(f"Terjadi kesalahan saat prediksi: {e}. Cek apakah model sudah dimuat dengan benar.")

        else:
            # Placeholder state yang lebih menarik visualnya
            st.markdown(f"""
            <div style="text-align: center; padding: 50px; color: {THEME_GRAY_TEXT}; border: 2px dashed {THEME_ORANGE_LIGHT}; border-radius: 15px;">
                <h2 style="color: {THEME_ORANGE_LIGHT};">👈 Menunggu Input Data</h2>
                <p>Masukkan data Recency, Frequency, dan Monetary di panel sebelah kiri, lalu klik tombol "Analisis Sekarang" untuk melihat prediksi AI.</p>
                <img src="https://cdn-icons-png.flaticon.com/512/1680/1680859.png" width="120" style="opacity: 0.5; margin-top: 20px;">
            </div>
            """, unsafe_allow_html=True)
