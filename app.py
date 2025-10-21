# -*- coding: utf-8 -*-
import streamlit as st
import cv2
import numpy as np
from PIL import Image as Image, ImageOps as ImagOps
from keras.models import load_model
import platform

# ============================================================
# CONFIGURACIÓN DE PÁGINA Y ESTÉTICA
# ============================================================
st.set_page_config(page_title="Reconocimiento de Imágenes", page_icon="🧠", layout="centered")

st.markdown("""
<style>
:root {
  --bg:#0b1120; --bg2:#0f172a;
  --panel:#111827; --border:#1f2937;
  --text:#f8fafc; --muted:#cbd5e1;
  --accent:#22d3ee; --accent2:#6366f1;
  --ok:#10b981; --warn:#f59e0b; --bad:#ef4444;
}
[data-testid="stAppViewContainer"]{
  background: linear-gradient(180deg, var(--bg) 0%, var(--bg2) 100%) !important;
  color: var(--text) !important;
  font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial;
}
main .block-container {padding-top: 2rem; padding-bottom: 3rem;}
h1,h2,h3 {color: var(--text); letter-spacing:-.02em;}
h1 span.grad{
  background: linear-gradient(90deg, var(--accent), var(--accent2));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.card {
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 1.2rem 1.5rem;
  box-shadow: 0 18px 45px rgba(0,0,0,.45);
  animation: fadeIn .6s ease;
}
@keyframes fadeIn { from {opacity:0; transform:translateY(10px);} to {opacity:1; transform:none;} }
.stButton > button {
  background: linear-gradient(90deg, var(--accent), var(--accent2));
  border: 0; color: #fff; font-weight:600;
  border-radius: 999px; padding: .7rem 1.2rem;
  box-shadow: 0 10px 30px rgba(99,102,241,.3);
  transition: all .2s ease;
}
.stButton > button:hover {transform: translateY(-1px); box-shadow: 0 14px 40px rgba(99,102,241,.4);}
.stCameraInput label div {background: #0f172a !important;}
.stTextInput input, .stTextArea textarea {
  background:#0f172a !important; color:#f8fafc !important;
  border:1px solid #334155 !important; border-radius:12px !important;
  transition: all .2s ease;
}
.stTextInput input:hover, .stTextArea textarea:hover {
  background:#132036 !important; border-color:#3b82f6 !important;
}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

def card_start(): st.markdown('<div class="card">', unsafe_allow_html=True)
def card_end():   st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# UI PRINCIPAL
# ============================================================
st.title("🧠 <span class='grad'>Reconocimiento de Imágenes</span>", unsafe_allow_html=True)
st.caption("Modelo entrenado con Teachable Machine — cargado en Keras y ejecutado en tiempo real 📸")

# Mostrar versión de Python (útil en Streamlit Cloud)
st.markdown(f"**Versión de Python:** `{platform.python_version()}`")

# ============================================================
# CARGA DE MODELO
# ============================================================
try:
    with st.spinner("Cargando modelo Keras…"):
        model = load_model('keras_model.h5')
        st.success("Modelo cargado correctamente ✅")
except Exception as e:
    st.error(f"❌ No se pudo cargar el modelo: {e}")
    st.stop()

# ============================================================
# INTERFAZ VISUAL
# ============================================================
image = Image.open('OIG5.jpg')
card_start()
st.image(image, width=350, caption="Ejemplo de referencia (modelo de Teachable Machine)")
card_end()

with st.sidebar:
    st.subheader("ℹ️ Instrucciones")
    st.write("1️⃣ Usa un modelo entrenado en [Teachable Machine](https://teachablemachine.withgoogle.com/).")
    st.write("2️⃣ Cárgalo en formato `.h5` y colócalo en el directorio del proyecto.")
    st.write("3️⃣ Usa tu cámara para capturar una imagen.")
    st.write("4️⃣ Observa el resultado en tiempo real 🔥")

# ============================================================
# CAPTURA DE IMAGEN
# ============================================================
card_start()
img_file_buffer = st.camera_input("📷 Toma una foto para analizar")
card_end()

# ============================================================
# PROCESAMIENTO
# ============================================================
if img_file_buffer is not None:
    card_start()
    st.subheader("🔎 Análisis de la imagen")

    try:
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        img = Image.open(img_file_buffer)
        img = img.resize((224, 224))
        img_array = np.array(img)
        normalized_image_array = (img_array.astype(np.float32) / 127.0) - 1
        data[0] = normalized_image_array

        with st.spinner("Procesando imagen…"):
            prediction = model.predict(data)
        
        # Mostrar probabilidades
        col1, col2 = st.columns(2)
        with col1:
            st.image(img, caption="Imagen capturada", use_container_width=True)
        with col2:
            st.markdown("### 📊 Resultados de clasificación")
            st.write(prediction)

        # Mostrar resultados interpretados
        if prediction[0][0] > 0.5:
            st.success(f"🟢 Izquierda — **{prediction[0][0]:.2f}** de probabilidad")
        elif prediction[0][1] > 0.5:
            st.info(f"🔵 Arriba — **{prediction[0][1]:.2f}** de probabilidad")
        else:
            st.warning("⚠️ No se detectó una clase dominante. Intenta con otra imagen.")

    except Exception as e:
        st.error(f"Error al procesar la imagen: {e}")
    card_end()

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.caption("Interfaz moderna con tema oscuro • Streamlit + Keras + Teachable Machine 💫")
