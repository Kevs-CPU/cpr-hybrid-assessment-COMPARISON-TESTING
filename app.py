
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

# =====================================================
# CSS: SINGLE-SCREEN DASHBOARD
# =====================================================

st.markdown("""
<style>

@import url(
'https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700;800&display=swap'
);

/* ==========================================
   NO PAGE SCROLLING
========================================== */

html, body, #root {
    height: 100% !important;
    overflow: hidden !important;
}

[data-testid="stAppViewContainer"],
[data-testid="stMain"],
section.main {
    height: 100vh !important;
    max-height: 100vh !important;
    overflow: hidden !important;
}

.block-container {
    height: 100vh !important;
    max-height: 100vh !important;
    overflow: hidden !important;
    max-width: 1550px;
    padding: .45rem 1.5rem .3rem !important;
    font-family: 'DM Sans', 'Segoe UI', sans-serif !important;
}

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
    font-family: 'DM Sans', 'Segoe UI', sans-serif !important;
}

[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
footer {
    display: none !important;
}

[data-testid="stVerticalBlock"] {
    gap: .38rem;
}

[data-testid="stElementContainer"] {
    margin: 0 !important;
}

/* ==========================================
   HEADER
========================================== */

.eyebrow {
    font-size: .68rem;
    font-weight: 700;
    color: rgba(255,255,255,.78) !important;
    letter-spacing: 1px;
}

.title {
    font-size: 1.55rem;
    font-weight: 800;
    letter-spacing: -.03em;
    line-height: 1.16;
    color: #ffffff !important;
}

.sub {
    font-size: .75rem;
    color: rgba(255,255,255,.78) !important;
    margin-top: 3px;
}

/* ==========================================
   BUTTON VISIBILITY
========================================== */

[data-testid="stButton"] button,
.stButton button {
    background: #ffffff !important;
    color: #0d1117 !important;
    border: 1px solid #ffffff !important;
    border-radius: 9px !important;
    font-weight: 800 !important;
    font-size: .75rem !important;
    min-height: 38px !important;
    padding: 5px 9px !important;
    white-space: normal !important;
}

[data-testid="stButton"] button *,
.stButton button span,
.stButton button p {
    color: #0d1117 !important;
}

[data-testid="stButton"] button:hover,
.stButton button:hover {
    background: #dceafa !important;
    color: #0d1117 !important;
    border-color: #dceafa !important;
}

[data-testid="stButton"] button:focus {
    box-shadow: 0 0 0 2px rgba(255,255,255,.4) !important;
}

/* ==========================================
   CSV UPLOADER
========================================== */

[data-testid="stFileUploader"] {
    background: rgba(13,17,23,.58) !important;
    border: 1px solid rgba(255,255,255,.22) !important;
    border-radius: 11px !important;
    padding: 5px !important;
}

[data-testid="stFileUploaderDropzone"] {
    background: rgba(13,17,23,.52) !important;
    border: 1px dashed rgba(255,255,255,.45) !important;
    border-radius: 9px !important;
    padding: 5px !important;
    min-height: 50px !important;
}

[data-testid="stFileUploader"] p,
[data-testid="stFileUploader"] span,
[data-testid="stFileUploader"] small {
    color: #ffffff !important;
}

[data-testid="stFileUploaderDropzone"] button {
    background: #ffffff !important;
    border: 1px solid #ffffff !important;
    border-radius: 8px !important;
    font-weight: 800 !important;
}

[data-testid="stFileUploaderDropzone"] button *,
[data-testid="stFileUploaderDropzone"] button span,
[data-testid="stFileUploaderDropzone"] button p {
    color: #172333 !important;
}

[data-testid="stFileUploaderDropzone"] button:hover {
    background: #dceafa !important;
}

[data-testid="stFileUploaderFile"] {
    padding: 0 !important;
}

/* ==========================================
   STATUS PILLS
========================================== */

.pills {
    display: flex;
    gap: .35rem;
    flex-wrap: nowrap;
    align-items: center;
    overflow: hidden;
    min-height: 27px;
}

.pill {
    font-size: .68rem;
    padding: 4px 9px;
    border-radius: 999px;
    white-space: nowrap;
    background: rgba(13,17,23,.55);
    border: 1px solid rgba(255,255,255,.22);
    color: #ffffff !important;
}

.pill.ok {
    border-color: #5be39a;
    color: #b9ffd9 !important;
}

.pill.bad {
    border-color: #ff8a80;
    color: #ffd0cc !important;
}

/* ==========================================
   SYSTEM SELECTOR
========================================== */

[data-testid="stRadio"] [role="radiogroup"] {
    gap: .25rem;
    justify-content: flex-end;
    flex-wrap: nowrap;
}

[data-testid="stRadio"] label {
    background: rgba(13,17,23,.55);
    border: 1px solid rgba(255,255,255,.25);
    border-radius: 999px;
    padding: 1px 9px;
    margin: 0;
}

[data-testid="stRadio"] label p {
    color: #ffffff !important;
    font-size: .68rem;
    font-weight: 600;
}

[data-testid="stRadio"] label:has(input:checked) {
    background: #ffffff;
}

[data-testid="stRadio"] label:has(input:checked) p {
    color: #0d1117 !important;
    font-weight: 800;
}

/* ==========================================
   CARDS
========================================== */

.card, .panel {
    background: rgba(13,17,23,.62);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(255,255,255,.17);
    border-radius: 13px;
}

.kpi {
    padding: 8px 11px;
    height: 69px;
}

.kpi .v {
    font-size: 1.5rem;
    font-weight: 800;
    line-height: 1.1;
    color: #ffffff !important;
}

.kpi .v.pending {
    color: rgba(255,255,255,.58) !important;
    font-size: 1.2rem;
    padding-top: 3px;
}

.kpi .l {
    font-size: .71rem;
    font-weight: 700;
    color: #ffffff !important;
}

.kpi .s {
    font-size: .62rem;
    color: rgba(255,255,255,.65) !important;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
}

/* ==========================================
   MAIN PANELS
========================================== */

.panel {
    height: 355px;
    min-height: 355px;
    max-height: 355px;
    overflow: hidden;
    padding: 11px 12px;
}

.ptitle {
    font-size: .91rem;
    font-weight: 800;
    margin-bottom: 8px;
    color: #ffffff !important;
}

.ptitle span {
    font-size: .65rem;
    font-weight: 400;
    color: rgba(255,255,255,.65) !important;
    margin-left: 5px;
}

.empty {
    color: rgba(255,255,255,.65) !important;
    font-size: .78rem;
    padding-top: 45px;
    text-align: center;
}

/* ==========================================
   COMPARISON BARS
========================================== */

.sys {
    padding: 6px 8px;
    margin-bottom: 5px;
    border-radius: 9px;
    border: 1px solid transparent;
}

.sys.hl {
    background: rgba(255,255,255,.09);
    border-color: rgba(255,255,255,.4);
}

.sh {
    display: flex;
    justify-content: space-between;
    font-size: .76rem;
    margin-bottom: 3px;
    gap: 5px;
}

.sh b {
    color: #ffffff !important;
    overflow-wrap: anywhere;
}

.sh span {
    color: rgba(255,255,255,.65) !important;
    font-size: .65rem;
}

.brow {
    display: grid;
    grid-template-columns: 58px 1fr 44px;
    align-items: center;
    gap: 7px;
    height: 15px;
}

.bl, .bv {
    font-size: .65rem;
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

/* ==========================================
   CONFUSION MATRIX
========================================== */

.cm {
    display: grid;
    gap: 4px;
}

.cm-h {
    font-size: .65rem;
    color: rgba(255,255,255,.8) !important;
    text-align: center;
    align-self: center;
    overflow-wrap: anywhere;
}

.cm-c {
    min-height: 34px;
    border-radius: 7px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    font-size: .85rem;
    color: #ffffff !important;
}

.note {
    font-size: .65rem;
    color: rgba(255,255,255,.65) !important;
    margin-top: 7px;
}

/* ==========================================
   RESEARCH FRAMEWORK
========================================== */

.fw {
    padding: 6px 8px;
    border-radius: 9px;
    margin-bottom: 5px;
    background: rgba(255,255,255,.06);
    border: 1px solid rgba(255,255,255,.12);
}

.fw.new {
    background: rgba(255,255,255,.13);
    border-color: rgba(255,255,255,.5);
}

.fw b {
    font-size: .75rem;
    color: #ffffff !important;
}

.fw div {
    font-size: .64rem;
    color: rgba(255,255,255,.77) !important;
    line-height: 1.3;
}

/* ==========================================
   GBC DETAILS
========================================== */

.gbc-box {
    background: rgba(23,48,78,.88);
    border: 1px solid rgba(135,185,240,.4);
    border-radius: 9px;
    padding: 8px;
    margin-top: 5px;
}

.gbc-title {
    font-size: .82rem;
    font-weight: 800;
    color: #ffffff !important;
    line-height: 1.3;
}

.gbc-heading {
    color: #a9d4fa !important;
    font-size: .59rem;
    letter-spacing: .8px;
    font-weight: 800;
    margin-top: 6px;
}

.gbc-text {
    font-size: .65rem;
    color: #ffffff !important;
    line-height: 1.3;
}

/* ==========================================
   STATUS FEEDBACK
========================================== */

.connection-success {
    color: #b9ffd9 !important;
    font-size: .7rem;
    font-weight: 700;
}

.connection-error {
    color: #ffd0cc !important;
    font-size: .7rem;
    font-weight: 700;
}

/* FOOTER */
.foot {
    font-size: .62rem;
    color: rgba(255,255,255,.5) !important;
    margin-top: 5px;
}

/* ==========================================
   SHORT DESKTOP SCREENS
========================================== */

@media (max-height: 760px) {
    .title {
        font-size: 1.3rem;
    }

    .panel {
        height: 315px;
        min-height: 315px;
        max-height: 315px;
    }

    .kpi {
        height: 62px;
    }

    .kpi .v {
        font-size: 1.3rem;
    }

    .block-container {
        padding-top: .25rem !important;
    }
}

@media (max-width: 900px) {
    .block-container {
        padding: .5rem !important;
    }
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# HELPER FUNCTIONS
# =====================================================

def esc(value):
    return html.escape(str(value))


def pct(value):
    return f"{value * 100:.1f}%"


def evaluate(data):
    """Calculate accuracy and macro-averaged metrics."""

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

    value_html = (
        f'<div class="v">{esc(value)}</div>'
        if value is not None
        else '<div class="v pending">Pending</div>'
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
        Blue = Correct.
        Red = Incorrect.
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

    tracking_uri = str(
        st.secrets["MLFLOW_TRACKING_URI"]
    ).strip()

    username = str(
        st.secrets["MLFLOW_TRACKING_USERNAME"]
    ).strip()

    password = str(
        st.secrets["MLFLOW_TRACKING_PASSWORD"]
    ).strip()

    os.environ["MLFLOW_TRACKING_URI"] = tracking_uri
    os.environ["MLFLOW_TRACKING_USERNAME"] = username
    os.environ["MLFLOW_TRACKING_PASSWORD"] = password

    import mlflow

    from mlflow.tracking import MlflowClient

    mlflow.set_tracking_uri(tracking_uri)

    client = MlflowClient(
        tracking_uri=tracking_uri
    )

    # Verify access
    client.search_experiments(max_results=1)

    experiment_name = "CPR_Dashboard_Connection_Check"

    experiment = client.get_experiment_by_name(
        experiment_name
    )

    if experiment is None:
        experiment_id = client.create_experiment(
            experiment_name
        )
    else:
        experiment_id = experiment.experiment_id

    # Connection test only. No CPR metrics.
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
# HEADER + CSV + VISIBLE MLFLOW BUTTON
# =====================================================

head, upload_col, mlflow_col = st.columns(
    [1.55, 1.0, .85],
    gap="small"
)

with head:

    st.markdown("""
    <div class="eyebrow">
        NORTH EASTERN MINDANAO STATE UNIVERSITY, LIANGA CAMPUS
    </div>

    <div class="title">
        AI-Assisted CPR Proper Execution Training System
    </div>

    <div class="sub">
        Comparative Research and Experimental Dashboard
        | BS Computer Science
    </div>
    """, unsafe_allow_html=True)


with upload_col:

    uploaded = st.file_uploader(
        "Experimental predictions CSV",
        type=["csv"],
        help="Upload validated experimental predictions."
    )


with mlflow_col:

    st.markdown(
        '<div class="eyebrow">HOSTED EXPERIMENT TRACKING</div>',
        unsafe_allow_html=True
    )

    test_button = st.button(
        "Test MLflow Connection",
        type="primary",
        use_container_width=True,
        key="mlflow_test_button"
    )


# =====================================================
# MLFLOW BUTTON ACTION
# =====================================================

if test_button:

    try:

        with st.spinner("Connecting to DagsHub MLflow..."):

            run_id = test_mlflow_connection()

            st.session_state["mlflow_status"] = "connected"
            st.session_state["mlflow_run_id"] = run_id

            st.session_state.pop(
                "mlflow_error",
                None
            )

    except Exception as error:

        st.session_state["mlflow_status"] = "failed"

        # Do not expose private credentials.
        st.session_state["mlflow_error"] = (
            type(error).__name__
        )

        st.session_state.pop(
            "mlflow_run_id",
            None
        )


# Connection status
if st.session_state.get("mlflow_status") == "connected":

    run_id = st.session_state.get(
        "mlflow_run_id",
        ""
    )

    st.markdown(
        f"""
        <div class="pills">
            <span class="pill ok">
                ✓ DagsHub MLflow Connected
            </span>
            <span class="pill">
                Run ID: {esc(run_id[:12])}...
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

elif st.session_state.get("mlflow_status") == "failed":

    st.markdown(
        f"""
        <div class="pills">
            <span class="pill bad">
                MLflow Connection Failed:
                {esc(st.session_state.get("mlflow_error", "Unknown error"))}
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

else:

    st.markdown(
        """
        <div class="pills">
            <span class="pill">
                MLflow connection not yet tested
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )


# =====================================================
# LOAD AND VALIDATE CSV
# =====================================================

df = None
results = {}
validation_message = None

if uploaded is not None:

    try:

        raw = pd.read_csv(
            uploaded,
            dtype="string"
        )

        raw.columns = [
            str(column).strip().lower()
            for column in raw.columns
        ]

        missing = [
            column for column in REQUIRED
            if column not in raw.columns
        ]

        if raw.empty:

            validation_message = (
                "The CSV contains no records."
            )

        elif missing:

            validation_message = (
                "Missing required columns: "
                + ", ".join(missing)
            )

        else:

            df = raw.copy()

            for column in REQUIRED:

                df[column] = (
                    df[column]
                    .astype("string")
                    .str.strip()
                )

            df = df.replace("", pd.NA)

            df = df.dropna(
                subset=REQUIRED
            ).copy()

            df["actual_label"] = (
                df["actual_label"].str.lower()
            )

            df["predicted_label"] = (
                df["predicted_label"].str.lower()
            )

            if df.empty:

                validation_message = (
                    "No usable records remain after removing "
                    "missing or blank values."
                )

                df = None

            else:

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
                        "system, participant, and clip."
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
                            "Inconsistent evaluator-approved labels "
                            "were found for the same test sample."
                        )

                        df = None

    except (
        pd.errors.EmptyDataError,
        pd.errors.ParserError,
        UnicodeDecodeError
    ):

        validation_message = (
            "Cannot read the uploaded CSV. Check the file format."
        )

    except Exception as error:

        validation_message = (
            "Dataset error: " + type(error).__name__
        )


# =====================================================
# SYSTEM RESULTS
# =====================================================

if df is not None:

    systems = list(df["system"].unique())

    results = {
        system: evaluate(group)
        for system, group in df.groupby(
            "system",
            sort=False
        )
    }

    # Verify identical test sample coverage
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
            '<span class="pill ok">Same test samples</span>'
        )

    elif len(systems) > 1:

        pills += (
            '<span class="pill bad">Different test samples</span>'
        )

else:

    systems = []
    pills = (
        '<span class="pill">'
        'Upload a valid experimental CSV to begin.'
        '</span>'
    )


# =====================================================
# SYSTEM SELECTOR
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

    default_index = (
        systems.index(hybrid)
        if hybrid else 0
    )

    status_col, switch_col = st.columns(
        [1.5, 1],
        gap="small"
    )

    with status_col:

        st.markdown(
            f'<div class="pills">{pills}</div>',
            unsafe_allow_html=True
        )

    with switch_col:

        view = st.radio(
            "System",
            systems,
            index=default_index,
            horizontal=True,
            label_visibility="collapsed"
        )

    cur = results.get(view)

else:

    st.markdown(
        f'<div class="pills">{pills}</div>',
        unsafe_allow_html=True
    )

    if validation_message:
        st.warning(validation_message)


# =====================================================
# KPI ROW
# =====================================================

subtitle = (
    f"{esc(view)}, macro average"
    if cur else
    "Waiting for experimental data"
)

kpi_items = [
    ("Accuracy", pct(cur["acc"]) if cur else None),
    ("Precision", pct(cur["prec"]) if cur else None),
    ("Recall", pct(cur["rec"]) if cur else None),
    ("F1-score", pct(cur["f1"]) if cur else None),
    ("Records evaluated", str(cur["n"]) if cur else None)
]

kpi_columns = st.columns(
    5,
    gap="small"
)

for column, (label, value) in zip(
    kpi_columns,
    kpi_items
):

    with column:

        st.markdown(
            kpi(label, value, subtitle),
            unsafe_allow_html=True
        )


# =====================================================
# MAIN DASHBOARD PANELS
# =====================================================

c1, c2, c3 = st.columns(
    [1.35, 1, 1.08],
    gap="small"
)


# SYSTEM COMPARISON
with c1:

    body = (
        comparison(results, view)
        if cur else
        """
        <div class="empty">
            System comparison will appear after valid
            experimental predictions are uploaded.
        </div>
        """
    )

    if cur and len(systems) > 1:

        sample_note = (
            '<div class="note">'
            'Same test samples: controlled comparison possible.'
            '</div>'
            if equal_samples
            else
            '<div class="note">'
            'Different test samples: scores are not a direct '
            'controlled comparison.'
            '</div>'
        )

        body += sample_note

    st.markdown(
        f"""
        <div class="panel">
            <div class="ptitle">
                System Comparison
                <span>Higher is better</span>
            </div>
            {body}
        </div>
        """,
        unsafe_allow_html=True
    )


# CONFUSION MATRIX
with c2:

    body = (
        confusion(cur["cm"])
        if cur else
        """
        <div class="empty">
            Confusion matrix will appear after valid
            experimental predictions are uploaded.
        </div>
        """
    )

    st.markdown(
        f"""
        <div class="panel">
            <div class="ptitle">
                Confusion Matrix
                <span>{esc(view) if cur else "Pending"}</span>
            </div>
            {body}
        </div>
        """,
        unsafe_allow_html=True
    )


# RESEARCH FRAMEWORK AND GBC
with c3:

    st.markdown("""
    <div class="panel">

        <div class="ptitle">
            Research Framework
        </div>

        <div class="fw">
            <b>Ecker et al. (2024)</b>
            <div>
                Existing system. MediaPipe Pose landmark analysis
                and CPR measurement evaluation.
            </div>
        </div>

        <div class="fw">
            <b>SmartCPR (2024)</b>
            <div>
                Existing system. MoveNet smartphone CPR assessment
                with measurement analysis and feedback.
            </div>
        </div>

        <div class="fw new">
            <b>Hybrid CPR System</b>
            <div>
                Proposed. MediaPipe Pose and Hand, Machine Learning,
                Rule-Based Assessment and Hybrid Decision Engine.
            </div>
        </div>

        <div class="gbc-box">

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
                Provisional. Pending dataset preparation,
                training, validation and computational testing.
            </div>

        </div>

        <div class="foot">
            NEMSU Lianga Campus | CPR Research Project | 2026
        </div>

    </div>
    """, unsafe_allow_html=True)


# =====================================================
# FOOTER
# =====================================================

st.caption(
    "Supplementary CPR research tool. "
    "Not a replacement for qualified CPR instructors, "
    "instrumented manikins, or official CPR guidelines."
)
