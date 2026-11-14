
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

/* ==========================================
   GLOBAL BACKGROUND AND TEXT
========================================== */

.stApp {
    background:
        radial-gradient(circle at 10% 10%,
        rgba(115, 169, 210, 0.20), transparent 35%),
        radial-gradient(circle at 90% 85%,
        rgba(139, 178, 204, 0.20), transparent 35%),
        linear-gradient(135deg, #edf3f8, #e5edf4, #f5f8fb);

    color: #203449 !important;
    min-height: 100vh;
    overflow-x: hidden;
}

/* Light theme consistency */
html, body, [data-testid="stAppViewContainer"] {
    color: #203449 !important;
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stToolbar"] {
    display: none;
}

footer {
    visibility: hidden;
}

/* Main content */
.block-container {
    max-width: 1500px;
    padding: 0.8rem 2rem 1rem;
}

/* All standard text */
.stApp h1,
.stApp h2,
.stApp h3,
.stApp h4,
.stApp p,
.stApp label,
.stApp li,
.stApp span,
.stApp small,
[data-testid="stMarkdownContainer"],
[data-testid="stCaptionContainer"] {
    color: #203449;
}

/* Headings */
h1 {
    font-size: 1.9rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.7px;
}

h2 {
    font-size: 1.15rem !important;
    font-weight: 750 !important;
}

h3 {
    font-size: 1rem !important;
    font-weight: 700 !important;
}

/* ==========================================
   GLASS HERO HEADER
========================================== */

.hero {
    background: rgba(255,255,255,0.58);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);

    border: 1px solid rgba(255,255,255,0.95);
    border-radius: 20px;

    padding: 17px 24px;
    margin-bottom: 9px;

    box-shadow: 0 8px 28px rgba(35,65,90,0.07);
}

.hero-label {
    color: #426987 !important;
    font-size: 0.68rem;
    font-weight: 800;
    letter-spacing: 1.8px;
    margin-bottom: 6px;
}

.hero-title {
    color: #203c56 !important;
    font-size: 1.7rem;
    font-weight: 800;
    line-height: 1.25;
}

.hero-subtitle {
    color: #536d84 !important;
    font-size: 0.85rem;
    margin-top: 7px;
}

/* ==========================================
   GLASS CARDS
========================================== */

.glass-card {
    background: rgba(255,255,255,0.62);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);

    border: 1px solid rgba(255,255,255,0.95);
    border-radius: 16px;

    padding: 15px 17px;
    min-height: 112px;

    box-shadow: 0 6px 22px rgba(35,65,90,0.06);
}

.card-label {
    font-size: 0.67rem;
    font-weight: 850;
    letter-spacing: 1.2px;
    color: #4d728f !important;
    margin-bottom: 8px;
}

.card-title {
    font-size: 1.04rem;
    font-weight: 800;
    color: #203c56 !important;
    margin-bottom: 6px;
}

.card-description {
    font-size: 0.78rem;
    color: #526b81 !important;
    line-height: 1.5;
}

.proposed-card {
    background: rgba(220,240,231,0.72);
    border: 1px solid rgba(125,190,158,0.65);
}

/* ==========================================
   STATUS CARDS
========================================== */

.status-card {
    background: rgba(255,255,255,0.65);
    backdrop-filter: blur(16px);

    border: 1px solid rgba(255,255,255,0.95);
    border-radius: 14px;

    padding: 11px 14px;
    text-align: center;

    box-shadow: 0 5px 18px rgba(35,65,90,0.05);
}

.status-value {
    font-size: 1.35rem;
    font-weight: 850;
    color: #244968 !important;
}

.status-name {
    font-size: 0.72rem;
    color: #526d83 !important;
    font-weight: 700;
}

/* ==========================================
   SECTION LABELS
========================================== */

.section-label {
    font-size: 1rem;
    font-weight: 800;
    color: #29445e !important;
    margin: 7px 0 6px;
}

/* ==========================================
   CSV UPLOADER - IMPORTANT FIX
========================================== */

[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.78) !important;
    border: 1px solid rgba(255,255,255,0.95) !important;
    border-radius: 14px !important;
    padding: 12px !important;

    box-shadow: 0 5px 18px rgba(35,65,90,0.06);
}

/* Dropzone background */
[data-testid="stFileUploaderDropzone"] {
    background: rgba(237,244,250,0.95) !important;
    border: 1.5px dashed #8ba9c0 !important;
    border-radius: 12px !important;
}

/* Upload instructions */
[data-testid="stFileUploaderDropzoneInstructions"],
[data-testid="stFileUploaderDropzoneInstructions"] *,
[data-testid="stFileUploader"] p,
[data-testid="stFileUploader"] span,
[data-testid="stFileUploader"] small {
    color: #29445e !important;
}

/* Browse files button */
[data-testid="stFileUploaderDropzone"] button {
    background: #dceaf5 !important;
    border: 1px solid #9bb8cf !important;
    border-radius: 8px !important;

    color: #203c56 !important;
    font-weight: 750 !important;
}

/* Force button text visibility */
[data-testid="stFileUploaderDropzone"] button *,
[data-testid="stFileUploaderDropzone"] button span,
[data-testid="stFileUploaderDropzone"] button p {
    color: #203c56 !important;
}

/* Hover */
[data-testid="stFileUploaderDropzone"] button:hover {
    background: #cbdfee !important;
    border-color: #7397b4 !important;
}

/* Uploaded file name and details */
[data-testid="stFileUploader"] [data-testid="stMarkdownContainer"],
[data-testid="stFileUploader"] [data-testid="stMarkdownContainer"] * {
    color: #29445e !important;
}

/* ==========================================
   ALERT BOXES
========================================== */

[data-testid="stAlert"] {
    background: rgba(255,255,255,0.75) !important;
    border: 1px solid rgba(255,255,255,0.95) !important;
    border-radius: 12px;
}

[data-testid="stAlert"] p,
[data-testid="stAlert"] span {
    color: #29445e !important;
}

/* ==========================================
   METRIC CARDS
========================================== */

[data-testid="stMetric"] {
    background: rgba(255,255,255,0.72) !important;
    border: 1px solid rgba(255,255,255,0.95);
    border-radius: 13px;
    padding: 10px 13px;
}

[data-testid="stMetricLabel"] {
    color: #526d83 !important;
}

[data-testid="stMetricValue"] {
    color: #244968 !important;
}

/* ==========================================
   DATAFRAME
========================================== */

[data-testid="stDataFrame"] {
    border: 1px solid #d4e1ec;
    border-radius: 12px;
    overflow: hidden;
}

/* ==========================================
   FOOTER
========================================== */

.footer {
    text-align: center;
    color: #647d91 !important;
    font-size: 0.7rem;
    padding: 8px 0;
}

/* ==========================================
   RESPONSIVE AND SCREEN FIT
========================================== */

@media (max-height: 800px) {
    .block-container {
        padding-top: 0.45rem;
        padding-bottom: 0.5rem;
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

/* Tablet and mobile */
@media (max-width: 900px) {
    .block-container {
        padding: 1rem;
    }

    .hero-title {
        font-size: 1.35rem;
    }

    .glass-card {
        min-height: auto;
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
        "Choose a CSV file",
        type=["csv"],
        help="Upload a validated experimental predictions CSV file."
    )

    if uploaded_file is not None:
        try:
            data = pd.read_csv(uploaded_file)

            if data.empty:
                st.error("The uploaded CSV contains no records.")

            else:
                st.success(
                    f"CSV uploaded successfully: {len(data)} records."
                )

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
                        "All required experimental columns are present."
                    )

                with st.expander("Preview uploaded dataset"):
                    st.dataframe(
                        data,
                        use_container_width=True
                    )

        except (pd.errors.EmptyDataError,
                pd.errors.ParserError,
                UnicodeDecodeError):
            st.error(
                "Unable to read the CSV file. Please check its format."
            )

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
        <div class="card-label">
            PROVISIONAL CLASSIFICATION MODEL
        </div>

        <div class="card-title">
            Gradient Boosting Classifier
        </div>

        <div class="card-description">
            Uses extracted body and hand movement features
            to classify selected CPR movement patterns.
            Final selection depends on validation performance
            and computational requirements.
        </div>

        <br>

        <div class="card-label">
            MLFLOW EXPERIMENT TRACKING: NOT CONNECTED
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
