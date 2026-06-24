import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error
import warnings
warnings.filterwarnings("ignore")

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FitPulse Analytics",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"]{
    font-family:'Inter',sans-serif;
}

/* ───── Antarctic Aurora Background ───── */

.stApp{
    background:#070b14;
    position:relative;
}

[data-testid="stAppViewContainer"]{
    background:transparent;
    position:relative;
    z-index:1;
}

.stApp:before{
content:"";
position:fixed;
top:0;
left:0;
width:100%;
height:100%;
pointer-events:none;

background:
radial-gradient(circle at 15% 20%, rgba(99,102,241,.60), transparent 32%),
radial-gradient(circle at 85% 15%, rgba(52,211,153,.55), transparent 32%),
radial-gradient(circle at 45% 75%, rgba(168,85,247,.55), transparent 32%),
radial-gradient(circle at 80% 80%, rgba(34,211,238,.50), transparent 28%),
radial-gradient(circle at 50% 50%, rgba(255,255,255,.08), transparent 40%);

filter:blur(70px);
animation:aurora 12s ease-in-out infinite alternate;

z-index:0;
}

header{
background:transparent!important;
}

/* ───── Sidebar Glass Effect ───── */

[data-testid="stSidebar"]{
background:rgba(13,17,23,.72);
backdrop-filter:blur(25px);
border-right:1px solid rgba(99,102,241,.15);
}

[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stMultiSelect label{
color:#94a3b8!important;
font-size:.82rem!important;
font-weight:500!important;
text-transform:uppercase!important;
letter-spacing:.05em!important;
}

/* ───── KPI Cards ───── */

.metric-card{
background:rgba(30,33,48,.65);
backdrop-filter:blur(20px);
border:1px solid rgba(99,102,241,.12);
border-radius:18px;
padding:24px 20px;
text-align:center;
transition:all .3s ease;
}

.metric-card:hover{
transform:translateY(-5px);
box-shadow:0 10px 35px rgba(99,102,241,.25);
border:1px solid rgba(99,102,241,.35);
}

.metric-value{
font-size:2.1rem;
font-weight:700;
background:linear-gradient(
90deg,
#6366f1,
#a78bfa,
#34d399
);

-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
line-height:1.1;
}

.metric-label{
font-size:.78rem;
color:#8b92a8;
text-transform:uppercase;
letter-spacing:.07em;
margin-top:6px;
font-weight:500;
}

.metric-delta{
font-size:.82rem;
color:#34d399;
margin-top:4px;
font-weight:500;
}

/* ───── Headings ───── */

.section-header{
font-size:1.25rem;
font-weight:650;
color:#e2e8f0;
margin-bottom:4px;
display:flex;
align-items:center;
gap:8px;
}

.section-sub{
font-size:.82rem;
color:#64748b;
margin-bottom:16px;
}

/* ───── Prediction Card ───── */

.predict-result{
background:rgba(30,41,59,.65);
backdrop-filter:blur(22px);
border:1px solid rgba(99,102,241,.15);
border-radius:18px;
padding:24px;
text-align:center;
}

.predict-cal{
font-size:3.2rem;
font-weight:800;

background:linear-gradient(
90deg,
#f59e0b,
#ef4444
);

-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
}

.predict-label{
color:#64748b;
font-size:.85rem;
margin-top:4px;
}

.predict-tier{
margin-top:12px;
font-size:1rem;
font-weight:600;
color:#34d399;
}

/* ───── Tabs ───── */

.stTabs [data-baseweb="tab-list"]{
background:rgba(30,33,48,.7);
backdrop-filter:blur(15px);
border-radius:12px;
padding:4px;
gap:2px;
}

.stTabs [data-baseweb="tab"]{
border-radius:8px;
color:#64748b;
font-weight:500;
}

.stTabs [aria-selected="true"]{
background:#6366f1!important;
color:white!important;
}

/* ───── Expanders + HR ───── */

.streamlit-expanderHeader{
color:#94a3b8!important;
}

hr{
border-color:#1e2130;
}

/* ───── Aurora Animation ───── */

@keyframes aurora{

0%{
transform:translate(-5%,-5%) scale(1);
}

50%{
transform:translate(5%,3%) scale(1.15);
}

100%{
transform:translate(-3%,5%) scale(1.05);
}

}

/* ───────── CYBER FUTURE EFFECTS ───────── */

/* Animated grid floor */

.stApp:after{
content:"";
position:fixed;
bottom:0;
left:0;
width:100%;
height:100%;

background-image:
linear-gradient(rgba(99,102,241,.05) 1px, transparent 1px),
linear-gradient(90deg, rgba(99,102,241,.05) 1px, transparent 1px);

background-size:50px 50px;

transform:
perspective(1000px)
rotateX(75deg)
scale(2.5);

transform-origin:bottom;

opacity:.35;

pointer-events:none;

animation:gridmove 14s linear infinite;
}


/* Floating cyber particles */

body:before{
content:"";

position:fixed;

top:0;
left:0;

width:100%;
height:100%;

background:
radial-gradient(circle at 10% 20%, rgba(52,211,153,.25) 0px, transparent 2px),
radial-gradient(circle at 30% 70%, rgba(99,102,241,.25) 0px, transparent 3px),
radial-gradient(circle at 80% 30%, rgba(168,85,247,.2) 0px, transparent 2px),
radial-gradient(circle at 65% 80%, rgba(34,211,238,.2) 0px, transparent 2px);

background-size:300px 300px;

animation:particles 20s linear infinite;

pointer-events:none;
opacity:.7;
}


/* Card glow */

.metric-card,
.predict-result{

box-shadow:
0 0 25px rgba(99,102,241,.08),
inset 0 0 25px rgba(255,255,255,.03);

position:relative;
overflow:hidden;

}

/* Animated border sweep */

.metric-card::before,
.predict-result::before{

content:"";

position:absolute;

top:-100%;
left:-100%;

width:60%;
height:300%;

background:
linear-gradient(
transparent,
rgba(255,255,255,.12),
transparent
);

transform:rotate(30deg);

animation:sweep 7s linear infinite;

}


/* futuristic scrollbar */

::-webkit-scrollbar{
width:10px;
}

::-webkit-scrollbar-track{
background:#111827;
}

::-webkit-scrollbar-thumb{

background:
linear-gradient(
#6366f1,
#a78bfa,
#34d399
);

border-radius:20px;
}


/* chart glow */

.js-plotly-plot{
border-radius:18px;
overflow:hidden;

box-shadow:
0 0 25px rgba(99,102,241,.06);
}


/* title animation */

h1{

animation:titleGlow 4s ease infinite alternate;

}


/* animations */

@keyframes titleGlow{

0%{
text-shadow:0 0 10px rgba(99,102,241,.3);
}

100%{
text-shadow:
0 0 20px rgba(99,102,241,.8),
0 0 40px rgba(168,85,247,.4);
}
}

@keyframes sweep{

0%{
left:-150%;
}

100%{
left:250%;
}

}

@keyframes particles{

0%{
transform:translateY(0px);
}

100%{
transform:translateY(-300px);
}

}

@keyframes gridmove{

0%{
transform:
perspective(1000px)
rotateX(75deg)
translateY(0px)
scale(2.5);
}

100%{
transform:
perspective(1000px)
rotateX(75deg)
translateY(50px)
scale(2.5);
}

}
</style>
""", unsafe_allow_html=True)
# ── Load & cache data + model ──────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("gym_members_exercise_tracking.csv")
    return df

@st.cache_resource
def train_model(df):
    df2 = df.copy()
    df2["Gender_Male"] = (df2["Gender"] == "Male").astype(int)
    df2 = pd.get_dummies(df2, columns=["Workout_Type"], drop_first=True)
    df2 = df2.drop("Gender", axis=1)
    X = df2.drop("Calories_Burned", axis=1)
    y = df2["Calories_Burned"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    metrics = {
        "r2": r2_score(y_test, preds),
        "mae": mean_absolute_error(y_test, preds),
        "feature_cols": X.columns.tolist()
    }
    return model, metrics

df_raw = load_data()
model, model_metrics = train_model(df_raw)

WORKOUT_TYPES = ["Cardio", "HIIT", "Strength", "Yoga"]
EXPERIENCE_MAP = {1: "Beginner", 2: "Intermediate", 3: "Advanced"}
PALETTE = ["#6366f1", "#a78bfa", "#34d399", "#f59e0b", "#ef4444", "#06b6d4"]

# ── Sidebar filters ────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 💪 FitPulse")
    st.markdown("<p style='color:#64748b;font-size:0.8rem;margin-top:-8px;'>Gym Intelligence Platform</p>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 🔧 Dashboard Filters")

    sel_gender = st.multiselect("Gender", ["Male", "Female"], default=["Male", "Female"])
    sel_workout = st.multiselect("Workout Type", WORKOUT_TYPES, default=WORKOUT_TYPES)
    sel_exp = st.multiselect("Experience Level",
                             options=[1, 2, 3],
                             default=[1, 2, 3],
                             format_func=lambda x: EXPERIENCE_MAP[x])
    age_range = st.slider("Age Range", int(df_raw["Age"].min()), int(df_raw["Age"].max()), (18, 59))

    st.markdown("---")
    st.markdown("<p style='color:#475569;font-size:0.75rem;text-align:center;'>Model R² = {:.4f} · MAE = {:.1f} kcal</p>".format(
        model_metrics["r2"], model_metrics["mae"]), unsafe_allow_html=True)

# ── Filter data ────────────────────────────────────────────────────────────────
df = df_raw[
    df_raw["Gender"].isin(sel_gender) &
    df_raw["Workout_Type"].isin(sel_workout) &
    df_raw["Experience_Level"].isin(sel_exp) &
    df_raw["Age"].between(age_range[0], age_range[1])
].copy()

df["Experience_Label"] = df["Experience_Level"].map(EXPERIENCE_MAP)

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='display:flex;align-items:center;gap:16px;margin-bottom:8px;'>
  <div>
    <h1 style='margin:0;font-size:2rem;font-weight:800;background:linear-gradient(90deg,#6366f1,#a78bfa);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;'>FitPulse Analytics</h1>
    <p style='margin:0;color:#64748b;font-size:0.9rem;'>Gym Member Intelligence Dashboard</p>
  </div>
</div>
""", unsafe_allow_html=True)

# ── KPI Row ────────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)

def kpi(col, value, label, delta=None):
    delta_html = f"<div class='metric-delta'>{delta}</div>" if delta else ""
    col.markdown(f"""
    <div class='metric-card'>
      <div class='metric-value'>{value}</div>
      <div class='metric-label'>{label}</div>
      {delta_html}
    </div>
    """, unsafe_allow_html=True)

kpi(k1, f"{len(df):,}", "Total Members")
kpi(k2, f"{df['Calories_Burned'].mean():.0f}", "Avg Calories Burned", "kcal / session")
kpi(k3, f"{df['Session_Duration (hours)'].mean():.1f}h", "Avg Session Duration")
kpi(k4, f"{df['BMI'].mean():.1f}", "Avg BMI")
kpi(k5, f"{df['Fat_Percentage'].mean():.1f}%", "Avg Body Fat")

st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

# ── Tabs ───────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🏋️ Performance", "👤 Member Profile", "🤖 Calorie Predictor"])

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1: OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════════
with tab1:
    r1c1, r1c2 = st.columns([1.2, 1])

    with r1c1:
        st.markdown("<div class='section-header'>🏃 Workout Type Distribution</div>", unsafe_allow_html=True)
        wt_counts = df["Workout_Type"].value_counts().reset_index()
        wt_counts.columns = ["Workout Type", "Count"]
        fig = px.bar(wt_counts, x="Workout Type", y="Count",
                     color="Workout Type", color_discrete_sequence=PALETTE,
                     template="plotly_dark", text="Count")
        fig.update_traces(textposition="outside", marker_line_width=0)
        fig.update_layout(showlegend=False, plot_bgcolor="#1a1f2e", paper_bgcolor="#1a1f2e",
                          font_color="#94a3b8", margin=dict(l=0, r=0, t=10, b=0),
                          xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor="#252a3a"),
                          height=280, bargap=0.25)
        st.plotly_chart(fig, use_container_width=True)

    with r1c2:
        st.markdown("<div class='section-header'>⚤ Gender Split</div>", unsafe_allow_html=True)
        g_counts = df["Gender"].value_counts()
        fig2 = go.Figure(go.Pie(
            labels=g_counts.index, values=g_counts.values, hole=0.6,
            marker=dict(colors=["#6366f1", "#f472b6"]),
            textfont=dict(size=13, color="white"),
        ))
        fig2.update_layout(showlegend=True,
                           legend=dict(font=dict(color="#94a3b8"), orientation="h", y=-0.1),
                           plot_bgcolor="#1a1f2e", paper_bgcolor="#1a1f2e",
                           margin=dict(l=0, r=0, t=10, b=20), height=280,
                           annotations=[dict(text=f"{len(df)}<br>Members", x=0.5, y=0.5,
                                             font_size=16, showarrow=False, font_color="white")])
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    r2c1, r2c2 = st.columns(2)

    with r2c1:
        st.markdown("<div class='section-header'>🎂 Age Distribution by Experience</div>", unsafe_allow_html=True)
        fig3 = px.histogram(df, x="Age", color="Experience_Label", nbins=20,
                            color_discrete_map={"Beginner": "#6366f1", "Intermediate": "#a78bfa", "Advanced": "#34d399"},
                            template="plotly_dark", barmode="overlay", opacity=0.75)
        fig3.update_layout(plot_bgcolor="#1a1f2e", paper_bgcolor="#1a1f2e", font_color="#94a3b8",
                           legend_title="Experience", margin=dict(l=0, r=0, t=10, b=0),
                           xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor="#252a3a"), height=270)
        st.plotly_chart(fig3, use_container_width=True)

    with r2c2:
        st.markdown("<div class='section-header'>⚖️ BMI vs Body Fat %</div>", unsafe_allow_html=True)
        fig4 = px.scatter(df, x="BMI", y="Fat_Percentage", color="Workout_Type",
                          size="Calories_Burned", color_discrete_sequence=PALETTE,
                          template="plotly_dark", hover_data=["Age", "Gender", "Experience_Label"], opacity=0.7)
        fig4.update_layout(plot_bgcolor="#1a1f2e", paper_bgcolor="#1a1f2e", font_color="#94a3b8",
                           margin=dict(l=0, r=0, t=10, b=0),
                           xaxis=dict(showgrid=True, gridcolor="#252a3a"),
                           yaxis=dict(showgrid=True, gridcolor="#252a3a"), height=270)
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("---")
    st.markdown("<div class='section-header'>📅 Avg Calories by Workout Type & Frequency</div>", unsafe_allow_html=True)
    heatmap_data = df.groupby(["Workout_Type", "Workout_Frequency (days/week)"])["Calories_Burned"].mean().reset_index()
    heatmap_pivot = heatmap_data.pivot(index="Workout_Type", columns="Workout_Frequency (days/week)", values="Calories_Burned")
    fig5 = px.imshow(heatmap_pivot, color_continuous_scale="Purples", text_auto=".0f",
                     template="plotly_dark", aspect="auto")
    fig5.update_layout(plot_bgcolor="#1a1f2e", paper_bgcolor="#1a1f2e", font_color="#94a3b8",
                       margin=dict(l=0, r=0, t=10, b=0),
                       coloraxis_colorbar=dict(tickfont=dict(color="#94a3b8")),
                       height=250, xaxis_title="Workout Frequency (days/week)", yaxis_title="")
    st.plotly_chart(fig5, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2: PERFORMANCE
# ═══════════════════════════════════════════════════════════════════════════════
with tab2:
    p1, p2 = st.columns(2)

    with p1:
        st.markdown("<div class='section-header'>🔥 Calories Burned by Workout Type</div>", unsafe_allow_html=True)
        fig_box = px.box(df, x="Workout_Type", y="Calories_Burned", color="Workout_Type",
                         color_discrete_sequence=PALETTE, template="plotly_dark", points="outliers")
        fig_box.update_layout(showlegend=False, plot_bgcolor="#1a1f2e", paper_bgcolor="#1a1f2e",
                              font_color="#94a3b8", margin=dict(l=0, r=0, t=10, b=0), height=300,
                              xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor="#252a3a"))
        st.plotly_chart(fig_box, use_container_width=True)

    with p2:
        st.markdown("<div class='section-header'>💓 BPM Zones by Experience Level</div>", unsafe_allow_html=True)
        bpm_melt = df.melt(id_vars=["Experience_Label"],
                           value_vars=["Resting_BPM", "Avg_BPM", "Max_BPM"],
                           var_name="BPM Type", value_name="BPM")
        fig_bpm = px.violin(bpm_melt, x="BPM Type", y="BPM", color="Experience_Label",
                            color_discrete_map={"Beginner": "#6366f1", "Intermediate": "#a78bfa", "Advanced": "#34d399"},
                            template="plotly_dark", box=True)
        fig_bpm.update_layout(plot_bgcolor="#1a1f2e", paper_bgcolor="#1a1f2e", font_color="#94a3b8",
                              margin=dict(l=0, r=0, t=10, b=0), height=300,
                              xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor="#252a3a"),
                              legend_title="Experience")
        st.plotly_chart(fig_bpm, use_container_width=True)

    st.markdown("---")
    p3, p4 = st.columns([1.5, 1])

    with p3:
        st.markdown("<div class='section-header'>⏱️ Session Duration vs Calories (by Experience)</div>", unsafe_allow_html=True)
        fig_scatter2 = px.scatter(df, x="Session_Duration (hours)", y="Calories_Burned",
                                  color="Experience_Label",
                                  color_discrete_map={"Beginner": "#6366f1", "Intermediate": "#a78bfa", "Advanced": "#34d399"},
                                  trendline="ols", template="plotly_dark", opacity=0.6,
                                  hover_data=["Workout_Type", "Age", "Gender"])
        fig_scatter2.update_layout(plot_bgcolor="#1a1f2e", paper_bgcolor="#1a1f2e", font_color="#94a3b8",
                                   margin=dict(l=0, r=0, t=10, b=0),
                                   xaxis=dict(showgrid=True, gridcolor="#252a3a"),
                                   yaxis=dict(showgrid=True, gridcolor="#252a3a"),
                                   height=320, legend_title="Experience")
        st.plotly_chart(fig_scatter2, use_container_width=True)

    with p4:
        st.markdown("<div class='section-header'>💧 Avg Water Intake by Workout Type</div>", unsafe_allow_html=True)
        water_df = df.groupby("Workout_Type")["Water_Intake (liters)"].mean().reset_index()
        water_df.columns = ["Workout Type", "Avg Water (L)"]
        fig_water = px.bar(water_df, x="Avg Water (L)", y="Workout Type", orientation="h",
                           color="Avg Water (L)", color_continuous_scale="Blues",
                           template="plotly_dark", text=water_df["Avg Water (L)"].round(2))
        fig_water.update_traces(texttemplate="%{text}L", textposition="outside")
        fig_water.update_layout(showlegend=False, coloraxis_showscale=False,
                                plot_bgcolor="#1a1f2e", paper_bgcolor="#1a1f2e", font_color="#94a3b8",
                                margin=dict(l=0, r=0, t=10, b=0),
                                xaxis=dict(showgrid=True, gridcolor="#252a3a"),
                                yaxis=dict(showgrid=False), height=320)
        st.plotly_chart(fig_water, use_container_width=True)

    st.markdown("---")
    st.markdown("<div class='section-header'>🔗 Feature Correlation Matrix</div>", unsafe_allow_html=True)
    corr_cols = ["Age", "Weight (kg)", "BMI", "Fat_Percentage", "Session_Duration (hours)",
                 "Calories_Burned", "Avg_BPM", "Resting_BPM", "Water_Intake (liters)",
                 "Workout_Frequency (days/week)"]
    corr_matrix = df[corr_cols].corr()
    fig_corr = px.imshow(corr_matrix, color_continuous_scale="RdBu_r", zmin=-1, zmax=1,
                         text_auto=".2f", template="plotly_dark")
    fig_corr.update_layout(plot_bgcolor="#1a1f2e", paper_bgcolor="#1a1f2e", font_color="#94a3b8",
                           margin=dict(l=0, r=0, t=10, b=0), height=380,
                           coloraxis_colorbar=dict(tickfont=dict(color="#94a3b8")))
    st.plotly_chart(fig_corr, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3: MEMBER PROFILE
# ═══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("<div class='section-header'>📋 Member Segmentation & Insights</div>", unsafe_allow_html=True)

    seg = df.groupby(["Experience_Label", "Workout_Type"]).agg(
        Members=("Age", "count"),
        Avg_Age=("Age", "mean"),
        Avg_Calories=("Calories_Burned", "mean"),
        Avg_BMI=("BMI", "mean"),
        Avg_Duration=("Session_Duration (hours)", "mean"),
        Avg_Fat=("Fat_Percentage", "mean")
    ).round(1).reset_index()
    seg.columns = ["Experience", "Workout", "Members", "Avg Age",
                   "Avg Calories", "Avg BMI", "Avg Duration (h)", "Avg Fat %"]

    st.dataframe(
        seg.style
        .background_gradient(subset=["Avg Calories"], cmap="Purples")
        .background_gradient(subset=["Avg Fat %"], cmap="RdYlGn_r")
        .format({"Avg Calories": "{:.0f}", "Avg BMI": "{:.1f}",
                 "Avg Duration (h)": "{:.2f}", "Avg Fat %": "{:.1f}%"}),
        use_container_width=True, height=320
    )

    st.markdown("---")
    m1, m2, m3 = st.columns(3)

    with m1:
        st.markdown("<div class='section-header'>📈 Weight Distribution</div>", unsafe_allow_html=True)
        fig_w = px.histogram(df, x="Weight (kg)", color="Gender",
                             color_discrete_map={"Male": "#6366f1", "Female": "#f472b6"},
                             template="plotly_dark", nbins=25, barmode="overlay", opacity=0.75)
        fig_w.update_layout(plot_bgcolor="#1a1f2e", paper_bgcolor="#1a1f2e", font_color="#94a3b8",
                            margin=dict(l=0, r=0, t=10, b=0), height=250, showlegend=True,
                            xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor="#252a3a"))
        st.plotly_chart(fig_w, use_container_width=True)

    with m2:
        st.markdown("<div class='section-header'>🏆 Experience Breakdown</div>", unsafe_allow_html=True)
        exp_df = df["Experience_Label"].value_counts().reset_index()
        exp_df.columns = ["Level", "Count"]
        fig_exp = px.funnel(exp_df, y="Level", x="Count", color="Level",
                            color_discrete_map={"Beginner": "#6366f1", "Intermediate": "#a78bfa", "Advanced": "#34d399"},
                            template="plotly_dark")
        fig_exp.update_layout(plot_bgcolor="#1a1f2e", paper_bgcolor="#1a1f2e", font_color="#94a3b8",
                              margin=dict(l=0, r=0, t=10, b=0), height=250, showlegend=False)
        st.plotly_chart(fig_exp, use_container_width=True)

    with m3:
        st.markdown("<div class='section-header'>📊 Workout Frequency Split</div>", unsafe_allow_html=True)
        freq_df = df["Workout_Frequency (days/week)"].value_counts().sort_index().reset_index()
        freq_df.columns = ["Days/Week", "Count"]
        fig_freq = px.bar(freq_df, x="Days/Week", y="Count", color="Days/Week",
                          color_continuous_scale="Purples", template="plotly_dark", text="Count")
        fig_freq.update_traces(textposition="outside")
        fig_freq.update_layout(plot_bgcolor="#1a1f2e", paper_bgcolor="#1a1f2e", font_color="#94a3b8",
                               margin=dict(l=0, r=0, t=10, b=0), height=250,
                               showlegend=False, coloraxis_showscale=False,
                               xaxis=dict(showgrid=False, title="Days/Week"),
                               yaxis=dict(showgrid=True, gridcolor="#252a3a"))
        st.plotly_chart(fig_freq, use_container_width=True)

    with st.expander("🔍 View Raw Member Data"):
        st.dataframe(df.drop("Experience_Label", axis=1), use_container_width=True, height=300)
        csv_bytes = df.drop("Experience_Label", axis=1).to_csv(index=False).encode()
        st.download_button("⬇️ Download Filtered Data as CSV", data=csv_bytes,
                           file_name="filtered_gym_members.csv", mime="text/csv")


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 4: CALORIE PREDICTOR
# ═══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("<div class='section-header'>🤖 AI-Powered Calorie Burn Predictor</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Fill in member details to predict estimated calories burned per session (Linear Regression · R² = {:.4f})</div>".format(
        model_metrics["r2"]), unsafe_allow_html=True)

    left, right = st.columns([1.1, 1])

    with left:
        st.markdown("#### 👤 Personal Info")
        a1, a2 = st.columns(2)
        age_p = a1.slider("Age", 18, 59, 30)
        gender_p = a2.selectbox("Gender", ["Male", "Female"])

        b1, b2 = st.columns(2)
        weight_p = b1.slider("Weight (kg)", 40.0, 130.0, 70.0, step=0.5)
        height_p = b2.slider("Height (m)", 1.50, 2.10, 1.75, step=0.01)

        bmi_p = weight_p / (height_p ** 2)
        fat_p = st.slider("Body Fat %", 5.0, 40.0, 20.0, step=0.5)

        st.markdown("#### 💪 Workout Details")
        c1, c2 = st.columns(2)
        workout_p = c1.selectbox("Workout Type", WORKOUT_TYPES)
        exp_p = c2.selectbox("Experience Level", [1, 2, 3], format_func=lambda x: EXPERIENCE_MAP[x])

        d1, d2 = st.columns(2)
        duration_p = d1.slider("Session Duration (hrs)", 0.5, 3.0, 1.0, step=0.25)
        freq_p = d2.slider("Frequency (days/week)", 1, 7, 3)

        st.markdown("#### 💓 Heart Rate")
        e1, e2, e3 = st.columns(3)
        rest_bpm = e1.number_input("Resting BPM", 40, 100, 60)
        avg_bpm = e2.number_input("Avg BPM", 80, 200, 140)
        max_bpm = e3.number_input("Max BPM", 120, 220, 180)

        water_p = st.slider("Water Intake (liters)", 1.0, 4.0, 2.5, step=0.1)

    with right:
        input_dict = {
            "Age": age_p,
            "Weight (kg)": weight_p,
            "Height (m)": height_p,
            "Max_BPM": max_bpm,
            "Avg_BPM": avg_bpm,
            "Resting_BPM": rest_bpm,
            "Session_Duration (hours)": duration_p,
            "Fat_Percentage": fat_p,
            "Water_Intake (liters)": water_p,
            "Workout_Frequency (days/week)": freq_p,
            "Experience_Level": exp_p,
            "BMI": bmi_p,
            "Gender_Male": 1 if gender_p == "Male" else 0,
            "Workout_Type_HIIT": 1 if workout_p == "HIIT" else 0,
            "Workout_Type_Strength": 1 if workout_p == "Strength" else 0,
            "Workout_Type_Yoga": 1 if workout_p == "Yoga" else 0,
        }
        input_df = pd.DataFrame([input_dict])[model_metrics["feature_cols"]]
        predicted_cal = max(0, model.predict(input_df)[0])

        if predicted_cal < 500:
            tier, tier_color = "🟡 Light Burn", "#f59e0b"
        elif predicted_cal < 800:
            tier, tier_color = "🟠 Moderate Burn", "#f97316"
        else:
            tier, tier_color = "🔴 High Burn", "#ef4444"

        pct = (df_raw["Calories_Burned"] < predicted_cal).mean() * 100

        st.markdown(f"""
        <div class='predict-result' style='margin-top:60px;'>
          <div style='color:#64748b;font-size:0.8rem;text-transform:uppercase;letter-spacing:0.1em;'>Estimated Calories Burned</div>
          <div class='predict-cal'>{predicted_cal:.0f}</div>
          <div class='predict-label'>kcal per session</div>
          <div class='predict-tier' style='color:{tier_color};'>{tier}</div>
          <hr style='border-color:#1e293b;margin:16px 0;'>
          <div style='color:#94a3b8;font-size:0.85rem;'>
            Better than <b style='color:white;'>{pct:.0f}%</b> of all members
          </div>
          <div style='color:#64748b;font-size:0.8rem;margin-top:8px;'>
            BMI: <b style='color:#a78bfa;'>{bmi_p:.1f}</b>
          </div>
        </div>
        """, unsafe_allow_html=True)

        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=predicted_cal,
            number=dict(suffix=" kcal", font=dict(size=22, color="#e2e8f0")),
            title=dict(text="Burn Intensity", font=dict(size=13, color="#94a3b8")),
            gauge=dict(
                axis=dict(range=[0, 1500], tickcolor="#94a3b8", tickfont=dict(color="#94a3b8")),
                bar=dict(color="#6366f1"),
                bgcolor="#1a1f2e",
                bordercolor="#2e3352",
                steps=[
                    dict(range=[0, 500], color="#1a1f2e"),
                    dict(range=[500, 800], color="#1e293b"),
                    dict(range=[800, 1500], color="#252a3a"),
                ],
                threshold=dict(line=dict(color="#ef4444", width=3),
                               thickness=0.75, value=df_raw["Calories_Burned"].mean())
            )
        ))
        fig_gauge.update_layout(paper_bgcolor="#1a1f2e", font_color="#94a3b8",
                                height=260, margin=dict(l=20, r=20, t=30, b=10))
        st.plotly_chart(fig_gauge, use_container_width=True)

        st.markdown("#### 🔍 Top Factors Influencing Prediction")
        feat_names = model_metrics["feature_cols"]
        coefs = model.coef_
        feat_impact = sorted(zip(feat_names, coefs * input_df.values[0]),
                             key=lambda x: abs(x[1]), reverse=True)[:7]
        impact_df = pd.DataFrame(feat_impact, columns=["Feature", "Impact"])
        fig_imp = px.bar(impact_df, x="Impact", y="Feature", orientation="h",
                         color="Impact", color_continuous_scale="RdBu",
                         template="plotly_dark", text=impact_df["Impact"].round(1))
        fig_imp.update_traces(textposition="outside")
        fig_imp.update_layout(plot_bgcolor="#1a1f2e", paper_bgcolor="#1a1f2e", font_color="#94a3b8",
                              margin=dict(l=0, r=0, t=10, b=0), height=280,
                              coloraxis_showscale=False,
                              xaxis=dict(showgrid=True, gridcolor="#252a3a"),
                              yaxis=dict(showgrid=False))
        st.plotly_chart(fig_imp, use_container_width=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center;color:#334155;font-size:0.75rem;padding:8px 0;'>
  FitPulse Analytics Platform · Built with Streamlit + Plotly ·
  Powered by Linear Regression (R² = {:.4f})
</div>
""".format(model_metrics["r2"]), unsafe_allow_html=True)