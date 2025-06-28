import streamlit as st
import numpy as np
import joblib

# Load semua resource
model = joblib.load("model.pkl")
encoder = joblib.load("encoder.pkl")
gejala_list = joblib.load("gejala.pkl")
gejala_translate = joblib.load("translated_gejala.pkl")
label_translate = joblib.load("translated_label.pkl")

# Judul dan deskripsi
st.set_page_config(page_title="Deteksi Penyakit", layout="centered")
st.title("🩺 Aplikasi Deteksi Penyakit")
st.markdown("Pilih gejala yang Anda alami, lalu klik tombol **Prediksi** untuk mengetahui kemungkinan penyakit.")

# Bagi jadi 2 kolom agar lebih enak dilihat
col1, col2 = st.columns(2)
selected_gejala = []

# Bikin checkbox gejala dalam 2 kolom
for i, g in enumerate(gejala_list):
    with (col1 if i % 2 == 0 else col2):
        if st.checkbox(gejala_translate[g], key=g):
            selected_gejala.append(g)

# Tombol prediksi
st.markdown("---")
if st.button("🔍 Prediksi Sekarang"):
    if not selected_gejala:
        st.warning("Silakan pilih minimal satu gejala terlebih dahulu.")
    else:
        input_array = np.zeros((1, len(gejala_list)))
        for g in selected_gejala:
            input_array[0, gejala_list.index(g)] = 1

        pred = model.predict(input_array)[0]
        label_en = encoder.classes_[pred]
        label_id = label_translate.get(label_en, label_en)

        st.success(f"🤖 Hasil Prediksi: **{label_id}**")

# st.markdown("---")
st.caption("Dibuat dengan ❤️ oleh Yaqin")
