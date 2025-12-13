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
    page_icon="🍊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================
# 2. ULTRA-AESTHETIC CSS (Theme: Modern Citrus & Dark Luxury)
# ======================
st.markdown("""
    <style>
        /* --- Import Font Modern: Outfit (Lebih sleek dari Poppins) --- */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

        /* --- Global Reset & Font --- */
        html, body, [class*="css"] {
            font-family: 'Outfit', sans-serif;
            color: #2C3E50;
        }

        /* --- BACKGROUND APP --- */
        .stApp {
            background-color: #FDFBF7; /* Cream sangat muda, hangat, nyaman di mata */
        }

        /* --- SIDEBAR: The Masterpiece --- */
        [data-testid="stSidebar"] {
            /* Gradasi Oranye Murni (Tangerine to Gold) - BUKAN MERAH */
            background: linear-gradient(135deg, #FF6B00 0%, #FF9E2C 100%);
            box-shadow: 5px 0 15px rgba(0,0,0,0.1);
        }
        
        /* Sidebar Text Elements */
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, 
        [data-testid="stSidebar"] span, [data-testid="stSidebar"] label, [data-testid="stSidebar"] div {
            color: #FFFFFF !important;
            text-shadow: 0 1px 2px rgba(0,0,0,0.1);
        }

        /* Customizing Radio Buttons di Sidebar (Menu Style) */
        .stRadio > div {
            background-color: rgba(255, 255, 255, 0.15); /* Efek Kaca Transparan */
            backdrop-filter: blur(10px);
            padding: 15px;
            border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.2);
            color: white;
        }
        
        /* Highlight item yang dipilih */
        .stRadio div[role='radiogroup'] > label[data-baseweb="radio"] {
            background-color: transparent;
            margin-bottom: 5px;
            padding: 8px;
            border-radius: 8px;
            transition: all 0.3s ease;
        }
        
        .stRadio div[role='radiogroup'] > label[data-baseweb="radio"]:hover {
            background-color: rgba(255,255,255,0.2);
        }

        /* --- HEADER & TITLES --- */
        [data-testid="stHeader"] {
            background-color: transparent !important;
        }
        
        /* Judul Halaman dengan Gradient Text Effect */
        h1, h2, h3 {
            background: -webkit-linear-gradient(0deg, #E65100, #FF9800);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800 !important;
            letter-spacing: -0.5px;
        }

        /* --- PREMIUM CARD DESIGN (Kotak Info) --- */
        .premium-card {
            background: #FFFFFF;
            border-radius: 20px;
            padding: 25px;
            /* Shadow Halus tapi Mewah */
            box-shadow: 0 10px 40px rgba(255, 107, 0, 0.08);
            border: 1px solid rgba(0,0,0,0.02);
            position: relative;
            overflow: hidden;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        /* Aksen Garis Oranye di Atas Kartu (Bukan di kiri, biar lebih modern) */
        .premium-card::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 6px;
            background: linear-gradient(90deg, #FF6B00, #FFB74D);
        }

        .premium-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 50px rgba(255, 107, 0, 0.15);
        }

        /* --- METRIC TYPOGRAPHY --- */
        .metric-label {
            font-size: 14px;
            color: #8C8C8C;
            font-weight: 500;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            margin-bottom: 5px;
        }

        .metric-value {
            font-size: 36px;
            color: #2D3436;
            font-weight: 700;
            letter-spacing: -1px;
        }

        /* --- BUTTONS CUSTOMIZATION --- */
        /* Mengubah warna tombol bawaan streamlit jadi oranye */
        .stButton > button {
            background: linear-gradient(90deg, #FF6B00 0%, #FF8F00 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            transition: 0.3s;
        }
        .stButton > button:hover {
            box-shadow: 0 5px 15px rgba(255, 107, 0, 0.4);
            transform: scale(1.02);
        }

    </style>
""", unsafe_allow_html=True)


# ======================
# 3. SIDEBAR NAVIGATION
# ======================
with st.sidebar:
    st.markdown('<div style="text-align: center; margin-top: 20px; margin-bottom: 30px;">', unsafe_allow_html=True)
    # Placeholder Logo (Ganti path logo kamu di sini)
    try:
        st.image("image/alllogo.png", width=200) 
    except:
        # Fallback jika logo error: Icon + Text
        st.markdown("""
            <h1 style='color: white !important; font-size: 60px; margin:0;'>🍊</h1>
            <h3 style='color: white !important; margin:0;'>CRM PRO</h3>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<p style='font-size: 12px; color: rgba(255,255,255,0.7); font-weight: 600; margin-bottom: 10px;'>MAIN MENU</p>", unsafe_allow_html=True)
    
    # Navigasi
    page = st.sidebar.radio(
        "",
        ["Executive Overview", "Dashboard RFM", "Prediksi & Insight"],
        index=0,
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Footer Elegan
    st.markdown("""
        <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 12px; text-align: center;">
            <p style="margin: 0; font-size: 13px; font-weight: 600;">Analyst Team</p>
            <p style="margin: 0; font-size: 11px; opacity: 0.7;">© 2025 Data Intelligence</p>
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
    st.stop()

# Load Models
try:
    scaler = pickle.load(open("model/scaler.pkl", "rb"))
    pca = pickle.load(open("model/pca.pkl", "rb"))
    kmeans = pickle.load(open("model/kmeans.pkl", "rb"))
except Exception:
    st.warning("⚠️ Model (scaler.pkl, pca.pkl, kmeans.pkl) belum ditemukan.")

# Mapping Nama Cluster & Rekomendasi
cluster_names = {
    0: "Low Value / Inactive",
    1: "High Value / Loyal",
    2: "Medium / Potential"
}
recommendation_text = {
    0: "🔍 <b>Reaktivasi:</b> Kirim voucher 'We Miss You', diskon urgensi tinggi.",
    1: "💎 <b>Retensi VIP:</b> Reward eksklusif, early access, layanan prioritas.",
    2: "📈 <b>Upselling:</b> Tawarkan bundling produk, program poin loyalty."
}


# ============================================================
# PAGE 1: EXECUTIVE OVERVIEW 
# ============================================================
if page == "Executive Overview":
    
    # --- HERO SECTION ---
    st.markdown("<h1 style='margin-bottom: 10px;'>👋 Welcome Back, Chief!</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 18px; color: #7F8C8D; margin-bottom: 30px;'>Here is your customer intelligence update for today.</p>", unsafe_allow_html=True)
    
    # --- TOP LEVEL METRICS (REVISED) ---
    total_orders_all = df['order_num_total_ever_online'].sum() + df['order_num_total_ever_offline'].sum()
    
    m1, m2, m3 = st.columns(3)
    
    with m1:
        st.markdown(f"""
        <div class="premium-card">
            <div class="metric-label">👥 Total Active Customers</div>
            <div class="metric-value">{df2.shape[0]:,}</div>
            <div style="font-size: 12px; color: #27AE60; margin-top: 5px;">▲ 12% vs last month</div>
        </div>
        """, unsafe_allow_html=True)
        
    with m2:
        st.markdown(f"""
        <div class="premium-card">
            <div class="metric-label">📦 Total Transactions</div>
            <div class="metric-value">{total_orders_all:,}</div>
            <div style="font-size: 12px; color: #27AE60; margin-top: 5px;">Online & Offline Combined</div>
        </div>
        """, unsafe_allow_html=True)

    with m3:
        st.markdown(f"""
        <div class="premium-card">
            <div class="metric-label">💰 Total Revenue Generated</div>
            <div class="metric-value">₺{df['Monetary'].sum()/1000000:.1f}M</div>
             <div style="font-size: 12px; color: #E67E22; margin-top: 5px;">Key Performance Indicator</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.write("") # Spacer

    # --- TABS FOR CONTENT ---
    tab1, tab2, tab3 = st.tabs(["🎯 Strategy Board", "📂 Data Explorer", "📈 Visual Analytics"])

    with tab1:
        st.markdown("### Why Segmentation Matters?")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.info("**1. Cost Efficiency**\nStop burning money on mass marketing. Target only those who matter.")
        with c2:
            st.warning("**2. Personalization**\nLoyal customers need rewards, inactive ones need urgency.")
        with c3:
            st.success("**3. Higher ROI**\nTargeted campaigns have proven to increase conversion by 3x.")

    with tab2:
        st.subheader("Master Database")
        st.dataframe(
            df2.head(10),
            use_container_width=True,
            column_config={
                "customer_value_total_ever_online": st.column_config.NumberColumn("Online Spend", format="₺ %.2f"),
                "customer_value_total_ever_offline": st.column_config.NumberColumn("Offline Spend", format="₺ %.2f")
            }
        )

    # --- VISUAL OVERVIEW (UPDATED) ---
    with tab3:
        st.subheader("Performance Visualizer")
        
        # Filter Logic (Sama seperti sebelumnya)
        min_date = df['first_order_date'].min().date()
        max_date = df['first_order_date'].max().date()
        
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            start_date = st.date_input("Start Date", value=min_date, min_value=min_date, max_value=max_date)
        with col_f2:
            end_date = st.date_input("End Date", value=max_date, min_value=min_date, max_value=max_date)
            
        mask = (df['first_order_date'].dt.date >= start_date) & (df['first_order_date'].dt.date <= end_date)
        df_filtered = df.loc[mask]

        if not df_filtered.empty:
            st.write("")
            col_viz1, col_viz2 = st.columns(2)
            
            # Chart 1: Line Chart
            with col_viz1:
                st.markdown("##### 📈 Growth Trend")
                df_trend = df_filtered.set_index('first_order_date').resample('MS').size().reset_index(name='count')
                fig_line = px.line(df_trend, x='first_order_date', y='count', markers=True, 
                                   color_discrete_sequence=["#FF6B00"])
                # Update Layout agar transparan dan elegan
                fig_line.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_line, use_container_width=True)

            # Chart 2: Pie Chart
            with col_viz2:
                st.markdown("##### 🥧 Channel Mix")
                fig_pie = px.pie(df_filtered, names='order_channel', color='order_channel', 
                                 color_discrete_sequence=px.colors.sequential.Oranges_r, hole=0.5)
                fig_pie.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_pie, use_container_width=True)
                
            # Chart 3 & 4 (Bar Charts)
            col_viz3, col_viz4 = st.columns(2)
            
            with col_viz3:
                st.markdown("##### 📦 Transaction Volume")
                # Data Prep
                data_vol = pd.DataFrame({
                    'Channel': ['Online', 'Offline'],
                    'Total': [df_filtered['order_num_total_ever_online'].sum(), df_filtered['order_num_total_ever_offline'].sum()]
                })
                fig_vol = px.bar(data_vol, x='Total', y='Channel', orientation='h', text='Total',
                                 color='Channel', color_discrete_map={'Online': '#FF8F00', 'Offline': '#2D3436'})
                fig_vol.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', showlegend=False)
                st.plotly_chart(fig_vol, use_container_width=True)
                
            with col_viz4:
                st.markdown("##### 💰 Revenue Split")
                data_rev = pd.DataFrame({
                    'Channel': ['Online', 'Offline'],
                    'Rev': [df_filtered['customer_value_total_ever_online'].sum(), df_filtered['customer_value_total_ever_offline'].sum()]
                })
                fig_rev = px.bar(data_rev, x='Rev', y='Channel', orientation='h', text='Rev',
                                 color='Channel', color_discrete_map={'Online': '#FF8F00', 'Offline': '#2D3436'})
                fig_rev.update_traces(texttemplate='₺%{text:.2s}')
                fig_rev.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', showlegend=False)
                st.plotly_chart(fig_rev, use_container_width=True)


# ============================================================
# PAGE 2: DASHBOARD RFM
# ============================================================
elif page == "Dashboard RFM":
    st.markdown("<h1>📊 RFM Deep Dive Analysis</h1>", unsafe_allow_html=True)
    
    # 0. Prep
    if "Cluster" in df.columns:
        df["Cluster Label"] = df["Cluster"].map(cluster_names)
    
    # 1. Filter
    with st.container(border=True):
        col_s1, col_s2 = st.columns([1, 3])
        with col_s1:
            st.markdown("### 🏷️ Filter Segment")
        with col_s2:
            cluster_options = ["Semua Cluster"] + list(df["Cluster Label"].unique())
            selected_cluster = st.selectbox("", options=cluster_options, label_visibility="collapsed")

    if selected_cluster == "Semua Cluster":
        df_rfm = df.copy() 
    else:
        df_rfm = df[df["Cluster Label"] == selected_cluster] 

    st.write("")

    # 2. KPI Cards (Updated Design)
    if not df_rfm.empty:
        avg_recency = df_rfm["Recency"].mean()
        avg_freq = df_rfm["Frequency"].mean()
        avg_monetary = df_rfm["Monetary"].mean()

        k1, k2, k3 = st.columns(3)
        with k1:
            st.markdown(f"""
            <div class="premium-card">
                <div class="metric-label">🕒 Avg. Recency</div>
                <div class="metric-value">{avg_recency:.0f} Days</div>
                <small style="color: #95A5A6;">Time since last purchase</small>
            </div>
            """, unsafe_allow_html=True)
        with k2:
            st.markdown(f"""
            <div class="premium-card">
                <div class="metric-label">🔄 Avg. Frequency</div>
                <div class="metric-value">{avg_freq:.1f} Orders</div>
                <small style="color: #95A5A6;">Transactions per customer</small>
            </div>
            """, unsafe_allow_html=True)
        with k3:
            st.markdown(f"""
            <div class="premium-card">
                <div class="metric-label">💸 Avg. Monetary</div>
                <div class="metric-value">₺{avg_monetary:,.0f}</div>
                <small style="color: #95A5A6;">Average spending value</small>
            </div>
            """, unsafe_allow_html=True)
    
    st.divider()

    # 3. Charts Area
    c_main1, c_main2 = st.columns([1.5, 1])
    
    with c_main1:
        st.subheader("🧊 3D Cluster Distribution")
        color_map = {
            "Low Value / Inactive": "#BDC3C7", 
            "High Value / Loyal": "#FF6B00",     
            "Medium / Potential": "#3498DB"
        }
        fig_3d = px.scatter_3d(df_rfm, x='Recency', y='Frequency', z='Monetary', color='Cluster Label',
                               color_discrete_map=color_map, opacity=0.8, height=500)
        fig_3d.update_layout(margin=dict(l=0, r=0, b=0, t=0), scene=dict(bgcolor='#FDFBF7'))
        st.plotly_chart(fig_3d, use_container_width=True)
        
    with c_main2:
        st.subheader("🏆 Top Categories")
        # Reuse Logic Cleaning
        def clean_list(x):
            if isinstance(x, str):
                x = x.strip("[]")
                return [i.strip().replace("'", "") for i in x.split(",")]
            return []

        if "interested_in_categories_12" in df_rfm.columns:
            df_cat = df_rfm.copy()
            df_cat["categories"] = df_cat["interested_in_categories_12"].apply(clean_list)
            df_exploded = df_cat.explode("categories")
            cat_counts = df_exploded["categories"].value_counts().reset_index()
            cat_counts.columns = ['Category', 'Count']
            
            fig_cat = px.bar(cat_counts.head(5).sort_values('Count'), x='Count', y='Category', orientation='h',
                             color='Count', color_continuous_scale='Oranges')
            fig_cat.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', showlegend=False)
            st.plotly_chart(fig_cat, use_container_width=True)

# ============================================================
# PAGE 3: PREDIKSI & INSIGHT
# ============================================================
elif page == "Prediksi & Insight":
    st.markdown("<h1 style='text-align: center; margin-bottom: 40px;'>🤖 AI Prediction Engine</h1>", unsafe_allow_html=True)
    
    col_input, col_res = st.columns([1, 2], gap="large")
    
    with col_input:
        st.markdown("""
        <div style="background: white; padding: 20px; border-radius: 15px; box-shadow: 0 5px 20px rgba(0,0,0,0.05);">
            <h4 style="margin-top:0;">Input Customer Data</h4>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        start_date = st.date_input("Last Transaction Date")
        end_date = st.date_input("Current Date", datetime.today())
        recency = (end_date - start_date).days
        
        freq = st.slider("Frequency (Total Transactions)", 1, 100, 5)
        mon = st.number_input("Monetary (Total Spend)", 0, 100000000, 500000)
        
        st.markdown("---")
        run_btn = st.button("🚀 Analyze Customer Profile", type="primary", use_container_width=True)

    with col_res:
        if run_btn:
            try:
                # Prediksi
                X = [[recency, freq, mon]]
                X_scaled = scaler.transform(X)
                X_pca = pca.transform(X_scaled)
                pred = kmeans.predict(X_pca)[0]
                
                label = cluster_names[pred]
                desc = recommendation_text[pred]
                
                # Dynamic Color for Result
                res_color = "#FF6B00" if pred == 1 else ("#3498DB" if pred == 2 else "#95A5A6")
                
                # Result Card
                st.markdown(f"""
                <div style="background: white; border-radius: 20px; padding: 40px; text-align: center; box-shadow: 0 10px 40px rgba(0,0,0,0.1); border-top: 8px solid {res_color};">
                    <h3 style="color: #7F8C8D; text-transform: uppercase; font-size: 14px; letter-spacing: 2px;">AI Segmentation Result</h3>
                    <h1 style="color: {res_color}; font-size: 48px; margin: 10px 0;">{label}</h1>
                    <hr style="margin: 20px auto; width: 50%; border-top: 1px solid #eee;">
                    <div style="background: #FDFBF7; padding: 20px; border-radius: 10px; border-left: 5px solid {res_color}; text-align: left;">
                        <h4 style="margin:0; color: {res_color};">💡 Actionable Strategy:</h4>
                        <p style="margin-top: 5px; font-size: 16px;">{desc}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.write("")
                
                # Detail Metrics Row
                m1, m2, m3 = st.columns(3)
                m1.metric("Recency", f"{recency} Days")
                m2.metric("Frequency", f"{freq} Orders")
                m3.metric("Monetary", f"₺{mon:,.0f}")
                
            except Exception as e:
                st.error("Model belum dimuat. Pastikan file pickle ada di folder model/.")
        else:
            # Empty State (Tampilan awal sebelum dipencet)
            st.markdown("""
            <div style="text-align: center; padding: 50px; opacity: 0.5;">
                <h2>👈 Enter data to see magic happen</h2>
                <p>Our AI will analyze the RFM pattern and suggest the best marketing action.</p>
            </div>
            """, unsafe_allow_html=True)
