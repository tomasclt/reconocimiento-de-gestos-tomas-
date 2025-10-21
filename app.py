# -*- coding: utf-8 -*-
import streamlit as st

# =========================
# CONFIG + TEMA (solo estética)
# =========================
st.set_page_config(page_title="Detección de Objetos en Tiempo Real", page_icon="🔍", layout="wide")

st.markdown("""
<style>
:root{
  --bg:#0b1120; --bg2:#0f172a;
  --panel:#111827; --border:#1f2937;
  --text:#f8fafc; --muted:#cbd5e1;
  --accent:#22d3ee; --accent2:#6366f1;
  --ok:#10b981; --warn:#f59e0b; --bad:#ef4444;
}

[data-testid="stAppViewContainer"]{
  background:
    radial-gradient(1200px 600px at 10% 0%, #0f172a 0%, transparent 60%),
    radial-gradient(900px 500px at 90% 0%, #0c1833 0%, transparent 60%),
    linear-gradient(180deg, var(--bg) 0%, var(--bg2) 100%) !important;
  color: var(--text) !important;
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial;
}
main .block-container{ padding-top: 1.4rem; padding-bottom: 2rem; }

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
  padding: 1.1rem 1.25rem;
  box-shadow: 0 20px 50px rgba(0,0,0,.45);
  animation: fadeIn .5s ease;
}
@keyframes fadeIn{ from{opacity:0; transform: translateY(10px);} to{opacity:1; transform:none;} }

/* Inputs y sliders */
.stTextInput input, .stNumberInput input{
  background:#0f172a !important; color:var(--text) !important;
  border:1px solid #334155 !important; border-radius:12px !important;
  transition: all .22s ease;
}
.stTextInput input:hover, .stNumberInput input:hover{ background:#132036 !important; border-color:#3b82f6 !important; }
.stTextInput input:focus, .stNumberInput input:focus{
  background:#0d1829 !important; color:#f8fafc !important;
  border-color: var(--accent) !important; box-shadow:0 0 0 2px rgba(34,211,238,.25);
}
.stSlider [data-baseweb="slider"] div[role="slider"]{ background: var(--accent) !important; }
.stSlider [data-baseweb="slider"] > div > div{ background:#1f2a44 !important; }

/* Botones */
.stButton > button{
  background: linear-gradient(90deg, var(--accent), var(--accent2));
  border: 0; color: #fff; font-weight: 600;
  border-radius: 999px; padding: .72rem 1.1rem;
  box-shadow: 0 12px 36px rgba(99,102,241,.35);
  transition: all .18s ease;
}
.stButton > button:hover{ transform: translateY(-1px); box-shadow: 0 16px 46px rgba(99,102,241,.45); }

/* Tablas dark */
.dataframe th{ background:#1e293b !important; color:#f1f5f9 !important; }
.dataframe td{ color:#e2e8f0 !important; }

/* Marco imagen */
.frame{ border:1px solid #1f2937; border-radius:16px; overflow:hidden; box-shadow:0 18px 50px rgba(0,0,0,.5); }

/* Toasts legibles */
[data-testid="stToast"] *{ color: var(--text) !important; }
</style>
""", unsafe_allow_html=True)

# Helpers visuales
def card_start(): st.markdown('<div class="card">', unsafe_allow_html=True)
def card_end():   st.markdown('</div>', unsafe_allow_html=True)

# =========================
# PROBADOR (anti-pantalla-vacía)
# =========================
st.title("🔍 <span class='grad'>Detección de Objetos</span> en Imágenes", help="Si ves este título, el front cargó bien.")._markdown
st.caption("Usa la cámara, ajusta umbrales en la barra lateral y corre YOLOv5. Si algo falla, verás el error aquí y no una pantalla vacía.")

# =========================
# TU APP YOLOV5 (misma lógica)
# =========================
import cv2, numpy as np, pandas as pd, torch, os, sys

@st.cache_resource
def load_yolov5_model(model_path='yolov5s.pt'):
    try:
        import yolov5
        try:
            model = yolov5.load(model_path, weights_only=False)
            return model
        except TypeError:
            try:
                model = yolov5.load(model_path)
                return model
            except Exception:
                st.warning("Intentando método alternativo de carga…")
                current_dir = os.path.dirname(os.path.abspath(__file__))
                if current_dir not in sys.path:
                    sys.path.append(current_dir)
                device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
                model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
                return model
    except Exception as e:
        # Mostrar error en UI (en vez de pantalla vacía)
        st.error(f"❌ Error al cargar el modelo: {e}")
        st.info(
            "Sugerencias:\n"
            "- Revisa `requirements.txt`: `torch`, `torchvision`, `yolov5`, `opencv-python-headless`, `pandas`, `numpy`, `streamlit`.\n"
            "- En entornos restringidos usa `opencv-python-headless`.\n"
            "- Prueba: `pip install torch==1.12.0 torchvision==0.13.0 yolov5==7.0.9`."
        )
        return None

# Sidebar (siempre visible)
st.sidebar.title("Parámetros")
with st.sidebar:
    conf = st.slider('Confianza mínima', 0.0, 1.0, 0.25, 0.01)
    iou  = st.slider('Umbral IoU', 0.0, 1.0, 0.45, 0.01)
    st.caption(f"Confianza: {conf:.2f} | IoU: {iou:.2f}")

    st.subheader('Opciones avanzadas')
    nms_class_agn = st.checkbox('NMS class-agnostic', False)
    multi_label   = st.checkbox('Múltiples etiquetas por caja', False)
    max_det       = st.number_input('Detecciones máximas', 10, 2000, 1000, 10)

# Carga de modelo con spinner, pero sin bloquear UI en error
card_start()
with st.spinner("Cargando modelo YOLOv5…"):
    model = load_yolov5_model()
card_end()

if model is not None:
    # Aplicar parámetros al modelo, protegidos (algunas versiones no exponen todos)
    try:    model.conf = conf
    except: pass
    try:    model.iou  = iou
    except: pass
    try:    model.agnostic = nms_class_agn
    except: pass
    try:    model.multi_label = multi_label
    except: pass
    try:    model.max_det = int(max_det)
    except: pass

    # Captura de cámara
    card_start()
    picture = st.camera_input("📸 Capturar imagen", key="camera")
    card_end()

    if picture:
        # Decodificar imagen
        try:
            bytes_data = picture.getvalue()
            cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
        except Exception as e:
            st.error(f"Error leyendo la imagen: {e}")
            st.stop()

        # Detección
        with st.spinner("Detectando objetos…"):
            try:
                results = model(cv2_img)
            except Exception as e:
                st.error(f"Error durante la detección: {e}")
                st.stop()

        # Imagen anotada si está disponible
        annotated = None
        try:
            r = results.render()
            if hasattr(results, 'imgs') and results.imgs:
                annotated = results.imgs[0]
            elif isinstance(r, list) and len(r)>0:
                annotated = r[0]
        except:
            annotated = None
        if annotated is None:
            annotated = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)

        # Parseo de predicciones (tu lógica)
        try:
            predictions = results.pred[0]
            boxes = predictions[:, :4]
            scores = predictions[:, 4]
            categories = predictions[:, 5]

            col1, col2 = st.columns([1.3, 1], gap="large")

            with col1:
                st.subheader("Imagen con detecciones")
                st.markdown('<div class="frame">', unsafe_allow_html=True)
                st.image(annotated, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with col2:
                st.subheader("Objetos detectados")

                import pandas as pd
                label_names = getattr(model, "names", {})
                category_count = {}
                for category in categories:
                    idx = int(category.item()) if hasattr(category, "item") else int(category)
                    category_count[idx] = category_count.get(idx, 0) + 1

                data = []
                for idx, count in category_count.items():
                    label = label_names.get(idx, str(idx))
                    conf_mean = scores[categories == idx].mean().item() if len(scores) else 0
                    data.append({"Categoría": label, "Cantidad": count, "Confianza promedio": f"{conf_mean:.2f}"})

                if data:
                    df = pd.DataFrame(data).sort_values("Cantidad", ascending=False)
                    st.dataframe(df, use_container_width=True)
                    st.bar_chart(df.set_index('Categoría')['Cantidad'])
                    st.toast("Detecciones listas ✅", icon="✅")
                else:
                    st.info("No se detectaron objetos con los parámetros actuales.")
                    st.caption("Prueba a reducir el umbral de confianza en la barra lateral.")
        except Exception as e:
            st.error(f"Error al procesar resultados: {e}")
else:
    # Si el modelo no cargó, seguimos mostrando la app (sin quedar en blanco)
    st.warning("El modelo no se cargó. Revisa dependencias o pesos. La UI sigue operativa para diagnóstico.")

# Footer
st.markdown("---")
st.caption("Streamlit + YOLOv5 + PyTorch • UI oscura y animada — si algo falla, lo verás en pantalla (no pantalla vacía).")

