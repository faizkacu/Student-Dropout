# =========================
# IMPORT LIBRARY
# =========================
import streamlit as st
import pandas as pd
import joblib
import numpy as np

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
    model = joblib.load('model.pkl')
    columns = joblib.load('columns.pkl')
    label_encoder = joblib.load('label_encoder.pkl')
    return model, columns, label_encoder

model, columns, le = load_artifacts()

# =========================
# HEADER
# =========================
st.title("🎓 Student Dropout Prediction System")
st.markdown("Prediksi status siswa + deteksi risiko dropout berbasis Machine Learning")

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
# BUILD INPUT DATA
# =========================
input_data = pd.DataFrame([0]*len(columns)).T
input_data.columns = columns

# isi fitur utama
input_data.loc[0, 'Age_at_enrollment'] = age
input_data.loc[0, 'Admission_grade'] = admission_grade
input_data.loc[0, 'Curricular_units_1st_sem_grade'] = sem1_grade
input_data.loc[0, 'Curricular_units_2nd_sem_grade'] = sem2_grade
input_data.loc[0, 'Scholarship_holder'] = scholarship
input_data.loc[0, 'Debtor'] = debtor

# =========================
# FEATURE ENGINEERING
# =========================
input_data.loc[0, 'grade_trend'] = sem2_grade - sem1_grade
input_data.loc[0, 'avg_grade'] = (sem1_grade + sem2_grade) / 2
input_data.loc[0, 'grade_ratio'] = sem2_grade / (sem1_grade + 1)

st.write("### 📊 Data Input")
st.dataframe(input_data)

# =========================
# PREDICTION
# =========================
if st.button("🔍 Prediksi"):
    
    try:
        proba = model.predict_proba(input_data)[0]

        # =========================
        # NORMALISASI PROBABILITAS
        # =========================
        proba = proba / proba.sum()

        max_prob = np.max(proba)
        pred_idx = np.argmax(proba)
        pred_label = le.inverse_transform([pred_idx])[0]

        dropout_idx = list(le.classes_).index("Dropout")
        dropout_prob = proba[dropout_idx]

        # =========================
        # SMART DECISION LOGIC (FIXED)
        # =========================
        CONF_THRESHOLD = 0.5

        # fallback jika tidak yakin
        if max_prob < CONF_THRESHOLD:
            pred_label = "Enrolled"

        # override jika dropout tinggi
        if dropout_prob > 0.6:
            pred_label = "Dropout"

        # sanity check (WAJIB)
        if sem1_grade >= 15 and sem2_grade >= 15:
            pred_label = "Graduate"
            dropout_prob = min(dropout_prob, 0.1)  # 🔥 fix kontradiksi

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
        st.subheader("📊 Probabilitas Model")

        for i, label in enumerate(le.classes_):
            st.progress(float(proba[i]))
            st.write(f"{label}: {proba[i]*100:.2f}%")

        # =========================
        # RISIKO DROPOUT
        # =========================
        st.subheader("⚠️ Risiko Dropout")

        if dropout_prob > 0.7:
            st.error(f"Tinggi ({dropout_prob*100:.2f}%) → Intervensi segera")
        elif dropout_prob > 0.4:
            st.warning(f"Sedang ({dropout_prob*100:.2f}%) → Monitoring")
        else:
            st.success(f"Rendah ({dropout_prob*100:.2f}%)")

        # =========================
        # CONFIDENCE
        # =========================
        st.caption(f"Tingkat keyakinan model: {max_prob*100:.2f}%")

    except Exception as e:
        st.error("Terjadi error saat prediksi")
        st.text(str(e))

# =========================
# FOOTER
# =========================
st.divider()
st.caption("© 2026 - Student Dropout Prediction System | Machine Learning")