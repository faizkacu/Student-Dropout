# =========================
# IMPORT LIBRARY
# =========================
import streamlit as st
import pandas as pd
import joblib
import numpy as np
import os

# =========================
# CONFIG PAGE
# =========================
st.set_page_config(
    page_title="Dropout Prediction",
    page_icon="📊",
    layout="wide"
)

# =========================
# SAFE LOAD ARTIFACTS
# =========================
@st.cache_resource
def load_artifacts():
    try:
        if not os.path.exists("model.pkl"):
            st.error("model.pkl tidak ditemukan")
            return None, None, None

        model = joblib.load("model.pkl")
        columns = joblib.load("columns.pkl")
        label_encoder = joblib.load("label_encoder.pkl")

        return model, columns, label_encoder

    except Exception as e:
        st.error("Gagal load model")
        st.text(str(e))
        return None, None, None

model, columns, le = load_artifacts()

# STOP jika model gagal load
if model is None:
    st.stop()

# =========================
# HEADER
# =========================
st.title("🎓 Student Dropout Prediction System")
st.markdown("Prediksi status siswa + deteksi risiko dropout")

st.divider()

# =========================
# INPUT USER
# =========================
st.subheader("📥 Input Data Siswa")

col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age at Enrollment", 15, 100, 20)
    admission_grade = st.number_input("Admission Grade", 0.0, 200.0, 120.0)
    sem1_grade = st.number_input("1st Semester Grade", 0.0, 20.0, 10.0)

with col2:
    sem2_grade = st.number_input("2nd Semester Grade", 0.0, 20.0, 10.0)
    scholarship = st.selectbox("Scholarship Holder", [0, 1])
    debtor = st.selectbox("Debtor", [0, 1])

# =========================
# BUILD INPUT DATA (SAFE)
# =========================
input_data = pd.DataFrame(0, index=[0], columns=columns)

# isi hanya jika kolom ada
def safe_set(col, value):
    if col in input_data.columns:
        input_data.loc[0, col] = value

safe_set('Age_at_enrollment', age)
safe_set('Admission_grade', admission_grade)
safe_set('Curricular_units_1st_sem_grade', sem1_grade)
safe_set('Curricular_units_2nd_sem_grade', sem2_grade)
safe_set('Scholarship_holder', scholarship)
safe_set('Debtor', debtor)

# =========================
# FEATURE ENGINEERING (SAFE)
# =========================
safe_set('grade_trend', sem2_grade - sem1_grade)
safe_set('avg_grade', (sem1_grade + sem2_grade) / 2)
safe_set('grade_ratio', sem2_grade / (sem1_grade + 1))

st.write("### 📊 Data Input")
st.dataframe(input_data)

# =========================
# PREDICTION
# =========================
if st.button("🔍 Prediksi"):
    
    try:
        proba = model.predict_proba(input_data)[0]

        # normalisasi
        proba = proba / proba.sum()

        max_prob = np.max(proba)
        pred_idx = np.argmax(proba)
        pred_label = le.inverse_transform([pred_idx])[0]

        dropout_idx = list(le.classes_).index("Dropout")
        dropout_prob = proba[dropout_idx]

        # =========================
        # DECISION LOGIC (IMPROVED)
        # =========================
        if max_prob < 0.5:
            pred_label = "Enrolled"

        if dropout_prob > 0.6:
            pred_label = "Dropout"

        # sanity rule
        if sem1_grade >= 15 and sem2_grade >= 15:
            pred_label = "Graduate"
            dropout_prob = min(dropout_prob, 0.1)

        st.divider()
        st.subheader("📢 Hasil Prediksi")

        # =========================
        # OUTPUT
        # =========================
        if pred_label == "Dropout":
            st.error("🔴 Berpotensi Dropout")
        elif pred_label == "Enrolled":
            st.warning("🟡 Perlu Monitoring")
        else:
            st.success("🟢 Berpotensi Lulus")

        st.metric("Prediksi Status", pred_label)

        # =========================
        # PROBABILITAS
        # =========================
        st.subheader("📊 Probabilitas")

        for i, label in enumerate(le.classes_):
            st.progress(float(proba[i]))
            st.write(f"{label}: {proba[i]*100:.2f}%")

        # =========================
        # RISIKO DROPOUT
        # =========================
        st.subheader("⚠️ Risiko Dropout")

        if dropout_prob > 0.7:
            st.error(f"Tinggi ({dropout_prob*100:.2f}%)")
        elif dropout_prob > 0.4:
            st.warning(f"Sedang ({dropout_prob*100:.2f}%)")
        else:
            st.success(f"Rendah ({dropout_prob*100:.2f}%)")

        st.caption(f"Confidence Model: {max_prob*100:.2f}%")

    except Exception as e:
        st.error("Error saat prediksi")
        st.text(str(e))

# =========================
# FOOTER
# =========================
st.divider()
st.caption("© 2026 - Student Dropout Prediction System")