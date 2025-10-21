# -*- coding: utf-8 -*-
import streamlit as st
import cv2
import numpy as np
# from PIL import Image
from PIL import Image as Image, ImageOps as ImagOps
from keras.models import load_model
import platform

# =========================
# Config de página (solo estética)
# =========================
st.set_page_config(page_title="Reconocimiento de Imágenes", page_icon="🧠", layout="centered")

# =========================
# Estilos (tema oscuro + animaciones). No cambia la lógica.
# =========================
st.markdown("""
<style>
:root{
  --bg:#0b1120; --bg2:#0f172a;
  --panel:#111827; --border:#1f2937;
  --text:#f8fafc; --muted:#cbd5e1;
  --accent:#22d3ee; --accent2:#6366f1;
}
[data-testid="stAppViewContainer"]{
  background: linear-gradient(180deg, var(--bg) 0%, var(--bg2) 100%) !important;
  color: var(--text) !important;
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial;
}
main .block-container{ padding-top: 1.8rem; padding-bottom: 2.2rem; }

h1,h2,h3{ color:#f9fafb !important; letter-spacing:-.02em; }
h1 span.grad{
  background: linear-gradient(90deg, var(--accent), var(--accent2));
  -webkit-background-clip: text; background-clip: text; color: transparent;
}

/* Tarjetas */
.card{
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 1.1rem 1.3rem;
  box-shadow: 0 18px 48px rgba(0,0,0,.45);
  animation: fadeIn .5s ease;
}
@keyframes fadeIn{ from{opacity:0; transform: translateY(10px);} to{opacity:1; transform:none;} }

/* Inputs / cámara */
.stCameraInput label div{ background:#0f172a !important; border-radius:14px; }
.stTextInput input, .stTextArea textarea{
  background:#0f172a !important; color:#f8fafc !important;
  border:1px solid #334155 !important; border-radius:12px !important;
  transition: all .2s ease;
}
.stTextInput input:hover, .stTextArea textarea:hover{ background:#132036 !important; border-color:#3b82f6 !important; }
.stTextInput input:focus, .stTextArea textarea:focus{
  background:#0d1829 !important; color:#f8fafc !important;
  border-color:#22d3ee !important; box-shadow:0 0 0 2px rgba(34,211,238,.25);
}

/* Botón */
.stButton > button{
  background: linear-gradient(90deg, var(--accent), var(--accent2));
  border:0; color:#fff; font-weight:600; border-radius:999px;
  padding:.72rem 1.15rem; box-shadow:0 12px 36px rgba(99,102,241,.35);
  transition: all .18s ease;
}
.stButton > button:hover{ transform: translateY(-1px); box-shadow:0 16px 46px rgba(99,102,241,.45); }

/* Tablas y textos */
.dataframe th{ background:#1e293b !important; color:#f1f5f9 !important; }
.dataframe td{ color:#e2e8f0 !important; }
footer{ visibility:hidden; }
</style>
""", unsafe_allow_html=True)

def card_start(): st.markdown('<div class="card">', unsafe_allow_html=True)
def card_end():   st.markdown('</div>', unsafe_allow_html=True)

# =========================
# Tu lógica (SIN CAMBIOS)
# =========================

# Muestra la versión de Python junto con detalles adicionales
st.write("Versión de Python:", platform.python_version())

model = load_model('keras_model.h5')
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

# Título + imagen de portada (solo visual)
st.markdown("## 🧠 <span class='grad'>Reconocimiento de Imágenes</span>", unsafe_allow_html=True)

card_start()
image = Image.open('OIG5.jpg')
st.image(image, width=350, caption="Ejemplo de referencia")
card_end()

with st.sidebar:
    st.subheader("Instrucciones")
    st.write("Usa un modelo entrenado en **Teachable Machine** (`keras_model.h5`).")
    st.write("Toma una foto con la cámara y la app te dirá la clase más probable.")

# Cámara (igual que antes)
card_start()
img_file_buffer = st.camera_input("📷 Toma una Foto")
card_end()

if img_file_buffer is not None:
    # To read image file buffer with OpenCV:
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    # To read image file buffer as a PIL Image:
    img = Image.open(img_file_buffer)

    newsize = (224, 224)
    img = img.resize(newsize)
    # To convert PIL Image to numpy array:
    img_array = np.array(img)

    # Normalize the image
    normalized_image_array = (img_array.astype(np.float32) / 127.0) - 1
    # Load the image into the array
    data[0] = normalized_image_array

    # run the inference (misma instrucción)
    prediction = model.predict(data)
    print(prediction)

    # Resultados (sin cambiar condiciones)
    card_start()
    st.subheader("🔎 Resultado")
    col1, col2 = st.columns(2)
    with col1:
        st.image(img, caption="Imagen capturada (224×224)", use_container_width=True)
    with col2:
        # Mantengo tus if intactos, solo les doy formato legible
        if prediction[0][0] > 0.5:
            st.header('Izquierda, con Probabilidad: ' + str(prediction[0][0]))
        if prediction[0][1] > 0.5:
            st.header('Arriba, con Probabilidad: ' + str(prediction[0][1]))
        # if prediction[0][2] > 0.5:
        #     st.header('Derecha, con Probabilidad: ' + str(prediction[0][2]))
        st.write("Vector de probabilidades bruto:")
        st.write(prediction)
    card_end()
