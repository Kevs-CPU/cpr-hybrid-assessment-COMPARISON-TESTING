import os
import html

import pandas as pd
import streamlit as st

# =====================================================
# PAGE CONFIGURATION
# =====================================================
st.set_page_config(
    page_title="CPR Research Dashboard",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

REQUIRED = [
    "participant_id",
    "clip_id",
    "system",
    "actual_label",
    "predicted_label",
]

TRACKING_URI = (
    "https://dagshub.com/Kevs-CPU/"
    "cpr-hybrid-assessment-COMPARISON-TESTING.mlflow"
)

# =====================================================
# FULL-SCREEN STYLE
# =====================================================
STYLE = r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');

:root {
    --page-bg: #f3f6fa;
    --card-bg: #ffffff;
    --border: #d7dee8;
    --border-strong: #aeb9c8;
    --text: #172333;
    --muted: #667085;
    --blue: #2563eb;
    --blue-soft: #eaf1ff;
    --green: #16834a;
    --red: #c0392b;
    --panel-height: calc(100dvh - 132px);
}

/* Never allow the browser page or Streamlit main area to scroll. */
html, body, #root,
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"] {
    width: 100% !important;
    height: 100% !important;
    min-height: 0 !important;
    overflow: hidden !important;
    font-family: 'DM Sans', 'Segoe UI', sans-serif !important;
}

html, body {
    margin: 0 !important;
    padding: 0 !important;
    background: var(--page-bg) !important;
}

.stApp {
    background: var(--page-bg) !important;
    color: var(--text) !important;
}

[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
footer,
#MainMenu {
    display: none !important;
}

.block-container {
    box-sizing: border-box !important;
    width: 100% !important;
    max-width: none !important;
    height: 100dvh !important;
    min-height: 0 !important;
    padding: 7px 10px 8px !important;
    margin: 0 !important;
    overflow: hidden !important;
}

/* Tighten Streamlit's default gaps so the dashboard fits one viewport. */
[data-testid="stVerticalBlock"] {
    gap: 6px !important;
    min-height: 0 !important;
}

[data-testid="stHorizontalBlock"] {
    align-items: stretch !important;
    gap: 8px !important;
    min-height: 0 !important;
}

[data-testid="column"] {
    min-width: 0 !important;
    min-height: 0 !important;
}

/* Section label */
.experimental-label {
    height: 15px;
    line-height: 15px;
    margin: 0 0 3px 2px;
    color: #536174;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.15px;
    text-transform: uppercase;
}

/* Top row cards */
.metric-card,
.action-card {
    box-sizing: border-box;
    height: 64px;
    width: 100%;
    padding: 8px 10px;
    overflow: hidden;
    background: var(--card-bg);
    border: 1px solid var(--border-strong);
    border-radius: 7px;
}

.metric-label {
    color: #4b596b;
    font-size: 11px;
    font-weight: 700;
    line-height: 1.2;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.metric-value {
    margin-top: 5px;
    color: var(--text);
    font-size: 22px;
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -.5px;
}

.metric-value.pending {
    color: #98a2b3;
    font-size: 17px;
    font-weight: 700;
}

.metric-subtitle {
    margin-top: 2px;
    color: var(--muted);
    font-size: 9px;
    line-height: 1.1;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.action-label {
    margin: 0 0 4px 1px;
    color: #4b596b;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: .35px;
    line-height: 1.1;
    text-transform: uppercase;
}

/* Compact CSV uploader */
[data-testid="stFileUploader"] {
    box-sizing: border-box !important;
    width: 100% !important;
    margin: 0 !important;
    padding: 0 !important;
    background: transparent !important;
    border: 0 !important;
}

[data-testid="stFileUploaderDropzone"] {
    box-sizing: border-box !important;
    height: 47px !important;
    min-height: 47px !important;
    padding: 4px 6px !important;
    background: #ffffff !important;
    border: 1px dashed #9aa8ba !important;
    border-radius: 7px !important;
}

[data-testid="stFileUploaderDropzoneInstructions"] {
    gap: 0 !important;
}

[data-testid="stFileUploaderDropzoneInstructions"] div,
[data-testid="stFileUploaderDropzoneInstructions"] span,
[data-testid="stFileUploaderDropzoneInstructions"] small {
    display: none !important;
}

[data-testid="stFileUploaderDropzone"] button {
    min-height: 30px !important;
    padding: 3px 9px !important;
    background: var(--blue-soft) !important;
    border: 1px solid #c7d7ff !important;
    border-radius: 6px !important;
    color: #1746a2 !important;
    font-size: 11px !important;
    font-weight: 800 !important;
}

[data-testid="stFileUploaderDropzone"] button * {
    color: #1746a2 !important;
}

[data-testid="stFileUploaderFile"] {
    display: none !important;
}

[data-testid="stFileUploader"] small,
[data-testid="stFileUploader"] label {
    display: none !important;
}

/* Buttons */
.stButton {
    margin: 0 !important;
}

.stButton button {
    box-sizing: border-box !important;
    width: 100% !important;
    min-height: 47px !important;
    height: 47px !important;
    padding: 5px 8px !important;
    background: #ffffff !important;
    border: 1px solid var(--border-strong) !important;
    border-radius: 7px !important;
    color: var(--text) !important;
    box-shadow: none !important;
    font-size: 11px !important;
    font-weight: 800 !important;
    line-height: 1.2 !important;
}

.stButton button:hover {
    background: var(--blue-soft) !important;
    border-color: #9bb8ff !important;
    color: #1746a2 !important;
}

.stButton button:focus,
.stButton button:active {
    box-shadow: none !important;
    outline: none !important;
}

/* Small status text under actions */
.mini-status {
    margin: 3px 1px 0;
    color: var(--muted);
    font-size: 9px;
    line-height: 1.15;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.mini-status.ok { color: var(--green); }
.mini-status.bad { color: var(--red); }

/* Main dashboard panels */
.panel {
    box-sizing: border-box;
    height: var(--panel-height);
    min-height: 0;
    width: 100%;
    padding: 12px 14px;
    overflow: hidden !important;
    background: var(--card-bg);
    border: 1px solid var(--border-strong);
    border-radius: 8px;
}

.panel-title {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    gap: 8px;
    margin: 0 0 10px;
    color: var(--text);
    font-size: 15px;
    font-weight: 800;
    line-height: 1.2;
}

.panel-subtitle {
    color: var(--muted);
    font-size: 10px;
    font-weight: 500;
    white-space: nowrap;
}

.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: calc(100% - 32px);
    padding: 10px;
    color: var(--muted);
    font-size: 13px;
    line-height: 1.5;
    text-align: center;
}

.empty-state strong {
    margin-bottom: 8px;
    color: #344054;
    font-size: 17px;
}

/* System comparison */
.systems-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    align-content: start;
    gap: 10px;
    max-height: calc(100% - 34px);
    overflow: hidden;
}

.system-card {
    box-sizing: border-box;
    min-width: 0;
    padding: 10px 11px;
    background: #fbfcfe;
    border: 1px solid #e1e7ef;
    border-radius: 7px;
}

.system-card.selected {
    background: #f5f8ff;
    border-color: #8eafff;
    box-shadow: inset 3px 0 0 var(--blue);
}

.system-heading {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 6px;
    margin-bottom: 9px;
    color: #263448;
    font-size: 12px;
    font-weight: 800;
}

.system-count {
    flex: 0 0 auto;
    color: var(--muted);
    font-size: 9px;
    font-weight: 500;
}

.metric-bar-row {
    display: grid;
    grid-template-columns: 58px minmax(30px, 1fr) 40px;
    gap: 7px;
    align-items: center;
    margin: 8px 0;
}

.metric-bar-label {
    color: #586579;
    font-size: 10px;
}

.metric-track {
    height: 7px;
    overflow: hidden;
    background: #e9eef5;
    border-radius: 99px;
}

.metric-fill {
    height: 100%;
    background: linear-gradient(90deg, #4b83f5, #2762d8);
    border-radius: 99px;
}

.metric-bar-value {
    color: #344054;
    font-size: 10px;
    font-weight: 800;
    text-align: right;
}

.dataset-note {
    margin-top: 10px;
    padding: 7px 9px;
    color: #526176;
    background: #f7f9fc;
    border: 1px solid #e6ebf2;
    border-radius: 6px;
    font-size: 9px;
    line-height: 1.35;
}

/* Middle column */
.middle-stack {
    display: grid;
    grid-template-rows: minmax(0, .92fr) minmax(0, 1.08fr);
    gap: 8px;
    height: var(--panel-height);
    min-height: 0;
}

.middle-stack .panel {
    height: auto;
    padding: 10px 9px;
}

.middle-stack .panel-title {
    display: block;
    margin-bottom: 8px;
    font-size: 12px;
}

.cm-grid {
    display: grid;
    gap: 3px;
    width: 100%;
}

.cm-head {
    min-width: 0;
    align-self: center;
    color: #667085;
    font-size: 8px;
    line-height: 1.15;
    text-align: center;
    overflow-wrap: anywhere;
}

.cm-cell {
    display: flex;
    align-items: center;
    justify-content: center;
    min-width: 0;
    min-height: 25px;
    padding: 2px;
    border-radius: 4px;
    color: #243247;
    font-size: 10px;
    font-weight: 800;
}

.cm-note {
    margin-top: 7px;
    color: #758195;
    font-size: 8px;
    line-height: 1.3;
}

.gbc-title {
    margin-bottom: 7px;
    color: #263448;
    font-size: 11px;
    font-weight: 800;
    line-height: 1.25;
}

.gbc-heading {
    margin: 7px 0 2px;
    color: #2563eb;
    font-size: 8px;
    font-weight: 800;
    letter-spacing: .55px;
}

.gbc-text {
    color: #536174;
    font-size: 9px;
    line-height: 1.35;
    overflow-wrap: anywhere;
}

/* Research framework */
.framework-panel {
    display: flex;
    flex-direction: column;
    gap: 7px;
    padding: 11px 9px;
}

.framework-panel .panel-title {
    margin-bottom: 2px;
    font-size: 13px;
}

.framework-item {
    display: flex;
    flex-direction: column;
    justify-content: center;
    flex: 1 1 0;
    min-height: 0;
    padding: 8px;
    overflow: hidden;
    background: #fbfcfe;
    border: 1px solid #e1e7ef;
    border-radius: 6px;
}

.framework-item.proposed {
    background: #f1f6ff;
    border-color: #a9c1ff;
}

.framework-name {
    margin-bottom: 5px;
    color: #263448;
    font-size: 10px;
    font-weight: 800;
    line-height: 1.25;
    overflow-wrap: anywhere;
}

.framework-description {
    color: #5e6b7d;
    font-size: 8.5px;
    line-height: 1.35;
    overflow-wrap: anywhere;
}

/* Compact layouts: no page scrolling */
@media (max-height: 700px) {
    :root { --panel-height: calc(100dvh - 138px); }
    .block-container { padding-top: 5px !important; padding-bottom: 5px !important; }
    .metric-card, .action-card { height: 59px; padding: 6px 8px; }
    .metric-value { margin-top: 3px; font-size: 19px; }
    .panel { padding: 9px 10px; }
    .system-card { padding: 7px 8px; }
    .metric-bar-row { margin: 6px 0; }
}

@media (max-width: 1100px) {
    :root { --panel-height: calc(100dvh - 126px); }
    .block-container { padding-left: 7px !important; padding-right: 7px !important; }
    .metric-card, .action-card { padding-left: 6px; padding-right: 6px; }
    .metric-label { font-size: 9px; }
    .metric-value { font-size: 18px; }
    .panel { padding-left: 8px; padding-right: 8px; }
    .framework-description, .gbc-text { font-size: 8px; }
}

@media (max-width: 760px) {
    :root { --panel-height: calc(100dvh - 118px); }
    [data-testid="stHorizontalBlock"] { gap: 4px !important; }
    .metric-card, .action-card { height: 55px; padding: 5px 4px; }
    .metric-label { font-size: 8px; }
    .metric-value { font-size: 15px; }
    .action-label { font-size: 8px; }
    .stButton button { font-size: 9px !important; }
    .panel-title { font-size: 12px; }
    .systems-grid { grid-template-columns: 1fr; }
    .system-card { padding: 5px 6px; }
    .metric-bar-row { margin: 4px 0; }
    .framework-item { padding: 5px; }
    .framework-name { font-size: 8px; }
    .framework-description { font-size: 7px; }
}
</style>
"""

st.markdown(STYLE, unsafe_allow_html=True)

# =====================================================
# HELPERS
# =====================================================
def esc(value):
    return html.escape(str(value))


def pct(value):
    return f"{value * 100:.1f}%"


def render(markup):
    """Render compact HTML without Markdown turning it into a code block."""
    compact = " ".join(
        line.strip() for line in markup.splitlines() if line.strip()
    )
    st.markdown(compact, unsafe_allow_html=True)


def evaluate(data):
    """Calculate accuracy and macro-averaged precision, recall and F1."""
    actual = data["actual_label"]
    predicted = data["predicted_label"]
    labels = sorted(set(actual) | set(predicted))

    matrix = pd.crosstab(actual, predicted).reindex(
        index=labels, columns=labels, fill_value=0
    )

    true_positive = pd.Series(matrix.values.diagonal(), index=labels)
    precision = (
        true_positive / matrix.sum(axis=0).replace(0, float("nan"))
    ).fillna(0)
    recall = (
        true_positive / matrix.sum(axis=1).replace(0, float("nan"))
    ).fillna(0)
    f1 = (
        2 * precision * recall / (precision + recall).replace(0, float("nan"))
    ).fillna(0)

    return {
        "n": len(data),
        "acc": float((actual == predicted).mean()),
        "prec": float(precision.mean()),
        "rec": float(recall.mean()),
        "f1": float(f1.mean()),
        "cm": matrix,
    }


def metric_card(label, value, subtitle):
    if value is None:
        value_html = '<div class="metric-value pending">Pending</div>'
    else:
        value_html = f'<div class="metric-value">{esc(value)}</div>'
    return f"""
    <div class="metric-card">
        <div class="metric-label">{esc(label)}</div>
        {value_html}
        <div class="metric-subtitle">{esc(subtitle)}</div>
    </div>
    """


def metric_bar(label, value):
    width = max(0.0, min(float(value) * 100, 100.0))
    return f"""
    <div class="metric-bar-row">
        <span class="metric-bar-label">{esc(label)}</span>
        <div class="metric-track"><div class="metric-fill" style="width:{width:.1f}%"></div></div>
        <span class="metric-bar-value">{pct(value)}</span>
    </div>
    """


def comparison_panel(results, selected, validation_message=None, same_samples=None):
    if not results:
        message = validation_message or "System comparison will appear after a valid CSV is uploaded."
        return f"""
        <div class="panel">
            <div class="panel-title">System Comparison</div>
            <div class="empty-state">
                <strong>System Comparison</strong>
                <span>{esc(message)}</span>
            </div>
        </div>
        """

    cards = []
    for name, result in results.items():
        selected_class = " selected" if name == selected else ""
        cards.append(f"""
        <div class="system-card{selected_class}">
            <div class="system-heading">
                <span>{esc(name)}</span>
                <span class="system-count">{result['n']} records</span>
            </div>
            {metric_bar('Accuracy', result['acc'])}
            {metric_bar('Precision', result['prec'])}
            {metric_bar('Recall', result['rec'])}
            {metric_bar('F1-score', result['f1'])}
        </div>
        """)

    note = "Metrics use the same test samples across systems." if same_samples else "Metrics are computed from the uploaded predictions and evaluator-approved actual labels."
    return f"""
    <div class="panel">
        <div class="panel-title">
            <span>System Comparison</span>
            <span class="panel-subtitle">Higher is better</span>
        </div>
        <div class="systems-grid">{''.join(cards)}</div>
        <div class="dataset-note">{esc(note)} The KPI cards and confusion matrix show: <b>{esc(selected)}</b>.</div>
    </div>
    """


def confusion_panel(matrix, selected):
    if matrix is None:
        return """
        <div class="panel">
            <div class="panel-title">Confusion Matrix</div>
            <div class="empty-state">Confusion matrix will appear after a valid CSV is uploaded.</div>
        </div>
        """

    maximum = max(int(matrix.values.max()), 1)
    labels = list(matrix.columns)
    cells = ['<div class="cm-head"></div>']
    cells.extend(f'<div class="cm-head">{esc(label)}</div>' for label in labels)

    for actual in matrix.index:
        cells.append(f'<div class="cm-head">{esc(actual)}</div>')
        for predicted in matrix.columns:
            value = int(matrix.loc[actual, predicted])
            alpha = 0.08 if value == 0 else 0.15 + 0.65 * value / maximum
            color = "37,99,235" if actual == predicted else "192,57,43"
            cells.append(
                f'<div class="cm-cell" style="background:rgba({color},{alpha:.2f})">{value}</div>'
            )

    return f"""
    <div class="panel">
        <div class="panel-title">Confusion Matrix <span class="panel-subtitle">{esc(selected)}</span></div>
        <div class="cm-grid" style="grid-template-columns:auto repeat({len(labels)}, minmax(0,1fr))">{''.join(cells)}</div>
        <div class="cm-note">Rows: actual · Columns: predicted<br>Blue: correct · Red: incorrect</div>
    </div>
    """


def gbc_panel():
    return """
    <div class="panel">
        <div class="gbc-title">Gradient Boosting Classifier (GBC)</div>
        <div class="gbc-heading">ALGORITHM TYPE</div>
        <div class="gbc-text">Supervised machine learning · Ensemble learning</div>
        <div class="gbc-heading">PURPOSE</div>
        <div class="gbc-text">Classifies selected CPR movement patterns as proper or improper using features from MediaPipe Pose and MediaPipe Hand.</div>
        <div class="gbc-heading">MODEL STATUS</div>
        <div class="gbc-text">Provisional · Pending dataset preparation, training, validation and computational testing.</div>
    </div>
    """


def framework_panel():
    return """
    <div class="panel framework-panel">
        <div class="panel-title">Research Framework</div>
        <div class="framework-item">
            <div class="framework-name">Ecker et al. (2024)</div>
            <div class="framework-description">Existing system · MediaPipe Pose landmark analysis and CPR measurement evaluation.</div>
        </div>
        <div class="framework-item">
            <div class="framework-name">SmartCPR (2024)</div>
            <div class="framework-description">Existing system · MoveNet smartphone CPR assessment with measurement analysis and feedback.</div>
        </div>
        <div class="framework-item proposed">
            <div class="framework-name">Hybrid CPR System</div>
            <div class="framework-description">Proposed · MediaPipe Pose and Hand, machine learning, rule-based assessment and hybrid decision engine.</div>
        </div>
    </div>
    """


def test_mlflow_connection():
    required_secrets = [
        "MLFLOW_TRACKING_URI",
        "MLFLOW_TRACKING_USERNAME",
        "MLFLOW_TRACKING_PASSWORD",
    ]
    missing = [
        key for key in required_secrets
        if key not in st.secrets or not str(st.secrets[key]).strip()
    ]
    if missing:
        raise ValueError("Missing or empty Streamlit Secrets: " + ", ".join(missing))

    tracking_uri = str(st.secrets["MLFLOW_TRACKING_URI"]).strip()
    username = str(st.secrets["MLFLOW_TRACKING_USERNAME"]).strip()
    password = str(st.secrets["MLFLOW_TRACKING_PASSWORD"]).strip()

    os.environ["MLFLOW_TRACKING_URI"] = tracking_uri
    os.environ["MLFLOW_TRACKING_USERNAME"] = username
    os.environ["MLFLOW_TRACKING_PASSWORD"] = password

    import mlflow
    from mlflow.tracking import MlflowClient

    mlflow.set_tracking_uri(tracking_uri)
    client = MlflowClient(tracking_uri=tracking_uri)
    client.search_experiments(max_results=1)

    experiment_name = "CPR_Dashboard_Connection_Check"
    experiment = client.get_experiment_by_name(experiment_name)
    if experiment is None:
        experiment_id = client.create_experiment(experiment_name)
    else:
        experiment_id = experiment.experiment_id

    with mlflow.start_run(
        experiment_id=experiment_id,
        run_name="DagsHub Connection Check Only",
    ):
        mlflow.set_tags({
            "run_type": "connection_check",
            "not_model_evaluation": "true",
            "project": "AI-Assisted CPR Research",
        })
        mlflow.log_param("purpose", "Verify Streamlit to DagsHub connectivity")
        run_id = mlflow.active_run().info.run_id

    return run_id


# =====================================================
# TOP STRIP: FIVE METRICS + CSV UPLOAD + CONNECTION TEST
# =====================================================
render('<div class="experimental-label">EXPERIMENTAL</div>')

top_cols = st.columns([1, 1, 1, 1, 1, 1.02, 1.02], gap="small")

metric_slots = []
for metric_col in top_cols[:5]:
    with metric_col:
        metric_slots.append(st.empty())

with top_cols[5]:
    render('<div class="action-label">UPLOAD CSV</div>')

    uploaded = st.file_uploader(
        "Experimental predictions CSV",
        type=["csv"],
        label_visibility="collapsed",
        key="experimental_csv_upload",
    )

    upload_status_slot = st.empty()

with top_cols[6]:
    render('<div class="action-label">TEST FLOW CONNECTION</div>')

    test_button = st.button(
        "Test Connection",
        use_container_width=True,
        key="mlflow_test_button",
    )

    connection_status_slot = st.empty()


if test_button:
    try:
        with st.spinner("Connecting..."):
            connection_run_id = test_mlflow_connection()

        st.session_state["mlflow_status"] = "connected"
        st.session_state["mlflow_run_id"] = connection_run_id
        st.session_state.pop("mlflow_error", None)

    except Exception as error:
        st.session_state["mlflow_status"] = "failed"
        st.session_state["mlflow_error"] = type(error).__name__
        st.session_state.pop("mlflow_run_id", None)


connection_state = st.session_state.get("mlflow_status")

if connection_state == "connected":
    run_id = st.session_state.get("mlflow_run_id", "")

    connection_status_slot.markdown(
        f'<div class="mini-status ok">Connected · Run {esc(run_id[:8])}</div>',
        unsafe_allow_html=True,
    )

elif connection_state == "failed":
    connection_status_slot.markdown(
        f'<div class="mini-status bad">Connection failed · {esc(st.session_state.get("mlflow_error", "Error"))}</div>',
        unsafe_allow_html=True,
    )

else:
    connection_status_slot.markdown(
        '<div class="mini-status">Not tested yet</div>',
        unsafe_allow_html=True,
    )


# =====================================================
# CSV LOADING AND VALIDATION
# =====================================================
df = None
results = {}
validation_message = None
same_samples = False
primary_system = None
primary_result = None

if uploaded is not None:
    try:
        raw = pd.read_csv(uploaded)

        raw.columns = [
            str(column).strip().lower()
            for column in raw.columns
        ]

        missing = [
            column for column in REQUIRED
            if column not in raw.columns
        ]

        if raw.empty:
            validation_message = "The CSV contains no records."

        elif missing:
            validation_message = (
                "Missing required columns: "
                + ", ".join(missing)
            )

        else:
            df = raw.dropna(subset=REQUIRED).copy()

            for column in REQUIRED:
                df[column] = (
                    df[column]
                    .astype(str)
                    .str.strip()
                )

            df["actual_label"] = (
                df["actual_label"].str.lower()
            )

            df["predicted_label"] = (
                df["predicted_label"].str.lower()
            )

            if df.empty:
                validation_message = (
                    "All rows contain missing required values."
                )
                df = None

            else:
                duplicate_rows = df.duplicated(
                    subset=[
                        "system",
                        "participant_id",
                        "clip_id",
                    ],
                    keep=False,
                )

                if duplicate_rows.any():
                    validation_message = (
                        "Duplicate records found for the same "
                        "system, participant and clip."
                    )
                    df = None

                else:
                    label_counts = (
                        df.groupby(
                            ["participant_id", "clip_id"]
                        )["actual_label"]
                        .nunique()
                    )

                    if (label_counts > 1).any():
                        validation_message = (
                            "Inconsistent evaluator labels were "
                            "found for the same test sample."
                        )
                        df = None

    except (
        pd.errors.EmptyDataError,
        pd.errors.ParserError,
        UnicodeDecodeError,
    ):
        validation_message = (
            "Cannot read the CSV. Please check the file format."
        )

    except Exception as error:
        validation_message = (
            "Dataset processing error: "
            + type(error).__name__
        )


if df is not None:
    systems = list(df["system"].unique())

    results = {
        system: evaluate(group)
        for system, group in df.groupby(
            "system",
            sort=False,
        )
    }

    sample_sets = {
        system: set(
            zip(
                group["participant_id"],
                group["clip_id"],
            )
        )
        for system, group in df.groupby(
            "system",
            sort=False,
        )
    }

    same_samples = (
        len(sample_sets) > 1
        and len({
            frozenset(samples)
            for samples in sample_sets.values()
        }) == 1
    )

    primary_system = next(
        (
            system for system in results
            if "hybrid" in system.lower()
        ),
        systems[0],
    )

    primary_result = results[primary_system]

    upload_status_slot.markdown(
        f'<div class="mini-status ok">Loaded · {len(df)} records · {len(systems)} systems</div>',
        unsafe_allow_html=True,
    )

elif uploaded is not None:
    upload_status_slot.markdown(
        f'<div class="mini-status bad">{esc(validation_message or "Invalid CSV")}</div>',
        unsafe_allow_html=True,
    )

else:
    upload_status_slot.markdown(
        '<div class="mini-status">CSV file not selected</div>',
        unsafe_allow_html=True,
    )


# =====================================================
# KPI CARDS
# =====================================================
if primary_result:
    subtitle = f"Selected system · {primary_system}"

    kpi_values = [
        ("Accuracy", pct(primary_result["acc"]), subtitle),
        ("Precision", pct(primary_result["prec"]), subtitle),
        ("Recall", pct(primary_result["rec"]), subtitle),
        ("F1-score", pct(primary_result["f1"]), subtitle),
        (
            "Records evaluated",
            str(primary_result["n"]),
            "Selected system records",
        ),
    ]

else:
    kpi_values = [
        ("Accuracy", None, "Waiting for CSV"),
        ("Precision", None, "Waiting for CSV"),
        ("Recall", None, "Waiting for CSV"),
        ("F1-score", None, "Waiting for CSV"),
        ("Records evaluated", None, "Waiting for CSV"),
    ]


for slot, (label, value, subtitle) in zip(
    metric_slots,
    kpi_values,
):
    slot.markdown(
        metric_card(label, value, subtitle),
        unsafe_allow_html=True,
    )


# =====================================================
# MAIN CONTENT: WIDE COMPARISON + MATRIX + FRAMEWORK
# =====================================================
left_col, middle_col, right_col = st.columns(
    [6.15, 1.02, 1.02],
    gap="small",
)

with left_col:
    render(
        comparison_panel(
            results,
            primary_system,
            validation_message,
            same_samples,
        )
    )

with middle_col:
    matrix = (
        primary_result["cm"]
        if primary_result
        else None
    )

    render(
        '<div class="middle-stack">'
        + confusion_panel(matrix, primary_system)
        + gbc_panel()
        + '</div>'
    )

with right_col:
    render(framework_panel())
