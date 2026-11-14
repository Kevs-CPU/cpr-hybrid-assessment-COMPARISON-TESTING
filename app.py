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
    initial_sidebar_state="collapsed"
)

REQUIRED = [
    "participant_id",
    "clip_id",
    "system",
    "actual_label",
    "predicted_label"
]

TRACKING_URI = (
    "https://dagshub.com/Kevs-CPU/"
    "cpr-hybrid-assessment-COMPARISON-TESTING.mlflow"
)

# =====================================================
# STYLE
# =====================================================

STYLE = """
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700;800&display=swap');

:root {
    /* Space used by everything ABOVE the dashboard grid
       (header row, status row, paddings).
       Bottom cut off?  -> increase this value.
       Empty gap at the bottom? -> decrease this value. */
    --reserved: 190px;
}

/* =====================================================
   PAGE: locked to the screen. The page itself never scrolls.
   ===================================================== */
html, body {
    height: 100%;
    overflow: hidden !important;
    font-family: 'DM Sans', 'Segoe UI', sans-serif !important;
}

.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    height: 100vh !important;
    height: 100dvh !important;
    overflow: hidden !important;
    font-family: 'DM Sans', 'Segoe UI', sans-serif !important;
}

/* BACKGROUND */
.stApp {
    color: #ffffff !important;
    background:
      linear-gradient(
        180deg,
        rgba(13,17,23,0) 0%,
        rgba(13,17,23,0) 22%,
        rgba(13,17,23,.88) 62%,
        #0d1117 100%
      ),
      repeating-linear-gradient(
        90deg,
        rgba(0,0,0,.16) 0 14px,
        rgba(255,255,255,.04) 14px 28px
      ),
      linear-gradient(
        90deg,
        #7a0e48 0%,
        #c4170f 40%,
        #d8230f 52%,
        #6d4fa3 72%,
        #1f8cf2 100%
      );
}

[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
footer {
    display: none !important;
}

.block-container {
    max-width: 1500px;
    padding: .6rem 1.5rem .3rem !important;
}

[data-testid="stVerticalBlock"] {
    gap: .4rem;
}

[data-testid="stHorizontalBlock"] {
    align-items: center;
}

/* TEXT */
.stApp h1,
.stApp h2,
.stApp h3,
.stApp p,
.stApp label,
.stApp span {
    color: #ffffff;
}

/* =====================================================
   HEADER
   ===================================================== */
.eyebrow {
    font-size: .68rem;
    font-weight: 700;
    color: rgba(255,255,255,.78) !important;
    letter-spacing: 1px;
    margin-bottom: 3px;
}

.title {
    font-size: 1.6rem;
    font-weight: 800;
    letter-spacing: -.03em;
    line-height: 1.2;
    color: #ffffff !important;
}

.sub {
    font-size: .78rem;
    color: rgba(255,255,255,.78) !important;
    margin-top: 3px;
}

/* UPLOADER (compact) */
[data-testid="stFileUploader"] {
    background: rgba(13,17,23,.58) !important;
    border: 1px solid rgba(255,255,255,.22) !important;
    border-radius: 12px !important;
    padding: 6px !important;
}

[data-testid="stFileUploaderDropzone"] {
    background: rgba(13,17,23,.52) !important;
    border: 1.5px dashed rgba(255,255,255,.42) !important;
    border-radius: 10px !important;
    padding: .3rem .6rem !important;
    min-height: 0 !important;
}

[data-testid="stFileUploaderDropzoneInstructions"] small {
    display: none !important;
}

[data-testid="stFileUploader"] p,
[data-testid="stFileUploader"] span,
[data-testid="stFileUploader"] small {
    color: #ffffff !important;
}

[data-testid="stFileUploaderFile"] {
    padding: 0 3px !important;
    min-height: 0 !important;
}

/* UPLOAD BUTTON */
[data-testid="stFileUploaderDropzone"] button {
    background: #ffffff !important;
    border: 1px solid #ffffff !important;
    border-radius: 8px !important;
    font-weight: 800 !important;
}

[data-testid="stFileUploaderDropzone"] button,
[data-testid="stFileUploaderDropzone"] button *,
[data-testid="stFileUploaderDropzone"] button span,
[data-testid="stFileUploaderDropzone"] button p {
    color: #172333 !important;
}

[data-testid="stFileUploaderDropzone"] button:hover {
    background: #dceafa !important;
}

/* BUTTONS (fixed)
   The global ".stApp p / .stApp span" rules turn the label inside
   a button white, which is invisible on a white button. The label
   color is forced on the button AND its children. */
.stButton button,
.stButton button:focus,
.stButton button:active,
[data-testid="stPopover"] button,
[data-testid="stPopoverButton"] {
    background: #ffffff !important;
    border: 1px solid rgba(255,255,255,.8) !important;
    border-radius: 9px !important;
    font-weight: 800 !important;
    min-height: 34px;
    box-shadow: none !important;
}

.stButton button,
.stButton button *,
.stButton button p,
.stButton button span,
.stButton button div,
[data-testid="stPopover"] button,
[data-testid="stPopover"] button *,
[data-testid="stPopoverButton"],
[data-testid="stPopoverButton"] * {
    color: #172333 !important;
}

.stButton button:hover,
.stButton button:focus-visible,
[data-testid="stPopover"] button:hover {
    background: #dceafa !important;
    border-color: #dceafa !important;
}

.stButton button:active {
    background: #c3d9f5 !important;
}

.stButton button:disabled {
    opacity: .55;
}

/* Dataset popover: wide enough to show the table */
[data-testid="stPopoverBody"] {
    min-width: min(760px, 92vw);
    max-height: 70vh;
}

/* MLFLOW STATUS (compact, replaces the big alert boxes) */
.mini {
    font-size: .68rem;
    line-height: 1.3;
    margin-top: 2px;
    padding: 4px 9px;
    border-radius: 8px;
    background: rgba(13,17,23,.55);
    border: 1px solid rgba(255,255,255,.22);
    color: rgba(255,255,255,.78) !important;
}

.mini.ok {
    border-color: #5be39a;
    color: #b9ffd9 !important;
}

.mini.bad {
    border-color: #ff8a80;
    color: #ffd0cc !important;
}

.mini a {
    color: #a9d4fa !important;
    font-weight: 700;
    text-decoration: underline;
}

/* =====================================================
   STATUS ROW: pills + system selector
   ===================================================== */
[data-testid="stRadio"] [role="radiogroup"] {
    gap: .3rem;
    justify-content: flex-end;
    flex-wrap: wrap;
}

[data-testid="stRadio"] label {
    background: rgba(13,17,23,.55);
    border: 1px solid rgba(255,255,255,.25);
    border-radius: 999px;
    padding: 2px 11px;
    margin: 0;
}

[data-testid="stRadio"] label p {
    color: #ffffff !important;
    font-size: .75rem;
    font-weight: 600;
    margin: 0;
}

[data-testid="stRadio"] label:has(input:checked) {
    background: #ffffff;
}

[data-testid="stRadio"] label:has(input:checked) p {
    color: #0d1117 !important;
    font-weight: 800;
}

.pills {
    display: flex;
    gap: .35rem;
    flex-wrap: wrap;
    align-items: center;
}

.pill {
    font-size: .72rem;
    padding: 3px 10px;
    border-radius: 999px;
    background: rgba(13,17,23,.55);
    border: 1px solid rgba(255,255,255,.22);
}

.pill.ok {
    border-color: #5be39a;
    color: #b9ffd9 !important;
}

.pill.bad {
    border-color: #ff8a80;
    color: #ffd0cc !important;
}

/* =====================================================
   DASHBOARD GRID: KPI row + 3 columns + legal line.
   Height = screen height minus the header area.
   ===================================================== */
.dash {
    height: calc(100vh - var(--reserved));
    height: calc(100dvh - var(--reserved));
    min-height: 330px;
    display: grid;
    grid-template-rows: auto minmax(0, 1fr) auto;
    gap: 8px;
}

.kpis {
    display: grid;
    grid-template-columns: repeat(5, minmax(0, 1fr));
    gap: 8px;
}

.panels {
    display: grid;
    grid-template-columns: 1.3fr 1fr 1fr;
    gap: 8px;
    min-height: 0;
}

.col {
    display: flex;
    flex-direction: column;
    gap: 8px;
    min-height: 0;
}

.card, .panel {
    background: rgba(13,17,23,.62);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(255,255,255,.17);
    border-radius: 14px;
}

/* KPI CARDS */
.kpi {
    padding: 8px 12px;
}

.kpi .v {
    font-size: 1.5rem;
    font-weight: 800;
    line-height: 1.15;
    color: #ffffff !important;
}

.kpi .v.pending {
    color: rgba(255,255,255,.58) !important;
    font-size: 1.2rem;
    padding-top: 3px;
}

.kpi .l {
    font-size: .75rem;
    font-weight: 700;
    color: #ffffff !important;
}

.kpi .s {
    font-size: .64rem;
    color: rgba(255,255,255,.67) !important;
    overflow-wrap: anywhere;
}

/* PANELS */
.panel {
    padding: 10px 12px;
    min-height: 0;
    flex: 0 1 auto;
    overflow-y: auto;
    overflow-x: hidden;
    scrollbar-width: thin;
    scrollbar-color: rgba(255,255,255,.3) transparent;
}

.panel.grow {
    flex: 1 1 0;
}

.ptitle {
    font-size: .92rem;
    font-weight: 800;
    margin-bottom: 7px;
    color: #ffffff !important;
}

.ptitle span {
    font-size: .67rem;
    font-weight: 400;
    color: rgba(255,255,255,.65) !important;
    margin-left: 7px;
}

.empty {
    color: rgba(255,255,255,.65) !important;
    font-size: .8rem;
    padding-top: 24px;
    text-align: center;
}

/* COMPARISON BARS */
.sys {
    padding: 5px 8px;
    margin-bottom: 5px;
    border-radius: 10px;
    border: 1px solid transparent;
}

.sys.hl {
    background: rgba(255,255,255,.09);
    border-color: rgba(255,255,255,.4);
}

.sh {
    display: flex;
    justify-content: space-between;
    font-size: .8rem;
    margin-bottom: 3px;
    gap: 5px;
}

.sh b {
    overflow-wrap: anywhere;
}

.sh span {
    color: rgba(255,255,255,.65) !important;
    font-size: .68rem;
}

.brow {
    display: grid;
    grid-template-columns: 58px 1fr 44px;
    align-items: center;
    gap: 8px;
    height: 14px;
}

.bl, .bv {
    font-size: .66rem;
    color: rgba(255,255,255,.85) !important;
}

.bv {
    text-align: right;
    font-weight: 800;
}

.track {
    height: 6px;
    border-radius: 99px;
    background: rgba(255,255,255,.12);
    overflow: hidden;
}

.fill {
    height: 100%;
    border-radius: 99px;
    background: linear-gradient(
        90deg,
        #e0261a,
        #8a3fb0,
        #2a8cf5
    );
}

/* CONFUSION MATRIX */
.cm {
    display: grid;
    gap: 4px;
}

.cm-h {
    font-size: .67rem;
    color: rgba(255,255,255,.8) !important;
    text-align: center;
    align-self: center;
    overflow-wrap: anywhere;
}

.cm-c {
    min-height: 34px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    font-size: .9rem;
    color: #ffffff !important;
}

.note {
    font-size: .66rem;
    color: rgba(255,255,255,.65) !important;
    margin-top: 7px;
}

/* RESEARCH FRAMEWORK */
.panel.fwp {
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.fw {
    flex: 1 1 auto;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 7px 10px;
    border-radius: 10px;
    background: rgba(255,255,255,.06);
    border: 1px solid rgba(255,255,255,.12);
}

.fw.new {
    background: rgba(255,255,255,.13);
    border-color: rgba(255,255,255,.5);
}

.fw b {
    font-size: .8rem;
    color: #ffffff !important;
}

.fw div {
    font-size: .69rem;
    color: rgba(255,255,255,.77) !important;
    line-height: 1.4;
}

/* GBC DETAILS */
.panel.gbc {
    background: rgba(23,48,78,.80);
    border: 1px solid rgba(135,185,240,.38);
}

.gbc-title {
    font-size: .9rem;
    font-weight: 800;
    color: #ffffff !important;
    line-height: 1.35;
}

.gbc-heading {
    color: #a9d4fa !important;
    font-size: .62rem;
    letter-spacing: .9px;
    font-weight: 800;
    margin-top: 7px;
}

.gbc-text {
    font-size: .7rem;
    color: #ffffff !important;
    line-height: 1.4;
}

/* LEGAL LINE */
.legal {
    font-size: .62rem;
    line-height: 1.3;
    color: rgba(255,255,255,.56) !important;
}

/* =====================================================
   SMALL SCREENS
   ===================================================== */
@media (max-height: 780px) {
    .title { font-size: 1.35rem; }
    .kpi { padding: 6px 10px; }
    .kpi .v { font-size: 1.3rem; }
    .cm-c { min-height: 28px; }
}

/* Phones / very small windows cannot fit everything on one screen,
   so only here the page is allowed to scroll. */
@media (max-width: 900px), (max-height: 540px) {
    html, body,
    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {
        height: auto !important;
        overflow-y: auto !important;
    }

    .block-container {
        padding: 1rem !important;
    }

    .dash {
        height: auto;
    }

    .kpis {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }

    .panels {
        grid-template-columns: 1fr;
    }

    .panel {
        overflow: visible;
    }
}

</style>
"""

st.markdown(STYLE, unsafe_allow_html=True)


# =====================================================
# HELPER FUNCTIONS
# =====================================================

def esc(value):
    return html.escape(str(value))


def pct(value):
    return f"{value * 100:.1f}%"


def render(markup):
    """Render raw HTML safely.

    Markdown treats any line indented by 4+ spaces that follows a
    blank line as a CODE BLOCK, which made raw HTML appear as text
    on the dashboard. Removing indentation and blank lines before
    rendering prevents that.
    """

    compact = " ".join(
        line.strip()
        for line in markup.splitlines()
        if line.strip()
    )

    st.markdown(compact, unsafe_allow_html=True)


def evaluate(data):
    """Calculate accuracy and macro-averaged classification metrics."""

    actual = data["actual_label"]
    predicted = data["predicted_label"]

    labels = sorted(set(actual) | set(predicted))

    matrix = pd.crosstab(
        actual,
        predicted
    ).reindex(
        index=labels,
        columns=labels,
        fill_value=0
    )

    true_positive = pd.Series(
        matrix.values.diagonal(),
        index=labels
    )

    precision = (
        true_positive /
        matrix.sum(axis=0).replace(0, float("nan"))
    ).fillna(0)

    recall = (
        true_positive /
        matrix.sum(axis=1).replace(0, float("nan"))
    ).fillna(0)

    f1 = (
        2 * precision * recall /
        (precision + recall).replace(0, float("nan"))
    ).fillna(0)

    return {
        "n": len(data),
        "acc": float((actual == predicted).mean()),
        "prec": float(precision.mean()),
        "rec": float(recall.mean()),
        "f1": float(f1.mean()),
        "cm": matrix
    }


def kpi(label, value, subtitle):

    if value is None:
        value_html = '<div class="v pending">Pending</div>'
    else:
        value_html = (
            f'<div class="v">{esc(value)}</div>'
        )

    return f"""
    <div class="card kpi">
        <div class="l">{esc(label)}</div>
        {value_html}
        <div class="s">{esc(subtitle)}</div>
    </div>
    """


def bar(label, value):

    width = max(0, min(value * 100, 100))

    return f"""
    <div class="brow">
        <span class="bl">{esc(label)}</span>
        <div class="track">
            <div class="fill" style="width:{width:.1f}%"></div>
        </div>
        <span class="bv">{pct(value)}</span>
    </div>
    """


def comparison(results, selected):

    output = ""

    for name, result in results.items():

        highlight = " hl" if name == selected else ""

        output += f"""
        <div class="sys{highlight}">
            <div class="sh">
                <b>{esc(name)}</b>
                <span>{result['n']} records</span>
            </div>
            {bar("Accuracy", result["acc"])}
            {bar("Precision", result["prec"])}
            {bar("Recall", result["rec"])}
            {bar("F1-score", result["f1"])}
        </div>
        """

    return output


def confusion(matrix):

    maximum = max(int(matrix.values.max()), 1)

    cells = (
        '<div class="cm-h"></div>'
        + "".join(
            f'<div class="cm-h">{esc(c)}</div>'
            for c in matrix.columns
        )
    )

    for actual in matrix.index:

        cells += f'<div class="cm-h">{esc(actual)}</div>'

        for predicted in matrix.columns:

            value = int(matrix.loc[actual, predicted])

            alpha = (
                0.06 if value == 0
                else 0.18 + 0.75 * value / maximum
            )

            color = (
                "31,140,242"
                if actual == predicted
                else "224,38,26"
            )

            cells += f"""
            <div class="cm-c"
                style="background:rgba({color},{alpha:.2f})">
                {value}
            </div>
            """

    return f"""
    <div class="cm"
        style="grid-template-columns:auto repeat({len(matrix.columns)}, minmax(0,1fr))">
        {cells}
    </div>

    <div class="note">
        Rows = Actual labels.
        Columns = Predicted labels.
        Blue = Correct predictions.
        Red = Incorrect predictions.
    </div>
    """


def mlflow_status_html():
    """Compact one-line MLflow connection status."""

    status = st.session_state.get("mlflow_status")

    if status == "connected":

        run_id = st.session_state.get("mlflow_run_id", "")

        return (
            '<div class="mini ok">'
            f'✓ Connected · Run {esc(run_id[:8])}… '
            f'<a href="{TRACKING_URI}" target="_blank" '
            'rel="noopener">Open DagsHub</a>'
            '</div>'
        )

    if status == "failed":

        error = st.session_state.get("mlflow_error", "Unknown error")

        return (
            '<div class="mini bad">'
            f'✕ Failed: {esc(error)}. Check secrets, token '
            'and DagsHub write permission.'
            '</div>'
        )

    return '<div class="mini">Connection not tested yet.</div>'


def dashboard_html(results, view, cur):
    """KPI row, three panels and legal line as ONE grid so every
    block lines up and the whole layout fits the screen."""

    subtitle = (
        f"{view}, macro average"
        if cur else
        "Waiting for experimental data"
    )

    cards = [
        ("Accuracy", pct(cur["acc"]) if cur else None),
        ("Precision", pct(cur["prec"]) if cur else None),
        ("Recall", pct(cur["rec"]) if cur else None),
        ("F1-score", pct(cur["f1"]) if cur else None),
        ("Records evaluated", str(cur["n"]) if cur else None)
    ]

    kpis = "".join(
        kpi(label, value, subtitle)
        for label, value in cards
    )

    comparison_body = (
        comparison(results, view)
        if cur else
        '<div class="empty">'
        'System comparison will appear after a valid CSV is uploaded.'
        '</div>'
    )

    confusion_body = (
        confusion(cur["cm"])
        if cur else
        '<div class="empty">'
        'Confusion matrix will appear after a valid CSV is uploaded.'
        '</div>'
    )

    view_tag = f"<span>{esc(view)}</span>" if cur else ""

    data_note = (
        " Metrics are computed from the uploaded predictions "
        "and evaluator-approved actual labels."
        if cur else ""
    )

    return f"""
    <div class="dash">

        <div class="kpis">
            {kpis}
        </div>

        <div class="panels">

            <div class="col">
                <div class="panel grow">
                    <div class="ptitle">
                        System Comparison
                        <span>Higher is better</span>
                    </div>
                    {comparison_body}
                </div>
            </div>

            <div class="col">

                <div class="panel">
                    <div class="ptitle">
                        Confusion Matrix
                        {view_tag}
                    </div>
                    {confusion_body}
                </div>

                <div class="panel grow gbc">
                    <div class="gbc-title">
                        Gradient Boosting Classifier (GBC)
                    </div>

                    <div class="gbc-heading">ALGORITHM TYPE</div>
                    <div class="gbc-text">
                        Supervised Machine Learning – Ensemble Learning
                    </div>

                    <div class="gbc-heading">PURPOSE</div>
                    <div class="gbc-text">
                        Classify selected CPR movement patterns as
                        proper or improper using extracted movement
                        features from MediaPipe Pose and MediaPipe Hand.
                    </div>

                    <div class="gbc-heading">MODEL STATUS</div>
                    <div class="gbc-text">
                        Provisional. Pending dataset preparation,
                        training, validation and computational testing.
                    </div>
                </div>

            </div>

            <div class="col">
                <div class="panel grow fwp">
                    <div class="ptitle">Research Framework</div>

                    <div class="fw">
                        <b>Ecker et al. (2024)</b>
                        <div>
                            Existing system. MediaPipe Pose landmark
                            analysis and CPR measurement evaluation.
                        </div>
                    </div>

                    <div class="fw">
                        <b>SmartCPR (2024)</b>
                        <div>
                            Existing system. MoveNet smartphone CPR
                            assessment with measurement analysis
                            and feedback.
                        </div>
                    </div>

                    <div class="fw new">
                        <b>Hybrid CPR System</b>
                        <div>
                            Proposed. MediaPipe Pose and Hand,
                            Machine Learning, Rule-Based Assessment
                            and Hybrid Decision Engine.
                        </div>
                    </div>
                </div>
            </div>

        </div>

        <div class="legal">
            NEMSU Lianga Campus | CPR Research Project | 2026.
            Supplementary CPR research and training tool.
            Not a replacement for qualified CPR instructors,
            instrumented manikins, or official CPR guidelines.{data_note}
        </div>

    </div>
    """


# =====================================================
# MLFLOW CONNECTION
# =====================================================

def test_mlflow_connection():

    required_secrets = [
        "MLFLOW_TRACKING_URI",
        "MLFLOW_TRACKING_USERNAME",
        "MLFLOW_TRACKING_PASSWORD"
    ]

    missing = [
        key for key in required_secrets
        if key not in st.secrets
        or not str(st.secrets[key]).strip()
    ]

    if missing:
        raise ValueError(
            "Missing or empty Streamlit Secrets: "
            + ", ".join(missing)
        )

    # Obtain credentials securely
    tracking_uri = str(
        st.secrets["MLFLOW_TRACKING_URI"]
    ).strip()

    username = str(
        st.secrets["MLFLOW_TRACKING_USERNAME"]
    ).strip()

    password = str(
        st.secrets["MLFLOW_TRACKING_PASSWORD"]
    ).strip()

    # Configure DagsHub authentication
    os.environ["MLFLOW_TRACKING_URI"] = tracking_uri
    os.environ["MLFLOW_TRACKING_USERNAME"] = username
    os.environ["MLFLOW_TRACKING_PASSWORD"] = password

    import mlflow

    from mlflow.tracking import MlflowClient

    mlflow.set_tracking_uri(tracking_uri)

    client = MlflowClient(
        tracking_uri=tracking_uri
    )

    # Verify server access
    client.search_experiments(
        max_results=1
    )

    experiment_name = (
        "CPR_Dashboard_Connection_Check"
    )

    experiment = client.get_experiment_by_name(
        experiment_name
    )

    if experiment is None:

        experiment_id = client.create_experiment(
            experiment_name
        )

    else:

        experiment_id = experiment.experiment_id

    # Record connection test only
    with mlflow.start_run(
        experiment_id=experiment_id,
        run_name="DagsHub Connection Check Only"
    ):

        mlflow.set_tags({
            "run_type": "connection_check",
            "not_model_evaluation": "true",
            "project": "AI-Assisted CPR Research"
        })

        mlflow.log_param(
            "purpose",
            "Verify Streamlit to DagsHub connectivity"
        )

        run_id = mlflow.active_run().info.run_id

    return run_id


# =====================================================
# ROW 1: HEADER + CSV UPLOAD + MLFLOW BUTTON
# =====================================================

head, upload_col, mlflow_col = st.columns(
    [1.5, 1.05, .85],
    gap="medium"
)

with head:

    render("""
    <div class="eyebrow">
        NORTH EASTERN MINDANAO STATE UNIVERSITY,
        LIANGA CAMPUS
    </div>

    <div class="title">
        AI-Assisted CPR Proper Execution Training System
    </div>

    <div class="sub">
        Comparative research and experimental dashboard
        for BS Computer Science
    </div>
    """)


with upload_col:

    render("""
    <div class="eyebrow">EXPERIMENTAL PREDICTIONS CSV</div>
    """)

    uploaded = st.file_uploader(
        "Experimental predictions CSV",
        type=["csv"],
        label_visibility="collapsed"
    )


with mlflow_col:

    render("""
    <div class="eyebrow">HOSTED EXPERIMENT TRACKING</div>
    """)

    test_button = st.button(
        "Test MLflow Connection",
        use_container_width=True,
        key="mlflow_test_button"
    )

    if test_button:

        with st.spinner("Connecting to DagsHub MLflow..."):

            try:

                connection_run_id = test_mlflow_connection()

                st.session_state["mlflow_status"] = "connected"
                st.session_state["mlflow_run_id"] = connection_run_id
                st.session_state.pop("mlflow_error", None)

            except Exception as error:

                st.session_state["mlflow_status"] = "failed"
                st.session_state["mlflow_error"] = (
                    type(error).__name__
                )
                st.session_state.pop("mlflow_run_id", None)

    render(mlflow_status_html())


# =====================================================
# DATA LOADING AND VALIDATION
# =====================================================

df = None
results = {}
pills = (
    '<span class="pill">'
    'Upload an experimental predictions CSV to begin.'
    '</span>'
)

validation_message = None

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

            df = raw.dropna(
                subset=REQUIRED
            ).copy()

            for column in [
                "participant_id",
                "clip_id",
                "system",
                "actual_label",
                "predicted_label"
            ]:

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

                # Every sample must have one prediction per system.
                duplicate_rows = df.duplicated(
                    subset=[
                        "system",
                        "participant_id",
                        "clip_id"
                    ],
                    keep=False
                )

                if duplicate_rows.any():

                    validation_message = (
                        "Duplicate records found for the same "
                        "system, participant, and clip. "
                        "Check the CSV before evaluating."
                    )

                    df = None

                else:

                    # The evaluator label must be consistent
                    # across all system predictions.
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
        UnicodeDecodeError
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
            sort=False
        )
    }

    # Verify that all systems use identical test samples
    sample_sets = {
        system: set(
            zip(
                group["participant_id"],
                group["clip_id"]
            )
        )
        for system, group in df.groupby(
            "system",
            sort=False
        )
    }

    equal_samples = (
        len(sample_sets) > 1
        and len({
            frozenset(samples)
            for samples in sample_sets.values()
        }) == 1
    )

    pills = (
        f'<span class="pill ok">✓ {esc(uploaded.name)}</span>'
        f'<span class="pill">{len(df)} records</span>'
        f'<span class="pill">{df["participant_id"].nunique()} participants</span>'
        f'<span class="pill">{df["clip_id"].nunique()} clips</span>'
        f'<span class="pill">{len(systems)} systems</span>'
    )

    if equal_samples:

        pills += (
            '<span class="pill ok">'
            'Same test samples'
            '</span>'
        )

    elif len(systems) > 1:

        pills += (
            '<span class="pill bad">'
            'Different test samples'
            '</span>'
        )


# Validation problems are shown as a compact pill instead of a
# large alert box, so they never push the layout off the screen.
if validation_message:

    pills = (
        '<span class="pill bad">'
        f'✕ {esc(validation_message)}'
        '</span>'
    )


# =====================================================
# ROW 2: DATASET BUTTON + STATUS PILLS + SYSTEM SELECTOR
# =====================================================

view = None
cur = None

if df is not None:

    hybrid = next(
        (
            system for system in results
            if "hybrid" in system.lower()
        ),
        None
    )

    options = systems

    default_index = (
        options.index(hybrid)
        if hybrid else 0
    )

    data_col, status_col, switch_col = st.columns(
        [.5, 1.6, 1.5],
        gap="small"
    )

    with data_col:

        # Opens as an overlay, so the page does not get taller.
        with st.popover(
            "📄 View dataset",
            use_container_width=True
        ):

            st.dataframe(
                df,
                use_container_width=True
            )

    with status_col:

        render(f'<div class="pills">{pills}</div>')

    with switch_col:

        view = st.radio(
            "System",
            options,
            index=default_index,
            horizontal=True,
            label_visibility="collapsed"
        )

    cur = results.get(view)

else:

    render(f'<div class="pills">{pills}</div>')


# =====================================================
# DASHBOARD: KPI + PANELS + LEGAL (one screen, no scrolling)
# =====================================================

render(dashboard_html(results, view, cur))
