# -*- coding: utf-8 -*-
import streamlit as st

# 1) Configuración de página (no cambia lógica)
st.set_page_config(page_title="App · UI Pro", page_icon="✨", layout="wide")

# 2) Estilos globales (tema oscuro + animaciones + legibilidad alta)
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
main .block-container{ padding-top:1.4rem; padding-bottom:2rem; }

/* Tipografía y textos */
h1,h2,h3{ color:#f9fafb !important; letter-spacing:-.02em; }
p, label, span, small, div, li { color:var(--muted); }
[data-testid="stMarkdownContainer"], [data-testid="stMarkdownContainer"] *{ color:var(--text) !important; opacity:1 !important; }

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

/* Inputs (siempre legibles, con hover/focus) */
.stTextInput input, .stNumberInput input, .stTextArea textarea,
.stSelectbox div[data-baseweb="select"] > div, .stMultiSelect > div > div{
  background:#0f172a !important; color:var(--text) !important;
  border:1px solid #334155 !important; border-radius:12px !important;
  transition: all .22s ease;
}
.stTextInput input:hover, .stNumberInput input:hover, .stTextArea textarea:hover,
.stSelectbox div[data-baseweb="select"] > div:hover, .stMultiSelect > div > div:hover{
  background:#132036 !important; border-color:#3b82f6 !important;
}
.stTextInput input:focus, .stNumberInput input:focus, .stTextArea textarea:focus,
.stSelectbox div[data-baseweb="select"] > div:focus, .stMultiSelect > div > div:focus{
  background:#0d1829 !important; color:#f8fafc !important;
  border-color: var(--accent) !important; box-shadow:0 0 0 2px rgba(34,211,238,.25);
}
.stTextArea textarea::placeholder, .stTextInput input::placeholder{ color:#93a2b8 !important; }

/* Sliders / Radio / Checkbox */
.stSlider [data-baseweb="slider"] div[role="slider"]{ background: var(--accent) !important; }
.stSlider [data-baseweb="slider"] > div > div{ background:#1f2a44 !important; }
input[type="radio"], input[type="checkbox"]{ accent-color: var(--accent2) !important; }

/* Botones pro */
.stButton > button, .stDownloadButton > button{
  background: linear-gradient(90deg, var(--accent), var(--accent2));
  border:0; color:#fff; font-weight:600; border-radius:999px;
  padding:.72rem 1.1rem; box-shadow:0 12px 36px rgba(99,102,241,.35);
  transition: all .18s ease;
}
.stButton > button:hover, .stDownloadButton > button:hover{
  transform: translateY(-1px); box-shadow:0 16px 46px rgba(99,102,241,.45);
}

/* Tablas dark */
.dataframe th{ background:#1e293b !important; color:#f1f5f9 !important; }
.dataframe td{ color:#e2e8f0 !important; }

/* Contenedores destacados (opcional) */
.frame{ border:1px solid #1f2937; border-radius:16px; overflow:hidden; box-shadow:0 18px 50px rgba(0,0,0,.5); }

/* Badges */
.badge{ display:inline-block; padding:.24rem .55rem; border-radius:999px; font-weight:700; font-size:.8rem; border:1px solid rgba(255,255,255,.12); }
.badge-ok{ background: rgba(16,185,129,.15); color:#86efac; border-color: rgba(16,185,129,.35); }
.badge-warn{ background: rgba(245,158,11,.15); color:#fde68a; border-color: rgba(245,158,11,.35); }
.badge-info{ background: rgba(34,211,238,.14); color:#a5f3fc; border-color: rgba(34,211,238,.35); }

/* Toasts/alerts legibles */
[data-testid="stToast"] *, .stAlert{ color:var(--text) !important; }
</style>
""", unsafe_allow_html=True)

# 3) Helpers visuales: tarjetas (opcionales, no cambian la lógica)
def card_start(): st.markdown('<div class="card">', unsafe_allow_html=True)
def card_end():   st.markdown('</div>', unsafe_allow_html=True)
def badge(text, kind="info"):
    kind_map = {"ok":"badge-ok","warn":"badge-warn","info":"badge-info"}
    st.markdown(f"<span class='badge {kind_map.get(kind,'badge-info')}'>{text}</span>", unsafe_allow_html=True)

