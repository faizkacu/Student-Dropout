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
# LOAD ARTIFACTS
# =========================
@st.cache_resource
def load_artifacts():
    try:
        if not os.path.exists("model.pkl"):
            st.error("model.pkl tidak ditemukan")
            return None, None

        model = joblib.load("model.pkl")
        columns = joblib.load("columns.pkl")

        return model, columns

    except Exception as e:
        st.error("Gagal load model")
        st.text(str(e))
        return None, None

model, columns = load_artifacts()

if model is None:
    st.stop()

# =========================
# HEADER
# =========================
st.title("🎓 Student Dropout Prediction System")
st.markdown("Prediksi kemungkinan siswa **Dropout atau Tidak**")

st.divider()

# =========================
# SIDEBAR INFO
# =========================
st.sidebar.header("📌 Informasi Model")
st.sidebar.write("""
- Output: Probabilitas Dropout  
- Fokus: Deteksi Risiko  
- Model berbasis Machine Learning
""")

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
# BUILD INPUT DATA
# =========================
input_data = pd.DataFrame(0, index=[0], columns=columns)

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
# FEATURE ENGINEERING (HARUS SAMA DENGAN TRAINING)
# =========================
grade_trend = sem2_grade - sem1_grade
avg_grade = (sem1_grade + sem2_grade) / 2
grade_ratio = sem2_grade / (sem1_grade + 1)

safe_set('grade_trend', grade_trend)
safe_set('avg_grade', avg_grade)
safe_set('grade_ratio', grade_ratio)

# 🔥 FEATURE TAMBAHAN (WAJIB)
safe_set('high_performance', int(avg_grade >= 14))
safe_set('low_performance', int(avg_grade < 10))
safe_set('consistent_good', int(sem1_grade >= 14 and sem2_grade >= 14))
safe_set('grade_improving', int(grade_trend > 0))
safe_set('financial_risk', int(debtor == 1 and scholarship == 0))

st.write("### 📊 Data Input")
st.dataframe(input_data)

# =========================
# PREDICTION
# =========================
if st.button("🔍 Prediksi"):

    try:
        # Probabilitas dropout
        dropout_prob = model.predict_proba(input_data)[0][1]

        # =========================
        # 🔥 DYNAMIC THRESHOLD
        # =========================
        threshold = 0.65

        # jika performa sangat baik → lebih ketat
        if avg_grade >= 15:
            threshold = 0.75

        # =========================
        # 🔥 RULE-BASED CORRECTION
        # =========================
        # sanity logic dunia nyata
        if sem1_grade >= 15 and sem2_grade >= 15:
            dropout_prob *= 0.3  # turunkan risiko drastis

        if scholarship == 1 and avg_grade >= 14:
            dropout_prob *= 0.5

        prediction = 1 if dropout_prob >= threshold else 0

        st.divider()
        st.subheader("📢 Hasil Prediksi")

        # =========================
        # OUTPUT
        # =========================
        if prediction == 1:
            st.error("🔴 Berpotensi Dropout")
        else:
            st.success("🟢 Tidak Dropout (Berpotensi Lulus)")

        # =========================
        # METRIC
        # =========================
        st.metric("Probabilitas Dropout", f"{dropout_prob*100:.2f}%")

        # =========================
        # VISUAL
        # =========================
        st.subheader("📊 Visualisasi Risiko")
        st.progress(float(dropout_prob))

        # =========================
        # INTERPRETASI
        # =========================
        st.subheader("🧠 Interpretasi Risiko")

        if dropout_prob > 0.75:
            st.error("Risiko sangat tinggi → intervensi segera")
        elif dropout_prob > 0.5:
            st.warning("Risiko sedang → perlu monitoring")
        else:
            st.success("Risiko rendah → kondisi aman")

        # =========================
        # CONFIDENCE
        # =========================
        confidence = max(dropout_prob, 1 - dropout_prob)
        st.caption(f"Tingkat keyakinan model: {confidence*100:.2f}%")

    except Exception as e:
        st.error("Terjadi error saat prediksi")
        st.text(str(e))

# =========================
# FOOTER
# =========================
st.divider()
st.caption("© 2026 - Student Dropout Prediction System")