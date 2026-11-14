
import streamlit as st
import pandas as pd

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="CPR Comparative Research Dashboard",
    page_icon="❤️",
    layout="wide"
)

# ==========================================
# HEADER
# ==========================================

st.title("AI-Assisted CPR Proper Execution Training System")

st.subheader("Comparative Research and Experimental Dashboard")

st.caption(
    "Undergraduate Thesis | BS Computer Science | "
    "Lianga, Surigao del Sur"
)

st.divider()

# ==========================================
# RESEARCH FRAMEWORK
# ==========================================

st.header("Research Framework")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("EXISTING SYSTEM 1")
    st.subheader("Ecker et al. (2024)")
    st.write("MediaPipe Pose-Based CPR Assessment")
    st.caption(
        "Video-based body landmark analysis "
        "and CPR measurement assessment."
    )

with col2:
    st.info("EXISTING SYSTEM 2")
    st.subheader("SmartCPR (2024)")
    st.write("MoveNet-Based CPR Assessment")
    st.caption(
        "Smartphone-based pose estimation "
        "and CPR performance assessment."
    )

with col3:
    st.success("PROPOSED SYSTEM")
    st.subheader("Our Hybrid CPR System")
    st.write(
        "MediaPipe Pose + MediaPipe Hand"
    )
    st.caption(
        "Machine Learning Classification + "
        "Rule-Based Assessment + Hybrid Decision Engine."
    )

st.divider()

# ==========================================
# EXPERIMENTAL STATUS
# ==========================================

st.header("Experimental Status")

status1, status2, status3 = st.columns(3)

with status1:
    st.metric("Existing Systems", "2")

with status2:
    st.metric("Proposed System", "1")

with status3:
    st.metric("Experimental Results", "Pending")

st.warning(
    "No actual experimental results are available yet. "
    "Performance metrics will only be displayed after "
    "valid testing data have been collected."
)

st.divider()

# ==========================================
# MACHINE LEARNING APPROACH
# ==========================================

st.header("Machine Learning Classification")

st.subheader("Gradient Boosting Classifier (GBC)")

st.write(
    "Gradient Boosting Classifier is the provisional "
    "Machine Learning candidate for classifying selected "
    "CPR movement patterns using extracted body and "
    "hand movement features."
)

st.caption(
    "The final algorithm selection will depend on "
    "dataset suitability, validation performance, "
    "and computational requirements."
)

st.divider()

# ==========================================
# EXPERIMENTAL DATASET UPLOAD
# ==========================================

st.header("Experimental Dataset")

st.write(
    "Upload validated experimental predictions "
    "to inspect the dataset used for system comparison."
)

uploaded_file = st.file_uploader(
    "Upload experimental predictions (CSV)",
    type=["csv"]
)

if uploaded_file is not None:

    try:
        data = pd.read_csv(uploaded_file)

        if data.empty:
            st.error("The uploaded CSV file contains no records.")

        else:
            st.success("Dataset uploaded successfully.")

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Total Records",
                    len(data)
                )

            with col2:
                st.metric(
                    "Total Columns",
                    len(data.columns)
                )

            st.subheader("Dataset Preview")

            st.dataframe(
                data,
                use_container_width=True
            )

            required_columns = [
                "participant_id",
                "clip_id",
                "system",
                "actual_label",
                "predicted_label"
            ]

            missing_columns = [
                col for col in required_columns
                if col not in data.columns
            ]

            if not missing_columns:
                st.success(
                    "Required experimental comparison columns detected."
                )
            else:
                st.warning(
                    "Missing columns: "
                    + ", ".join(missing_columns)
                    + ". Classification evaluation is not yet available."
                )

    except pd.errors.EmptyDataError:
        st.error("The uploaded CSV file is empty.")

    except pd.errors.ParserError:
        st.error("Unable to read the CSV structure. Check the file format.")

    except Exception as error:
        st.error(f"Dataset processing error: {error}")

else:
    st.info(
        "No experimental dataset uploaded. "
        "Results will appear after actual testing."
    )

st.divider()

# ==========================================
# EXPERIMENTAL EVALUATION
# ==========================================

st.header("Planned Evaluation Metrics")

metric1, metric2, metric3, metric4 = st.columns(4)

with metric1:
    st.write("Accuracy")

with metric2:
    st.write("Precision")

with metric3:
    st.write("Recall")

with metric4:
    st.write("F1-Score")

st.caption(
    "These metrics will be calculated after independent "
    "model testing using evaluator-approved reference labels."
)

st.divider()

# ==========================================
# MLflow INTEGRATION
# ==========================================

st.header("Machine Learning Experiment Tracking")

st.info(
    "MLflow integration is pending. "
    "The hosted tracking service will record model parameters, "
    "evaluation metrics, and experiment runs after configuration."
)

st.divider()

# ==========================================
# RESEARCH LIMITATIONS
# ==========================================

st.header("Research Scope and Limitations")

st.write(
    "The proposed application is designed as a supplementary "
    "CPR training and assessment tool for selected observable "
    "movements during simulated adult chest-compression practice."
)

st.write(
    "The system does not replace qualified CPR instructors, "
    "practical assessment using an appropriate instrumented "
    "manikin, or official CPR guidelines."
)

# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "AI-Assisted CPR Proper Execution Training System | "
    "NEMSU - Lianga Campus | BS Computer Science | 2026"
)
