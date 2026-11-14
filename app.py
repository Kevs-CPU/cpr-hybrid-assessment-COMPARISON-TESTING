
import streamlit as st
import pandas as pd

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="CPR Research Dashboard",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# PROFESSIONAL GLASSMORPHISM DESIGN
# ==========================================

st.markdown("""
<style>

/* Main background */
.stApp {
    background:
        radial-gradient(circle at 10% 10%,
        rgba(115, 169, 210, 0.22), transparent 35%),
        radial-gradient(circle at 90% 85%,
        rgba(139, 178, 204, 0.22), transparent 35%),
        linear-gradient(135deg, #edf3f8, #e5edf4, #f5f8fb);

    height: 100vh;
    overflow: hidden;
}

/* Remove unnecessary header and footer */
[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stToolbar"] {
    display: none;
}

footer {
    visibility: hidden;
}

/* Main container */
.block-container {
    max-width: 1500px;
    padding: 0.8rem 2rem 0.4rem;
}

/* Compact spacing */
[data-testid="stVerticalBlock"] {
    gap: 0.55rem;
}

/* Typography */
h1, h2, h3, p, label {
    color: #203449;
}

h1 {
    font-size: 2rem !important;
    font-weight: 750 !important;
    letter-spacing: -1px;
}

h2 {
    font-size: 1.15rem !important;
    font-weight: 700 !important;
}

h3 {
    font-size: 1rem !important;
}

/* Hero glass panel */
.hero {
    background: rgba(255, 255, 255, 0.48);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);

    border: 1px solid rgba(255,255,255,0.85);
    border-radius: 20px;

    padding: 17px 24px;
    box-shadow: 0 8px 28px rgba(35, 65, 90, 0.07);
    margin-bottom: 4px;
}

.hero-label {
    color: #5680a2;
    font-size: 0.69rem;
    font-weight: 800;
    letter-spacing: 2px;
    margin-bottom: 5px;
}

.hero-title {
    color: #203c56;
    font-size: 1.75rem;
    font-weight: 800;
    line-height: 1.18;
    margin: 0;
}

.hero-subtitle {
    color: #647b90;
    font-size: 0.88rem;
    margin-top: 7px;
}

/* Glass cards */
.glass-card {
    background: rgba(255, 255, 255, 0.52);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);

    border: 1px solid rgba(255,255,255,0.85);
    border-radius: 16px;

    padding: 15px 17px;
    min-height: 112px;

    box-shadow: 0 6px 22px rgba(35, 65, 90, 0.055);
}

.card-label {
    font-size: 0.68rem;
    font-weight: 800;
    letter-spacing: 1.3px;
    color: #66829a;
    margin-bottom: 8px;
}

.card-title {
    font-size: 1.05rem;
    font-weight: 750;
    color: #29445e;
    margin-bottom: 5px;
}

.card-description {
    font-size: 0.79rem;
    color: #667d90;
    line-height: 1.45;
}

.proposed-card {
    background: rgba(220, 240, 231, 0.55);
    border: 1px solid rgba(125, 190, 158, 0.55);
}

/* Status cards */
.status-card {
    background: rgba(255,255,255,0.52);
    backdrop-filter: blur(16px);

    border: 1px solid rgba(255,255,255,0.85);
    border-radius: 14px;

    padding: 11px 14px;
    text-align: center;
}

.status-value {
    font-size: 1.35rem;
    font-weight: 800;
    color: #294b68;
}

.status-name {
    font-size: 0.72rem;
    color: #71869a;
    font-weight: 650;
}

/* Section label */
.section-label {
    font-size: 1rem;
    font-weight: 750;
    color: #29445e;
    margin: 4px 0 5px;
}

/* Upload area */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.45);
    border: 1px dashed rgba(91,130,162,0.45);
    border-radius: 13px;
    padding: 9px;
}

[data-testid="stFileUploaderDropzone"] {
    background: rgba(255,255,255,0.4);
    border: none;
}

/* Alerts */
[data-testid="stAlert"] {
    background: rgba(255,255,255,0.58);
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.8);
}

/* Metric cards */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.48);
    border: 1px solid rgba(255,255,255,0.85);
    border-radius: 13px;
    padding: 9px 12px;
}

[data-testid="stMetricLabel"] {
    color: #71869a;
}

[data-testid="stMetricValue"] {
    color: #294b68;
}

/* Footer */
.footer {
    text-align: center;
    color: #8497a8;
    font-size: 0.7rem;
    padding: 5px 0;
}

/* Desktop screen fitting */
@media (max-height: 800px) {
    .block-container {
        padding-top: 0.45rem;
        padding-bottom: 0.15rem;
    }

    .hero {
        padding: 12px 19px;
    }

    .glass-card {
        min-height: 100px;
        padding: 11px 14px;
    }

    h1 {
        font-size: 1.65rem !important;
    }
}

/* Smaller screens: allow access to all content */
@media (max-width: 900px) {
    .stApp {
        height: auto;
        min-height: 100vh;
        overflow: auto;
    }

    .block-container {
        padding: 1rem;
    }
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# HEADER
# ==========================================

st.markdown("""
<div class="hero">
    <div class="hero-label">
        NORTH EASTERN MINDANAO STATE UNIVERSITY
        | LIANGA CAMPUS
    </div>

    <div class="hero-title">
        AI-Assisted CPR Proper Execution Training System
    </div>

    <div class="hero-subtitle">
        Comparative Research and Experimental Dashboard
        &nbsp; • &nbsp; BS Computer Science
    </div>
</div>
""", unsafe_allow_html=True)


# ==========================================
# RESEARCH FRAMEWORK
# ==========================================

st.markdown(
    '<div class="section-label">Research Framework</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    st.markdown("""
    <div class="glass-card">
        <div class="card-label">EXISTING SYSTEM 01</div>
        <div class="card-title">Ecker et al. (2024)</div>
        <div class="card-description">
            MediaPipe Pose-based CPR assessment.
            Body landmark analysis and CPR measurement evaluation.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="glass-card">
        <div class="card-label">EXISTING SYSTEM 02</div>
        <div class="card-title">SmartCPR (2024)</div>
        <div class="card-description">
            MoveNet-based smartphone CPR assessment
            with measurement analysis and feedback.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="glass-card proposed-card">
        <div class="card-label">PROPOSED CONTRIBUTION</div>
        <div class="card-title">Hybrid CPR System</div>
        <div class="card-description">
            MediaPipe Pose + Hand, Machine Learning,
            Rule-Based Assessment and Hybrid Decision Engine.
        </div>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# EXPERIMENTAL STATUS
# ==========================================

st.markdown(
    '<div class="section-label">Experimental Status</div>',
    unsafe_allow_html=True
)

s1, s2, s3, s4 = st.columns(4, gap="small")

with s1:
    st.markdown("""
    <div class="status-card">
        <div class="status-value">02</div>
        <div class="status-name">Existing References</div>
    </div>
    """, unsafe_allow_html=True)

with s2:
    st.markdown("""
    <div class="status-card">
        <div class="status-value">01</div>
        <div class="status-name">Proposed System</div>
    </div>
    """, unsafe_allow_html=True)

with s3:
    st.markdown("""
    <div class="status-card">
        <div class="status-value">GBC</div>
        <div class="status-name">Provisional ML Model</div>
    </div>
    """, unsafe_allow_html=True)

with s4:
    st.markdown("""
    <div class="status-card">
        <div class="status-value">Pending</div>
        <div class="status-name">Experimental Results</div>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# DATASET AND MODEL
# ==========================================

left, right = st.columns([1.25, 1], gap="medium")

with left:

    st.markdown(
        '<div class="section-label">Experimental Dataset</div>',
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Upload validated prediction data (CSV)",
        type=["csv"],
        label_visibility="collapsed"
    )

    if uploaded_file is not None:
        try:
            data = pd.read_csv(uploaded_file)

            if data.empty:
                st.error("The uploaded CSV contains no records.")

            else:
                required = [
                    "participant_id",
                    "clip_id",
                    "system",
                    "actual_label",
                    "predicted_label"
                ]

                missing = [
                    col for col in required
                    if col not in data.columns
                ]

                if missing:
                    st.warning(
                        "Missing columns: " + ", ".join(missing)
                    )

                else:
                    st.success(
                        f"Validated structure detected: "
                        f"{len(data)} records."
                    )

        except (pd.errors.EmptyDataError,
                pd.errors.ParserError,
                UnicodeDecodeError):
            st.error("Unable to read this CSV file.")

    else:
        st.caption(
            "No experimental data uploaded. "
            "Results will remain pending until valid testing."
        )


with right:

    st.markdown(
        '<div class="section-label">Machine Learning Approach</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="glass-card">
        <div class="card-label">PROVISIONAL CLASSIFICATION MODEL</div>
        <div class="card-title">
            Gradient Boosting Classifier
        </div>
        <div class="card-description">
            Uses extracted body and hand movement features
            to classify selected CPR movement patterns.
            Final selection depends on validation and
            computational performance.
        </div>
        <br>
        <div class="card-label">
            MLflow EXPERIMENT TRACKING: NOT CONNECTED
        </div>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# PLANNED EVALUATION METRICS
# ==========================================

st.markdown(
    '<div class="section-label">Planned Evaluation Metrics</div>',
    unsafe_allow_html=True
)

m1, m2, m3, m4 = st.columns(4, gap="small")

with m1:
    st.metric("Accuracy", "Pending")

with m2:
    st.metric("Precision", "Pending")

with m3:
    st.metric("Recall", "Pending")

with m4:
    st.metric("F1-Score", "Pending")


# ==========================================
# FOOTER
# ==========================================

st.markdown("""
<div class="footer">
    NEMSU - Lianga Campus
    &nbsp; | &nbsp;
    AI-Assisted CPR Research Project
    &nbsp; | &nbsp;
    2026
</div>
""", unsafe_allow_html=True)
