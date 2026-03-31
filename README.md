# Proyek Akhir: Menyelesaikan Permasalahan Perusahaan Edutech

## Business Understanding
Jaya jaya institute menghadapi tantangan utama berupa tingginya angka dropout siswa, yang berdampak langsung pada penurunan revenue, efektivitas program pembelajaran, serta reputasi institusi.

Dropout tidak hanya menyebabkan kehilangan pelanggan, tetapi juga menunjukkan adanya masalah dalam engagement, kualitas pembelajaran, atau pengalaman pengguna secara keseluruhan.

### Permasalahan Bisnis
Berikut permasalahan utama yang ingin diselesaikan:

- Tingginya tingkat dropout siswa tanpa adanya sistem prediksi dini
- Kurangnya insight terkait faktor-faktor yang menyebabkan siswa dropout
- Tidak adanya sistem berbasis data untuk membantu pengambilan keputusan
- Kesulitan dalam menentukan prioritas intervensi terhadap siswa berisiko tinggi

### Cakupan Proyek
Proyek ini mencakup:
- Data Understanding & Exploratory Data Analysis (EDA)
- Data Preprocessing (cleaning, encoding, scaling, handling imbalance)
- Pembangunan model machine learning untuk klasifikasi dropout
- Evaluasi performa model
- Pembuatan prototype berbasis Streamlit
- Penyusunan rekomendasi berbasis data

### Persiapan

Sumber data: https://github.com/dicodingacademy/dicoding_dataset/tree/main/students_performance

Setup environment:
```
python -m venv venv
venv\Scripts\activate
pip install -r model-requirements.txt
```

## Business Dashboard
Jelaskan tentang business dashboard yang telah dibuat. Jika ada, sertakan juga link untuk mengakses dashboard tersebut.

Link untuk mengakses dashboard: https://lookerstudio.google.com/reporting/d01d46a0-84e0-4152-a629-5ececb33a7f6 

## Menjalankan Sistem Machine Learning
Jelaskan cara menjalankan protoype sistem machine learning yang telah dibuat. Selain itu, sertakan juga link untuk mengakses prototype tersebut.

```
-> Jalankan perintah berikut untuk menjalankan prototype (local):
streamlit run app.py
-> Akses prototype melalui link berikut (deploy):
student-dropout-faizkacu.streamlit.app
```

## Conclusion
Ada beberapa kesimpulan yang saya dapat tarik dari proyek ini:
- Model terbaik adalah Logistic Regression dengan performa tinggi (accuracy 94.35%, recall 90.84%, F1-score 92.63%, ROC-AUC 0.97). Fitur paling berpengaruh adalah avg_grade, grade_trend, dan indikator performa seperti high_performance, yang menegaskan bahwa faktor akademik dominan dalam prediksi dropout.
- Model terbaik adalah Logistic Regression dengan performa tinggi (accuracy 94.35%, recall 90.84%, F1-score 92.63%, ROC-AUC 0.97). Fitur paling berpengaruh adalah avg_grade, grade_trend, dan indikator performa seperti high_performance, yang menegaskan bahwa faktor akademik dominan dalam prediksi dropout.

### Rekomendasi Action Items
Berikan beberapa rekomendasi action items yang harus dilakukan perusahaan guna menyelesaikan permasalahan atau mencapai target mereka.
- Mahasiswa dengan rata-rata nilai rendah (average_score < 10) memiliki risiko dropout yang lebih tinggi. Institusi harus mengembangkan program intervensi akademik, seperti bimbingan belajar tambahan, workshop keterampilan belajar, atau sesi konsultasi dengan dosen pembimbing untuk membantu mahasiswa meningkatkan performa akademik mereka.
- Hasil analisis menunjukkan bahwa mahasiswa dengan status menunggak (Debtor = 1) dan tidak menerima beasiswa (Scholarship_holder = 0) memiliki risiko dropout lebih tinggi, bahkan ketika performa akademik tidak terlalu buruk. Oleh karena itu, institusi perlu mengembangkan sistem identifikasi otomatis berbasis data keuangan untuk mendeteksi mahasiswa dalam kondisi ini, kemudian memberikan bantuan seperti beasiswa darurat atau skema cicilan fleksibel. Prioritas diberikan pada mahasiswa yang juga mengalami penurunan akademik, karena kombinasi faktor finansial dan akademik terbukti meningkatkan risiko dropout secara signifikan.
