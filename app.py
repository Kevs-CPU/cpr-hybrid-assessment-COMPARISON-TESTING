import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="CPR Comparative Research Dashboard",
    page_icon="❤️",
    layout="wide"
)

st.title("AI-Assisted CPR Proper Execution Training System")

st.subheader("Comparative Research Dashboard")

st.write(
    "Research Project: Lianga, Surigao del Sur"
)

st.divider()

st.header("Research Framework")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("EXISTING SYSTEM 1")
    st.write("Ecker et al. (2024)")
    st.caption("MediaPipe Pose-based CPR assessment")

with col2:
    st.info("EXISTING SYSTEM 2")
    st.write("SmartCPR (2024)")
    st.caption("MoveNet-based CPR assessment")

with col3:
    st.success("PROPOSED SYSTEM")
    st.write("Our Hybrid CPR System")
    st.caption(
        "MediaPipe Pose + Hand + Machine Learning "
        "+ Rule-Based Assessment"
    )

st.divider()

st.header("Experimental Results")

st.warning(
    "No experimental results have been recorded yet. "
    "Actual results will appear after model testing."
)

st.header("Experimental Dataset")

uploaded_file = st.file_uploader(
    "Upload validated experimental predictions (CSV)",
    type=["csv"]
)

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)

    st.write("Uploaded dataset preview")
    st.dataframe(data, use_container_width=True)

st.divider()

st.header("Machine Learning Model")

st.write("Selected candidate: Gradient Boosting Classifier (GBC)")

st.caption(
    "The algorithm remains provisional until validation "
    "and computational testing are completed."
)

st.header("Experiment Tracking")

st.info(
    "MLflow integration will be connected after "
    "the hosted experiment tracking workspace is configured."
)

st.caption(
    "Supplementary CPR training and research evaluation tool. "
    "Not a replacement for qualified CPR instructors "
    "or instrumented manikin assessment."
)
