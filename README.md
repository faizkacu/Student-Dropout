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
pip install -r requirements.txt
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
- Beberapa faktor memiliki pengaruh signifikan terhadap kemungkinan dropout, yang dapat diidentifikasi melalui feature importance.
- Model machine learning berhasil mengidentifikasi siswa berisiko dropout dengan performa yang baik pada metrik-metrik yang ditentukan.
- Pada hasil evaluasi model, terlihat bahwa model memiliki akurasi yang cukup tinggi, namun masih terdapat ruang untuk perbaikan terutama dalam hal recall untuk kelas dropout.

### Rekomendasi Action Items
Berikan beberapa rekomendasi action items yang harus dilakukan perusahaan guna menyelesaikan permasalahan atau mencapai target mereka.
- Tingkatkan engagement melalui Reward kepada mahasiswa, perbaikan kurikulum dan Reminder aktivitas
- Fokus pada jurusan-jurusan mahasiswa yang tinggi dropout-nya
- Berikan intervensi personal untuk siswa berisiko tinggi:
