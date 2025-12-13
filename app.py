import streamlit as st
import pandas as pd
import pickle
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from plotly.subplots import make_subplots

# ======================
# 1. CONFIG PAGE
# ======================
st.set_page_config(
    page_title="Customer Intelligence HQ",
    page_icon="🍊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================
# 2. ADVANCED CSS STYLING (THEME: ORANGE LUXURY)
# ======================
st.markdown("""
    <style>
        /* --- Import Font: Outfit --- */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Outfit', sans-serif;
            color: #2D3436;
        }

        /* --- Global Background --- */
        .stApp {
            background-color: #FDFBF7; /* Cream sangat muda */
        }

        /* --- Sidebar Gradient --- */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #EF8505 0%, #FF6B00 100%);
            border-right: 1px solid rgba(255,255,255,0.2);
        }
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, 
        [data-testid="stSidebar"] span, [data-testid="stSidebar"] p, [data-testid="stSidebar"] label {
            color: white !important;
        }

        /* --- Glassmorphism Cards --- */
        .metric-card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 10px 30px rgba(239, 133, 5, 0.1);
            border: 1px solid rgba(255,255,255,0.5);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        .metric-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(239, 133, 5, 0.2);
            border-color: #EF8505;
        }
        .metric-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0;
            width: 6px; height: 100%;
            background: #EF8505;
            border-radius: 4px 0 0 4px;
        }

        /* --- Typography --- */
        h1, h2, h3 {
            font-weight: 700 !important;
        }
        .highlight-text {
            background: -webkit-linear-gradient(45deg, #EF8505, #F2C94C);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        /* --- Radio Button Styling --- */
        .stRadio > div {
            background: rgba(255,255,255,0.15);
            padding: 15px;
            border-radius: 12px;
            backdrop-filter: blur(10px);
        }

        /* --- Button Styling --- */
        .stButton > button {
            background: linear-gradient(90deg, #EF8505 0%, #FF9F43 100%);
            color: white;
            border: none;
            padding: 10px 24px;
            border-radius: 8px;
            font-weight: 600;
            transition: 0.3s;
            width: 100%;
        }
        .stButton > button:hover {
            box-shadow: 0 5px 15px rgba(239, 133, 5, 0.4);
            transform: scale(1.02);
        }
        
        /* --- Plotly Chart Container --- */
        .js-plotly-plot .plotly .modebar {
            orientation: v;
        }
    </style>
""", unsafe_allow_html=True)

# ======================
# 3. HELPER FUNCTIONS
# ======================
def clean_list(x):
    """Membersihkan string list menjadi list python asli"""
    if isinstance(x, str):
        x = x.strip("[]")
        if not x: return []
        return [i.strip().replace("'", "") for i in x.split(",")]
    return []

def format_currency(value):
    if value >= 1000000:
        return f"₺{value/1000000:.1f}M"
    elif value >= 1000:
        return f"₺{value/1000:.1f}K"
    return f"₺{value:,.0f}"

# ======================
# 4. LOAD DATA & MODELS
# ======================
@st.cache_data
def load_data():
    try:
        df_main = pd.read_excel("dataset/data_with_cluster.xlsx")
        df_raw = pd.read_csv("dataset/flo_data_20k.csv")
        if "first_order_date" in df_main.columns:
            df_main["first_order_date"] = pd.to_datetime(df_main["first_order_date"])
        return df_main, df_raw
    except Exception as e:
        return None, None

df, df2 = load_data()

# Error Handling Jika Data Gagal Load
if df is None:
    st.error("❌ Gagal memuat data. Pastikan file 'data_with_cluster.xlsx' dan 'flo_data_20k.csv' ada di folder 'dataset'.")
    st.stop()

# Load Models
try:
    scaler = pickle.load(open("model/scaler.pkl", "rb"))
    pca = pickle.load(open("model/pca.pkl", "rb"))
    kmeans = pickle.load(open("model/kmeans.pkl", "rb"))
    model_loaded = True
except:
    model_loaded = False

# Mapping
cluster_names = {0: "Low Value / Inactive", 1: "High Value / Loyal", 2: "Medium / Potential"}
cluster_colors = {0: "#95A5A6", 1: "#EF8505", 2: "#2980B9"} # Grey, Orange, Blue
if "Cluster" in df.columns:
    df["Cluster Label"] = df["Cluster"].map(cluster_names)

# ======================
# 5. SIDEBAR NAVIGATION
# ======================
with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    try:
        st.image("image/alllogo.png", width=200) 
    except:
        st.markdown("<h1 style='color:white;'>🍊 PRO CRM</h1>", unsafe_allow_html=True)
    
    st.markdown("<p style='font-size: 12px; opacity: 0.8; margin-top: -10px;'>INTELLIGENT DASHBOARD</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    page = st.sidebar.radio(
        "NAVIGASI UTAMA",
        ["Executive Overview", "Deep Dive RFM", "AI Prediction"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.info("💡 **Tips:** Gunakan mode 'Light' pada settings browser Anda untuk pengalaman visual terbaik.")

# ============================================================
# PAGE 1: EXECUTIVE OVERVIEW 
# ============================================================
if page == "Executive Overview":
    st.markdown("<h1 class='highlight-text'>Executive Summary</h1>", unsafe_allow_html=True)
    st.markdown("Overview performa bisnis secara menyeluruh dari integrasi data Online & Offline.")
    
    # --- GLOBAL FILTER ---
    with st.expander("🗓️ Filter Tanggal Transaksi", expanded=False):
        c_f1, c_f2 = st.columns(2)
        min_date = df['first_order_date'].min().date()
        max_date = df['first_order_date'].max().date()
        start_date = c_f1.date_input("Mulai", min_date, min_value=min_date, max_value=max_date)
        end_date = c_f2.date_input("Sampai", max_date, min_value=min_date, max_value=max_date)

    # Filter Logic
    mask = (df['first_order_date'].dt.date >= start_date) & (df['first_order_date'].dt.date <= end_date)
    df_filtered = df.loc[mask]

    st.markdown("<br>", unsafe_allow_html=True)

    # --- KPI CARDS (THE "WAH" FACTOR) ---
    col1, col2, col3, col4 = st.columns(4)
    
    # Kalkulasi Metric
    total_cust = df_filtered.shape[0]
    total_rev = df_filtered['Monetary'].sum()
    total_trx = df_filtered['Frequency'].sum()
    avg_aov = total_rev / total_trx if total_trx > 0 else 0

    metrics = [
        ("Total Customers", f"{total_cust:,}", "👥"),
        ("Total Revenue", format_currency(total_rev), "💰"),
        ("Total Transactions", f"{total_trx:,}", "📦"),
        ("Avg. Order Value", f"₺{avg_aov:,.0f}", "💳")
    ]

    for col, (label, value, icon) in zip([col1, col2, col3, col4], metrics):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 24px; float: right; opacity: 0.2;">{icon}</div>
                <div style="font-size: 13px; font-weight: 500; color: #7F8C8D; text-transform: uppercase;">{label}</div>
                <div style="font-size: 28px; font-weight: 800; color: #2D3436; margin-top: 5px;">{value}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- ROW 1: GROWTH & CHANNEL ---
    c_chart1, c_chart2 = st.columns([2, 1])

    with c_chart1:
        st.subheader("📈 Growth Trend")
        # Area Chart Gradient
        df_trend = df_filtered.set_index('first_order_date').resample('M').size().reset_index(name='count')
        fig_area = px.area(
            df_trend, x='first_order_date', y='count',
            labels={'first_order_date': 'Bulan', 'count': 'New Customers'},
            color_discrete_sequence=['#EF8505']
        )
        fig_area.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', 
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='#eee'),
            margin=dict(t=10, l=0, r=0, b=0)
        )
        st.plotly_chart(fig_area, use_container_width=True)

    with c_chart2:
        st.subheader("🥧 Channel Mix")
        # Donut Chart Modern
        fig_pie = px.pie(
            df_filtered, names='order_channel', 
            color_discrete_sequence=px.colors.sequential.Oranges_r,
            hole=0.6
        )
        fig_pie.update_layout(
            showlegend=False,
            margin=dict(t=20, l=20, r=20, b=20),
            annotations=[dict(text='Channel', x=0.5, y=0.5, font_size=20, showarrow=False)]
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # --- ROW 2: ADVANCED CATEGORY INSIGHT (SUNBURST) ---
    st.markdown("---")
    st.subheader("🛍️ Category & Interest Analysis")
    
    if "interested_in_categories_12" in df_filtered.columns:
        # Preprocessing khusus visualisasi
        df_cat = df_filtered.copy()
        df_cat["clean_cats"] = df_cat["interested_in_categories_12"].apply(clean_list)
        df_exploded = df_cat.explode("clean_cats")
        
        # Agregasi untuk Sunburst: Channel -> Category -> Count
        df_sunburst = df_exploded.groupby(['order_channel', 'clean_cats']).size().reset_index(name='count')
        # Ambil Top 50 interaksi biar chart ga berat
        df_sunburst = df_sunburst.nlargest(50, 'count')

        c_sun, c_bar = st.columns([1.5, 1])
        
        with c_sun:
            st.markdown("##### Hierarki: Channel vs Kategori")
            
            fig_sun = px.sunburst(
                df_sunburst, 
                path=['order_channel', 'clean_cats'], 
                values='count',
                color='count',
                color_continuous_scale='Oranges'
            )
            fig_sun.update_layout(margin=dict(t=0, l=0, r=0, b=0), height=400)
            st.plotly_chart(fig_sun, use_container_width=True)
            
        with c_bar:
            st.markdown("##### Top 10 Kategori Terlaris")
            cat_rank = df_exploded['clean_cats'].value_counts().head(10).reset_index()
            cat_rank.columns = ['Category', 'Sales']
            
            fig_bar = px.bar(
                cat_rank, x='Sales', y='Category', orientation='h',
                text='Sales', color='Sales', color_continuous_scale='Oranges'
            )
            fig_bar.update_layout(
                yaxis=dict(autorange="reversed"), 
                xaxis=dict(showgrid=False),
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_bar, use_container_width=True)

# ============================================================
# PAGE 2: DEEP DIVE RFM
# ============================================================
elif page == "Deep Dive RFM":
    st.markdown("<h1 class='highlight-text'>Customer Segmentation</h1>", unsafe_allow_html=True)
    st.write("Analisis mendalam karakteristik 3 cluster utama pelanggan menggunakan pendekatan RFM.")

    # Cluster Filter
    selected_cluster_label = st.selectbox("Pilih Segmen:", ["Semua Segmen"] + list(cluster_names.values()))
    
    if selected_cluster_label != "Semua Segmen":
        df_rfm = df[df["Cluster Label"] == selected_cluster_label]
    else:
        df_rfm = df

    # --- ADVANCED RADAR CHART (SPIDER WEB) ---
    st.markdown("### 🕸️ RFM Character Comparison (Radar Chart)")
    st.caption("Membandingkan karakteristik rata-rata tiap cluster. Data dinormalisasi (0-1) untuk visualisasi.")

    # Prepare Data for Radar
    df_radar = df.groupby("Cluster Label")[['Recency', 'Frequency', 'Monetary']].mean()
    
    # Min-Max Normalization agar skala grafik seimbang
    df_normalized = (df_radar - df_radar.min()) / (df_radar.max() - df_radar.min())
    df_normalized = df_normalized.reset_index()

    fig_radar = go.Figure()
    
    # Loop untuk setiap cluster
    colors = ['#95A5A6', '#EF8505', '#3498DB'] # Sesuaikan urutan warna
    
    for i, row in df_normalized.iterrows():
        fig_radar.add_trace(go.Scatterpolar(
            r=[row['Recency'], row['Frequency'], row['Monetary']],
            theta=['Recency (Kebaruan)', 'Frequency (Seringnya)', 'Monetary (Uang)'],
            fill='toself',
            name=row['Cluster Label'],
            line_color=colors[i] if i < 3 else '#EF8505'
        ))

    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=True,
        height=450,
        margin=dict(t=20, b=20)
    )
    st.plotly_chart(fig_radar, use_container_width=True)

    # --- 3D SCATTER & DISTRIBUTION ---
    c_3d, c_dist = st.columns([1.5, 1])

    with c_3d:
        st.subheader("🧊 3D Customer Mapping")
        fig_3d = px.scatter_3d(
            df_rfm, x='Recency', y='Frequency', z='Monetary',
            color='Cluster Label',
            color_discrete_map={v: k for k, v in cluster_colors.items()}, # Logic mapping warna
            opacity=0.6, size_max=10
        )
        fig_3d.update_layout(margin=dict(l=0, r=0, b=0, t=0), height=500)
        st.plotly_chart(fig_3d, use_container_width=True)

    with c_dist:
        st.subheader("📊 Statistik Segmen")
        if selected_cluster_label != "Semua Segmen":
            avg_mon = df_rfm['Monetary'].mean()
            avg_freq = df_rfm['Frequency'].mean()
            avg_rec = df_rfm['Recency'].mean()
            
            st.markdown(f"""
            <div class="metric-card" style="border-left: 5px solid #EF8505;">
                <h4>Rata-rata {selected_cluster_label}</h4>
                <hr>
                <p><b>Monetary:</b> ₺{avg_mon:,.0f}</p>
                <div style="background:#eee; height:8px; border-radius:4px; width:100%; margin-bottom:10px;">
                    <div style="background:#EF8505; height:100%; border-radius:4px; width: {min(100, (avg_mon/df['Monetary'].max())*100)}%;"></div>
                </div>
                
                <p><b>Frequency:</b> {avg_freq:.1f} Transaksi</p>
                <div style="background:#eee; height:8px; border-radius:4px; width:100%; margin-bottom:10px;">
                    <div style="background:#2980B9; height:100%; border-radius:4px; width: {min(100, (avg_freq/df['Frequency'].max())*100)}%;"></div>
                </div>

                <p><b>Recency:</b> {avg_rec:.1f} Hari</p>
                <div style="background:#eee; height:8px; border-radius:4px; width:100%; margin-bottom:10px;">
                    <div style="background:#95A5A6; height:100%; border-radius:4px; width: {min(100, (avg_rec/df['Recency'].max())*100)}%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Pilih salah satu segmen di atas untuk melihat detail statistik spesifik.")

# ============================================================
# PAGE 3: AI PREDICTION (ACTIONABLE)
# ============================================================
elif page == "AI Prediction":
    st.markdown("<h1 class='highlight-text'>Predictive Engine</h1>", unsafe_allow_html=True)
    st.write("Simulasi cerdas untuk menentukan persona pelanggan baru secara Real-Time.")

    if not model_loaded:
        st.warning("⚠️ Model Machine Learning belum dimuat. Pastikan file pickle tersedia.")
        st.stop()

    c_input, c_result = st.columns([1, 2], gap="large")

    with c_input:
        st.markdown("### 📝 Input Parameter")
        with st.container(border=True):
            last_trx = st.date_input("Tanggal Transaksi Terakhir", datetime.today())
            ref_date = st.date_input("Tanggal Referensi", datetime.today())
            
            recency_val = (ref_date - last_trx).days
            if recency_val < 0: st.error("Tanggal referensi harus setelah tanggal transaksi!")
            
            freq_val = st.number_input("Frequency (Kali Belanja)", 1, 500, 5)
            mon_val = st.number_input("Monetary (Total Uang)", 0, 100000000, 500000, step=10000)
            
            predict_btn = st.button("🔍 Analisis Pelanggan")

    with c_result:
        if predict_btn:
            # Prediction Logic
            try:
                X_input = [[recency_val, freq_val, mon_val]]
                X_scaled = scaler.transform(X_input)
                X_pca = pca.transform(X_scaled)
                cluster_pred = kmeans.predict(X_pca)[0]
                
                label_pred = cluster_names[cluster_pred]
                color_pred = cluster_colors[cluster_pred] if cluster_pred in cluster_colors else "#333"
                
                # --- RESULT CARD WITH ANIMATION STYLE ---
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, {color_pred} 0%, {color_pred}88 100%);
                    padding: 40px;
                    border-radius: 20px;
                    color: white;
                    text-align: center;
                    box-shadow: 0 20px 50px rgba(0,0,0,0.2);
                    animation: fadeIn 1s;
                ">
                    <h2 style="margin:0; font-weight:300; opacity:0.9;">Hasil Analisis</h2>
                    <h1 style="font-size: 56px; margin: 10px 0; text-shadow: 0 2px 10px rgba(0,0,0,0.2);">{label_pred}</h1>
                    <hr style="border-color: rgba(255,255,255,0.3);">
                    <p style="font-size: 18px; margin-top:20px;">Rekomendasi Strategi:</p>
                    <div style="background: rgba(255,255,255,0.2); padding: 15px; border-radius: 10px; font-weight: 500;">
                       {
                           "🎯 Berikan Diskon Agresif & Program Reaktivasi" if cluster_pred == 0 else
                           "💎 Tawarkan Program Loyalitas Eksklusif & Early Access" if cluster_pred == 1 else
                           "📈 Tawarkan Bundling Produk & Cross-Selling"
                       }
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # --- GAUGE INDICATOR (Just for Visual Fun) ---
                st.markdown("<br>", unsafe_allow_html=True)
                c_g1, c_g2, c_g3 = st.columns(3)
                c_g1.metric("Recency Score", f"{recency_val} Hari", delta_color="inverse")
                c_g2.metric("Frequency Score", f"{freq_val}x", delta_color="normal")
                c_g3.metric("Monetary Score", format_currency(mon_val), delta_color="normal")

            except Exception as e:
                st.error(f"Error dalam prediksi: {e}")
        else:
            # Placeholder State
            st.markdown("""
            <div style="text-align: center; padding: 50px; opacity: 0.5;">
                <h1 style="font-size: 80px;">🤖</h1>
                <h3>Menunggu Input Data...</h3>
                <p>Masukkan data RFM di panel kiri untuk melihat hasil segmentasi AI.</p>
            </div>
            """, unsafe_allow_html=True)
