import streamlit as st
import cv2
import numpy as np
import pytesseract
from PIL import Image

# ─────────────────────────────────────────────
# CONFIGURACIÓN DE LA PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="OCR Vision Pink",
    page_icon="💖",
    layout="centered"
)

# ─────────────────────────────────────────────
# ESTILOS PERSONALIZADOS
# ─────────────────────────────────────────────
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

/* Fondo principal */
.stApp {
    background: linear-gradient(135deg, #0f0f14, #1b1022);
    color: white;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #161621 !important;
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* Títulos sidebar */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #ff85c2 !important;
    font-weight: 700 !important;
}

/* Texto sidebar */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label {
    color: #f5f5f7 !important;
}

/* Título principal */
h1 {
    color: #ff4fa3 !important;
    text-align: center;
    font-size: 3rem !important;
    font-weight: 700 !important;
    margin-bottom: 8px;
}

/* Subtítulos */
h2, h3 {
    color: #ff85c2 !important;
}

/* Texto */
p, span, label {
    color: #f5f5f7 !important;
}

/* Cards */
.custom-card {
    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(10px);
    border-radius: 22px;
    padding: 25px;
    margin-top: 20px;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 8px 28px rgba(0,0,0,0.25);
}

/* Camera input */
[data-testid="stCameraInput"] {
    background: rgba(255,255,255,0.03);
    border-radius: 18px;
    padding: 15px;
    border: 2px solid #ff4fa3;
}

/* Radio buttons */
.stRadio > div {
    background: rgba(255,255,255,0.03);
    padding: 10px;
    border-radius: 14px;
}

/* Botones */
.stButton > button {
    background: linear-gradient(135deg, #ff4fa3, #ff85c2) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.7rem 1.4rem !important;
    font-weight: 600 !important;
    transition: 0.3s ease !important;
    box-shadow: 0 4px 18px rgba(255,79,163,0.3);
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(255,79,163,0.4);
}

/* Resultado OCR */
.result-box {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    border-left: 5px solid #ff4fa3;
    border-radius: 18px;
    padding: 22px;
    margin-top: 25px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.2);
}

/* Scroll */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-thumb {
    background: #ff4fa3;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="custom-card">

<h1>💖 OCR Vision</h1>

<p style='text-align:center; font-size:18px; margin-top:10px;'>
Reconocimiento óptico de caracteres mediante inteligencia artificial.
Escanea texto desde una fotografía en tiempo real.
</p>

</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:

    st.markdown("## ⚙️ Configuración")

    st.markdown("""
    <div class="custom-card">

    Selecciona si deseas aplicar un filtro visual antes del reconocimiento OCR.

    </div>
    """, unsafe_allow_html=True)

    filtro = st.radio(
        "Aplicar Filtro",
        ('Con Filtro', 'Sin Filtro')
    )

# ─────────────────────────────────────────────
# CONTENIDO PRINCIPAL
# ─────────────────────────────────────────────
st.markdown("""
<div class="custom-card">

### 📸 Captura una imagen

Toma una fotografía para detectar y extraer automáticamente el texto presente en la imagen.

</div>
""", unsafe_allow_html=True)

img_file_buffer = st.camera_input(" ")

# ─────────────────────────────────────────────
# OCR
# ─────────────────────────────────────────────
if img_file_buffer is not None:

    # Lectura imagen con OpenCV
    bytes_data = img_file_buffer.getvalue()

    cv2_img = cv2.imdecode(
        np.frombuffer(bytes_data, np.uint8),
        cv2.IMREAD_COLOR
    )

    # Aplicar filtro
    if filtro == 'Con Filtro':
        cv2_img = cv2.bitwise_not(cv2_img)
    else:
        cv2_img = cv2_img

    # Conversión RGB
    img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)

    # OCR
    text = pytesseract.image_to_string(img_rgb)

    # Resultado
    st.markdown("""
    <div class="result-box">
    <h3>📝 Texto Detectado</h3>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="custom-card">

    <p style="
        font-size:17px;
        line-height:1.8;
        color:#f5f5f7;
        white-space: pre-wrap;
    ">
    {text}
    </p>

    </div>
    """, unsafe_allow_html=True)
