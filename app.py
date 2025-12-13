# ============================================================
# CUSTOMER INTELLIGENCE HUB - ADVANCED EXECUTIVE VERSION
# ============================================================

import streamlit as st
import pandas as pd
import pickle
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# 1. PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Customer Intelligence Hub",
    page_icon="🟠",
    layout="wide"
)

# ============================================================
# 2. GLOBAL ORANGE PREMIUM THEME
# ============================================================
st.markdown("""
<style>

/* ---------- GLOBAL ---------- */
.stApp {
    background: linear-gradient(180deg, #FFF7ED 0%, #FFFFFF 40%);
    font-family: 'Inter', sans-serif;
}

/* ---------- SIDEBAR ---------- */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #F97316, #EA580C);
}
[data-testid="stSidebar"] * {
    color: white !important;
}
[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.3);
}

/* ---------- HEADER ---------- */
[data-testid="stHeader"] {
    background: rgba(255,255,255,0.8);
    backdrop-filter: blur(10px);
}

/* ---------- PREMIUM CARDS ---------- */
.premium-card {
    background: linear-gradient(135deg, #FFFFFF, #FFF7ED);
    border-radius: 18px;
    padding: 22px;
    box-shadow: 0 10px 25px rgba(249,115,22,0.18);
    border-left: 6px solid #F97316;
    transition: 0.3s;
}
.premium-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 15px 35px rgba(249,115,22,0.28);
}

.metric-label {
    font-size: 14px;
    color: #7C2D12;
    font-weight: 600;
    text-transform: uppercase;
}
.metric-value {
    font-size: 34px;
    font-weight: 800;
    color: #9A3412;
}

/* ---------- SECTION TITLES ---------- */
.section-title {
    font-size: 26px;
    font-weight: 800;
    color: #9A3412;
}
.section-sub {
    color: #78350F;
    font-size: 15px;
}

/* ---------- BUTTON ---------- */
.stButton>button {
    background: linear-gradient(135deg, #F97316, #EA580C);
    color: white;
    border-radius: 12px;
    font-weight: 700;
    border: none;
    padding: 0.6rem 1.2rem;
}
.stButton>button:hover {
    background: linear-gradient(135deg, #EA580C, #C2410C);
}

/* ---------- TABS ---------- */
.stTabs [data-baseweb="tab"] {
    font-weight: 700;
    color: #7C2D12;
}
.stTabs [aria-selected="true"] {
    background-color: #FFEDD5;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# 3. SIDEBAR
# ============================================================
with st.sidebar:
    try:
        st.image("image/alllogo.png", width=200)
    except:
        pass

    st.markdown("## 🧭 Navigation")
    page = st.radio(
        "",
        ["Executive Overview", "Dashboard RFM", "Prediksi & Insight"],
        index=0
    )
    st.markdown("---")
    st.caption("© 2025 Customer Intelligence System")

# ============================================================
# 4. LOAD DATA
# ============================================================
df = pd.read_excel("dataset/data_with_cluster.xlsx")
df2 = pd.read_csv("dataset/flo_data_20k.csv")
df["first_order_date"] = pd.to_datetime(df["first_order_date"])

# ============================================================
# 5. LOAD MODEL
# ============================================================
scaler = pickle.load(open("model/scaler.pkl", "rb"))
pca = pickle.load(open("model/pca.pkl", "rb"))
kmeans = pickle.load(open("model/kmeans.pkl", "rb"))

cluster_names = {
    0: "Low Value / Inactive",
    1: "High Value / Loyal",
    2: "Medium / Potential"
}

recommendation_text = {
    0: "Reaktivasi agresif dengan voucher & urgency campaign.",
    1: "Program VIP, loyalty premium, early access.",
    2: "Upselling & bundling untuk naik kelas."
}

df["Cluster Label"] = df["Cluster"].map(cluster_names)

# ============================================================
# PAGE 1 – EXECUTIVE OVERVIEW
# ============================================================
if page == "Executive Overview":

    st.markdown("<div class='section-title'>🟠 Customer Intelligence Hub</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>From Mass Marketing to Precision Strategy</div>", unsafe_allow_html=True)
    st.divider()

    total_orders = df["order_num_total_ever_online"].sum() + df["order_num_total_ever_offline"].sum()
    total_revenue = df["Monetary"].sum()

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div class="premium-card">
            <div class="metric-label">Total Customers</div>
            <div class="metric-value">{df2.shape[0]:,}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="premium-card">
            <div class="metric-label">Total Orders</div>
            <div class="metric-value">{total_orders:,}</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="premium-card">
            <div class="metric-label">Total Revenue</div>
            <div class="metric-value">₺{total_revenue/1e6:.1f}M</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    tab1, tab2 = st.tabs(["📈 Growth & Channel", "🧩 Category Insights"])

    with tab1:
        df_month = df.set_index("first_order_date").resample("M").size().reset_index(name="New Customer")
        fig_line = px.line(
            df_month,
            x="first_order_date",
            y="New Customer",
            markers=True,
            color_discrete_sequence=["#F97316"]
        )
        fig_line.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_line, use_container_width=True)

        fig_pie = px.pie(
            df,
            names="order_channel",
            hole=0.55,
            color_discrete_sequence=px.colors.sequential.Oranges
        )
        fig_pie.update_traces(textinfo="percent+label")
        st.plotly_chart(fig_pie, use_container_width=True)

    with tab2:
        def clean_list(x):
            if isinstance(x, str):
                return [i.strip().replace("'", "") for i in x.strip("[]").split(",")]
            return []

        df_cat = df.copy()
        df_cat["cat"] = df_cat["interested_in_categories_12"].apply(clean_list)
        df_exp = df_cat.explode("cat")
        cat = df_exp["cat"].value_counts().head(6).sort_values()

        fig_cat = px.bar(
            cat,
            orientation="h",
            color=cat.values,
            color_continuous_scale=px.colors.sequential.Oranges
        )
        fig_cat.update_layout(showlegend=False)
        st.plotly_chart(fig_cat, use_container_width=True)

# ============================================================
# PAGE 2 – DASHBOARD RFM
# ============================================================
elif page == "Dashboard RFM":

    st.markdown("<div class='section-title'>📊 RFM Deep Dive</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Behavioral Segmentation Analysis</div>", unsafe_allow_html=True)
    st.divider()

    selected = st.selectbox(
        "Pilih Cluster",
        ["All"] + list(df["Cluster Label"].unique())
    )

    df_rfm = df if selected == "All" else df[df["Cluster Label"] == selected]

    k1, k2, k3 = st.columns(3)
    k1.metric("Avg Recency", f"{df_rfm['Recency'].mean():.1f} days")
    k2.metric("Avg Frequency", f"{df_rfm['Frequency'].mean():.1f}")
    k3.metric("Avg Monetary", f"₺{df_rfm['Monetary'].mean():,.0f}")

    fig_3d = px.scatter_3d(
        df_rfm,
        x="Recency",
        y="Frequency",
        z="Monetary",
        color="Cluster Label",
        opacity=0.7,
        color_discrete_sequence=["#9A3412", "#F97316", "#FDBA74"]
    )
    st.plotly_chart(fig_3d, use_container_width=True)

# ============================================================
# PAGE 3 – PREDIKSI & INSIGHT
# ============================================================
else:

    st.markdown("<div class='section-title'>🤖 AI Customer Predictor</div>", unsafe_allow_html=True)
    st.divider()

    col1, col2 = st.columns([1,1.5])

    with col1:
        last = st.date_input("Last Transaction Date")
        today = st.date_input("Today", datetime.today())
        rec = (today - last).days
        freq = st.number_input("Frequency", 1, 100, 5)
        mon = st.number_input("Monetary", 0, 100_000_000, 500_000)
        run = st.button("Analyze")

    with col2:
        if run:
            X = [[rec, freq, mon]]
            pred = kmeans.predict(pca.transform(scaler.transform(X)))[0]
            label = cluster_names[pred]

            st.markdown(f"""
            <div class="premium-card">
                <h2 style="color:#F97316">{label}</h2>
                <p>{recommendation_text[pred]}</p>
            </div>
            """, unsafe_allow_html=True)
