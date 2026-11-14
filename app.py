
import streamlit as st
import pandas as pd

# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="CPR Research Dashboard",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================================================
# MLflow-INSPIRED PROFESSIONAL THEME
# ==================================================

st.markdown("""
<style>

/* GLOBAL */
.stApp {
    background: linear-gradient(
        135deg,
        #f4f6fa 0%,
        #edf2f8 55%,
        #f8fafc 100%
    );
    color: #27364b;
    min-height: 100vh;
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stToolbar"] {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

.block-container {
    max-width: 1500px;
    padding: 0.75rem 2rem 0.5rem;
}

/* TYPOGRAPHY */
h1, h2, h3, h4, p, label {
    color: #27364b;
}

.stMarkdown p {
    color: #46566b;
}

h1 {
    font-size: 1.75rem !important;
    font-weight: 800 !important;
}

h2 {
    font-size: 1.12rem !important;
    font-weight: 750 !important;
}

h3 {
    font-size: 1rem !important;
    font-weight: 700 !important;
}

/* HEADER */
.hero {
    background: rgba(255, 255, 255, 0.88);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);

    border: 1px solid #dce4ef;
    border-left: 5px solid #2775bd;
    border-radius: 13px;

    padding: 15px 22px;
    margin-bottom: 12px;

    box-shadow: 0 4px 15px rgba(30, 52, 80, 0.055);
}

.hero-label {
    color: #2775bd !important;
    font-size: 0.66rem;
    font-weight: 850;
    letter-spacing: 1.5px;
    margin-bottom: 5px;
}

.hero-title {
    color: #1c2f48 !important;
    font-size: 1.65rem;
    font-weight: 800;
    line-height: 1.25;
}

.hero-subtitle {
    color: #697a90 !important;
    font-size: 0.82rem;
    margin-top: 5px;
}

/* SECTION TITLES */
.section-title {
    font-size: 0.98rem;
    font-weight: 800;
    color: #243b56 !important;
    margin: 8px 0 7px;
}

/* RESEARCH CARDS */
.research-card {
    background: rgba(255,255,255,0.88);
    backdrop-filter: blur(15px);

    border: 1px solid #dce4ef;
    border-radius: 13px;

    padding: 13px 15px;
    min-height: 112px;

    box-shadow: 0 3px 12px rgba(30,52,80,0.04);
}

.research-card-proposed {
    background: rgba(232, 242, 252, 0.92);
    border: 1px solid #b9d4ec;
}

.card-label {
    font-size: 0.64rem;
    font-weight: 850;
    letter-spacing: 1.2px;
    color: #3477b1 !important;
    margin-bottom: 7px;
}

.card-title {
    font-size: 1rem;
    font-weight: 800;
    color: #243b56 !important;
    margin-bottom: 5px;
}

.card-description {
    font-size: 0.76rem;
    line-height: 1.45;
    color: #596b80 !important;
}

/* STATUS CARDS */
.status-card {
    background: rgba(255,255,255,0.9);
    border: 1px solid #dce4ef;
    border-radius: 11px;

    padding: 9px;
    text-align: center;
}

.status-value {
    font-size: 1.3rem;
    font-weight: 850;
    color: #216eae !important;
}

.status-name {
    font-size: 0.69rem;
    font-weight: 700;
    color: #63758a !important;
}

/* GBC FEATURE CARD */
.gbc-card {
    background: linear-gradient(
        120deg,
        #183653 0%,
        #234e78 60%,
        #2b6594 100%
    );

    border: 1px solid #315f88;
    border-radius: 14px;

    padding: 15px 17px;
    min-height: 210px;

    box-shadow: 0 5px 18px rgba(25,56,88,0.13);
}

.gbc-label {
    color: #b9d9f5 !important;
    font-size: 0.64rem;
    font-weight: 850;
    letter-spacing: 1.3px;
}

.gbc-title {
    color: #ffffff !important;
    font-size: 1.25rem;
    font-weight: 850;
    margin: 6px 0 11px;
}

.gbc-heading {
    color: #a9d4fa !important;
    font-size: 0.66rem;
    font-weight: 850;
    letter-spacing: 1px;
    margin-top: 9px;
}

.gbc-text {
    color: #f0f5fb !important;
    font-size: 0.78rem;
    line-height: 1.45;
    margin-top: 3px;
}

/* GLASS PANELS */
.panel {
    background: rgba(255,255,255,0.86);
    border: 1px solid #dce4ef;
    border-radius: 13px;
    padding: 13px 15px;
    box-shadow: 0 3px 12px rgba(30,52,80,0.04);
}

/* CSV UPLOADER */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.94) !important;
    border: 1px solid #d4dfeb !important;
    border-radius: 12px !important;
    padding: 10px !important;
}

/* Dropzone */
[data-testid="stFileUploaderDropzone"] {
    background: #f3f7fc !important;
    border: 1px dashed #8daac6 !important;
    border-radius: 9px !important;
}

/* Upload instruction text */
[data-testid="stFileUploaderDropzoneInstructions"],
[data-testid="stFileUploaderDropzoneInstructions"] *,
[data-testid="stFileUploader"] p,
[data-testid="stFileUploader"] span,
[data-testid="stFileUploader"] small {
    color: #344a62 !important;
}

/* Browse files button */
[data-testid="stFileUploaderDropzone"] button {
    background: #dceafa !important;
    border: 1px solid #91b5d8 !important;
    border-radius: 7px !important;
    color: #174d7a !important;
    font-weight: 750 !important;
}

[data-testid="stFileUploaderDropzone"] button * {
    color: #174d7a !important;
}

[data-testid="stFileUploaderDropzone"] button:hover {
    background: #c9def2 !important;
    border-color: #548ab9 !important;
}

/* ALERTS */
[data-testid="stAlert"] {
    background: #f5f8fc;
    border-radius: 10px;
    border: 1px solid #dce5ef;
}

[data-testid="stAlert"] p,
[data-testid="stAlert"] span {
    color: #334a62 !important;
}

/* METRICS */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.9);
    border: 1px solid #dce4ef;
    border-radius: 11px;
    padding: 9px 12px;
}

[data-testid="stMetricLabel"] {
    color: #60748b !important;
}

[data-testid="stMetricValue"] {
    color: #216eae !important;
}

/* BUTTONS */
.stButton button {
    background: #216eae;
    border: 1px solid #216eae;
    border-radius: 8px;
    color: white !important;
    font-weight: 700;
}

.stButton button:hover {
    background: #185a91;
    border-color: #185a91;
    color: white !important;
}

/* FOOTER */
.footer {
    text-align: center;
    color: #8291a3 !important;
    font-size: 0.68rem;
    padding: 6px 0;
}

/* RESPONSIVE */
@media (max-width: 900px) {
    .block-container {
        padding: 1rem;
    }

    .hero-title {
        font-size: 1.3rem;
    }

    .research-card {
        min-height: auto;
    }
}

</style>
""", unsafe_allow_html=True)


# ==================================================
# HEADER
# ==================================================

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
        &nbsp; | &nbsp; Bachelor of Science in Computer Science
    </div>
</div>
""", unsafe_allow_html=True)


# ==================================================
# RESEARCH FRAMEWORK
# ==================================================

st.markdown(
    '<div class="section-title">Research Framework</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    st.markdown("""
    <div class="research-card">
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
    <div class="research-card">
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
    <div class="research-card research-card-proposed">
        <div class="card-label">PROPOSED CONTRIBUTION</div>
        <div class="card-title">Hybrid CPR System</div>
        <div class="card-description">
            MediaPipe Pose + MediaPipe Hand,
            Machine Learning, Rule-Based Assessment
            and Hybrid Decision Engine.
        </div>
    </div>
    """, unsafe_allow_html=True)


# ==================================================
# EXPERIMENTAL STATUS
# ==================================================

st.markdown(
    '<div class="section-title">Experimental Status</div>',
    unsafe_allow_html=True
)

s1, s2, s3, s4 = st.columns(4, gap="small")

status_items = [
    (s1, "02", "Existing Systems"),
    (s2, "01", "Proposed System"),
    (s3, "GBC", "Provisional Algorithm"),
    (s4, "Pending", "Experimental Results")
]

for column, value, label in status_items:
    with column:
        st.markdown(f"""
        <div class="status-card">
            <div class="status-value">{value}</div>
            <div class="status-name">{label}</div>
        </div>
        """, unsafe_allow_html=True)


# ==================================================
# MAIN CONTENT: DATASET + GBC
# ==================================================

left, right = st.columns([1.05, 1.25], gap="medium")

with left:

    st.markdown(
        '<div class="section-title">Experimental Dataset</div>',
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=["csv"],
        help="Upload validated experimental prediction data."
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

                required_columns = [
                    "participant_id",
                    "clip_id",
                    "system",
                    "actual_label",
                    "predicted_label"
                ]

                missing = [
                    column for column in required_columns
                    if column not in data.columns
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

        except (
            pd.errors.EmptyDataError,
            pd.errors.ParserError,
            UnicodeDecodeError
        ):
            st.error(
                "Unable to read the CSV. Please check its format."
            )

        except Exception as error:
            st.error(f"Dataset error: {error}")

    else:
        st.caption(
            "No experimental dataset uploaded. "
            "Actual results will appear after testing."
        )


with right:

    st.markdown(
        '<div class="section-title">Selected Machine Learning Algorithm</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="gbc-card">

        <div class="gbc-label">
            PROVISIONAL SELECTED ALGORITHM
        </div>

        <div class="gbc-title">
            Gradient Boosting Classifier (GBC)
        </div>

        <div class="gbc-heading">
            ALGORITHM TYPE
        </div>

        <div class="gbc-text">
            Supervised Machine Learning – Ensemble Learning
        </div>

        <div class="gbc-heading">
            PURPOSE
        </div>

        <div class="gbc-text">
            Classify selected CPR movement patterns as
            proper or improper using extracted movement
            features from MediaPipe Pose and MediaPipe Hand.
        </div>

        <div class="gbc-heading">
            MODEL STATUS
        </div>

        <div class="gbc-text">
            Pending dataset preparation, model training,
            validation, and computational testing.
        </div>

    </div>
    """, unsafe_allow_html=True)


# ==================================================
# EVALUATION METRICS
# ==================================================

st.markdown(
    '<div class="section-title">Planned Evaluation Metrics</div>',
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


# ==================================================
# MLFLOW STATUS
# ==================================================

st.markdown("""
<div class="panel">
    <div class="card-label">
        EXPERIMENT TRACKING
    </div>

    <div class="card-title">
        MLflow Integration
    </div>

    <div class="card-description">
        Hosted MLflow tracking will record model parameters,
        experiment runs, evaluation metrics, and model artifacts
        after the tracking service is configured.
    </div>
</div>
""", unsafe_allow_html=True)


# ==================================================
# FOOTER
# ==================================================

st.markdown("""
<div class="footer">
    NEMSU - Lianga Campus
    &nbsp; | &nbsp;
    AI-Assisted CPR Research Project
    &nbsp; | &nbsp;
    2026
</div>
""", unsafe_allow_html=True)
