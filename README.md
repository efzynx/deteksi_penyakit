
# 🩺 Aplikasi Deteksi Penyakit Berbasis Gejala

Aplikasi ini memanfaatkan Machine Learning untuk memprediksi kemungkinan penyakit berdasarkan gejala yang kamu alami.  
Dilengkapi dengan terjemahan gejala dan hasil prediksi ke Bahasa Indonesia agar lebih user-friendly dan bisa digunakan siapa saja.

## 🚀 Fitur Utama

- ✅ Deteksi penyakit berdasarkan input gejala
- 🌐 Antarmuka web interaktif dengan **Streamlit**
- 🇮🇩 Terjemahan otomatis gejala dan hasil ke Bahasa Indonesia
- ⚡ Model Random Forest dengan akurasi tinggi
- 📦 Sudah dilatih dan bisa langsung digunakan

## 📸 Tampilan Aplikasi

![demo-app](https://raw.githubusercontent.com/efzynx/deteksi_penyakit/refs/heads/main/src/preview.jpg)

## 🧠 Teknologi yang Digunakan

- Python
- Scikit-learn
- Streamlit
- Deep-Translator
- Pandas & Numpy
- Joblib

## 📁 Struktur Folder

```
.
├── model.pkl
├── encoder.pkl
├── gejala.pkl
├── translated_gejala.pkl
├── translated_label.pkl
├── disease_app.py
├── RF_DeteksiPenyakit.ipynb
└── README.md
```

## ⚙️ Cara Menjalankan Aplikasi

### 1. Clone repositori ini:

```bash
git clone https://github.com/efzynx/deteksi_penyakit.git
cd repo-nya
```

### 2. Install dependencies:

Pastikan sudah menggunakan Python 3.10+ dan virtual environment aktif

```bash
pip install -r requirements.txt
```

### 3. Jalankan aplikasi Streamlit:

```bash
streamlit run disease_app.py
```

### 4. Buka di browser:
- Local: http://localhost:8501
- Network: http://<ip-lokal-kamu>:8501

## 🧪 Contoh Gejala

- Nyeri perut
- Demam tinggi
- Pusing
- Mual
- Batuk berdahak

> Pilih gejala melalui checkbox dan tekan tombol **Prediksi**.

## 📌 Catatan

- Model sudah dilatih di Google Colab dan disimpan ke file `.pkl`.
- Untuk performa terbaik, pastikan koneksi internet stabil saat menggunakan translator di tahap awal (opsional).
- Semua hasil prediksi hanya sebagai estimasi dan **bukan pengganti diagnosis dokter profesional**.

## 🧑‍💻 Kontributor

- **Fauzan** — [LinkedIn](https://linkedin.com/in/efzyn) | [GitHub](https://github.com/efzynx)

## 📜 Lisensi

MIT License © 2025
