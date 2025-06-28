import streamlit as st
import numpy as np
import joblib
import datetime

# Load semua resource
model = joblib.load("model.pkl")
encoder = joblib.load("encoder.pkl")
gejala_list = joblib.load("gejala.pkl")
gejala_translate = joblib.load("translated_gejala.pkl")
label_translate = joblib.load("translated_label.pkl")

# Konfigurasi halaman
st.set_page_config(
    page_title="Deteksi Penyakit",
    page_icon="🏥",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS
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
        
        .symptoms-container {
            max-height: 400px;
            overflow-y: auto;
            padding: 10px;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            margin-bottom: 20px;
            background-color: var(--container-bg);
        }
        
        .stCheckbox>label {
            font-size: 15px;
            padding: 6px 8px;
            margin: 2px 0;
            border-radius: 4px;
            transition: all 0.2s;
        }
        
        .stCheckbox>label:hover {
            background-color: rgba(76, 175, 80, 0.1);
        }
        
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
            padding: 10px 24px;
            font-weight: bold;
            transition: all 0.3s;
        }
        
        .reset-btn {
            background-color: #f44336 !important;
            margin-left: 10px;
        }
        
        .button-container {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for reset
if 'reset' not in st.session_state:
    st.session_state.reset = False

# Header
col_img, col_title = st.columns([1, 3])
with col_img:
    st.image("https://cdn-icons-png.flaticon.com/512/2785/2785482.png", width=80)
with col_title:
    st.title("Aplikasi Deteksi Penyakit")

st.markdown("""
    <div style='text-align: center; margin-bottom: 20px; color: var(--text-color);'>
        Pilih gejala yang Anda alami dari daftar di bawah ini, lalu klik tombol <b>Prediksi</b> 
        untuk mengetahui kemungkinan penyakit yang Anda derita.
    </div>
""", unsafe_allow_html=True)

# Container untuk gejala dengan scroll
st.subheader("Gejala yang Dialami")
with st.container():
    # Container dengan scroll
    with st.expander("📋 Daftar Gejala", expanded=True):
        with st.container():
            st.markdown('<div class="symptoms-container">', unsafe_allow_html=True)
            
            selected_gejala = []
            cols = st.columns(2)
            
            for i, g in enumerate(gejala_list):
                with cols[i % 2]:
                    # Use a unique key for each checkbox and handle reset
                    checkbox_state = st.checkbox(
                        gejala_translate[g], 
                        key=f"checkbox_{g}",
                        value=False if st.session_state.reset else st.session_state.get(f"checkbox_{g}", False),
                        help="Centang jika Anda mengalami gejala ini"
                    )
                    if checkbox_state:
                        selected_gejala.append(g)
            
            st.markdown('</div>', unsafe_allow_html=True)

# Tombol aksi
col1, col2 = st.columns([3, 1])
with col1:
    predict_btn = st.button("🔍 Prediksi Sekarang", key="predict", use_container_width=True)
with col2:
    reset_btn = st.button("🗑️ Reset Pilihan", key="reset_btn", type="secondary", use_container_width=True)

if reset_btn:
    st.session_state.reset = True
    st.rerun()
else:
    st.session_state.reset = False

# Proses prediksi
if predict_btn:
    if not selected_gejala:
        st.warning("⚠️ Silakan pilih minimal satu gejala terlebih dahulu.")
    else:
        with st.spinner('Sedang menganalisis gejala...'):
            input_array = np.zeros((1, len(gejala_list)))
            for g in selected_gejala:
                input_array[0, gejala_list.index(g)] = 1

            pred = model.predict(input_array)[0]
            label_en = encoder.classes_[pred]
            label_id = label_translate.get(label_en, label_en)
            
            st.markdown(f"""
                <div style='background-color: var(--success-bg); color: var(--success-text); 
                            border-radius: 5px; padding: 15px; margin-bottom: 15px;'>
                    <div style='font-size: 24px; font-weight: bold; margin-bottom: 10px;'>Hasil Prediksi</div>
                    <div style='display: flex; align-items: center;'>
                        <span style='font-size: 30px; margin-right: 15px;'>🩺</span>
                        <span style='font-size: 22px;'><b>{label_id}</b></span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            st.markdown("""
                <div style='margin-top: 20px; padding: 15px; background-color: var(--advice-bg); 
                            color: var(--advice-text); border-radius: 5px;'>
                    <b>💡 Saran:</b> Hasil ini merupakan prediksi berdasarkan gejala yang dipilih. 
                    Untuk diagnosis yang lebih akurat, disarankan untuk berkonsultasi langsung dengan dokter.
                </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown(f"""
    <div style='text-align: center; margin-top: 30px; color: var(--footer-text); font-size: 14px;'>
        <hr style='margin: 20px 0; border: 0.5px solid var(--border-color);'>
        Dibuat dengan ❤️ oleh Yaqin X Efzyn<br>
        © {datetime.datetime.now().year} Aplikasi Deteksi Penyakit
    </div>
""", unsafe_allow_html=True)