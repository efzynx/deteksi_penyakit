import streamlit as st
import numpy as np
import joblib
import datetime

# --- FUNGSI UNTUK MEMUAT RESOURCE ---
@st.cache_resource
def load_resources():
    model = joblib.load("model.pkl")
    encoder = joblib.load("encoder.pkl")
    gejala_list = joblib.load("gejala.pkl")
    gejala_translate = joblib.load("translated_gejala.pkl")
    label_translate = joblib.load("translated_label.pkl")
    return model, encoder, gejala_list, gejala_translate, label_translate

# Muat semua resource
try:
    model, encoder, gejala_list, gejala_translate, label_translate = load_resources()
except FileNotFoundError as e:
    st.error(f"Gagal memuat file resource: {e}. Pastikan semua file .pkl ada di direktori yang sama.")
    st.stop()


# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Deteksi Penyakit",
    page_icon="🏥",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS KUSTOM ---
st.markdown("""
    <style>
        .stApp {
            background-color: var(--background-color);
            color: var(--text-color);
        }
        
        :root {
            --background-color: #f5f5f5;
            --text-color: #333333;
            --container-bg: #ffffff;
            --success-bg: #d4edda;
            --success-text: #155724;
            --advice-bg: #e7f3fe;
            --advice-text: #0c5460;
            --footer-text: #666666;
            --border-color: #eeeeee;
        }
        
        @media (prefers-color-scheme: dark) {
            :root {
                --background-color: #0e1117;
                --text-color: #f0f2f6;
                --container-bg: #1e2130;
                --success-bg: #1a3a1e;
                --success-text: #a3d9a5;
                --advice-bg: #1a2a3a;
                --advice-text: #a3c7d9;
                --footer-text: #aaaaaa;
                --border-color: #3a4a5a;
            }
        }
        
        .stCheckbox>label {
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 15px;
            padding: 8px;
            margin: 4px 0;
            border-radius: 6px;
            transition: all 0.2s;
            border: 1px solid transparent;
            cursor: pointer;
        }
        
        .stCheckbox>label:hover {
            background-color: rgba(76, 175, 80, 0.1);
            border-color: rgba(76, 175, 80, 0.2);
        }
        
        .stButton>button {
            border-radius: 8px;
            padding: 10px 24px;
            font-weight: bold;
            transition: all 0.3s;
        }

        /* Menargetkan tombol di dalam kolom pertama untuk styling */
        div[data-testid="stHorizontalBlock"] > div:nth-child(1) button {
            background-color: #22940d; 
            color: white;             
            border: 1px solid #22940d; 
        }

        /* Efek hover pada tombol */
        div[data-testid="stHorizontalBlock"] > div:nth-child(1) button:hover {
            background-color: #1b750b;
            border: 1px solid #1b750b;
        }
    </style>
""", unsafe_allow_html=True)


if 'reset' not in st.session_state:
    st.session_state.reset = False

# --- UI APLIKASI ---

# Header
col_img, col_title = st.columns([1, 4])
with col_img:
    st.image("https://cdn-icons-png.flaticon.com/512/2785/2785482.png", width=80)
with col_title:
    st.title("Aplikasi Deteksi Penyakit")

st.markdown("""
    <div style='text-align: center; margin-bottom: 20px; color: var(--text-color);'>
        Pilih gejala yang Anda alami, lalu klik tombol <b>Prediksi</b> untuk mengetahui kemungkinan penyakit Anda.
    </div>
""", unsafe_allow_html=True)


st.subheader("Pilih Gejala yang Anda Alami")

with st.container(height=430, border=True):
    selected_gejala = []
    cols = st.columns(2)
    
    for i, g in enumerate(gejala_list):
        with cols[i % 2]:
            checkbox_state = st.checkbox(
                gejala_translate.get(g, g.replace("_", " ").title()),
                key=f"cb_{g}",
                value=False if st.session_state.reset else st.session_state.get(f"cb_{g}", False)
            )
            if checkbox_state:
                selected_gejala.append(g)

st.write("")

# --- Tombol Aksi ---
col1, col2 = st.columns([3, 1])
with col1:
    predict_btn = st.button("🔍 Prediksi Sekarang", use_container_width=True, type="primary")
with col2:
    reset_btn = st.button("🗑️ Reset", use_container_width=True)

# --- Logika Reset ---
if reset_btn:
    st.session_state.reset = True
    st.rerun()
else:
    st.session_state.reset = False

# --- PROSES PREDIKSI ---
if predict_btn:
    if not selected_gejala:
        st.warning("⚠️ Silakan pilih minimal satu gejala terlebih dahulu.", icon="✋")
    else:
        with st.spinner('Menganalisis gejala Anda...'):
            input_array = np.zeros((1, len(gejala_list)))
            for g in selected_gejala:
                if g in gejala_list:
                    input_array[0, gejala_list.index(g)] = 1

            pred_index = model.predict(input_array)[0]
            label_en = encoder.classes_[pred_index]
            label_id = label_translate.get(label_en, label_en)
            
            st.markdown(f"""
                <div style='background-color: var(--success-bg); color: var(--success-text); 
                            border: 1px solid #c3e6cb; border-radius: 8px; padding: 15px; margin-top: 20px;'>
                    <div style='font-size: 18px; font-weight: bold; margin-bottom: 10px;'>Hasil Prediksi Penyakit:</div>
                    <div style='display: flex; align-items: center;'>
                        <span style='font-size: 30px; margin-right: 15px;'>🩺</span>
                        <span style='font-size: 24px; font-weight: bold;'>{label_id}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            st.markdown("""
                <div style='margin-top: 20px; padding: 15px; background-color: var(--advice-bg); 
                            color: var(--advice-text); border: 1px solid #bee5eb; border-radius: 8px;'>
                    <b>💡 Penting:</b> Hasil ini adalah prediksi awal. Untuk diagnosis akurat, <b>sangat disarankan berkonsultasi langsung dengan dokter.</b>
                </div>
            """, unsafe_allow_html=True)

# --- FOOTER ---
st.markdown(f"""
    <div style='text-align: center; margin-top: 40px; color: var(--footer-text); font-size: 14px;'>
        <hr style='margin: 20px 0; border: 0.5px solid var(--border-color);'>
        Dibuat dengan ❤️ oleh Yaqin<br>
        © {datetime.datetime.now().year} Aplikasi Deteksi Penyakit
    </div>
""", unsafe_allow_html=True)
