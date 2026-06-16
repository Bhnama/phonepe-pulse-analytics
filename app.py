import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sqlite3
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline
import warnings
warnings.filterwarnings("ignore")

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PhonePe Pulse Analytics",
    page_icon="💜",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.main { background: #0f0f1a; }
[data-testid="stSidebar"] { background: #1a1a2e; border-right: 1px solid #2d2d4e; }
[data-testid="stSidebar"] * { color: #e0e0ff !important; }

.kpi-card {
    background: linear-gradient(135deg, #1e1e3f 0%, #2d2d5e 100%);
    border: 1px solid #5b2d8e;
    border-radius: 16px;
    padding: 20px 24px;
    text-align: center;
    box-shadow: 0 4px 24px rgba(91,45,142,0.3);
    transition: transform 0.2s;
}
.kpi-card:hover { transform: translateY(-3px); }
.kpi-label { font-size: 12px; color: #a78bfa; font-weight: 600; letter-spacing: 1.2px; text-transform: uppercase; }
.kpi-value { font-size: 28px; font-weight: 700; color: #ffffff; margin: 6px 0 2px; }
.kpi-delta { font-size: 12px; color: #34d399; }

.section-title {
    font-size: 20px; font-weight: 700; color: #c4b5fd;
    border-left: 4px solid #7c3aed;
    padding-left: 12px; margin: 24px 0 12px;
}

.insight-box {
    background: #1a1a2e;
    border-left: 3px solid #7c3aed;
    border-radius: 8px;
    padding: 14px 18px;
    margin: 8px 0;
    color: #d1d5db;
    font-size: 14px;
}

div[data-testid="stSelectbox"] > div { background: #1e1e3f; border: 1px solid #4c1d95; border-radius: 8px; }
div[data-testid="stSlider"] { padding: 4px 0; }
</style>
""", unsafe_allow_html=True)

# ── Data loading ───────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    xl = pd.ExcelFile("data/phonepe_data.xlsx")
    state_txn   = pd.read_excel(xl, "State_Txn and Users")
    state_split = pd.read_excel(xl, "State_TxnSplit")
    state_dev   = pd.read_excel(xl, "State_DeviceData")
    dist_txn    = pd.read_excel(xl, "District_Txn and Users")
    dist_demo   = pd.read_excel(xl, "District Demographics")
    return state_txn, state_split, state_dev, dist_txn, dist_demo

@st.cache_resource
def build_sqlite(state_txn, state_split, state_dev, dist_txn, dist_demo):
    return {
        "state_txn": state_txn,
        "state_split": state_split,
        "state_dev": state_dev,
        "dist_txn": dist_txn,
        "dist_demo": dist_demo,
    }

state_txn, state_split, state_dev, dist_txn, dist_demo = load_data()
sql_tables = build_sqlite(state_txn, state_split, state_dev, dist_txn, dist_demo)

def run_query(sql):
    with sqlite3.connect(":memory:") as temp_conn:
        for table_name, df in sql_tables.items():
            df.to_sql(table_name, temp_conn, if_exists="replace", index=False)
        return pd.read_sql_query(sql, temp_conn)

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 💜 PhonePe Pulse")
    st.markdown("##### India Digital Payments Analytics")
    st.markdown("---")
    page = st.radio("Navigate", [
        "🏠 Overview",
        "📊 State Analysis",
        "🗺️ India Map",
        "📱 Device Insights",
        "🤖 ML Forecast",
        "🗄️ SQL Explorer",
    ])
    st.markdown("---")
    st.markdown("**Dataset**")
    st.caption(f"States: {state_txn['State'].nunique()}")
    st.caption(f"Districts: {dist_txn['District'].nunique()}")
    st.caption(f"Period: Q1 2018 – Q2 2021")
    st.caption(f"Records: {len(state_txn):,} state rows")

# ── Helper: plotly dark theme ──────────────────────────────────────────────────
DARK = dict(
    plot_bgcolor="#0f0f1a",
    paper_bgcolor="#0f0f1a",
    font_color="#e0e0ff",
    xaxis=dict(gridcolor="#2d2d4e", zerolinecolor="#2d2d4e"),
    yaxis=dict(gridcolor="#2d2d4e", zerolinecolor="#2d2d4e"),
)

PURPLE_SEQ = px.colors.sequential.Purples
ACCENT = ["#7c3aed","#a78bfa","#34d399","#f59e0b","#f87171","#38bdf8"]

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 – OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
if page == "🏠 Overview":
    st.markdown("<h1 style='color:#c4b5fd;font-size:2rem;'>💜 PhonePe Pulse — India Digital Payments</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#9ca3af;'>Comprehensive analytics dashboard · Q1 2018 to Q2 2021</p>", unsafe_allow_html=True)

    # KPI row
    total_txn   = state_txn["Transactions"].sum()
    total_amt   = state_txn["Amount (INR)"].sum()
    total_users = state_txn["Registered Users"].max() * state_txn["State"].nunique()
    total_opens = state_txn["App Opens"].sum()

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-label">Total Transactions</div>
            <div class="kpi-value">{total_txn/1e9:.2f}B</div>
            <div class="kpi-delta">↑ Across all states</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-label">Total Amount</div>
            <div class="kpi-value">₹{total_amt/1e12:.2f}T</div>
            <div class="kpi-delta">↑ In INR</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-label">States Covered</div>
            <div class="kpi-value">{state_txn['State'].nunique()}</div>
            <div class="kpi-delta">↑ All Indian states</div></div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-label">App Opens</div>
            <div class="kpi-value">{total_opens/1e9:.2f}B</div>
            <div class="kpi-delta">↑ Total sessions</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # National trend
    st.markdown("<div class='section-title'>📈 National Transaction Growth</div>", unsafe_allow_html=True)
    nat = state_txn.groupby(["Year","Quarter"])[["Transactions","Amount (INR)"]].sum().reset_index()
    nat["Period"] = nat["Year"].astype(str) + " Q" + nat["Quarter"].astype(str)

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(
        x=nat["Period"], y=nat["Transactions"]/1e6,
        mode="lines+markers", name="Transactions (M)",
        line=dict(color="#7c3aed", width=3),
        marker=dict(size=8, color="#a78bfa"),
        fill="tozeroy", fillcolor="rgba(124,58,237,0.12)"
    ), secondary_y=False)
    fig.add_trace(go.Scatter(
        x=nat["Period"], y=nat["Amount (INR)"]/1e9,
        mode="lines+markers", name="Amount (B INR)",
        line=dict(color="#34d399", width=3, dash="dot"),
        marker=dict(size=8, color="#34d399")
    ), secondary_y=True)
    fig.update_layout(**DARK, height=380, legend=dict(bgcolor="#1a1a2e"),
                      title=dict(text="Transactions & Amount Over Time", font=dict(color="#c4b5fd")))
    fig.update_yaxes(title_text="Transactions (Millions)", secondary_y=False, color="#a78bfa")
    fig.update_yaxes(title_text="Amount (Billion ₹)", secondary_y=True, color="#34d399")
    st.plotly_chart(fig, use_container_width=True)

    # Transaction type split
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='section-title'>💳 Transaction Type Split</div>", unsafe_allow_html=True)
        txn_type = state_split.groupby("Transaction Type")["Transactions"].sum().reset_index()
        fig2 = px.pie(txn_type, values="Transactions", names="Transaction Type",
                      color_discrete_sequence=ACCENT, hole=0.45)
        fig2.update_layout(**DARK, height=360, showlegend=True,
                           legend=dict(bgcolor="#1a1a2e"),
                           annotations=[dict(text="PhonePe", x=0.5, y=0.5,
                                            font_size=16, font_color="#c4b5fd", showarrow=False)])
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        st.markdown("<div class='section-title'>📱 Top Device Brands</div>", unsafe_allow_html=True)
        brand_agg = state_dev.groupby("Brand")["Registered Users"].sum().nlargest(8).reset_index()
        fig3 = px.bar(brand_agg, x="Registered Users", y="Brand", orientation="h",
                      color="Registered Users", color_continuous_scale="Purples")
        fig3.update_layout(**{**DARK, "height":360, "coloraxis_showscale":False,
                              "yaxis": {**DARK["yaxis"], "categoryorder":"total ascending"}})
        st.plotly_chart(fig3, use_container_width=True)

    # Key insights
    st.markdown("<div class='section-title'>💡 Key Insights</div>", unsafe_allow_html=True)
    top_state = state_txn.groupby("State")["Transactions"].sum().idxmax()
    top_brand = state_dev.groupby("Brand")["Registered Users"].sum().idxmax()
    growth = ((nat["Transactions"].iloc[-1] - nat["Transactions"].iloc[0]) / nat["Transactions"].iloc[0] * 100)
    for insight in [
        f"🚀 Transactions grew by <b>{growth:.0f}%</b> from Q1 2018 to Q2 2021 — driven by COVID-19 accelerating digital adoption.",
        f"🏆 <b>{top_state}</b> leads all states in total transaction volume across the entire period.",
        f"📱 <b>{top_brand}</b> devices dominate PhonePe registrations, reflecting India's budget smartphone boom.",
        "💸 Peer-to-peer payments account for the largest share of all transactions across every state.",
        "🌆 Higher population density districts show a positive correlation with transaction volume.",
    ]:
        st.markdown(f"<div class='insight-box'>{insight}</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 – STATE ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📊 State Analysis":
    st.markdown("<h1 style='color:#c4b5fd;'>📊 State-Level Analysis</h1>", unsafe_allow_html=True)

    states_list = sorted(state_txn["State"].unique())
    sel_state   = st.selectbox("Select a state", states_list, index=states_list.index("Maharashtra"))

    # KPIs for selected state
    s = state_txn[state_txn["State"] == sel_state]
    c1, c2, c3, c4 = st.columns(4)
    metrics = [
        ("Total Transactions", f"{s['Transactions'].sum()/1e6:.1f}M", "All quarters"),
        ("Total Amount",       f"₹{s['Amount (INR)'].sum()/1e9:.1f}B", "In INR"),
        ("Peak Users",         f"{s['Registered Users'].max()/1e6:.2f}M", "Single quarter peak"),
        ("Avg ATV",            f"₹{s['ATV (INR)'].mean():,.0f}", "Average txn value"),
    ]
    for col, (label, val, delta) in zip([c1,c2,c3,c4], metrics):
        with col:
            st.markdown(f"""<div class="kpi-card">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{val}</div>
                <div class="kpi-delta">{delta}</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Trend chart for state
    s2 = s.copy()
    s2["Period"] = s2["Year"].astype(str) + " Q" + s2["Quarter"].astype(str)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='section-title'>📈 Transactions Over Time</div>", unsafe_allow_html=True)
        fig = px.area(s2, x="Period", y="Transactions",
                      color_discrete_sequence=["#7c3aed"],
                      title=f"{sel_state} – Quarterly Transactions")
        fig.update_layout(**DARK, height=320)
        fig.update_traces(fillcolor="rgba(124,58,237,0.2)", line_width=2.5)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("<div class='section-title'>💰 App Opens vs Registered Users</div>", unsafe_allow_html=True)
        fig2 = make_subplots(specs=[[{"secondary_y": True}]])
        fig2.add_trace(go.Bar(x=s2["Period"], y=s2["Registered Users"]/1e6,
                              name="Reg. Users (M)", marker_color="#7c3aed", opacity=0.7), secondary_y=False)
        fig2.add_trace(go.Scatter(x=s2["Period"], y=s2["App Opens"]/1e6,
                                  mode="lines+markers", name="App Opens (M)",
                                  line=dict(color="#34d399", width=2.5)), secondary_y=True)
        fig2.update_layout(**DARK, height=320, legend=dict(bgcolor="#1a1a2e"))
        st.plotly_chart(fig2, use_container_width=True)

    # Transaction type for state
    st.markdown("<div class='section-title'>💳 Transaction Types Breakdown</div>", unsafe_allow_html=True)
    sp = state_split[state_split["State"] == sel_state].copy()
    sp["Period"] = sp["Year"].astype(str) + " Q" + sp["Quarter"].astype(str)
    fig3 = px.bar(sp, x="Period", y="Transactions", color="Transaction Type",
                  color_discrete_sequence=ACCENT, barmode="stack")
    fig3.update_layout(**DARK, height=360, legend=dict(bgcolor="#1a1a2e"))
    st.plotly_chart(fig3, use_container_width=True)

    # Top vs Bottom states comparison
    st.markdown("<div class='section-title'>🏆 All States Ranked</div>", unsafe_allow_html=True)
    agg = state_txn.groupby("State")["Transactions"].sum().reset_index().sort_values("Transactions")
    agg["Color"] = agg["State"].apply(lambda x: "#7c3aed" if x == sel_state else "#4c1d95")
    fig4 = px.bar(agg, x="Transactions", y="State", orientation="h",
                  color="Color", color_discrete_map="identity")
    fig4.update_layout(**DARK, height=700, showlegend=False)
    st.plotly_chart(fig4, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 – INDIA MAP
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🗺️ India Map":
    st.markdown("<h1 style='color:#c4b5fd;'>🗺️ India Choropleth Map</h1>", unsafe_allow_html=True)

    metric_choice = st.selectbox("Map metric", ["Transactions", "Amount (INR)", "Registered Users", "App Opens"])
    year_choice   = st.selectbox("Year", sorted(state_txn["Year"].unique()))

    map_df = state_txn[state_txn["Year"] == year_choice].groupby("State")[metric_choice].sum().reset_index()

    # GeoJSON for India states
    import urllib.request, json
    GEOJSON_URL = "https://raw.githubusercontent.com/geohacker/india/master/state/india_telengana.geojson"

    @st.cache_data
    def load_geojson():
        try:
            with urllib.request.urlopen(GEOJSON_URL, timeout=5) as r:
                return json.loads(r.read())
        except Exception:
            return None

    geojson = load_geojson()

    if geojson:
        fig = px.choropleth(
            map_df, geojson=geojson,
            featureidkey="properties.NAME_1",
            locations="State", color=metric_choice,
            color_continuous_scale="Purples",
            title=f"India – {metric_choice} ({year_choice})"
        )
        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(**DARK, height=600, coloraxis_colorbar=dict(title=metric_choice, tickfont=dict(color="#e0e0ff")))
    else:
        # Fallback: bubble map using lat/lon approximations
        state_coords = {
            "Maharashtra": (19.75, 75.71), "Karnataka": (15.31, 75.71),
            "Telangana": (18.11, 79.01), "Andhra Pradesh": (15.91, 79.74),
            "Tamil Nadu": (11.12, 78.65), "Gujarat": (22.25, 71.19),
            "Rajasthan": (27.02, 74.21), "Uttar Pradesh": (26.84, 80.94),
            "Madhya Pradesh": (22.97, 78.65), "West Bengal": (22.98, 87.85),
            "Bihar": (25.09, 85.31), "Punjab": (31.14, 75.34),
            "Haryana": (29.05, 76.08), "Delhi": (28.70, 77.10),
            "Kerala": (10.85, 76.27), "Odisha": (20.94, 84.80),
            "Assam": (26.20, 92.93), "Jharkhand": (23.61, 85.27),
            "Chhattisgarh": (21.27, 81.86), "Uttarakhand": (30.06, 79.54),
            "Himachal Pradesh": (31.10, 77.17), "Goa": (15.29, 74.12),
            "Jammu & Kashmir": (33.77, 76.57), "Manipur": (24.66, 93.90),
            "Meghalaya": (25.46, 91.36), "Tripura": (23.94, 91.98),
            "Nagaland": (26.15, 94.56), "Mizoram": (23.16, 92.93),
            "Arunachal Pradesh": (28.21, 94.72), "Sikkim": (27.53, 88.51),
        }
        map_df["Lat"] = map_df["State"].map(lambda s: state_coords.get(s, (20, 80))[0])
        map_df["Lon"] = map_df["State"].map(lambda s: state_coords.get(s, (20, 80))[1])
        fig = px.scatter_geo(
            map_df, lat="Lat", lon="Lon", size=metric_choice,
            color=metric_choice, hover_name="State",
            color_continuous_scale="Purples", size_max=60,
            title=f"India – {metric_choice} ({year_choice})"
        )
        fig.update_geos(
            scope="asia", center=dict(lat=20, lon=79),
            projection_scale=4, visible=True,
            bgcolor="#0f0f1a", lakecolor="#0f0f1a",
            landcolor="#1a1a2e", coastlinecolor="#2d2d4e",
            countrycolor="#2d2d4e",
        )
        fig.update_layout(**DARK, height=600)

    st.plotly_chart(fig, use_container_width=True)

    # Animated bar race
    st.markdown("<div class='section-title'>🎬 Animated Bar Race – State Rankings</div>", unsafe_allow_html=True)
    race_df = state_txn.copy()
    race_df["Period"] = race_df["Year"].astype(str) + "-Q" + race_df["Quarter"].astype(str)
    race_agg = race_df.groupby(["Period","State"])["Transactions"].sum().reset_index()
    top10_states = state_txn.groupby("State")["Transactions"].sum().nlargest(10).index.tolist()
    race_top = race_agg[race_agg["State"].isin(top10_states)].sort_values(["Period","Transactions"])

    fig_race = px.bar(
        race_top, x="Transactions", y="State", animation_frame="Period",
        orientation="h", range_x=[0, race_top["Transactions"].max()*1.1],
        color="State", color_discrete_sequence=px.colors.sequential.Purples[2:],
        title="Top 10 States – Transaction Volume Over Time"
    )
    fig_race.update_layout(**{**DARK, "height":480,
                              "yaxis": {**DARK["yaxis"], "categoryorder":"total ascending"},
                              "showlegend":False})
    st.plotly_chart(fig_race, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 – DEVICE INSIGHTS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📱 Device Insights":
    st.markdown("<h1 style='color:#c4b5fd;'>📱 Device Brand Analytics</h1>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='section-title'>🥇 Overall Brand Market Share</div>", unsafe_allow_html=True)
        brand_total = state_dev.groupby("Brand")["Registered Users"].sum().nlargest(10).reset_index()
        fig = px.pie(brand_total, values="Registered Users", names="Brand",
                     color_discrete_sequence=ACCENT + px.colors.sequential.Purples,
                     hole=0.4)
        fig.update_layout(**DARK, height=380, legend=dict(bgcolor="#1a1a2e"))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("<div class='section-title'>📊 Brand Usage Over Time</div>", unsafe_allow_html=True)
        top6 = state_dev.groupby("Brand")["Registered Users"].sum().nlargest(6).index.tolist()
        brand_time = state_dev[state_dev["Brand"].isin(top6)].copy()
        brand_time["Period"] = brand_time["Year"].astype(str) + " Q" + brand_time["Quarter"].astype(str)
        bt_agg = brand_time.groupby(["Period","Brand"])["Registered Users"].sum().reset_index()
        fig2 = px.line(bt_agg, x="Period", y="Registered Users", color="Brand",
                       color_discrete_sequence=ACCENT, line_shape="spline")
        fig2.update_layout(**DARK, height=380, legend=dict(bgcolor="#1a1a2e"))
        fig2.update_traces(line_width=2.5)
        st.plotly_chart(fig2, use_container_width=True)

    # State-level device heatmap
    st.markdown("<div class='section-title'>🔥 State × Brand Heatmap</div>", unsafe_allow_html=True)
    top5b = state_dev.groupby("Brand")["Registered Users"].sum().nlargest(5).index.tolist()
    hm = state_dev[state_dev["Brand"].isin(top5b)].groupby(["State","Brand"])["Registered Users"].sum().unstack(fill_value=0)
    hm_norm = hm.div(hm.sum(axis=1), axis=0)  # normalize per state
    fig3 = px.imshow(
        hm_norm.round(3), color_continuous_scale="Purples",
        labels=dict(color="Share"), title="Device Brand Share per State (Top 5 Brands)",
        aspect="auto"
    )
    fig3.update_layout(**DARK, height=620, coloraxis_colorbar=dict(tickfont=dict(color="#e0e0ff")))
    st.plotly_chart(fig3, use_container_width=True)

    # Top brand per state table
    st.markdown("<div class='section-title'>🏆 Dominant Brand per State</div>", unsafe_allow_html=True)
    dom = (state_dev.sort_values("Registered Users", ascending=False)
           .drop_duplicates("State")[["State","Brand","Registered Users","Percentage"]]
           .sort_values("Registered Users", ascending=False)
           .reset_index(drop=True))
    st.dataframe(dom.style.background_gradient(subset=["Registered Users"], cmap="Purples"),
                 use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 5 – ML FORECAST
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🤖 ML Forecast":
    st.markdown("<h1 style='color:#c4b5fd;'>🤖 ML Transaction Forecast</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#9ca3af;'>Polynomial regression to predict future quarterly transaction growth</p>", unsafe_allow_html=True)

    states_list = sorted(state_txn["State"].unique())
    sel_state   = st.selectbox("Select state", states_list, index=states_list.index("Maharashtra"))
    degree      = st.slider("Polynomial degree", 1, 4, 2)
    forecast_q  = st.slider("Quarters to forecast", 2, 8, 4)

    sdf = state_txn[state_txn["State"] == sel_state].copy().sort_values(["Year","Quarter"])
    sdf["t"] = np.arange(len(sdf))
    sdf["Period"] = sdf["Year"].astype(str) + " Q" + sdf["Quarter"].astype(str)

    X = sdf["t"].values.reshape(-1, 1)
    y = sdf["Transactions"].values

    model = Pipeline([("poly", PolynomialFeatures(degree=degree, include_bias=False)),
                      ("lr", LinearRegression())])
    model.fit(X, y)

    t_future = np.arange(len(sdf), len(sdf) + forecast_q).reshape(-1, 1)
    y_pred_hist  = model.predict(X)
    y_pred_future = model.predict(t_future)

    # Build future period labels
    last_yr, last_q = sdf["Year"].iloc[-1], sdf["Quarter"].iloc[-1]
    future_labels = []
    yr, qr = last_yr, last_q
    for _ in range(forecast_q):
        qr += 1
        if qr > 4:
            qr = 1; yr += 1
        future_labels.append(f"{yr} Q{qr}")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=sdf["Period"], y=y/1e6,
        mode="lines+markers", name="Actual",
        line=dict(color="#7c3aed", width=2.5),
        marker=dict(size=7, color="#a78bfa")
    ))
    fig.add_trace(go.Scatter(
        x=sdf["Period"], y=y_pred_hist/1e6,
        mode="lines", name="Model fit",
        line=dict(color="#34d399", width=2, dash="dot")
    ))
    fig.add_trace(go.Scatter(
        x=future_labels, y=y_pred_future/1e6,
        mode="lines+markers", name="Forecast",
        line=dict(color="#f59e0b", width=2.5, dash="dash"),
        marker=dict(size=9, color="#f59e0b", symbol="diamond"),
    ))
    fig.update_layout(
        **DARK, height=440,
        title=dict(text=f"{sel_state} – Transaction Forecast (Degree {degree} Poly Regression)",
                   font=dict(color="#c4b5fd")),
        legend=dict(bgcolor="#1a1a2e"),
        xaxis_title="Quarter", yaxis_title="Transactions (Millions)"
    )
    st.plotly_chart(fig, use_container_width=True)

    # R² score
    from sklearn.metrics import r2_score, mean_absolute_error
    r2  = r2_score(y, y_pred_hist)
    mae = mean_absolute_error(y, y_pred_hist)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""<div class="kpi-card"><div class="kpi-label">R² Score</div>
            <div class="kpi-value">{r2:.4f}</div>
            <div class="kpi-delta">Model accuracy</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="kpi-card"><div class="kpi-label">MAE</div>
            <div class="kpi-value">{mae/1e6:.2f}M</div>
            <div class="kpi-delta">Mean absolute error</div></div>""", unsafe_allow_html=True)
    with c3:
        next_q = y_pred_future[0]
        st.markdown(f"""<div class="kpi-card"><div class="kpi-label">Next Quarter Forecast</div>
            <div class="kpi-value">{next_q/1e6:.1f}M</div>
            <div class="kpi-delta">Transactions predicted</div></div>""", unsafe_allow_html=True)

    st.markdown("<div class='section-title'>📋 Forecast Table</div>", unsafe_allow_html=True)
    forecast_df = pd.DataFrame({
        "Quarter": future_labels,
        "Forecasted Transactions": [f"{v/1e6:.2f}M" for v in y_pred_future],
        "Raw Value": [int(v) for v in y_pred_future]
    })
    st.dataframe(forecast_df, use_container_width=True)

    st.markdown("""<div class='insight-box'>
        ⚠️ <b>Note:</b> This is a polynomial regression model trained on historical data.
        Real-world forecasts should account for external factors like policy changes,
        competitor activity, and economic conditions. Use this as a directional indicator only.
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 6 – SQL EXPLORER
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🗄️ SQL Explorer":
    st.markdown("<h1 style='color:#c4b5fd;'>🗄️ SQL Explorer</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#9ca3af;'>Run live SQL queries on the PhonePe dataset — powered by SQLite</p>", unsafe_allow_html=True)

    # Preset queries
    PRESETS = {
        "Top 10 states by transactions": """SELECT State,
       SUM(Transactions) AS Total_Transactions,
       ROUND(SUM("Amount (INR)")/1e9, 2) AS Amount_Billion_INR
FROM state_txn
GROUP BY State
ORDER BY Total_Transactions DESC
LIMIT 10;""",
        "Quarterly growth (national)": """SELECT Year, Quarter,
       SUM(Transactions) AS Total_Txn,
       ROUND(SUM("Amount (INR)")/1e9,2) AS Amount_B
FROM state_txn
GROUP BY Year, Quarter
ORDER BY Year, Quarter;""",
        "Most popular transaction type per year": """SELECT Year, "Transaction Type",
       SUM(Transactions) AS Total
FROM state_split
GROUP BY Year, "Transaction Type"
ORDER BY Year, Total DESC;""",
        "Top device brand per state": """SELECT State, Brand,
       MAX("Registered Users") AS Peak_Users
FROM state_dev
GROUP BY State
ORDER BY Peak_Users DESC;""",
        "Population density vs avg transactions": """SELECT d.State, d.District,
       AVG(d.Density) AS Avg_Density,
       SUM(t.Transactions) AS Total_Txn
FROM dist_txn t
JOIN dist_demo d ON t.State = d.State AND t.District = d.District
GROUP BY d.State, d.District
ORDER BY Total_Txn DESC
LIMIT 20;""",
        "User to population ratio by state": """SELECT t.State,
       MAX(t."Registered Users") AS Registered_Users,
       SUM(d.Population) AS Population,
       ROUND(CAST(MAX(t."Registered Users") AS FLOAT)/SUM(d.Population), 4) AS User_Pop_Ratio
FROM state_txn t
JOIN dist_demo d ON t.State = d.State
GROUP BY t.State
ORDER BY User_Pop_Ratio DESC;""",
    }

    preset = st.selectbox("📂 Load a preset query", ["(write your own)"] + list(PRESETS.keys()))
    default_sql = PRESETS.get(preset, "SELECT * FROM state_txn LIMIT 10;")

    sql = st.text_area("✏️ SQL Query", value=default_sql, height=160)

    st.markdown("**Available tables:** `state_txn` · `state_split` · `state_dev` · `dist_txn` · `dist_demo`")

    if st.button("▶ Run Query", type="primary"):
        try:
            result = run_query(sql)
            st.success(f"✅ {len(result)} rows returned")
            st.dataframe(result, use_container_width=True)

            # Auto visualize if numeric columns exist
            num_cols = result.select_dtypes(include="number").columns.tolist()
            str_cols = result.select_dtypes(include="object").columns.tolist()
            if num_cols and str_cols:
                st.markdown("<div class='section-title'>📊 Auto Visualization</div>", unsafe_allow_html=True)
                fig = px.bar(result.head(20), x=str_cols[0], y=num_cols[0],
                             color_discrete_sequence=["#7c3aed"])
                fig.update_layout(**DARK, height=380)
                st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"❌ Query error: {e}")

    # Schema reference
    with st.expander("📖 Schema Reference"):
        schema = {
            "state_txn": ["State","Year","Quarter","Transactions","Amount (INR)","ATV (INR)","Registered Users","App Opens"],
            "state_split": ["State","Year","Quarter","Transaction Type","Transactions","Amount (INR)","ATV (INR)"],
            "state_dev": ["State","Year","Quarter","Brand","Registered Users","Percentage"],
            "dist_txn": ["State","Year","Quarter","District","Code","Transactions","Amount (INR)","ATV (INR)","Registered Users","App Opens"],
            "dist_demo": ["State","District","Headquarters","Population","Area (sq km)","Density","Code","Alternate Name"],
        }
        for tbl, cols in schema.items():
            st.markdown(f"**`{tbl}`** — {', '.join([f'`{c}`' for c in cols])}")
