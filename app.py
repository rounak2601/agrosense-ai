import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="AgroSense AI", page_icon="🌿", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; background-color: #f0f7f2; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 2rem 3rem; }

[data-testid="stSidebar"] {
    background: linear-gradient(175deg, #0d3b2e 0%, #1a5c42 60%, #2d8a5e 100%);
}
[data-testid="stSidebar"] * { color: #e8f5ee !important; }
[data-testid="stSidebar"] .stRadio label {
    background: rgba(255,255,255,0.07); border: 1px solid rgba(76,175,125,0.25);
    border-radius: 10px; padding: 10px 16px; margin: 4px 0;
    cursor: pointer; transition: all 0.25s ease; display: block; font-size: 0.95rem; font-weight: 500;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(76,175,125,0.25); border-color: #4caf7d; transform: translateX(4px);
}
.top-banner {
    background: linear-gradient(135deg, #0d3b2e 0%, #1a5c42 50%, #2d8a5e 100%);
    border-radius: 18px; padding: 2.4rem 3rem; margin-bottom: 2rem;
    position: relative; overflow: hidden; box-shadow: 0 8px 40px rgba(13,59,46,0.25);
}
.top-banner::before {
    content:''; position:absolute; top:-60px; right:-60px; width:220px; height:220px;
    background: radial-gradient(circle, rgba(76,175,125,0.3) 0%, transparent 70%); border-radius:50%;
}
.banner-badge {
    display:inline-block; background:rgba(201,168,76,0.25); border:1px solid #c9a84c;
    color:#f0d070 !important; padding:4px 14px; border-radius:20px;
    font-size:0.78rem; font-weight:600; letter-spacing:1px; text-transform:uppercase; margin-bottom:0.8rem;
}
.banner-title { font-family:'Playfair Display',serif; font-size:2.3rem; font-weight:700; color:#fff; margin:0; line-height:1.2; }
.banner-sub { font-size:0.98rem; color:rgba(255,255,255,0.82); margin-top:0.5rem; font-weight:400; }

.metric-card {
    background:white; border-radius:14px; padding:1.1rem 1.3rem;
    box-shadow: 0 4px 20px rgba(13,59,46,0.10); border-left:4px solid #2d8a5e; transition:transform 0.2s ease;
}
.metric-card:hover { transform:translateY(-3px); }
.metric-icon { font-size:1.5rem; margin-bottom:0.3rem; }
.metric-value { font-family:'Playfair Display',serif; font-size:1.6rem; font-weight:700; color:#0d3b2e; line-height:1; }
.metric-label { font-size:0.72rem; color:#2d5a3d; font-weight:600; margin-top:0.3rem; text-transform:uppercase; letter-spacing:0.5px; }

.section-header { display:flex; align-items:center; gap:10px; margin:1.6rem 0 1rem; }
.section-header h2 { font-family:'Playfair Display',serif; font-size:1.4rem; font-weight:700; color:#1a6b44; margin:0; }
.section-line { flex:1; height:1px; background:linear-gradient(90deg, #4caf7d, transparent); }

.how-card {
    background:white; border-radius:14px; padding:1.4rem;
    box-shadow: 0 4px 20px rgba(13,59,46,0.10); border-top:3px solid #2d8a5e; text-align:center;
}
.how-step { font-size:1.9rem; margin-bottom:0.4rem; }
.how-title { font-family:'Playfair Display',serif; font-size:1rem; font-weight:700; color:#0d3b2e; margin-bottom:0.4rem; }
.how-desc { font-size:0.83rem; color:#1a3a28; line-height:1.6; font-weight:400; }
.step-num {
    display:inline-block; background:#1a5c42; color:white;
    width:24px; height:24px; border-radius:50%; font-size:0.78rem;
    font-weight:700; line-height:24px; text-align:center; margin-bottom:0.7rem;
}
.input-card {
    background:white; border-radius:16px; padding:1.6rem;
    box-shadow: 0 4px 20px rgba(13,59,46,0.10); border:1px solid rgba(76,175,125,0.2); margin-bottom:1.2rem;
}
.input-card-title {
    font-family:'Playfair Display',serif; font-size:1.1rem; font-weight:700; color:#0d3b2e;
    margin-bottom:1rem; padding-bottom:0.7rem; border-bottom:2px solid rgba(76,175,125,0.25);
}
.stNumberInput input {
    border:2px solid rgba(76,175,125,0.35) !important; border-radius:10px !important;
    padding:0.5rem 0.8rem !important; font-size:1rem !important; font-weight:600 !important;
    color:#0d3b2e !important; background:#f5fcf7 !important;
}
.range-hint { font-size:0.73rem; color:#1a5c42; font-weight:600; margin-top:-0.4rem; margin-bottom:0.7rem; }
.result-box {
    background:linear-gradient(135deg, #0d3b2e, #1a5c42); border-radius:16px; padding:1.8rem;
    text-align:center; box-shadow:0 8px 32px rgba(13,59,46,0.25); animation:fadeInUp 0.5s ease;
}
.result-crop-name {
    font-family:'Playfair Display',serif; font-size:2.2rem; font-weight:700;
    color:white; text-transform:capitalize; margin:0.4rem 0;
}
.result-label { font-size:0.78rem; color:rgba(255,255,255,0.75); text-transform:uppercase; letter-spacing:1px; }
.result-confidence {
    display:inline-block; background:rgba(76,175,125,0.35); border:1px solid #6dcf97;
    color:#c8ffdc; padding:5px 18px; border-radius:20px; font-size:0.88rem; font-weight:600; margin-top:0.8rem;
}
.yield-result {
    background:linear-gradient(135deg, #0d3b2e, #1e6b45); border-radius:16px; padding:1.8rem;
    text-align:center; box-shadow:0 8px 32px rgba(13,59,46,0.25);
}
.yield-value { font-family:'Playfair Display',serif; font-size:3rem; font-weight:700; color:#6dffaa; }
.tip-box {
    background:#e8f7ee; border:1px solid rgba(45,138,94,0.35); border-left:4px solid #2d8a5e;
    border-radius:10px; padding:0.9rem 1.2rem; margin-top:1rem; font-size:0.87rem; color:#0d2a1c; font-weight:400;
}
.unit-box {
    background:#fff8e1; border:1px solid #f0c040; border-left:4px solid #e6a817;
    border-radius:10px; padding:0.9rem 1.2rem; margin-top:0.8rem; font-size:0.87rem; color:#5a3e00; font-weight:400;
}
.stButton > button {
    background:linear-gradient(135deg, #1a5c42, #2d8a5e); color:white; border:none;
    border-radius:10px; padding:0.7rem 2rem; font-size:1rem; font-weight:600;
    font-family:'DM Sans',sans-serif; width:100%;
    box-shadow:0 4px 15px rgba(45,138,94,0.35); transition:all 0.25s ease;
}
.stButton > button:hover { transform:translateY(-2px); box-shadow:0 6px 20px rgba(45,138,94,0.5); }
.footer {
    text-align:center; padding:2rem 0 1rem; color:#1a4731; font-size:0.82rem; font-weight:500;
    border-top:1px solid rgba(76,175,125,0.2); margin-top:3rem;
}
@keyframes fadeInUp { from{opacity:0;transform:translateY(20px);} to{opacity:1;transform:translateY(0);} }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# LOAD MODELS & DATA
# ─────────────────────────────────────────────
@st.cache_resource
def load_models():
    with open('crop_model.pkl','rb') as f: cm = pickle.load(f)
    with open('yield_model.pkl','rb') as f: ym = pickle.load(f)
    with open('label_encoder.pkl','rb') as f: le = pickle.load(f)
    return cm, ym, le

@st.cache_data
def load_data():
    crop_df = pd.read_csv('Crop_recommendation.csv')
    apy_df  = pd.read_csv('APY.csv')
    apy_df.columns = apy_df.columns.str.strip()
    apy_df  = apy_df.dropna(subset=['Crop'])
    apy_df['Production'] = pd.to_numeric(apy_df['Production'], errors='coerce')
    apy_df['Production'].fillna(apy_df['Production'].median(), inplace=True)

    # ── FIX: Use per-crop IQR cleaning instead of global ──
    # This prevents removing legitimate high-yield crops like Onion (10-25 t/ha)
    cleaned = []
    for crop_name, grp in apy_df.groupby('Crop'):
        Q1 = grp['Yield'].quantile(0.05)
        Q3 = grp['Yield'].quantile(0.95)
        grp = grp[(grp['Yield'] >= Q1) & (grp['Yield'] <= Q3)]
        cleaned.append(grp)
    apy_df = pd.concat(cleaned, ignore_index=True)
    return crop_df, apy_df

crop_model, yield_model, le = load_models()
crop_df, apy_df = load_data()

CROP_EMOJI = {
    'rice':'🌾','maize':'🌽','jute':'🌿','cotton':'🌸','coconut':'🥥','papaya':'🍈',
    'orange':'🍊','apple':'🍎','muskmelon':'🍈','watermelon':'🍉','grapes':'🍇',
    'mango':'🥭','banana':'🍌','pomegranate':'🍎','lentil':'🫘','blackgram':'🫘',
    'mungbean':'🫘','mothbeans':'🫘','pigeonpeas':'🫘','kidneybeans':'🫘','chickpea':'🫘','coffee':'☕'
}
CROP_TIPS = {
    'rice':'Grows best in waterlogged fields. Ensure standing water during the growing season.',
    'maize':'Needs well-drained soil. Plant in rows with 60–75 cm spacing.',
    'cotton':'Deep, well-drained soil preferred. Requires a warm climate throughout growth.',
    'banana':'Requires consistent moisture and high potassium for fruit development.',
    'coffee':'Grows best in shade with high humidity. Avoid waterlogging.',
    'mango':'Requires a dry spell for flowering. Avoid frost-prone areas.',
    'coconut':'Thrives in coastal areas with high humidity and sandy loam soil.',
    'apple':'Requires cold winters for dormancy. Best grown in hilly regions.',
    'grapes':'Needs deep, well-drained soil and lots of sunshine.',
    'watermelon':'Loves sandy loam soil. Needs full sun and warm temperatures.',
}

# ── Shared chart layout ──
def chart_layout(title="", height=400):
    return dict(
        paper_bgcolor='white', plot_bgcolor='#f9fdf9',
        font=dict(family='DM Sans', size=13, color='#111111'),
        title=dict(text=f"<b>{title}</b>",
                   font=dict(family='Playfair Display', size=16, color='#0d3b2e'), x=0, xanchor='left'),
        height=height,
        margin=dict(t=55, b=60, l=60, r=40),
        xaxis=dict(showgrid=True, gridcolor='#ddeee4',
                   tickfont=dict(size=12, color='#111111'),
                   title_font=dict(size=13, color='#111111')),
        yaxis=dict(showgrid=True, gridcolor='#ddeee4',
                   tickfont=dict(size=12, color='#111111'),
                   title_font=dict(size=13, color='#111111')),
    )

SEQ_SCALE = [[0,'#c8f0d8'],[0.3,'#4caf7d'],[0.6,'#1a5c42'],[1,'#0d3b2e']]

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:1.5rem 0 1rem;'>
        <div style='font-size:2.6rem;'>🌿</div>
        <div style='font-family:"Playfair Display",serif; font-size:1.35rem; font-weight:700; color:#e8f5ee;'>AgroSense AI</div>
        <div style='font-size:0.7rem; color:rgba(255,255,255,0.6); margin-top:0.3rem; letter-spacing:1.5px;'>SMART FARMING PLATFORM</div>
    </div>
    <hr style='border-color:rgba(76,175,125,0.3); margin:0.5rem 0 1rem;'>
    """, unsafe_allow_html=True)

    page = st.radio("Navigate", [
        "🏠  Home", "🌱  Crop Advisor", "📈  Yield Predictor", "📊  Data Insights", "🗺️  Crop Map"
    ], label_visibility="collapsed")

    st.markdown("""
    <hr style='border-color:rgba(76,175,125,0.2); margin:1.5rem 0 1rem;'>
    <div style='font-size:0.72rem; color:rgba(255,255,255,0.6); text-align:center; line-height:2.1;'>
        ✅ Crop Model Loaded<br>✅ Yield Model Loaded<br>22 Crops · 293K Records<br>28 States + 8 Union Territories
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════
# HOME
# ═══════════════════════════════
if "Home" in page:
    st.markdown("""
    <div class='top-banner'>
        <div class='banner-badge'>✦ AI Powered Agriculture</div>
        <div class='banner-title'>Smart Crop Intelligence<br>for Indian Farmers 🌾</div>
        <div class='banner-sub'>Predict the best crop to grow & expected yield using soil data, climate conditions,<br>and 20+ years of Indian farming records.</div>
    </div>""", unsafe_allow_html=True)

    # 5 metric cards — 28 States + 8 UTs
    cols = st.columns(5)
    for col, (icon, val, label) in zip(cols, [
        ("🌱","99.3%","Crop Accuracy"),("📈","99.4%","Yield R² Score"),
        ("🌾","22","Crops Supported"),("📋","293K","Training Records"),("🗺️","28+8","States & UTs"),
    ]):
        with col:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-icon'>{icon}</div>
                <div class='metric-value'>{val}</div>
                <div class='metric-label'>{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<div class='section-header'><h2>🧭 How It Works</h2><div class='section-line'></div></div>", unsafe_allow_html=True)
    for col, (num, icon, title, desc) in zip(st.columns(4), [
        ("1","🧪","Enter Soil Data","Go to Crop Advisor. Enter your soil's Nitrogen (N), Phosphorus (P), Potassium (K) and pH from a soil test report."),
        ("2","🌤️","Add Climate Info","Enter your region's average temperature, humidity and annual rainfall in mm."),
        ("3","🤖","Get AI Prediction","Our Random Forest model (99.3% accurate) instantly tells you the best crop for your soil and climate."),
        ("4","📈","Predict Your Yield","Switch to Yield Predictor. Enter your farm area to get estimated harvest in tonnes per hectare."),
    ]):
        with col:
            st.markdown(f"""
            <div class='how-card'>
                <div class='step-num'>{num}</div>
                <div class='how-step'>{icon}</div>
                <div class='how-title'>{title}</div>
                <div class='how-desc'>{desc}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-header'><h2>✨ What You Can Do</h2><div class='section-line'></div></div>", unsafe_allow_html=True)
    f1, f2 = st.columns(2)
    with f1:
        st.markdown("""
        <div class='input-card'>
            <div class='input-card-title'>🌱 Crop Advisor</div>
            <p style='color:#0d2a1c; line-height:1.8; font-size:0.92rem;'>Enter your <b>soil nutrients (N, P, K)</b> and <b>climate data</b> to get an instant AI-powered crop recommendation with confidence score and farming tips.</p>
            <div style='background:#e5f5ec; border-radius:8px; padding:0.7rem 1rem; font-size:0.85rem; color:#0d3b2e; font-weight:600;'>
                ✅ 22 crops &nbsp;·&nbsp; ✅ 99.32% accuracy &nbsp;·&nbsp; ✅ Top 5 options shown
            </div>
        </div>""", unsafe_allow_html=True)
    with f2:
        st.markdown("""
        <div class='input-card'>
            <div class='input-card-title'>📈 Yield Predictor</div>
            <p style='color:#0d2a1c; line-height:1.8; font-size:0.92rem;'>Select your <b>state, crop, season and area</b> to get expected yield in <b>tonnes per hectare</b> — backed by 20 years of real Indian government farming records.</p>
            <div style='background:#e5f5ec; border-radius:8px; padding:0.7rem 1rem; font-size:0.85rem; color:#0d3b2e; font-weight:600;'>
                ✅ 293K records &nbsp;·&nbsp; ✅ Per-crop calibrated &nbsp;·&nbsp; ✅ All seasons covered
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div class='section-header'><h2>📊 Dataset Overview</h2><div class='section-line'></div></div>", unsafe_allow_html=True)
    d1, d2 = st.columns(2)
    with d1:
        counts = crop_df['label'].value_counts().reset_index()
        counts.columns = ['Crop','Count']
        fig = px.bar(counts, x='Crop', y='Count', color='Count',
                     color_continuous_scale=SEQ_SCALE,
                     labels={'Crop':'Crop Name','Count':'Number of Records'})
        fig.update_layout(**chart_layout('Records per Crop — Crop Dataset', 380))
        fig.update_layout(coloraxis_showscale=False)
        fig.update_xaxes(tickangle=45, tickfont=dict(size=10, color='#111'))
        st.plotly_chart(fig, use_container_width=True)
    with d2:
        top10 = apy_df['Crop'].value_counts().head(10).reset_index()
        top10.columns = ['Crop','Count']
        fig2 = px.bar(top10, x='Count', y='Crop', orientation='h',
                      color='Count', color_continuous_scale=SEQ_SCALE,
                      text='Count', labels={'Count':'Number of Records','Crop':'Crop Name'})
        fig2.update_traces(textposition='outside', textfont=dict(size=12, color='#111111'))
        fig2.update_layout(**chart_layout('Top 10 Most Grown Crops — APY Dataset', 380))
        fig2.update_layout(coloraxis_showscale=False)
        fig2.update_yaxes(tickfont=dict(size=12, color='#111111'))
        st.plotly_chart(fig2, use_container_width=True)

# ═══════════════════════════════
# CROP ADVISOR
# ═══════════════════════════════
elif "Crop Advisor" in page:
    st.markdown("""
    <div class='top-banner'>
        <div class='banner-badge'>✦ Classification Model</div>
        <div class='banner-title'>🌱 Crop Advisor</div>
        <div class='banner-sub'>Enter your soil nutrients and climate data to get an instant AI crop recommendation.</div>
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns([1.3, 1])
    with col1:
        st.markdown("<div class='input-card'><div class='input-card-title'>🧪 Soil Nutrients</div>", unsafe_allow_html=True)
        st.markdown("<div class='tip-box' style='margin-bottom:1rem;'>💡 <b>Where to get these?</b> From a soil test at your nearest Krishi Kendra. Values are in kg/ha.</div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("**🟢 Nitrogen (N)**")
            st.markdown("<div class='range-hint'>Range: 0 – 140 kg/ha</div>", unsafe_allow_html=True)
            N = st.number_input("N_v", min_value=0, max_value=140, value=50, label_visibility="collapsed")
        with c2:
            st.markdown("**🟡 Phosphorus (P)**")
            st.markdown("<div class='range-hint'>Range: 5 – 145 kg/ha</div>", unsafe_allow_html=True)
            P = st.number_input("P_v", min_value=5, max_value=145, value=50, label_visibility="collapsed")
        with c3:
            st.markdown("**🟠 Potassium (K)**")
            st.markdown("<div class='range-hint'>Range: 5 – 205 kg/ha</div>", unsafe_allow_html=True)
            K = st.number_input("K_v", min_value=5, max_value=205, value=48, label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='input-card'><div class='input-card-title'>🌤️ Climate Conditions</div>", unsafe_allow_html=True)
        st.markdown("<div class='tip-box' style='margin-bottom:1rem;'>💡 Use your city's average values. pH 7 = neutral, below 7 = acidic, above 7 = alkaline. Rainfall = annual average in mm.</div>", unsafe_allow_html=True)
        c4, c5 = st.columns(2)
        with c4:
            st.markdown("**🌡️ Temperature (°C)**")
            st.markdown("<div class='range-hint'>Cold: 8–15 | Mild: 15–30 | Hot: 30–44</div>", unsafe_allow_html=True)
            temp = st.number_input("tp_v", min_value=8.0, max_value=44.0, value=25.0, step=0.5, label_visibility="collapsed")
            st.markdown("**💧 Humidity (%)**")
            st.markdown("<div class='range-hint'>Dry: < 40 | Moderate: 40–70 | Humid: > 70</div>", unsafe_allow_html=True)
            humidity = st.number_input("hm_v", min_value=14.0, max_value=100.0, value=70.0, step=1.0, label_visibility="collapsed")
        with c5:
            st.markdown("**🧫 Soil pH**")
            st.markdown("<div class='range-hint'>Acidic: < 6 | Neutral: 6–7 | Alkaline: > 7</div>", unsafe_allow_html=True)
            ph = st.number_input("ph_v", min_value=3.5, max_value=9.9, value=6.5, step=0.1, label_visibility="collapsed")
            st.markdown("**🌧️ Rainfall (mm)**")
            st.markdown("<div class='range-hint'>Low: < 60 | Medium: 60–150 | High: > 150</div>", unsafe_allow_html=True)
            rainfall = st.number_input("rf_v", min_value=20.0, max_value=300.0, value=100.0, step=5.0, label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)
        predict_btn = st.button("🔍 Recommend Best Crop", use_container_width=True)

    with col2:
        st.markdown("<div class='section-header'><h2>Your Soil Profile</h2><div class='section-line'></div></div>", unsafe_allow_html=True)
        cats  = ['Nitrogen','Phosphorus','Potassium','Temperature','Humidity','pH','Rainfall']
        vnorm = [N/140, P/145, K/205, temp/44, humidity/100, ph/9.9, rainfall/300]
        fig_r = go.Figure(go.Scatterpolar(
            r=vnorm+[vnorm[0]], theta=cats+[cats[0]],
            fill='toself', fillcolor='rgba(45,138,94,0.18)',
            line=dict(color='#1a5c42', width=2.5),
        ))
        fig_r.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0,1], showticklabels=False, gridcolor='#bbb'),
                angularaxis=dict(tickfont=dict(size=12, color='#0d3b2e'), gridcolor='#bbb')
            ),
            showlegend=False, paper_bgcolor='white',
            font_family='DM Sans', margin=dict(t=30,b=30,l=50,r=50), height=290
        )
        st.plotly_chart(fig_r, use_container_width=True)

        if predict_btn:
            inp_d = np.array([[N, P, K, temp, humidity, ph, rainfall]])
            pred  = crop_model.predict(inp_d)[0]
            cname = le.inverse_transform([pred])[0]
            proba = crop_model.predict_proba(inp_d)[0]
            conf  = round(max(proba)*100, 1)
            emoji = CROP_EMOJI.get(cname,'🌿')
            tip   = CROP_TIPS.get(cname, f'{cname.capitalize()} grows well under your conditions.')

            st.markdown(f"""
            <div class='result-box'>
                <div class='result-label'>Recommended Crop</div>
                <div style='font-size:3rem;'>{emoji}</div>
                <div class='result-crop-name'>{cname.upper()}</div>
                <div class='result-confidence'>✓ {conf}% Confidence</div>
            </div>
            <div class='tip-box'>💡 <b>Farming Tip:</b> {tip}</div>
            """, unsafe_allow_html=True)

            top5i = np.argsort(proba)[::-1][:5]
            top5c = le.inverse_transform(top5i)
            top5p = proba[top5i]*100
            bar_cols = ['#0d3b2e','#1a5c42','#2d8a5e','#4caf7d','#7dd4a0']
            fig_t = go.Figure(go.Bar(
                x=top5p, y=top5c, orientation='h',
                marker_color=bar_cols,
                text=[f"{p:.1f}%" for p in top5p], textposition='outside',
                textfont=dict(size=13, color='#0d3b2e')
            ))
            # FIX: Don't pass xaxis/yaxis inside chart_layout AND update_layout together
            layout = chart_layout('Top 5 Crop Probabilities', 220)
            layout['xaxis'] = dict(range=[0,115], showgrid=False, showticklabels=False)
            layout['yaxis'] = dict(showgrid=False, tickfont=dict(size=13, color='#111111'))
            fig_t.update_layout(**layout)
            st.plotly_chart(fig_t, use_container_width=True)

# ═══════════════════════════════
# YIELD PREDICTOR
# ═══════════════════════════════
elif "Yield Predictor" in page:
    st.markdown("""
    <div class='top-banner'>
        <div class='banner-badge'>✦ Regression Model</div>
        <div class='banner-title'>📈 Yield Predictor</div>
        <div class='banner-sub'>Predict expected crop yield in tonnes/ha from location, crop type, season and farm area.</div>
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns([1.2,1])
    with col1:
        st.markdown("<div class='input-card'><div class='input-card-title'>📍 Location & Crop Details</div>", unsafe_allow_html=True)
        st.markdown("<div class='tip-box' style='margin-bottom:1rem;'>💡 Select your state, crop and season. Farm area: 1 acre ≈ 0.4 ha | 1 bigha ≈ 0.25 ha.</div>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            state  = st.selectbox("📍 State",   sorted(apy_df['State'].unique()))
            crop   = st.selectbox("🌾 Crop",    sorted(apy_df['Crop'].unique()))
        with c2:
            season   = st.selectbox("🗓️ Season",   sorted(apy_df['Season'].unique()))
            district = st.selectbox("🏘️ District", sorted(apy_df['District'].unique()))
        c3, c4 = st.columns(2)
        with c3:
            st.markdown("**Farm Area (hectares)**")
            st.markdown("<div class='range-hint'>1 acre = 0.4 ha | 1 bigha ≈ 0.25 ha</div>", unsafe_allow_html=True)
            area = st.number_input("ar_v", min_value=0.01, value=10.0, step=1.0, label_visibility="collapsed")
        with c4:
            crop_year = st.number_input("📅 Crop Year", min_value=1997, max_value=2030, value=2024)
        st.markdown("**Expected Production (tonnes)**")
        st.markdown("<div class='range-hint'>Your estimated total harvest weight in tonnes</div>", unsafe_allow_html=True)
        production = st.number_input("pr_v", min_value=0.0, value=50.0, step=5.0, label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)
        predict_yield_btn = st.button("📈 Predict Yield", use_container_width=True)

    with col2:
        if predict_yield_btn:
            from sklearn.preprocessing import LabelEncoder as LE
            def safe_enc(series, val):
                l = LE(); l.fit(series)
                return l.transform([val])[0] if val in l.classes_ else 0

            inp = np.array([[safe_enc(apy_df['State'],state), safe_enc(apy_df['District'],district),
                             safe_enc(apy_df['Crop'],crop), crop_year,
                             safe_enc(apy_df['Season'],season), area, production]])
            pred_y  = yield_model.predict(inp)[0]
            total_e = pred_y * area
            avg_y   = apy_df[apy_df['Crop']==crop]['Yield'].mean()
            diff    = pred_y - avg_y
            ds      = f"+{diff:.2f}" if diff>=0 else f"{diff:.2f}"
            dc      = "#55e890" if diff>=0 else "#ff8080"

            # Unit note: Yield in dataset = Production(tonnes) / Area(ha) = tonnes/ha
            st.markdown(f"""
            <div class='yield-result'>
                <div style='color:rgba(255,255,255,0.75); font-size:0.8rem; text-transform:uppercase; letter-spacing:1px;'>Predicted Yield</div>
                <div class='yield-value'>{pred_y:.2f}</div>
                <div style='color:rgba(255,255,255,0.7); font-size:0.95rem; font-weight:500;'>tonnes per hectare (t/ha)</div>
                <hr style='border-color:rgba(76,175,125,0.4); margin:0.9rem 0;'>
                <div style='color:rgba(255,255,255,0.7); font-size:0.8rem;'>Estimated Total Harvest</div>
                <div style='font-family:"Playfair Display",serif; font-size:1.7rem; color:#aaffcc; font-weight:700;'>{total_e:,.1f} tonnes</div>
                <div style='color:rgba(255,255,255,0.5); font-size:0.76rem;'>({area} ha × {pred_y:.2f} t/ha)</div>
                <hr style='border-color:rgba(76,175,125,0.4); margin:0.8rem 0;'>
                <div style='color:rgba(255,255,255,0.7); font-size:0.8rem;'>vs Avg Yield for {crop}</div>
                <div style='font-size:1.2rem; font-weight:700; color:{dc};'>{ds} t/ha</div>
            </div>""", unsafe_allow_html=True)

            # Unit explanation box
            st.markdown(f"""
            <div class='unit-box'>
                📏 <b>Unit Guide:</b> The yield shown is in <b>tonnes per hectare (t/ha)</b>.<br>
                To convert: 1 t/ha = 1,000 kg/ha = 10 quintals/ha.<br>
                Avg yield for <b>{crop}</b> in this dataset: <b>{avg_y:.2f} t/ha</b>
                ({avg_y*1000:,.0f} kg/ha or {avg_y*10:.0f} quintals/ha).
            </div>""", unsafe_allow_html=True)

            # Gauge
            crop_max = apy_df[apy_df['Crop']==crop]['Yield'].quantile(0.95)
            crop_p33 = apy_df[apy_df['Crop']==crop]['Yield'].quantile(0.33)
            crop_p66 = apy_df[apy_df['Crop']==crop]['Yield'].quantile(0.66)
            fig_g = go.Figure(go.Indicator(
                mode="gauge+number",
                value=round(pred_y,2),
                number={'suffix':' t/ha','font':{'size':24,'color':'#0d3b2e','family':'Playfair Display'}},
                title={'text':f'Yield Range for {crop}','font':{'size':13,'family':'DM Sans','color':'#0d3b2e'}},
                gauge={
                    'axis':{'range':[0, crop_max], 'tickfont':{'size':11,'color':'#111'}},
                    'bar':{'color':'#1a5c42'},
                    'steps':[
                        {'range':[0, crop_p33],'color':'#d5f0e0'},
                        {'range':[crop_p33, crop_p66],'color':'#7dd4a0'},
                        {'range':[crop_p66, crop_max],'color':'#2d8a5e'}
                    ],
                    'threshold':{'line':{'color':'#c9a84c','width':3},'value':avg_y}
                }
            ))
            fig_g.update_layout(paper_bgcolor='white', font_family='DM Sans', height=260, margin=dict(t=45,b=15,l=30,r=30))
            st.plotly_chart(fig_g, use_container_width=True)

        else:
            avg_s = apy_df.groupby('Season')['Yield'].mean().reset_index()
            avg_s['Yield_r'] = avg_s['Yield'].round(2)
            season_colors = ['#0d3b2e','#1a5c42','#2d8a5e','#4caf7d','#7dd4a0','#b0e8c8']
            fig_s = go.Figure(go.Bar(
                x=avg_s['Season'], y=avg_s['Yield'],
                marker_color=season_colors[:len(avg_s)],
                text=avg_s['Yield_r'], textposition='outside',
                textfont=dict(size=13, color='#111111')
            ))
            layout_s = chart_layout('Average Yield by Season (t/ha)', 380)
            layout_s['xaxis'] = dict(title='Season', showgrid=True, gridcolor='#ddeee4',
                                     tickfont=dict(size=13, color='#111111'))
            layout_s['yaxis'] = dict(title='Average Yield (t/ha)', showgrid=True, gridcolor='#ddeee4',
                                     tickfont=dict(size=12, color='#111111'))
            fig_s.update_layout(**layout_s)
            st.plotly_chart(fig_s, use_container_width=True)
            st.markdown("<div class='tip-box'>👆 Fill in the form and click <b>Predict Yield</b> to see your result.<br>📏 Yield unit: <b>tonnes per hectare (t/ha)</b>. Example: Onion = ~15 t/ha.</div>", unsafe_allow_html=True)

# ═══════════════════════════════
# DATA INSIGHTS
# ═══════════════════════════════
elif "Data Insights" in page:
    st.markdown("""
    <div class='top-banner'>
        <div class='banner-badge'>✦ Exploratory Data Analysis</div>
        <div class='banner-title'>📊 Data Insights</div>
        <div class='banner-sub'>Visual analysis of soil conditions, crop distributions and yield patterns across India.</div>
    </div>""", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🌱  Crop Dataset", "📈  APY Dataset"])

    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            fig = px.histogram(crop_df, x='N', nbins=35, color_discrete_sequence=['#1a5c42'],
                               labels={'N':'Nitrogen (kg/ha)','count':'Count'})
            fig.update_layout(**chart_layout('Nitrogen (N) Distribution'))
            fig.update_traces(marker_line_color='white', marker_line_width=0.5)
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            fig = px.histogram(crop_df, x='rainfall', nbins=35, color_discrete_sequence=['#2d8a5e'],
                               labels={'rainfall':'Rainfall (mm)','count':'Count'})
            fig.update_layout(**chart_layout('Rainfall Distribution (mm)'))
            fig.update_traces(marker_line_color='white', marker_line_width=0.5)
            st.plotly_chart(fig, use_container_width=True)

        c3, c4 = st.columns(2)
        with c3:
            fig = px.histogram(crop_df, x='ph', nbins=35, color_discrete_sequence=['#236e4a'],
                               labels={'ph':'Soil pH','count':'Count'})
            fig.update_layout(**chart_layout('Soil pH Distribution'))
            fig.update_traces(marker_line_color='white', marker_line_width=0.5)
            st.plotly_chart(fig, use_container_width=True)
        with c4:
            fig = px.histogram(crop_df, x='humidity', nbins=35, color_discrete_sequence=['#4caf7d'],
                               labels={'humidity':'Humidity (%)','count':'Count'})
            fig.update_layout(**chart_layout('Humidity Distribution (%)'))
            fig.update_traces(marker_line_color='white', marker_line_width=0.5)
            st.plotly_chart(fig, use_container_width=True)

        fig_b = px.box(crop_df, x='label', y='temperature',
                       color_discrete_sequence=['#1a5c42'],
                       labels={'label':'Crop Name','temperature':'Temperature (°C)'})
        fig_b.update_layout(**chart_layout('Temperature Range Required by Each Crop', 430))
        fig_b.update_xaxes(tickangle=40, tickfont=dict(size=11, color='#111111'))
        st.plotly_chart(fig_b, use_container_width=True)

        corr = crop_df[['N','P','K','temperature','humidity','ph','rainfall']].corr().round(2)
        fig_h = px.imshow(corr, text_auto=True,
                          color_continuous_scale=[[0,'#2166ac'],[0.5,'#f7f7f7'],[1,'#b2182b']],
                          zmin=-1, zmax=1)
        fig_h.update_layout(
            paper_bgcolor='white',
            font=dict(family='DM Sans', size=14, color='#111111'),
            title=dict(text='<b>Correlation Heatmap — Soil & Climate Features</b>',
                       font=dict(family='Playfair Display', size=16, color='#0d3b2e')),
            margin=dict(t=55,b=40,l=60,r=40), height=430,
            xaxis=dict(tickfont=dict(size=13, color='#111111')),
            yaxis=dict(tickfont=dict(size=13, color='#111111')),
            coloraxis_colorbar=dict(tickfont=dict(size=12, color='#111111'))
        )
        fig_h.update_traces(textfont=dict(size=14, color='#111111'))
        st.plotly_chart(fig_h, use_container_width=True)

    with tab2:
        c1, c2 = st.columns(2)
        with c1:
            t15 = apy_df['Crop'].value_counts().head(15).reset_index()
            t15.columns = ['Crop','Count']
            fig = px.bar(t15, x='Count', y='Crop', orientation='h',
                         color='Count', color_continuous_scale=SEQ_SCALE,
                         text='Count', labels={'Count':'Number of Records','Crop':'Crop Name'})
            fig.update_traces(textposition='outside', textfont=dict(size=12, color='#111111'))
            fig.update_layout(**chart_layout('Top 15 Most Grown Crops in India', 450))
            fig.update_layout(coloraxis_showscale=False)
            fig.update_yaxes(tickfont=dict(size=12, color='#111111'))
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            sc = apy_df['Season'].value_counts().reset_index()
            sc.columns = ['Season','Count']
            fig = px.pie(sc, values='Count', names='Season',
                         color_discrete_sequence=['#0d3b2e','#1a5c42','#2d8a5e','#4caf7d','#7dd4a0','#b0e8c8'],
                         hole=0.4)
            fig.update_traces(textfont=dict(size=13, color='#111111'), textinfo='label+percent', pull=[0.03]*len(sc))
            fig.update_layout(
                paper_bgcolor='white',
                font=dict(family='DM Sans', size=13, color='#111111'),
                title=dict(text='<b>Crop Distribution by Season</b>',
                           font=dict(family='Playfair Display', size=16, color='#0d3b2e')),
                margin=dict(t=55,b=30,l=30,r=30), height=450
            )
            st.plotly_chart(fig, use_container_width=True)

        yr = apy_df.groupby('Crop_Year')['Yield'].mean().reset_index()
        fig = px.line(yr, x='Crop_Year', y='Yield', markers=True,
                      color_discrete_sequence=['#1a5c42'],
                      labels={'Crop_Year':'Year','Yield':'Average Yield (t/ha)'})
        fig.update_layout(**chart_layout('Average Yield Trend Across India (1997–2020)', 380))
        fig.update_traces(line_width=2.5, marker_size=8,
                          marker=dict(color='#0d3b2e', line=dict(width=2, color='white')))
        st.plotly_chart(fig, use_container_width=True)

        st_top = apy_df.groupby('State')['Yield'].mean().nlargest(15).reset_index()
        st_top['Yield_r'] = st_top['Yield'].round(2)
        fig = px.bar(st_top, x='Yield', y='State', orientation='h',
                     color='Yield', color_continuous_scale=SEQ_SCALE,
                     text='Yield_r', labels={'Yield':'Average Yield (t/ha)','State':'State'})
        fig.update_traces(textposition='outside', textfont=dict(size=12, color='#111111'))
        fig.update_layout(**chart_layout('Top 15 States by Average Yield (t/ha)', 480))
        fig.update_layout(coloraxis_showscale=False)
        fig.update_yaxes(tickfont=dict(size=12, color='#111111'))
        st.plotly_chart(fig, use_container_width=True)

# ═══════════════════════════════
# CROP MAP
# ═══════════════════════════════
elif "Crop Map" in page:
    st.markdown("""
    <div class='top-banner'>
        <div class='banner-badge'>✦ Geographic Analysis</div>
        <div class='banner-title'>🗺️ India Crop Map</div>
        <div class='banner-sub'>Explore crop production and yield patterns across Indian states and union territories.</div>
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2.2])
    with col1:
        sel_crop = st.selectbox("🌾 Select Crop", sorted(apy_df['Crop'].unique()))
        metric   = st.radio("📊 Metric", ["Average Yield","Total Production","Total Area"])
        cd = apy_df[apy_df['Crop']==sel_crop]
        bs  = cd.groupby('State')['Yield'].mean().idxmax()
        bsn = cd.groupby('Season')['Yield'].mean().idxmax()
        avg_y = cd['Yield'].mean()
        st.markdown(f"""
        <div class='input-card' style='margin-top:1rem;'>
            <div class='input-card-title'>📋 {sel_crop} Stats</div>
            <div style='font-size:0.87rem; color:#0d2a1c; line-height:2.4; font-weight:400;'>
                📍 <b>States grown in:</b> {cd['State'].nunique()}<br>
                📅 <b>Data years:</b> {int(cd['Crop_Year'].min())} – {int(cd['Crop_Year'].max())}<br>
                📈 <b>Avg Yield:</b> {avg_y:.2f} t/ha ({avg_y*1000:,.0f} kg/ha)<br>
                🏆 <b>Best State:</b> {bs}<br>
                🗓️ <b>Best Season:</b> {bsn}
            </div>
        </div>""", unsafe_allow_html=True)

    with col2:
        filtered = apy_df[apy_df['Crop']==sel_crop]
        if metric == "Average Yield":
            sd = filtered.groupby('State')['Yield'].mean().reset_index(); sd.columns=['State','Value']; lbl='Avg Yield (t/ha)'
        elif metric == "Total Production":
            sd = filtered.groupby('State')['Production'].sum().reset_index(); sd.columns=['State','Value']; lbl='Production (tonnes)'
        else:
            sd = filtered.groupby('State')['Area'].sum().reset_index(); sd.columns=['State','Value']; lbl='Area (ha)'

        sd = sd.sort_values('Value',ascending=True).tail(20)
        sd['Val_r'] = sd['Value'].round(2)
        fig = px.bar(sd, x='Value', y='State', orientation='h',
                     color='Value', color_continuous_scale=SEQ_SCALE,
                     text='Val_r', labels={'Value':lbl,'State':'State'})
        fig.update_traces(textposition='outside', textfont=dict(size=12, color='#111111'))
        fig.update_layout(**chart_layout(f'{sel_crop} — {metric} by State (Top 20)', 520))
        fig.update_layout(coloraxis_colorbar_title=lbl)
        fig.update_yaxes(tickfont=dict(size=12, color='#111111'))
        st.plotly_chart(fig, use_container_width=True)

    yc = apy_df[apy_df['Crop']==sel_crop].groupby('Crop_Year')['Yield'].mean().reset_index()
    fig2 = px.area(yc, x='Crop_Year', y='Yield', markers=True,
                   color_discrete_sequence=['#1a5c42'],
                   labels={'Crop_Year':'Year','Yield':'Average Yield (t/ha)'})
    fig2.update_layout(**chart_layout(f'{sel_crop} — Yield Trend Over Years', 380))
    fig2.update_traces(fillcolor='rgba(45,138,94,0.12)', line_width=2.5,
                       marker_size=7, marker=dict(color='#0d3b2e', line=dict(width=2, color='white')))
    st.plotly_chart(fig2, use_container_width=True)

# FOOTER
st.markdown("""
<div class='footer'>
    🌿 AgroSense AI &nbsp;·&nbsp; Built with Streamlit & Scikit-learn &nbsp;·&nbsp; Random Forest Models<br>
    Crop Accuracy: 99.32% &nbsp;·&nbsp; Yield R²: 0.9936 &nbsp;·&nbsp; 28 States + 8 Union Territories
</div>
""", unsafe_allow_html=True)
