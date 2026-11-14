import os
import html
import pandas as pd
import streamlit as st

import html

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="CPR Research Dashboard",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

REQUIRED = ["participant_id", "clip_id", "system", "actual_label", "predicted_label"]

# ==========================================
# STYLE: MLflow-inspired striped gradient, one-screen layout
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700;800&display=swap');

html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    height: 100vh; overflow: hidden !important;
    font-family: 'DM Sans', 'Segoe UI', sans-serif !important;
}
.stApp {
    color: #fff !important;
    background:
      linear-gradient(180deg, rgba(13,17,23,0) 0%, rgba(13,17,23,0) 22%,
                      rgba(13,17,23,.88) 62%, #0d1117 100%),
      repeating-linear-gradient(90deg, rgba(0,0,0,.16) 0 14px, rgba(255,255,255,.04) 14px 28px),
      linear-gradient(90deg, #7a0e48 0%, #c4170f 40%, #d8230f 52%, #6d4fa3 72%, #1f8cf2 100%);
}
[data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"],
footer { display: none !important; }
.block-container { max-width: 1500px; padding: .8rem 2rem .4rem !important; }
[data-testid="stVerticalBlock"] { gap: .55rem; }
[data-testid="stElementContainer"], [data-testid="stMarkdownContainer"] { margin: 0; }

/* header */
.eyebrow { font-size: .78rem; font-weight: 500; color: rgba(255,255,255,.78); }
.title { font-size: 1.75rem; font-weight: 800; letter-spacing: -.03em; line-height: 1.15; }
.sub { font-size: .82rem; color: rgba(255,255,255,.78); margin-top: 2px; }

/* uploader */
[data-testid="stFileUploader"] * { color: #fff !important; }
[data-testid="stFileUploader"] section {
    background: rgba(13,17,23,.55) !important; border: 1.5px dashed rgba(255,255,255,.4) !important;
    border-radius: 12px !important; padding: .4rem .7rem !important;
}
[data-testid="stFileUploader"] small { display: none; }
[data-testid="stFileUploader"] button { background: #fff !important; border: 0 !important;
    border-radius: 8px !important; font-weight: 700 !important; }
[data-testid="stFileUploader"] button * { color: #0d1117 !important; }
[data-testid="stFileUploaderFile"] { padding: 0 !important; min-height: 0 !important; }

/* system switcher */
[data-testid="stRadio"] [role="radiogroup"] { gap: .35rem; justify-content: flex-end; flex-wrap: nowrap; }
[data-testid="stRadio"] label { background: rgba(13,17,23,.55); border: 1px solid rgba(255,255,255,.25);
    border-radius: 999px; padding: 2px 14px; margin: 0; cursor: pointer; }
[data-testid="stRadio"] label > div:first-child { display: none; }
[data-testid="stRadio"] label p { color: #fff !important; font-size: .8rem; font-weight: 500; }
[data-testid="stRadio"] label:has(input:checked) { background: #fff; }
[data-testid="stRadio"] label:has(input:checked) p { color: #0d1117 !important; font-weight: 700; }

/* status pills */
.pills { display: flex; gap: .4rem; flex-wrap: nowrap; overflow: hidden; align-items: center; height: 32px; }
.pill { font-size: .78rem; padding: 4px 12px; border-radius: 999px; white-space: nowrap;
    background: rgba(13,17,23,.55); border: 1px solid rgba(255,255,255,.22); }
.pill.ok { border-color: #5be39a; color: #b9ffd9; }
.pill.bad { border-color: #ff8a80; color: #ffd0cc; }

/* cards */
.card, .panel { background: rgba(13,17,23,.58); backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px); border: 1px solid rgba(255,255,255,.16); border-radius: 14px; }
.kpi { padding: 10px 16px; height: 84px; }
.kpi .v { font-size: 1.8rem; font-weight: 800; letter-spacing: -.03em; line-height: 1.1; }
.kpi .v.pending { color: rgba(255,255,255,.55); font-size: 1.4rem; padding-top: 5px; }
.kpi .l { font-size: .8rem; font-weight: 700; }
.kpi .s { font-size: .72rem; color: rgba(255,255,255,.65); white-space: nowrap; overflow: hidden; }

.panel { padding: 12px 16px; height: calc(100vh - 292px); min-height: 230px; overflow: hidden; }
.ptitle { font-size: .98rem; font-weight: 800; margin-bottom: 8px; }
.ptitle span { font-size: .72rem; font-weight: 400; color: rgba(255,255,255,.65); margin-left: 8px; }
.empty { color: rgba(255,255,255,.6); font-size: .85rem; padding-top: 14%; text-align: center; }

/* comparison bars */
.sys { padding: 6px 10px; margin-bottom: 6px; border-radius: 10px; border: 1px solid transparent; }
.sys.hl { background: rgba(255,255,255,.08); border-color: rgba(255,255,255,.4); }
.sh { display: flex; justify-content: space-between; font-size: .84rem; margin-bottom: 3px; }
.sh span { color: rgba(255,255,255,.65); font-size: .74rem; }
.brow { display: grid; grid-template-columns: 62px 1fr 48px; align-items: center; gap: 8px; height: 17px; }
.bl, .bv { font-size: .72rem; color: rgba(255,255,255,.8); }
.bv { text-align: right; font-weight: 700; color: #fff; }
.track { height: 7px; border-radius: 99px; background: rgba(255,255,255,.12); overflow: hidden; }
.fill { height: 100%; border-radius: 99px; background: linear-gradient(90deg, #e0261a, #8a3fb0, #2a8cf5); }

/* confusion matrix */
.cm { display: grid; gap: 4px; }
.cm-h { font-size: .72rem; color: rgba(255,255,255,.75); text-align: center; align-self: center;
    overflow: hidden; text-overflow: ellipsis; }
.cm-c { min-height: 38px; border-radius: 8px; display: flex; align-items: center;
    justify-content: center; font-weight: 800; font-size: .95rem; }
.note { font-size: .72rem; color: rgba(255,255,255,.6); margin-top: 8px; }

/* framework */
.fw { padding: 8px 12px; border-radius: 10px; margin-bottom: 7px; background: rgba(255,255,255,.06);
    border: 1px solid rgba(255,255,255,.12); }
.fw.new { background: rgba(255,255,255,.13); border-color: rgba(255,255,255,.5); }
.fw b { font-size: .86rem; } .fw div { font-size: .73rem; color: rgba(255,255,255,.72); line-height: 1.35; }
.foot { font-size: .68rem; color: rgba(255,255,255,.5); margin-top: 4px; }

@media (max-height: 760px) {
  .title { font-size: 1.4rem; } .kpi { height: 72px; padding: 6px 14px; }
  .kpi .v { font-size: 1.45rem; } .cm-c { min-height: 30px; } .panel { height: calc(100vh - 268px); }
}
@media (max-width: 900px) {
  html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
      height: auto; overflow: auto !important; }
  .panel { height: auto; }
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# HELPERS
# ==========================================
def esc(x):
    return html.escape(str(x))


def pct(v):
    return f"{v * 100:.1f}%"


def evaluate(df):
    """Accuracy plus macro-averaged precision, recall and F1."""
    y, p = df["actual_label"], df["predicted_label"]
    labels = sorted(set(y) | set(p))
    cm = pd.crosstab(y, p).reindex(index=labels, columns=labels, fill_value=0)
    tp = pd.Series(cm.values.diagonal(), index=labels)
    prec = (tp / cm.sum(axis=0)).fillna(0)
    rec = (tp / cm.sum(axis=1)).fillna(0)
    f1 = (2 * prec * rec / (prec + rec)).fillna(0)
    return {"n": len(df), "acc": float((y == p).mean()), "prec": float(prec.mean()),
            "rec": float(rec.mean()), "f1": float(f1.mean()), "cm": cm}


def kpi(label, value, sub):
    val = f'<div class="v">{value}</div>' if value else '<div class="v pending">Pending</div>'
    return f'<div class="card kpi"><div class="l">{label}</div>{val}<div class="s">{sub}</div></div>'


def bar(name, v):
    return (f'<div class="brow"><span class="bl">{name}</span><div class="track">'
            f'<div class="fill" style="width:{v * 100:.1f}%"></div></div><span class="bv">{pct(v)}</span></div>')


def comparison(results, view):
    out = ""
    for name, r in results.items():
        hl = " hl" if name == view else ""
        out += (f'<div class="sys{hl}"><div class="sh"><b>{esc(name)}</b><span>{r["n"]} records</span></div>'
                + bar("Accuracy", r["acc"]) + bar("Precision", r["prec"])
                + bar("Recall", r["rec"]) + bar("F1-score", r["f1"]) + "</div>")
    return out


def confusion(cm):
    mx = max(int(cm.values.max()), 1)
    cells = '<div class="cm-h"></div>' + "".join(f'<div class="cm-h">{esc(c)}</div>' for c in cm.columns)
    for a in cm.index:
        cells += f'<div class="cm-h">{esc(a)}</div>'
        for p in cm.columns:
            v = int(cm.loc[a, p])
            alpha = 0.06 if v == 0 else 0.18 + 0.75 * v / mx
            rgb = "31,140,242" if a == p else "224,38,26"
            cells += f'<div class="cm-c" style="background:rgba({rgb},{alpha:.2f})">{v}</div>'
    return (f'<div class="cm" style="grid-template-columns:auto repeat({len(cm.columns)},1fr)">{cells}</div>'
            '<div class="note">Rows are actual labels, columns are predicted labels. '
            'Blue cells are correct, red cells are errors.</div>')


# ==========================================
# HEADER + UPLOADER
# ==========================================
head, up_col = st.columns([1.5, 1], gap="large")
with head:
    st.markdown("""
<div class="eyebrow">North Eastern Mindanao State University, Lianga Campus</div>
<div class="title">AI-Assisted CPR Proper Execution Training System</div>
<div class="sub">Comparative research and experimental dashboard for BS Computer Science</div>
""", unsafe_allow_html=True)
with up_col:
    uploaded = st.file_uploader("Experimental predictions CSV", type=["csv"],
                                label_visibility="collapsed")

# ==========================================
# LOAD + COMPUTE (automatic on upload)
# ==========================================
df, results, pills = None, {}, ""
if uploaded is None:
    pills = '<span class="pill">Upload the predictions CSV and every result appears here automatically</span>'
else:
    try:
        raw = pd.read_csv(uploaded)
        raw.columns = [str(c).strip().lower() for c in raw.columns]
        missing = [c for c in REQUIRED if c not in raw.columns]
        if raw.empty:
            pills = '<span class="pill bad">The CSV has no records</span>'
        elif missing:
            pills = f'<span class="pill bad">Missing columns: {esc(", ".join(missing))}</span>'
        else:
            df = raw.dropna(subset=REQUIRED).copy()
            for c in ("actual_label", "predicted_label"):
                df[c] = df[c].astype(str).str.strip().str.lower()
            df["system"] = df["system"].astype(str).str.strip()
            if df.empty:
                df = None
                pills = '<span class="pill bad">Every row has an empty required value</span>'
    except (pd.errors.EmptyDataError, pd.errors.ParserError, UnicodeDecodeError):
        pills = '<span class="pill bad">Cannot read this file. Check that it is a valid CSV</span>'

view = "All systems"
sel_col = None
if df is not None:
    systems = list(df["system"].unique())
    results = {s: evaluate(g) for s, g in df.groupby("system", sort=False)}
    results["All systems"] = evaluate(df)
    options = ["All systems"] + systems
    hybrid = next((s for s in systems if "hybrid" in s.lower()), None)
    default = options.index(hybrid) if hybrid else 0
    pills = (f'<span class="pill ok">✓ {esc(uploaded.name)}</span>'
             f'<span class="pill">{len(df)} records</span>'
             f'<span class="pill">{df["participant_id"].nunique()} participants</span>'
             f'<span class="pill">{df["clip_id"].nunique()} clips</span>'
             f'<span class="pill">{len(systems)} systems</span>')

strip, switch = st.columns([1.5, 1], gap="large")
with strip:
    st.markdown(f'<div class="pills">{pills}</div>', unsafe_allow_html=True)
with switch:
    if df is not None:
        view = st.radio("System", options, index=default, horizontal=True,
                        label_visibility="collapsed")

cur = results.get(view)

# ==========================================
# KPI ROW
# ==========================================
sub = f"{esc(view)}, macro average" if cur else "Waiting for experimental data"
k = st.columns(5, gap="small")
cards = [("Accuracy", pct(cur["acc"]) if cur else None), ("Precision", pct(cur["prec"]) if cur else None),
         ("Recall", pct(cur["rec"]) if cur else None), ("F1-score", pct(cur["f1"]) if cur else None),
         ("Records evaluated", str(cur["n"]) if cur else None)]
for col, (label, value) in zip(k, cards):
    with col:
        st.markdown(kpi(label, value, sub if label != "Records evaluated" else esc(view) if cur else sub),
                    unsafe_allow_html=True)

# ==========================================
# MAIN PANELS
# ==========================================
c1, c2, c3 = st.columns([1.4, 1, 0.95], gap="small")

with c1:
    body = comparison({s: r for s, r in results.items() if s != "All systems"}, view) if cur \
        else '<div class="empty">System comparison will appear after the CSV is uploaded.</div>'
    st.markdown(f'<div class="panel"><div class="ptitle">System comparison'
                f'<span>Higher is better</span></div>{body}</div>', unsafe_allow_html=True)

with c2:
    body = confusion(cur["cm"]) if cur \
        else '<div class="empty">The confusion matrix will appear after the CSV is uploaded.</div>'
    st.markdown(f'<div class="panel"><div class="ptitle">Confusion matrix'
                f'<span>{esc(view) if cur else ""}</span></div>{body}</div>', unsafe_allow_html=True)

with c3:
    st.markdown("""
<div class="panel"><div class="ptitle">Research framework</div>
<div class="fw"><b>Ecker et al. (2024)</b><div>Existing system. MediaPipe Pose landmark analysis and CPR measurement evaluation.</div></div>
<div class="fw"><b>SmartCPR (2024)</b><div>Existing system. MoveNet smartphone CPR assessment with measurement analysis and feedback.</div></div>
<div class="fw new"><b>Hybrid CPR System</b><div>Proposed. MediaPipe Pose and Hand, machine learning, rule-based assessment and a hybrid decision engine.</div></div>
<div class="fw"><b>Gradient Boosting Classifier</b><div>Provisional model. MLflow experiment tracking: not connected.</div></div>
<div class="foot">NEMSU Lianga Campus, AI-Assisted CPR Research Project, 2026</div></div>
""", unsafe_allow_html=True)


# ==================================================
# HOSTED MLFLOW CONNECTION TEST
# ==================================================

def test_mlflow_connection():

    required_secrets = [
        "MLFLOW_TRACKING_URI",
        "MLFLOW_TRACKING_USERNAME",
        "MLFLOW_TRACKING_PASSWORD"
    ]

    missing = [
        key for key in required_secrets
        if key not in st.secrets
    ]

    if missing:
        raise ValueError(
            "Missing Streamlit Secrets: " + ", ".join(missing)
        )

    # Load private credentials from Streamlit Secrets
    os.environ["MLFLOW_TRACKING_URI"] = str(
        st.secrets["MLFLOW_TRACKING_URI"]
    )

    os.environ["MLFLOW_TRACKING_USERNAME"] = str(
        st.secrets["MLFLOW_TRACKING_USERNAME"]
    )

    os.environ["MLFLOW_TRACKING_PASSWORD"] = str(
        st.secrets["MLFLOW_TRACKING_PASSWORD"]
    )

    # Import after setting credentials
    import mlflow
    from mlflow.tracking import MlflowClient

    tracking_uri = os.environ["MLFLOW_TRACKING_URI"]

    mlflow.set_tracking_uri(tracking_uri)

    client = MlflowClient(
        tracking_uri=tracking_uri
    )

    # Verify access to the tracking server
    client.search_experiments(max_results=1)

    # Create a separate connection-check experiment
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

    # Log a connection check only.
    # No model accuracy or CPR evaluation metrics.
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


# ==================================================
# MLFLOW DASHBOARD CONNECTION PANEL
# ==================================================

st.divider()

st.markdown(
    '<div class="section-title">MLflow Experiment Tracking</div>',
    unsafe_allow_html=True
)

st.caption(
    "Connect the live CPR dashboard to the hosted "
    "DagsHub MLflow tracking server."
)

if st.button(
    "Test MLflow Connection",
    type="primary",
    use_container_width=True
):

    with st.spinner(
        "Connecting to DagsHub MLflow..."
    ):

        try:
            run_id = test_mlflow_connection()

            st.success(
                "Successfully connected to DagsHub MLflow! "
                "Connection-check run recorded."
            )

            st.code(
                f"Connection-check Run ID: {run_id}"
            )

            st.markdown(
                "[Open DagsHub MLflow Tracking UI]"
                "(https://dagshub.com/Kevs-CPU/"
                "cpr-hybrid-assessment-COMPARISON-TESTING.mlflow)"
            )

            st.info(
                "This is a connection test only. "
                "No CPR model was trained and no performance "
                "metrics were recorded."
            )

        except Exception as error:

            st.error(
                f"MLflow connection failed: "
                f"{type(error).__name__}: {error}"
            )

            st.warning(
                "Check your tracking URI, credentials, "
                "repository permissions, and deployment logs."
            )

