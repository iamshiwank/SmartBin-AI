import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from datetime import datetime

REPORT_FILE = Path(__file__).parent / "waste_reports.csv"

REPORT_COLUMNS = [
    "Timestamp",
    "Location",
    "Issue",
    "Description"
]


def save_waste_report(location, issue, description):
    report = pd.DataFrame([{
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Location": location,
        "Issue": issue,
        "Description": description
    }])

    if REPORT_FILE.exists():
        report.to_csv(
            REPORT_FILE,
            mode="a",
            header=False,
            index=False
        )
    else:
        report.to_csv(REPORT_FILE, index=False)

st.set_page_config(
    page_title="SmartBin AI",
    page_icon="♻️",
    layout="wide"
)


# ---------- SmartBin AI eco dashboard styling ----------
# Use this in-app selector for a fully coordinated light/dark design.
if "appearance" not in st.session_state:
    st.session_state.appearance = "Light"

appearance = st.sidebar.radio(
    "🎨 Dashboard appearance",
    ["Light", "Dark"],
    key="appearance",
    horizontal=True
)
dark_mode = appearance == "Dark"

if dark_mode:
    C = {
        "app_bg": "#0b1512",
        "app_bg2": "#10231a",
        "text": "#e5f4e9",
        "muted": "#a7c4b1",
        "sidebar1": "#071f18",
        "sidebar2": "#0d3325",
        "card": "#14271d",
        "card2": "#192f23",
        "border": "#294b36",
        "accent": "#5cda91",
        "accent_dark": "#1d9b5b",
        "note": "#142f20",
        "chart_bg": "#13251b",
        "grid": "#294536",
    }
else:
    C = {
        "app_bg": "#f5fbf7",
        "app_bg2": "#eff8f2",
        "text": "#153b32",
        "muted": "#477063",
        "sidebar1": "#064e3b",
        "sidebar2": "#03382c",
        "card": "#ffffff",
        "card2": "#f2fbf5",
        "border": "#d7eadf",
        "accent": "#087443",
        "accent_dark": "#29985a",
        "note": "#e6f7e9",
        "chart_bg": "#f8fcf9",
        "grid": "#d8eadf",
    }

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');
:root {{
  color-scheme: {"dark" if dark_mode else "light"};
}}
.stApp, [data-testid="stAppViewContainer"] {{
    background: radial-gradient(ellipse at 92% 2%, {"rgba(30,120,70,.15)" if dark_mode else "rgba(187,247,208,.42)"}, transparent 28%),
                linear-gradient(135deg, {C["app_bg"]} 0%, {C["app_bg2"]} 55%, {C["app_bg"]} 100%) !important;
    color: {C["text"]} !important;
}}
[data-testid="stHeader"] {{ background: {C["app_bg"]} !important; }}
[data-testid="stMainBlockContainer"] {{ color: {C["text"]} !important; }}
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, {C["sidebar1"]} 0%, {C["sidebar2"]} 100%) !important;
    border-right: 1px solid {C["border"]};
}}
[data-testid="stSidebar"] * {{ color: #f0fdf4 !important; }}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {{ color: #d1fae5 !important; }}
h1, h2, h3 {{ font-family: 'Manrope', sans-serif !important; color: {("#d8f3df" if dark_mode else "#123f32")} !important; letter-spacing: -.025em; }}
h1 {{ font-weight: 800 !important; }}
h2, h3 {{ font-weight: 700 !important; }}
p, label, [data-testid="stMarkdownContainer"] {{ color: {C["text"]}; }}
small, [data-testid="stCaptionContainer"] {{ color: {C["muted"]} !important; }}
[data-testid="stMetric"] {{
    background: linear-gradient(145deg, {C["card"]} 0%, {C["card2"]} 100%) !important;
    border: 1px solid {C["border"]} !important; border-radius: 18px; padding: 18px 20px;
    box-shadow: 0 5px 18px rgba(0,0,0,{"0.16" if dark_mode else "0.055"});
}}
[data-testid="stMetricLabel"] {{ color: {C["muted"]} !important; }}
[data-testid="stMetricValue"] {{ color: {C["accent"]} !important; font-weight: 800; }}
.stButton > button, .stFormSubmitButton > button {{
    border: 0; border-radius: 12px; background: linear-gradient(100deg,{C["accent"]},{C["accent_dark"]});
    color: white !important; font-weight: 700; padding: .58rem 1.1rem;
}}
.stButton > button:hover, .stFormSubmitButton > button:hover {{
    color: white !important; box-shadow: 0 5px 14px rgba(8,116,67,.2); transform: translateY(-1px);
}}
[data-testid="stDataFrame"], [data-testid="stTable"] {{
    border: 1px solid {C["border"]} !important; border-radius: 14px; overflow: hidden;
}}
[data-baseweb="select"] > div, [data-baseweb="input"] > div, [data-baseweb="textarea"] > div {{
    background-color: {C["card"]} !important; border-color: {C["border"]} !important; color: {C["text"]} !important;
}}
input, textarea {{ color: {C["text"]} !important; }}
[data-testid="stForm"] {{ border-color: {C["border"]} !important; }}
[data-testid="stAlert"] {{ background-color: {C["card2"]} !important; color: {C["text"]} !important; }}
hr {{ border-color: {C["border"]} !important; }}
.eco-hero {{
    position: relative; overflow: hidden; padding: 27px 30px; border-radius: 22px; margin: 0 0 22px 0;
    background: linear-gradient(115deg, #064e3b 0%, #087443 58%, #4d9c53 100%);
    color: #f0fdf4; box-shadow: 0 12px 30px rgba(0,0,0,{"0.25" if dark_mode else "0.14"});
}}
.eco-hero:after {{ content: "🌿"; position: absolute; right: 25px; top: 2px; font-size: 92px; opacity: .22; transform: rotate(-15deg); }}
.eco-hero h1 {{ color: #fff !important; margin: 0 0 7px 0; font-size: 2.15rem; }}
.eco-hero p {{ color: #dcfce7 !important; font-size: 1rem; margin: 0; max-width: 75%; }}
.eco-pill {{ display: inline-block; background: rgba(236,253,243,.16); border: 1px solid rgba(236,253,243,.25); color: #f0fdf4 !important; padding: 5px 11px; border-radius: 999px; font-size: .78rem; margin-bottom: 12px; }}
.eco-note {{ background: {C["note"]}; border: 1px solid {C["border"]}; border-left: 5px solid {C["accent_dark"]}; padding: 14px 17px; border-radius: 13px; color: {C["text"]} !important; margin: 8px 0 16px; }}
.eco-footer {{ text-align: center; color: {C["muted"]}; font-size: .82rem; padding: 18px 0 6px; }}
@media (max-width:700px) {{ .eco-hero {{ padding:22px; }} .eco-hero h1 {{ font-size:1.7rem; }} .eco-hero:after {{ font-size:58px; right:12px; }} }}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("# 🌿 SmartBin AI")
    st.markdown("**Cleaner bins. Greener tomorrow.**")
    st.markdown("---")
    st.markdown("### ♻️ Your sustainability hub")
    st.markdown("📊 Dashboard overview")
    st.markdown("📝 Report waste")
    st.markdown("🍃 Waste sorting guide")
    st.markdown("🚛 Collection priority")
    st.markdown("🌍 Environmental insights")
    st.markdown("---")
    

st.markdown("""
<div class="eco-hero">
  <div class="eco-pill">♻️ SMART WASTE MANAGEMENT</div>
  <h1>SmartBin AI</h1>
  <p>Smarter waste collection for a cleaner campus and a greener future.
  Monitor bins, guide responsible disposal, and prioritize collection.</p>
</div>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="eco-note">🌱 <b>Small actions, big impact.</b> '
    'Use the dashboard to spot bins that need attention and encourage responsible waste sorting.</div>',
    unsafe_allow_html=True
)

# Sample smart-bin data for our prototype
data = pd.DataFrame({
    "Bin": ["BIN-001", "BIN-002", "BIN-003", "BIN-004", "BIN-005"],
    "Location": [
        "College Gate",
        "Cafeteria",
        "Library",
        "Parking Area",
        "Garden"
    ],
    "Fill Level (%)": [85, 45, 92, 30, 68]
})

# Dashboard metrics
col1, col2, col3 = st.columns(3)

col1.metric("Total Smart Bins", len(data))
col2.metric("Bins Nearly Full", int((data["Fill Level (%)"] >= 80).sum()))
col3.metric("Average Fill Level", f"{data['Fill Level (%)'].mean():.1f}%")

st.divider()

# Fill-level chart
st.subheader("📊 Bin Fill-Level Monitoring")

fig = px.bar(
    data,
    x="Bin",
    y="Fill Level (%)",
    color="Fill Level (%)",
    hover_data=["Location"],
    title="Current Waste Bin Fill Levels",
    range_y=[0, 100],
    color_continuous_scale=["#b7e4c7", "#52b788", "#087443"],
    template=("plotly_dark" if dark_mode else "plotly_white")
)

# Keep chart text readable even when the Streamlit app is in dark mode.
# The chart uses its own clean, light plotting surface in both themes.
fig.update_layout(
    paper_bgcolor="#f8fcf9",
    plot_bgcolor="#f8fcf9",
    font=dict(family="DM Sans, sans-serif", color="#244c3d", size=12),
    title_font=dict(family="Manrope, sans-serif", size=17, color="#123f32"),
    margin=dict(l=18, r=18, t=55, b=18),
    coloraxis_colorbar=dict(
        title=dict(text="Fill Level (%)", font=dict(color="#244c3d")),
        tickfont=dict(color="#244c3d")
    ),
    yaxis=dict(
        title=dict(text="Fill Level (%)", font=dict(color="#244c3d")),
        tickfont=dict(color="#244c3d"),
        gridcolor="rgba(120,150,130,0.25)",
        zerolinecolor="rgba(120,150,130,0.3)"
    ),
    xaxis=dict(
        title=dict(text="Bin", font=dict(color="#244c3d")),
        tickfont=dict(color="#244c3d"),
        showgrid=False
    )
)

st.plotly_chart(fig, use_container_width=True)

# Bin status table
st.subheader("📍 Bin Status")

data["Status"] = data["Fill Level (%)"].apply(
    lambda level: "Needs Collection" if level >= 80
    else "Monitor" if level >= 60
    else "Normal"
)

st.dataframe(data, use_container_width=True)

st.caption(
    "Prototype demonstration using sample data; "
    "not connected to physical sensors."
)

st.divider()

st.header("📝 Report a Waste Problem")

with st.form("waste_report_form"):
    location = st.selectbox(
        "Select Location",
        ["College Gate", "Cafeteria", "Library",
         "Parking Area", "Garden", "Other"]
    )

    issue = st.selectbox(
        "Type of Problem",
        [
            "Overflowing Bin",
            "Waste Scattered Around",
            "Uncollected Garbage",
            "Damaged Bin",
            "Other"
        ]
    )

    description = st.text_area(
        "Describe the problem",
        placeholder="Explain the waste problem..."
    )

    submitted = st.form_submit_button("Submit Report")

    if submitted:
        save_waste_report(location, issue, description)
        st.success("✅ Waste report saved successfully!")
        st.write("**Location:**", location)
        st.write("**Problem:**", issue)
        st.write("**Description:**", description)

st.divider()

st.header("🤖 Smart Waste-Sorting Assistant")

st.write(
    "Select a waste item to learn how to dispose of it responsibly."
)

waste_options = {
    "Plastic Bottle": (
        "Plastic Waste",
        "Empty and rinse the bottle. Place it in the "
        "appropriate plastic recycling bin where accepted."
    ),
    "Banana Peel": (
        "Organic Waste",
        "Place it in a compost or wet-waste bin."
    ),
    "Paper": (
        "Paper Waste",
        "Keep paper clean and dry, then place it in "
        "a paper recycling collection."
    ),
    "Glass Bottle": (
        "Glass Waste",
        "Separate it for glass recycling where accepted. "
        "Handle broken glass carefully."
    ),
    "Battery": (
        "Hazardous Waste",
        "Do not put batteries in ordinary waste bins. "
        "Take them to an authorized battery collection point."
    ),
    "Food Leftovers": (
        "Organic Waste",
        "Use a wet-waste collection or composting system "
        "where available."
    ),
    "Old Mobile Phone": (
        "Electronic Waste",
        "Take it to an authorized e-waste collection centre."
    ),
    "Used Tissue": (
        "General Waste",
        "Usually place used tissues in general waste, "
        "unless local collection rules specify otherwise."
    )
}

selected_item = st.selectbox(
    "Choose a waste item",
    list(waste_options.keys())
)

if st.button("Analyze Waste"):
    category, advice = waste_options[selected_item]

    st.success(f"Recommended Category: {category}")
    st.info(advice)

    st.caption(
        "Recommendations are rule-based demonstrations. "
        "Follow your local waste collection guidelines."
    )

st.divider()

st.header("🚛 Smart Collection Priority")

st.write(
    "Identify which bins should be prioritized for waste collection."
)

priority_data = data.copy()

def recommend_collection(fill_level):
    if fill_level >= 90:
        return "🔴 Urgent"
    elif fill_level >= 80:
        return "🟠 High"
    elif fill_level >= 60:
        return "🟡 Moderate"
    else:
        return "🟢 Low"

priority_data["Collection Priority"] = (
    priority_data["Fill Level (%)"].apply(recommend_collection)
)

priority_data = priority_data.sort_values(
    by="Fill Level (%)",
    ascending=False
)

st.dataframe(
    priority_data[
        ["Bin", "Location", "Fill Level (%)", "Collection Priority"]
    ],
    use_container_width=True,
    hide_index=True
)

urgent_bins = priority_data[
    priority_data["Fill Level (%)"] >= 90
]

high_bins = priority_data[
    (priority_data["Fill Level (%)"] >= 80)
    & (priority_data["Fill Level (%)"] < 90)
]

st.metric("Urgent Collection", len(urgent_bins))
st.metric("High Priority", len(high_bins))

if not priority_data.empty:
    top_bin = priority_data.iloc[0]

    st.warning(
        f"Recommended next collection: {top_bin['Bin']} "
        f"at {top_bin['Location']} "
        f"({top_bin['Fill Level (%)']}% full)."
    )

st.caption(
    "Collection priorities use demonstration data and "
    "fixed thresholds, not live sensor readings."
)


st.divider()

st.header("🌱 Environmental Impact Insights")

st.write(
    "Explore waste collection indicators and sustainability opportunities "
    "using the current demonstration data."
)

# Estimate relative waste accumulation
average_fill = data["Fill Level (%)"].mean()
bins_needing_attention = int(
    (data["Fill Level (%)"] >= 80).sum()
)
bins_below_threshold = len(data) - bins_needing_attention

col1, col2, col3 = st.columns(3)

col1.metric(
    "Average Bin Fill Level",
    f"{average_fill:.1f}%"
)

col2.metric(
    "Bins Requiring Attention",
    bins_needing_attention
)

col3.metric(
    "Bins Below 80% Fill",
    bins_below_threshold
)

st.subheader("💡 Sustainability Recommendations")

st.markdown("""
- **Improve collection planning:** Prioritize bins with high fill levels.
- **Reduce food waste:** Encourage composting of suitable organic waste.
- **Increase recycling:** Keep recyclable materials separated from general waste.
- **Dispose of e-waste safely:** Direct batteries and electronic devices to
  authorized collection points.
- **Promote responsible disposal:** Encourage students to use designated bins.
""")

if bins_needing_attention > 0:
    st.info(
        f"{bins_needing_attention} of {len(data)} demonstration bins "
        "have reached at least 80% capacity and should be reviewed "
        "for collection."
    )
else:
    st.success(
        "No demonstration bins have reached the 80% attention threshold."
    )

st.caption(
    "Environmental indicators are calculated from sample bin fill levels. "
    "No actual waste weight, carbon emissions, or environmental savings "
    "have been measured."
)


st.markdown("""
<div class="eco-footer">
    🌿 SmartBin AI &nbsp; 
</div>
""", unsafe_allow_html=True)
