import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

# ══════════════════════════════════════════════════════════════
# CONFIG & THEME
# ══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Vita Wallet — CFO Strategic Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Color palette - VitaWallet Brand Colors (Light Theme)
COLORS = {
    'primary': '#00C9A7',      # VitaWallet turquoise/green
    'secondary': '#0066FF',    # VitaWallet blue
    'accent': '#00C9A7',       # Turquoise accent
    'warning': '#F5A623',      # Warm amber
    'success': '#00C9A7',      # Vita green
    'danger': '#FF6B6B',       # Soft red
    'dark': '#1A1A2E',         # Deep navy for text
    'light': '#F8FAFB',        # Very light gray bg
    'bg': '#FFFFFF',           # White background
    'card_bg': '#FFFFFF',      # White cards
    'text': '#2D3748',         # Dark gray text
    'muted': '#718096',        # Muted gray
    'border': '#E2E8F0',       # Light border
    'vita_blue': '#0066FF',    # Logo blue
    'vita_green': '#00C9A7',   # Logo green
    'payouts_b2b': '#0066FF',
    'payouts_b2c': '#00C9A7',
    'exchange': '#F5A623',
    'payins_b2b': '#8B5CF6',
    'forwards': '#EC4899',
    'float_inc': '#00C9A7',
    'vita_card': '#0066FF',
}

# Custom CSS - VitaWallet Light Theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        letter-spacing: -0.01em;
    }

    /* Main container - Light background */
    .stApp {
        background: linear-gradient(180deg, #F8FAFB 0%, #FFFFFF 100%);
    }

    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1440px;
    }

    /* Sidebar - VitaWallet Light Style */
    [data-testid="stSidebar"] {
        background: #FFFFFF;
        border-right: 1px solid #E2E8F0;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #2D3748;
    }

    /* Sidebar toggle button - make it more visible */
    [data-testid="collapsedControl"],
    [data-testid="stSidebarCollapseButton"],
    button[kind="header"],
    [data-testid="baseButton-header"] {
        background: #00C9A7 !important;
        border-radius: 0 8px 8px 0 !important;
        border: none !important;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.15) !important;
        min-width: 2rem !important;
        min-height: 2.5rem !important;
    }
    [data-testid="collapsedControl"] svg,
    [data-testid="stSidebarCollapseButton"] svg,
    button[kind="header"] svg,
    [data-testid="baseButton-header"] svg {
        color: white !important;
        stroke: white !important;
        fill: white !important;
    }

    /* Expand button when sidebar is collapsed */
    [data-testid="stSidebarCollapsedControl"] {
        background: #00C9A7 !important;
        border-radius: 0 8px 8px 0 !important;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.2) !important;
        padding: 0.5rem !important;
    }
    [data-testid="stSidebarCollapsedControl"] svg {
        color: white !important;
        stroke: white !important;
    }

    /* Radio buttons - Vita Style */
    [data-testid="stSidebar"] .stRadio > div {
        gap: 0.2rem;
    }

    [data-testid="stSidebar"] .stRadio label {
        background: transparent;
        border-radius: 12px;
        padding: 0.7rem 1rem !important;
        margin: 0.1rem 0;
        transition: all 0.25s ease;
        border: 1px solid transparent;
        color: #4A5568;
    }

    [data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(0, 201, 167, 0.08);
        color: #00C9A7;
    }

    [data-testid="stSidebar"] .stRadio label[data-checked="true"] {
        background: linear-gradient(135deg, #00C9A7, #00B896);
        color: white !important;
        border-radius: 12px;
        font-weight: 600;
    }

    [data-testid="stSidebar"] .stRadio label[data-checked="true"] span {
        color: white !important;
    }

    /* Metric Cards - White with cyan border */
    .metric-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 1.75rem;
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 201, 167, 0.12);
        border-color: #00C9A7;
    }
    .metric-value {
        font-size: 2.6rem;
        font-weight: 800;
        color: #0066FF;
        line-height: 1.1;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #718096;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-top: 0.5rem;
        font-weight: 600;
    }
    .metric-delta {
        font-size: 0.95rem;
        margin-top: 0.4rem;
        font-weight: 500;
    }
    .delta-up { color: #00C9A7; }
    .delta-down { color: #FF6B6B; }

    /* Section Headers */
    .section-header {
        font-size: 1.3rem;
        font-weight: 700;
        color: #2D3748;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #00C9A7;
        display: inline-block;
    }

    /* Strength/Weakness Cards */
    .sw-card {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 1.2rem 1.4rem;
        margin: 0.5rem 0;
        border-left: 4px solid;
        border: 1px solid #E2E8F0;
        font-size: 1.1rem;
        transition: all 0.25s ease;
    }
    .sw-card:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
    }
    .strength { border-left: 4px solid #00C9A7 !important; }
    .weakness { border-left: 4px solid #FF6B6B !important; }

    /* Proposal Cards */
    .proposal-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 1.4rem 1.6rem;
        margin: 0.5rem 0;
        transition: all 0.25s ease;
    }
    .proposal-card:hover {
        border-color: #00C9A7;
        box-shadow: 0 4px 15px rgba(0, 201, 167, 0.1);
    }
    .proposal-badge {
        display: inline-block;
        padding: 0.25rem 0.8rem;
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: 700;
        margin-right: 0.5rem;
        letter-spacing: 0.5px;
    }

    /* Scenario Output */
    .scenario-output {
        background: #FFFFFF;
        border: 2px solid #00C9A7;
        border-radius: 16px;
        padding: 1.75rem;
    }
    .scenario-big {
        font-size: 2.8rem;
        font-weight: 800;
        color: #0066FF;
    }

    /* Valuation Box */
    .val-box {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 20px;
        padding: 2.25rem;
        text-align: center;
        transition: all 0.25s ease;
    }
    .val-box:hover {
        border-color: #00C9A7;
        box-shadow: 0 8px 25px rgba(0, 201, 167, 0.1);
    }
    .val-amount {
        font-size: 3.2rem;
        font-weight: 800;
    }
    .val-label {
        font-size: 0.9rem;
        color: #718096;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 600;
    }

    /* Hide Streamlit elements but keep sidebar trigger functional */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {height: 0px; background: transparent;}

    /* Page Title */
    .page-title {
        font-size: 2.1rem;
        font-weight: 800;
        color: #0066FF;
        margin-bottom: 0.2rem;
        letter-spacing: -0.02em;
    }
    .page-subtitle {
        font-size: 1.05rem;
        color: #718096;
        margin-bottom: 1.5rem;
        font-weight: 400;
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        background: #F8FAFB;
        border-radius: 10px;
        font-weight: 600;
        color: #2D3748;
    }
    .streamlit-expanderHeader:hover {
        background: rgba(0, 201, 167, 0.08);
    }

    /* Slider styling */
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #00C9A7, #0066FF);
    }

    /* Toggle styling */
    .stToggle label span {
        font-weight: 500;
        color: #2D3748;
    }

    /* Text color fixes for light theme */
    .stMarkdown, .stText, p, span, div {
        color: #2D3748;
    }

    /* Info boxes */
    .info-box {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1rem 1.2rem;
    }
    .info-box-accent {
        background: linear-gradient(135deg, rgba(0, 201, 167, 0.05), rgba(0, 102, 255, 0.05));
        border: 1px solid rgba(0, 201, 167, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# DATA
# ══════════════════════════════════════════════════════════════
MESES = ['Mes 1', 'Mes 2', 'Mes 3', 'Mes 4']

DATA = {
    'revenue': [352978, 381724, 478609, 360467],
    'gastos': [290432, 290152, 384939, 320474],
    'cash': [2688667, 2595101, 3085277, 3231872],
    'headcount': [61, 61, 57, 58],
    # Revenue por línea (corregido del Excel)
    'rev_payouts_b2b': [281711, 303602, 389162, 264741],
    'rev_payouts_b2c': [37080, 38996, 37543, 39851],
    'rev_exchange': [34187, 39127, 50359, 49232],
    'rev_payins_b2b': [0, 0, 1546, 6643],
    # Desglose Exchange B2B/B2C (nuevo)
    'rev_exchange_b2b': [28728, 32743, 45880, 42976],
    'rev_exchange_b2c': [5458, 6384, 4479, 6256],
    # GTV (corregido del Excel)
    'gtv_payouts_b2b': [40186000, 48461200, 69585000, 47906000],
    'gtv_payouts_b2c': [2495976, 2893301, 2862897, 3088382],
    'gtv_payins_b2b': [0, 0, 129426, 485049],
    'gtv_payouts_total': [42682044, 51354673, 72448634, 50994350],
    # Volúmenes Exchange (nuevo del Excel)
    'vol_exchange_ventas_b2b': [37990879, 46551246, 67119333, 47790270],
    'vol_exchange_compras_b2b': [7955534, 6210183, 3513810, 4708377],
    'vol_exchange_ventas_b2c': [543235, 690050, 908847, 725178],
    'vol_exchange_compras_b2c': [1089656, 2147553, 1175741, 1270818],
    # Take rates (corregido)
    'take_payouts_b2b': [0.70, 0.63, 0.56, 0.55],
    'take_payouts_b2c': [1.49, 1.35, 1.31, 1.29],
    'take_payins_b2b': [0, 0, 1.19, 1.37],
    # CAC y LTV
    'cac_b2b': [684, 967, 2646, 999],
    'cac_b2c': [11.97, 12.23, 20.14, 15.37],
    'ltv_b2b': [30861, 30807, 39520, 37165],
    'ltv_b2c': [921, 727, 563, 728],
    # Churn y otros
    'churn_b2b': [2.64, -1.30, 1.00, 1.45],
    'churn_b2c': [1.23, 1.15, 0.92, 1.11],
    'cogs': [116992, 78264, 130868, 77290],
    'personal': [94540, 93089, 88344, 106514],
    'marketing': [14622, 46821, 93867, 56772],
    'admin': [33401, 26839, 26392, 28806],
    'tax': [23265, 24522, 29269, 26290],
    'banking': [5275, 20214, 15938, 17454],
    'inversiones': [2337, 403, 261, 7348],
    'tx_rejected': [1387, 2788, 2734, 2245],
    'b2b_users_est': [323, 342, 353, 396],
    # Avg GTV per User B2B (del Excel)
    'avg_gtv_user_b2b': [124415.07, 141699.92, 197126.73, 120974.67],
}

# Derived
DATA['op_margin'] = [(r-g)/r*100 for r,g in zip(DATA['revenue'], DATA['gastos'])]
DATA['gross_margin'] = [(r-c)/r*100 for r,c in zip(DATA['revenue'], DATA['cogs'])]
DATA['rev_per_emp'] = [r/h for r,h in zip(DATA['revenue'], DATA['headcount'])]
DATA['mktg_efficiency'] = [r/m for r,m in zip(DATA['revenue'], DATA['marketing'])]

# ARPU B2B Total = (Payouts B2B + Exchange B2B + Payins B2B) / Usuarios B2B
DATA['arpu_b2b_total'] = [
    (DATA['rev_payouts_b2b'][i] + DATA['rev_exchange_b2b'][i] + DATA['rev_payins_b2b'][i]) / DATA['b2b_users_est'][i]
    for i in range(4)
]

# CAC Payback usa ARPU total B2B, no solo Payouts
DATA['cac_payback_b2b'] = [c/a if a>0 else 0 for c,a in zip(DATA['cac_b2b'], DATA['arpu_b2b_total'])]
DATA['eff_take_rate'] = [r/(gb+gc+pi)*100 if (gb+gc+pi)>0 else 0 for r,gb,gc,pi in zip(DATA['revenue'], DATA['gtv_payouts_b2b'], DATA['gtv_payouts_b2c'], DATA['gtv_payins_b2b'])]

# ══════════════════════════════════════════════════════════════
# BASE = Promedio M1-M4 (run-rate representativo)
# ══════════════════════════════════════════════════════════════
BASE = {}
for key, vals in DATA.items():
    if isinstance(vals, list) and len(vals) == 4:
        BASE[key] = sum(vals) / 4

# Excepción: Payins B2B usa M4 (producto nuevo, M1-M2 son $0)
BASE['rev_payins_b2b'] = DATA['rev_payins_b2b'][3]  # $6,744

# Promedios clave para referencia rápida
BASE_REVENUE = BASE['revenue']              # ~$393,444
BASE_GASTOS = BASE['gastos']                # ~$321,499
BASE_COGS = BASE['cogs']                    # ~$100,854
BASE_PERSONAL = BASE['personal']            # ~$95,622
BASE_MARKETING = BASE['marketing']          # ~$53,020
BASE_ADMIN = BASE['admin']                  # ~$28,860
BASE_TAX = BASE['tax']                      # ~$25,837
BASE_BANKING = BASE['banking']              # ~$14,720
BASE_INVERSIONES = BASE['inversiones']      # ~$2,587
BASE_HEADCOUNT = BASE['headcount']          # ~59.25
BASE_OP_MARGIN = (BASE_REVENUE - BASE_GASTOS) / BASE_REVENUE * 100  # ~18.3%
BASE_GROSS_MARGIN = (BASE_REVENUE - BASE_COGS) / BASE_REVENUE * 100  # ~74.4%

# GTV promedios
BASE_GTV_B2B = BASE['gtv_payouts_b2b']      # ~$51.5M
BASE_GTV_B2C = BASE['gtv_payouts_b2c']      # ~$2.4M
BASE_GTV_PAYINS = BASE['gtv_payins_b2b']    # ~$256K (solo M3-M4)

# ══════════════════════════════════════════════════════════════
# CLIENTES B2B Y MÉTRICAS POR USUARIO
# ══════════════════════════════════════════════════════════════

# Usuarios B2B activos por mes (ya existe en DATA como b2b_users_est)
DATA['users_b2b'] = DATA['b2b_users_est']  # [323, 342, 353, 396]

# avg_gtv_user_b2b ya viene del Excel en DATA, no se recalcula

# Revenue por cliente B2B por línea de negocio
DATA['rev_per_user_payouts_b2b'] = [
    DATA['rev_payouts_b2b'][i] / DATA['users_b2b'][i] if DATA['users_b2b'][i] > 0 else 0
    for i in range(4)
]
DATA['rev_per_user_exchange_b2b'] = [
    DATA['rev_exchange_b2b'][i] / DATA['users_b2b'][i] if DATA['users_b2b'][i] > 0 else 0
    for i in range(4)
]
DATA['rev_per_user_payins_b2b'] = [
    DATA['rev_payins_b2b'][i] / DATA['users_b2b'][i] if DATA['users_b2b'][i] > 0 else 0
    for i in range(4)
]
DATA['rev_per_user_total_b2b'] = [
    DATA['rev_per_user_payouts_b2b'][i] +
    DATA['rev_per_user_exchange_b2b'][i] +
    DATA['rev_per_user_payins_b2b'][i]
    for i in range(4)
]

# Take rate efectivo por usuario B2B
DATA['take_rate_per_user_b2b'] = [
    (DATA['rev_per_user_total_b2b'][i] / DATA['avg_gtv_user_b2b'][i] * 100)
    if DATA['avg_gtv_user_b2b'][i] > 0 else 0
    for i in range(4)
]

# Promedios para BASE
BASE['users_b2b'] = sum(DATA['users_b2b']) / 4                              # ~353.5
BASE['avg_gtv_user_b2b'] = sum(DATA['avg_gtv_user_b2b']) / 4                # ~$146,054
BASE['rev_per_user_total_b2b'] = sum(DATA['rev_per_user_total_b2b']) / 4
BASE['rev_per_user_payouts_b2b'] = sum(DATA['rev_per_user_payouts_b2b']) / 4
BASE['rev_per_user_exchange_b2b'] = sum(DATA['rev_per_user_exchange_b2b']) / 4
BASE['rev_per_user_payins_b2b'] = sum(DATA['rev_per_user_payins_b2b']) / 4
BASE['take_rate_per_user_b2b'] = sum(DATA['take_rate_per_user_b2b']) / 4
BASE['arpu_b2b_total'] = sum(DATA['arpu_b2b_total']) / 4

# Churn promedio B2B - usar los 4 meses (Vita tiene 6 años, M1 no es onboarding)
# Datos: [2.64%, -1.30%, 1.00%, 1.45%] → promedio = 0.95%
# M2 negativo (-1.30%) = expansión neta, se incluye como está (no usar abs())
AVG_CHURN_B2B = sum(DATA['churn_b2b']) / 4 / 100  # promedio M1-M4 como decimal = 0.0095
# Para cálculos de CLTV, usar valor seguro (mínimo 0.5% para evitar división por cero)
AVG_CHURN_B2B_SAFE = max(0.005, AVG_CHURN_B2B)  # = 0.0095 (0.95%)

# ARPU B2B — SOLO PAYOUTS (consistente con base de clientes derivada de Payouts)
# Exchange y Payins son oportunidad de cross-sell, no se incluyen en cálculo base
BASE_ARPU_PAYOUTS_B2B = np.mean([DATA['rev_payouts_b2b'][i] / DATA['b2b_users_est'][i] for i in range(4)])  # ~$872

# CLTV y MRR B2B — usando ARPU solo Payouts
BASE_MRR_B2B = BASE['users_b2b'] * BASE_ARPU_PAYOUTS_B2B  # ~$308K
BASE_CLTV_B2B = BASE_ARPU_PAYOUTS_B2B / AVG_CHURN_B2B_SAFE if AVG_CHURN_B2B_SAFE > 0 else 0  # ~$92K
BASE_ARR_B2B = BASE_MRR_B2B * 12  # ~$3.7M

# CLTV/CAC ratio y LTV/CAC promedio
AVG_CAC_B2B = sum(DATA['cac_b2b']) / 4  # ~$1,324
BASE_LTV_CAC = BASE_CLTV_B2B / AVG_CAC_B2B if AVG_CAC_B2B > 0 else 0  # ~69x

# ARPU total (para referencia de cross-sell upside)
BASE_ARPU_TOTAL_B2B = BASE['rev_per_user_total_b2b']  # ~$994 (incluye Exchange + Payins)
CROSS_SELL_UPSIDE = (BASE_ARPU_TOTAL_B2B / BASE_ARPU_PAYOUTS_B2B - 1) * 100  # ~14%

# ══════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════
def metric_card(label, value, delta=None, delta_dir=None, prefix="", suffix=""):
    delta_html = ""
    if delta is not None:
        cls = "delta-up" if delta_dir == "up" else "delta-down"
        arrow = "↑" if delta_dir == "up" else "↓"
        delta_html = f'<div class="metric-delta {cls}">{arrow} {delta}</div>'
    return f'''
    <div class="metric-card">
        <div class="metric-value">{prefix}{value}{suffix}</div>
        <div class="metric-label">{label}</div>
        {delta_html}
    </div>'''

def format_k(v):
    if abs(v) >= 1_000_000: return f"${v/1_000_000:.1f}M"
    elif abs(v) >= 1000: return f"${v/1000:.0f}K"
    else: return f"${v:,.0f}"

def plotly_theme(fig, height=400):
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor='rgba(255,255,255,0)',
        plot_bgcolor='rgba(255,255,255,0)',
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#2D3748", size=16),
        height=height,
        margin=dict(l=55, r=30, t=55, b=55),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=14, color="#4A5568"),
            bgcolor="rgba(255, 255, 255, 0.9)",
            bordercolor="#E2E8F0",
            borderwidth=1
        ),
    )
    fig.update_xaxes(gridcolor='#EDF2F7', linecolor='#E2E8F0', tickfont=dict(color='#4A5568', size=14), title_font=dict(size=14))
    fig.update_yaxes(gridcolor='#EDF2F7', linecolor='#E2E8F0', tickfont=dict(color='#4A5568', size=14), title_font=dict(size=14))
    return fig

# ══════════════════════════════════════════════════════════════
# SIDEBAR - Scenario Builder Parameters (fixed, collapsible)
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    st.image("logo_vita.jpg", use_container_width=True)
    st.markdown("""
    <div style="text-align:center; padding:0.3rem 0 0.8rem 0; border-bottom:1px solid #E2E8F0; margin-bottom:1rem;">
        <div style="font-size:0.7rem; color:#718096; letter-spacing:1px;">SCENARIO BUILDER</div>
    </div>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════
    # PAYOUTS B2B — Clientes = f(take rate, países)
    # ══════════════════════════════════════════════════════════════
    st.markdown(f'<div style="font-size:0.75rem; color:{COLORS["muted"]}; margin-bottom:4px; font-weight:700;">PAYOUTS B2B</div>', unsafe_allow_html=True)

    take_b2b = st.slider("Take Rate Payouts B2B (%)", 0.30, 0.55, 0.50, 0.01, key="sb_tr_b2b",
        help="M4: 0.55%. Bajar precio = más clientes. Dato: drop 0.70→0.55 generó 18 clientes/mes")

    new_countries = st.slider("Nuevos Países", 0, 3, 3, 1, key="sb_countries",
        help="Bolivia, Perú, España — cada país aporta ~50 clientes B2B/año")

    clients_per_country = 50  # clientes B2B por país nuevo en 12 meses

    # Ritmo orgánico: 15bp de baja = 18 clientes/mes (dato real M1-M4)
    # Cada bp adicional de baja = 18/15 = 1.2 clientes/mes más
    base_rate = 18  # clientes/mes con drop actual (0.70→0.55)
    additional_drop_bp = max(0, (0.55 - take_b2b) * 100)  # bp adicionales
    additional_rate = additional_drop_bp * (18 / 15)  # proporcional al dato real
    monthly_client_rate = base_rate + additional_rate

    # Clientes M16
    organic_growth = int(monthly_client_rate * 12)
    country_growth = new_countries * clients_per_country
    clients_payouts = 396 + organic_growth + country_growth
    clients_b2b_m16 = clients_payouts  # alias para compatibilidad

    # Revenue
    gtv_per_client_payouts = np.mean(DATA['avg_gtv_user_b2b'])
    gtv_b2b_m16 = clients_payouts * gtv_per_client_payouts  # GTV total para COGS
    rev_b2b_proj = clients_payouts * gtv_per_client_payouts * (take_b2b / 100)
    arpu_b2b_m16 = rev_b2b_proj / clients_payouts if clients_payouts > 0 else 0
    new_clients_b2b = clients_payouts - 396

    # Feedback con tasa de crecimiento implícita
    rebaja_text = f'+ {additional_rate:.0f} por rebaja' if additional_drop_bp > 0 else ''
    paises_text = f'+ {country_growth} por {new_countries} países' if new_countries > 0 else ''
    growth_pct_payouts = ((rev_b2b_proj / BASE['rev_payouts_b2b']) - 1) * 100 if BASE['rev_payouts_b2b'] > 0 else 0
    growth_color = COLORS['success'] if growth_pct_payouts >= 50 else COLORS['warning']
    st.markdown(f"""<div style="font-size:0.78rem; color:{COLORS['muted']}; line-height:1.6; background:#F7FAFC; padding:10px; border-radius:6px; margin-top:8px;">
Ritmo: <b>{monthly_client_rate:.0f} cli/mes</b> ({base_rate} orgánico {rebaja_text}) {paises_text}<br>
Clientes M16: <b>{clients_payouts:,}</b> → Revenue: <b>{format_k(rev_b2b_proj)}/mes</b><br>
<span style="color:{growth_color}; font-weight:700;">Crecimiento implícito: +{growth_pct_payouts:.0f}%</span></div>""", unsafe_allow_html=True)

    # Para compatibilidad con código existente
    mult_b2b = gtv_b2b_m16 / BASE_GTV_B2B if BASE_GTV_B2B > 0 else 1
    pct_from_clients = 60  # Default

    # ══════════════════════════════════════════════════════════════
    # PAYINS B2B — "Clientes mandan → take rate de escala → revenue"
    # ══════════════════════════════════════════════════════════════
    st.markdown("<hr style='margin:16px 0; border:none; border-top:1px solid #E2E8F0;'>", unsafe_allow_html=True)
    st.markdown("**📊 PAYINS B2B**")
    st.markdown(f"<div style='font-size:0.72rem;color:{COLORS['muted']};margin-bottom:8px;'>Clientes mandan → take rate de escala → revenue</div>", unsafe_allow_html=True)

    # Payins: producto nuevo, target es escalar agresivamente
    # M4 tiene ~2 clientes, target 50 clientes = ×25 en clientes
    clients_payins_m16 = st.slider("Clientes Payins M16", 5, 100, 50, 5, key="sb_cli_pi",
        help="Target de clientes exportadores")

    # Take rate se deriva de la escala: pocos = 1.37% (actual), muchos = 0.65%
    # Curva logarítmica para que baje más rápido al principio
    scale_factor = np.log(clients_payins_m16 / 2) / np.log(100 / 2)  # 0 at 2 clients, 1 at 100
    scale_factor = min(1.0, max(0.0, scale_factor))
    take_payins_derived = 1.37 - scale_factor * (1.37 - 0.65)

    # GTV per Payins client (M4: $491K GTV / ~2 clientes = ~$250K/cliente)
    avg_gtv_payins_client = 250000
    gtv_payins_m16 = clients_payins_m16 * avg_gtv_payins_client
    rev_payins_proj = gtv_payins_m16 * (take_payins_derived / 100)

    growth_pct_payins = ((rev_payins_proj / BASE['rev_payins_b2b']) - 1) * 100 if BASE['rev_payins_b2b'] > 0 else 0
    st.markdown(f"""<div style='background:#F7FAFC; padding:10px; border-radius:6px; font-size:0.8rem; margin-top:8px;'>
Take Rate: <b>{take_payins_derived:.2f}%</b> | GTV: <b>{format_k(gtv_payins_m16)}</b> | Revenue: <b>{format_k(rev_payins_proj)}</b><br>
<span style="color:{COLORS['success']}; font-weight:700;">Crecimiento: ×{rev_payins_proj/BASE['rev_payins_b2b']:.0f}</span></div>""", unsafe_allow_html=True)

    # Para compatibilidad - calcular mult_payins equivalente
    mult_payins = rev_payins_proj / BASE['rev_payins_b2b'] if BASE['rev_payins_b2b'] > 0 else 1
    take_payins = take_payins_derived
    clients_payins = clients_payins_m16  # alias para el resumen

    # ══════════════════════════════════════════════════════════════
    # RESUMEN TOTAL B2B
    # ══════════════════════════════════════════════════════════════
    total_b2b_m4 = 398
    total_b2b_m16 = clients_payouts + clients_payins
    mult_total = total_b2b_m16 / total_b2b_m4
    target_color = COLORS['success'] if mult_total >= 2.8 else COLORS['warning']
    meta_check = '✅ Meta 3×' if mult_total >= 2.8 else ''

    st.markdown(f"""<div style="background:{COLORS['card_bg']}; border-radius:10px; padding:0.8rem; margin-top:0.8rem; border:1px solid #E2E8F0;">
<span style="font-size:0.85rem; color:{COLORS['text']};">👥 Clientes B2B: {total_b2b_m4} → <b style="color:{target_color};">{total_b2b_m16:,}</b> (<b style="color:{target_color};">{mult_total:.1f}x</b>) {meta_check}</span><br>
<span style="font-size:0.75rem; color:{COLORS['muted']};">Payouts: {clients_payouts:,} (orgánico + países) | Payins: {clients_payins} (exportadores)</span>
</div>""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════
    # EXCHANGE + B2C
    # ══════════════════════════════════════════════════════════════
    st.markdown("<hr style='margin:16px 0; border:none; border-top:1px solid #E2E8F0;'>", unsafe_allow_html=True)
    st.markdown("**📊 OTROS PRODUCTOS**")

    # Exchange: correlacionado con Payouts B2B (mismo cliente usa ambos)
    exchange_ratio = BASE['rev_exchange'] / BASE['rev_payouts_b2b']  # ~0.19
    rev_ex_proj = rev_b2b_proj * exchange_ratio
    mult_exchange = rev_ex_proj / BASE['rev_exchange'] if BASE['rev_exchange'] > 0 else 1

    st.markdown(f"""<div style='font-size:0.8rem; color:{COLORS["muted"]}; margin-bottom:8px;'>
        Exchange: correlacionado con Payouts B2B ({exchange_ratio*100:.0f}% del revenue B2B)
        → <span style='font-weight:700;'>{format_k(rev_ex_proj)}</span>
    </div>""", unsafe_allow_html=True)

    mult_b2c = st.slider("Payouts B2C (×)", 1.0, 4.0, 2.5, 0.1, key="sb_b2c",
        help="España + Vita Card como drivers")

    st.markdown("**👥 Operaciones**")
    hc_target = st.slider("Headcount Target", 58, 80, 64, 1, key="sb_hc")
    hiring_mode = st.toggle("Contratación gradual", value=True, key="hiring_mode",
        help="ON: hires escalonados en 12 meses. OFF: todos desde mes 5.")

    # Mostrar impacto de modo de contratación
    new_positions = max(0, hc_target - 58)
    if new_positions > 0:
        costo_anual_inmediato = new_positions * 2500 * 12
        hire_interval = 12 / new_positions if new_positions > 0 else 999
        costo_anual_gradual = sum(min(new_positions, int((i+1) / hire_interval)) * 2500 for i in range(12)) if new_positions > 0 else 0
        ahorro = costo_anual_inmediato - costo_anual_gradual
        if hiring_mode:
            st.markdown(f"""<span style="font-size:0.75rem; color:{COLORS['success']};">
                Gradual: ahorro de {format_k(ahorro)} en 12 meses vs contratar todos de una</span>""",
                unsafe_allow_html=True)
        else:
            st.markdown(f"""<span style="font-size:0.75rem; color:{COLORS['warning']};">
                Inmediato: +{format_k(ahorro)} en costos vs contratación gradual</span>""",
                unsafe_allow_html=True)

    mktg_monthly = st.slider("Marketing ($K/mes)", 20, 100, 55, 5, key="sb_mktg")

    # Mostrar CAC implícito basado en marketing y nuevos clientes B2B
    total_new_clients_12m = new_clients_b2b + clients_payins_m16  # Nuevos B2B + Payins
    mktg_12m = mktg_monthly * 1000 * 12
    effective_cac = mktg_12m / total_new_clients_12m if total_new_clients_12m > 0 else 0
    cac_color = COLORS['success'] if effective_cac < 1500 else COLORS['warning'] if effective_cac < 2500 else COLORS['danger']
    st.markdown(f"""<div style='background:#F7FAFC; padding:8px; border-radius:6px; font-size:0.78rem; margin-top:6px;'>
        <span style='color:{COLORS["muted"]}'>Marketing 12m:</span> {format_k(mktg_12m)} ÷ {total_new_clients_12m:.0f} clientes nuevos =
        <span style='color:{cac_color}; font-weight:700;'>CAC ${effective_cac:,.0f}</span>
    </div>""", unsafe_allow_html=True)

    st.markdown("**🚀 Innovación**")
    fwd_on = st.toggle("Forwards FX", value=True, key="sb_fwd_on")
    ai_on = st.toggle("AI Sales Agent", value=True, key="sb_ai_on")
    card_on = st.toggle("Vita Card", value=True, key="sb_card_on")

    if fwd_on:
        fwd_rev = st.slider("Forwards ($/mes)", 15000, 80000, 45000, 5000, key="sb_fwd_rev")
    else:
        fwd_rev = 0
    if card_on:
        card_rev = st.slider("Vita Card ($/mes)", 10000, 60000, 40000, 5000, key="sb_card_rev")
    else:
        card_rev = 0

    with st.expander("📋 Justificación de Supuestos — ¿Por qué estos defaults?"):
        st.markdown(f"""
        <div style="font-size:0.82rem; color:#4A5568; line-height:1.8;">
        <table style="width:100%; border-collapse:collapse;">
            <tr style="border-bottom:2px solid {COLORS['dark']};">
                <td style="color:{COLORS['muted']}; font-size:0.7rem; text-transform:uppercase; padding:6px 0;">Parámetro</td>
                <td style="color:{COLORS['muted']}; font-size:0.7rem; text-transform:uppercase; text-align:center; padding:6px 0;">Default</td>
                <td style="color:{COLORS['muted']}; font-size:0.7rem; text-transform:uppercase; padding:6px 0;">Justificación</td>
            </tr>
            <tr style="border-bottom:1px solid {COLORS['dark']};">
                <td style="padding:8px 0; font-weight:600;">Payouts B2B</td>
                <td style="text-align:center; color:{COLORS['primary']}; font-weight:700;">×1.8</td>
                <td style="padding:8px 0; color:{COLORS['muted']}; font-size:0.78rem;">
                    Negocio core, maduro. 3 nuevos países aportan volumen.
                    Top 50 clientes con programa VIP. Take rate baja de 0.55% a 0.50%
                    pero GTV compensa. Crecimiento conservador para línea de 6 años.</td>
            </tr>
            <tr style="border-bottom:1px solid {COLORS['dark']};">
                <td style="padding:8px 0; font-weight:600;">Payouts B2C</td>
                <td style="text-align:center; color:{COLORS['primary']}; font-weight:700;">×2.5</td>
                <td style="padding:8px 0; color:{COLORS['muted']}; font-size:0.78rem;">
                    España como game changer (500K+ latinoamericanos enviando remesas).
                    Vita Card como driver de transacciones. CAC de $15 permite escalar
                    eficientemente con marketing digital.</td>
            </tr>
            <tr style="border-bottom:1px solid {COLORS['dark']};">
                <td style="padding:8px 0; font-weight:600;">Exchange</td>
                <td style="text-align:center; color:{COLORS['primary']}; font-weight:700;">×2.0</td>
                <td style="padding:8px 0; color:{COLORS['muted']}; font-size:0.78rem;">
                    Crece naturalmente con el volumen transaccional. No requiere
                    estrategia separada. Correlacionado con Payouts.</td>
            </tr>
            <tr style="border-bottom:1px solid {COLORS['dark']};">
                <td style="padding:8px 0; font-weight:600;">Payins B2B</td>
                <td style="text-align:center; color:{COLORS['primary']}; font-weight:700;">×18</td>
                <td style="padding:8px 0; color:{COLORS['muted']}; font-size:0.78rem;">
                    Multiplicador alto sobre base mínima ($6.6K). Target real: ~$120K/mes.
                    Producto creció ×4.3 en su primer mes (M3→M4). Cross-sell natural:
                    exportadores son el reverso de los importadores que ya usan Payouts.
                    Take rate converge a 0.65% a escala.</td>
            </tr>
            <tr style="border-bottom:1px solid {COLORS['dark']};">
                <td style="padding:8px 0; font-weight:600;">Take Rate B2B</td>
                <td style="text-align:center; color:{COLORS['primary']}; font-weight:700;">0.50%</td>
                <td style="padding:8px 0; color:{COLORS['muted']}; font-size:0.78rem;">
                    Tendencia actual: 0.70% → 0.55% en 4 meses. Presión competitiva
                    natural al escalar. 0.50% es piso realista. Compensar con
                    volumen y productos de valor agregado (forwards, treasury).</td>
            </tr>
            <tr style="border-bottom:1px solid {COLORS['dark']};">
                <td style="padding:8px 0; font-weight:600;">Take Rate Payins</td>
                <td style="text-align:center; color:{COLORS['primary']}; font-weight:700;">0.65%</td>
                <td style="padding:8px 0; color:{COLORS['muted']}; font-size:0.78rem;">
                    Hoy 1.37% (producto nuevo, pocos clientes). A escala con grandes
                    exportadores, converge al rango de Payouts. 0.65% es
                    conservador vs el 1.37% actual.</td>
            </tr>
            <tr style="border-bottom:1px solid {COLORS['dark']};">
                <td style="padding:8px 0; font-weight:600;">Headcount</td>
                <td style="text-align:center; color:{COLORS['primary']}; font-weight:700;">64</td>
                <td style="padding:8px 0; color:{COLORS['muted']}; font-size:0.78rem;">
                    +6 sobre los 58 actuales. Perfiles: compliance para nuevos países (2),
                    sales B2B (2), producto/tech (2). Crecimiento disciplinado —
                    triplicar revenue con solo 10% más de equipo = apalancamiento operativo.</td>
            </tr>
            <tr style="border-bottom:1px solid {COLORS['dark']};">
                <td style="padding:8px 0; font-weight:600;">Marketing</td>
                <td style="text-align:center; color:{COLORS['primary']}; font-weight:700;">$55K/mes</td>
                <td style="padding:8px 0; color:{COLORS['muted']}; font-size:0.78rem;">
                    Promedio actual: $53K. Mantener nivel similar pero con mejor
                    eficiencia (de 7x a 10x+). El crecimiento viene de producto
                    y expansión geográfica, no de quemar más en marketing.</td>
            </tr>
            <tr style="border-bottom:1px solid {COLORS['dark']};">
                <td style="padding:8px 0; font-weight:600;">Nuevos Países</td>
                <td style="text-align:center; color:{COLORS['primary']}; font-weight:700;">3</td>
                <td style="padding:8px 0; color:{COLORS['muted']}; font-size:0.78rem;">
                    Bolivia, Perú, España. Ya tienen sociedades constituidas en los 3.
                    No es greenfield — es activar infraestructura que ya existe.
                    +$5K/mes por país en admin/legal/oficina.</td>
            </tr>
            <tr style="border-bottom:1px solid {COLORS['dark']};">
                <td style="padding:8px 0; font-weight:600;">Forwards FX</td>
                <td style="text-align:center; color:{COLORS['primary']}; font-weight:700;">$45K/mes</td>
                <td style="padding:8px 0; color:{COLORS['muted']}; font-size:0.78rem;">
                    Spread de 0.15-0.25% sobre nocional. Back-to-back con banco
                    (sin posición propia). Vita ya tiene licencia de Intermediario IF.
                    Requiere +1 especialista. Diferenciador vs competencia en pricing.</td>
            </tr>
            <tr style="border-bottom:1px solid {COLORS['dark']};">
                <td style="padding:8px 0; font-weight:600;">Vita Card</td>
                <td style="text-align:center; color:{COLORS['primary']}; font-weight:700;">$40K/mes</td>
                <td style="padding:8px 0; color:{COLORS['muted']}; font-size:0.78rem;">
                    Visa digital ya existente. Revenue por interchange + FX spread
                    en compras internacionales. Driver de transacciones B2C y
                    retención de saldos.</td>
            </tr>
            <tr>
                <td style="padding:8px 0; font-weight:600;">AI Sales Agent</td>
                <td style="text-align:center; color:{COLORS['primary']}; font-weight:700;">ON</td>
                <td style="padding:8px 0; color:{COLORS['muted']}; font-size:0.78rem;">
                    Automatización de prospección y calificación de leads B2B.
                    Ahorro: ~$19K/mes ($14K marketing + $5K headcount).
                    Implementable en 3-4 meses con herramientas disponibles.</td>
            </tr>
        </table>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-top:1.5rem; padding-top:1rem; border-top:1px solid #E2E8F0; text-align:center;">
        <div style="font-size:0.65rem; color:#A0AEC0;">Ajusta parámetros aquí</div>
        <div style="font-size:0.65rem; color:#A0AEC0;">Ve resultados en Scenario Builder →</div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# HEADER & TABS NAVIGATION
# ══════════════════════════════════════════════════════════════

# Compact header with branding
st.markdown(f"""
<div style="display:flex; justify-content:space-between; align-items:center; padding:0.5rem 0; margin-bottom:0;">
    <div style="display:flex; align-items:baseline; gap:0.75rem;">
        <span style="font-size:1.5rem; font-weight:800; color:{COLORS['accent']};">VITA</span>
        <span style="font-size:0.9rem; color:#718096;">CFO Strategic Analysis</span>
    </div>
    <div style="font-size:0.85rem; color:#4A5568;">
        Pablo Martinez · Feb 2026
    </div>
</div>
<hr style="margin:0.3rem 0 0.8rem 0; border:none; border-top:1px solid #E2E8F0;">
""", unsafe_allow_html=True)

# Horizontal tabs navigation
tab_exec, tab_rev, tab_unit, tab_costs, tab_strat, tab_scenario, tab_val = st.tabs([
    "📊 Executive Summary",
    "💰 Revenue",
    "🎯 Unit Economics",
    "💸 Costs & P&L",
    "🚀 Strategy",
    "🔮 Scenario Builder",
    "📈 Valuation"
])

# ══════════════════════════════════════════════════════════════
# PAGE 1: EXECUTIVE SUMMARY
# ══════════════════════════════════════════════════════════════
with tab_exec:
    st.markdown('<div class="page-title">Executive Summary</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Vista panorámica — ¿Dónde está Vita hoy?</div>', unsafe_allow_html=True)

    # Calculate metrics usando BASE (run-rate promedio M1-M4)
    margin_trend = DATA['op_margin']
    base_rev_per_emp = BASE_REVENUE / DATA['headcount'][3]  # Rev base / headcount actual
    base_ltv_cac = BASE_LTV_CAC  # Usa CLTV calculado con ARPU solo Payouts (~69x)

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        # Revenue Run-Rate (promedio)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{format_k(BASE_REVENUE)}</div>
            <div class="metric-label">Revenue Run-Rate</div>
            <div style="font-size:0.85rem; color:{COLORS['secondary']}; margin-top:0.3rem;">
                Promedio M1-M4
            </div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(metric_card("Cash Position", format_k(DATA['cash'][3]),
            delta=f"+{format_k(DATA['cash'][3]-DATA['cash'][2])} MoM", delta_dir="up"), unsafe_allow_html=True)
    with c3:
        # Margen Operativo BASE con tendencia
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{BASE_OP_MARGIN:.1f}%</div>
            <div class="metric-label">Margen Operativo</div>
            <div style="font-size:0.8rem; color:#718096; margin-top:0.3rem;">
                {margin_trend[0]:.0f}% → {margin_trend[1]:.0f}% → {margin_trend[2]:.0f}% → {margin_trend[3]:.0f}%
            </div>
            <div style="font-size:0.85rem; color:{COLORS['secondary']}; margin-top:0.2rem; font-weight:500;">
                Base: Promedio M1-M4
            </div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(metric_card("LTV/CAC B2B", f"{base_ltv_cac:.0f}x",
            delta="Top 1% industria", delta_dir="up"), unsafe_allow_html=True)
    with c5:
        st.markdown(metric_card("Team", f"{DATA['headcount'][3]}", suffix=" personas",
            delta=f"Rev/Emp: {format_k(base_rev_per_emp)}", delta_dir="up"), unsafe_allow_html=True)

    # Segunda fila de métricas - Clientes y Unit Economics
    st.markdown("<div style='height:0.8rem;'></div>", unsafe_allow_html=True)
    c6, c7, c8, c9, c10 = st.columns(5)
    with c6:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="font-size:2.2rem;">{BASE['users_b2b']:.0f}</div>
            <div class="metric-label">Clientes B2B Activos</div>
            <div class="metric-delta delta-up">M4: {DATA['users_b2b'][3]} (+{((DATA['users_b2b'][3]/DATA['users_b2b'][0])-1)*100:.0f}% vs M1)</div>
        </div>""", unsafe_allow_html=True)
    with c7:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="font-size:2.2rem;">${BASE['avg_gtv_user_b2b']/1000:,.0f}K</div>
            <div class="metric-label">Ticket Mensual B2B</div>
            <div style="font-size:0.85rem; color:{COLORS['muted']}; margin-top:0.3rem;">GTV prom. por cliente</div>
        </div>""", unsafe_allow_html=True)
    with c8:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="font-size:2.2rem;">${BASE_ARPU_PAYOUTS_B2B:,.0f}</div>
            <div class="metric-label">ARPU B2B (Payouts)</div>
            <div style="font-size:0.85rem; color:{COLORS['secondary']}; margin-top:0.3rem;">+${BASE['rev_per_user_total_b2b']-BASE_ARPU_PAYOUTS_B2B:,.0f} cross-sell</div>
        </div>""", unsafe_allow_html=True)
    with c9:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="font-size:2.2rem;">${BASE_MRR_B2B/1000:,.0f}K</div>
            <div class="metric-label">MRR B2B</div>
            <div class="metric-delta delta-up">ARR: ${BASE_ARR_B2B/1e6:,.1f}M</div>
        </div>""", unsafe_allow_html=True)
    with c10:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="font-size:2.2rem;">${BASE_CLTV_B2B/1000:,.0f}K</div>
            <div class="metric-label">CLTV B2B</div>
            <div class="metric-delta delta-up">LTV/CAC: {BASE_LTV_CAC:.0f}x</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">📈 Evolución Revenue</div>', unsafe_allow_html=True)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=MESES, y=DATA['revenue'],
        marker=dict(color=[COLORS['primary'], COLORS['primary'], COLORS['secondary'], COLORS['primary']]),
        text=[format_k(v) for v in DATA['revenue']], textposition='inside',
        textfont=dict(size=16, color='#FFFFFF', family='Plus Jakarta Sans'),
        name='Revenue'))
    # Línea de promedio (run-rate)
    fig.add_hline(y=BASE_REVENUE, line_dash="dot", line_color=COLORS['secondary'], line_width=2,
        annotation_text=f"Run-Rate: {format_k(BASE_REVENUE)}",
        annotation_position="top right",
        annotation_font_color=COLORS['secondary'],
        annotation_font_size=15)
    fig.add_annotation(x='Mes 3', y=DATA['revenue'][2]+25000,
        text="📅 Nov: spike<br>pre-Navidad", showarrow=True, arrowhead=2,
        arrowcolor=COLORS['warning'], font=dict(size=10, color=COLORS['warning']), ax=0, ay=-40)
    fig.add_annotation(x='Mes 4', y=DATA['revenue'][3]+25000,
        text="📅 Dic: cierre<br>de año", showarrow=True, arrowhead=2,
        arrowcolor=COLORS['muted'], font=dict(size=10, color=COLORS['muted']), ax=0, ay=-40)
    fig = plotly_theme(fig, height=350)
    fig.update_layout(showlegend=False, yaxis_title="USD/mes")
    fig.update_yaxes(range=[0, 560000])
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header">✅ Fortalezas</div>', unsafe_allow_html=True)
        for title, desc in [
            (f"LTV/CAC {BASE_LTV_CAC:.0f}x", "Top 1% de la industria fintech global (ARPU solo Payouts B2B)"),
            ("Cash Flow Positivo", "3 de 4 meses con generación neta de caja — cash creció $543K en el período"),
            (f"Churn B2B {sum(DATA['churn_b2b'])/4:.2f}%", "Promedio 4 meses — incluye M2 con expansión neta (-1.3%)"),
            ("CAC Payback < 2 meses", "Recuperas inversión en adquisición rapidísimo"),
            ("Cash $3.2M", "Posición de caja sólida sin necesidad de equity"),
            ("Multipaís operativo", "Infraestructura ya probada cross-border"),
        ]:
            st.markdown(f'<div class="sw-card strength"><strong style="font-size:1.05rem;">{title}</strong><br><span style="color:#718096; font-size:1rem;">{desc}</span></div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-header">⚠️ Oportunidades de Mejora</div>', unsafe_allow_html=True)
        avg_rev_emp = sum(DATA['rev_per_emp']) / 4
        opportunities = [
            ("Margen operativo volátil", f"Rango: {min(DATA['op_margin']):.0f}%-{max(DATA['op_margin']):.0f}% — estacionalidad y marketing errático comprimen el M4"),
            ("Concentración B2B Payouts", "73% del revenue en una línea — diversificar es prioridad"),
            ("Compresión de take rates", "Ha bajado de 0.70% a 0.55% en 4 meses — esperable estabilización en 0.45-0.50%"),
            ("Marketing", "Gasto errático ($15K-$94K) — establecer presupuesto estable y medir con medias móviles"),
            ("Rule of 40 y métricas", "Con 4 meses de data y estacionalidad, mejor evaluar como promedio móvil"),
            (f"Revenue/employee {format_k(avg_rev_emp)}", "Promedio M1-M4 — target para escalar: $12-15K"),
            ("Productos de valor agregado", "Forwards FX y Vita Card como palancas de margen y retención"),
        ]
        for title, desc in opportunities:
            st.markdown(f'<div class="sw-card weakness"><strong style="font-size:1.05rem;">{title}</strong><br><span style="color:#718096; font-size:1rem;">{desc}</span></div>', unsafe_allow_html=True)

    # Nota metodológica
    st.markdown(f"""
    <div style="background:linear-gradient(135deg, rgba(0, 102, 255, 0.06), rgba(0, 201, 167, 0.06));
                border-radius:12px; padding:1rem 1.25rem; margin-top:1.5rem; border:1px solid rgba(0, 102, 255, 0.15);">
        <div style="display:flex; align-items:flex-start; gap:0.75rem;">
            <div style="font-size:1.2rem;">📋</div>
            <div>
                <div style="font-weight:600; color:#2D3748; margin-bottom:0.25rem; font-size:1.05rem;">Nota metodológica</div>
                <div style="font-size:0.9rem; color:#4A5568; line-height:1.6;">
                    Con solo 4 meses de data y estacionalidad marcada (Mes 3 concentra pagos de importadores),
                    los indicadores mensuales son volátiles. Este análisis prioriza <strong>tendencias y promedios</strong>
                    sobre puntos individuales para una evaluación más robusta.
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# PAGE 2: REVENUE DEEP DIVE
# ══════════════════════════════════════════════════════════════
with tab_rev:
    st.markdown('<div class="page-title">Revenue Deep Dive</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Composición, tendencias y oportunidades por línea de negocio</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown('<div class="section-header">Revenue por Línea de Negocio</div>', unsafe_allow_html=True)
        fig = go.Figure()
        for name, values, color in [
            ('Payouts B2B', DATA['rev_payouts_b2b'], COLORS['payouts_b2b']),
            ('Payouts B2C', DATA['rev_payouts_b2c'], COLORS['payouts_b2c']),
            ('Exchange', DATA['rev_exchange'], COLORS['exchange']),
            ('Payins B2B', DATA['rev_payins_b2b'], COLORS['payins_b2b']),
        ]:
            fig.add_trace(go.Bar(name=name, x=MESES, y=values, marker_color=color,
                text=[format_k(v) if v > 5000 else "" for v in values], textposition='inside',
                textfont=dict(size=15, family='Plus Jakarta Sans')))
        fig.update_layout(barmode='stack')
        fig = plotly_theme(fig, height=400)
        fig.update_layout(yaxis_title="USD/mes")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('<div class="section-header">Revenue Mix (Run-Rate)</div>', unsafe_allow_html=True)
        labels = ['Payouts B2B', 'Payouts B2C', 'Exchange', 'Payins B2B']
        values = [BASE['rev_payouts_b2b'], BASE['rev_payouts_b2c'], BASE['rev_exchange'], BASE['rev_payins_b2b']]
        colors = [COLORS['payouts_b2b'], COLORS['payouts_b2c'], COLORS['exchange'], COLORS['payins_b2b']]
        fig = go.Figure(go.Pie(labels=labels, values=values, hole=0.55,
            marker=dict(colors=colors, line=dict(color='#2D3748', width=2)),
            textinfo='percent+label', textfont=dict(size=15, family='Plus Jakarta Sans')))
        fig = plotly_theme(fig, height=400)
        fig.update_layout(showlegend=False, annotations=[dict(text=f"<b>{format_k(sum(values))}</b><br>Run-Rate",
            x=0.5, y=0.5, font=dict(size=16, color='#2D3748', family='Plus Jakarta Sans'), showarrow=False)])
        st.plotly_chart(fig, use_container_width=True)
    
    # Take rates
    st.markdown('<div class="section-header">📉 Evolución Take Rates — La Historia Crítica</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([3, 2])
    with col1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=MESES, y=DATA['take_payouts_b2b'], name='Payouts B2B',
            mode='lines+markers+text', line=dict(color=COLORS['payouts_b2b'], width=3), marker=dict(size=10),
            text=[f"{v:.2f}%" for v in DATA['take_payouts_b2b']], textposition='bottom center', textfont=dict(size=12)))
        fig.add_trace(go.Scatter(x=MESES, y=DATA['take_payouts_b2c'], name='Payouts B2C',
            mode='lines+markers+text', line=dict(color=COLORS['payouts_b2c'], width=3), marker=dict(size=10),
            text=[f"{v:.2f}%" for v in DATA['take_payouts_b2c']], textposition='top left', textfont=dict(size=12)))
        # Payins solo tiene datos en M3 y M4
        payins_take_m3_m4 = [DATA['take_payins_b2b'][2], DATA['take_payins_b2b'][3]]  # [1.19, 1.37]
        fig.add_trace(go.Scatter(x=['Mes 3', 'Mes 4'], y=payins_take_m3_m4, name='Payins B2B',
            mode='lines+markers+text', line=dict(color=COLORS['payins_b2b'], width=3, dash='dot'), marker=dict(size=10),
            text=[f"{v:.2f}%" for v in payins_take_m3_m4], textposition='bottom right', textfont=dict(size=12)))
        fig = plotly_theme(fig, height=380)
        fig.update_layout(yaxis_title="Take Rate %")
        fig.update_yaxes(range=[0, 2.0])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown(f"""
        <div style="background:#FFFFFF; border-radius:12px; padding:1rem; border:1px solid #E2E8F0; border-left:4px solid #FF6B6B; box-shadow: 0 1px 3px rgba(0,0,0,0.04); margin-bottom:0.8rem;">
            <div style="font-weight:700; color:#FF6B6B; margin-bottom:0.4rem; font-size:0.95rem;">⚠️ Take Rates en Compresión</div>
            <div style="font-size:0.95rem; color:#4A5568; line-height:1.5;">
                Payouts B2B pasó de 0.70% a 0.55% en el período. Posibles causas: presión competitiva, cambio en mix de clientes, descuentos por volumen, o una combinación. Con solo 4 meses de data es prematuro atribuir causalidad. <em>Requiere análisis de cohortes por cliente para diagnosticar.</em>
            </div>
        </div>
        <div style="background:#FFFFFF; border-radius:12px; padding:1rem; border:1px solid #E2E8F0; border-left:4px solid {COLORS['secondary']}; box-shadow: 0 1px 3px rgba(0,0,0,0.04); margin-bottom:0.8rem;">
            <div style="font-weight:700; color:{COLORS['secondary']}; margin-bottom:0.4rem; font-size:0.95rem;">💡 Payins B2B: Margen Inicial Alto</div>
            <div style="font-size:0.95rem; color:#4A5568; line-height:1.5;">
                Take rate de 1.19%-1.37% probablemente refleja los primeros clientes, típicamente más pequeños y menos sensibles a precio. Si se escala hacia exportadores de mayor volumen, es razonable esperar convergencia a ~0.65%. <em>La oportunidad está en volumen + cross-sell, no en mantener márgenes iniciales.</em>
            </div>
        </div>
        <div style="background:#FFFFFF; border-radius:12px; padding:1rem; border:1px solid #E2E8F0; border-left:4px solid {COLORS['warning']}; box-shadow: 0 1px 3px rgba(0,0,0,0.04);">
            <div style="font-weight:700; color:{COLORS['warning']}; margin-bottom:0.4rem; font-size:0.95rem;">📅 Estacionalidad Mes 3</div>
            <div style="font-size:0.95rem; color:#4A5568; line-height:1.5;">
                Mes 3 muestra spike de +25% en revenue. Podría corresponder a estacionalidad (concentración de pagos de fin de año) o a un evento puntual. Sin data histórica de años anteriores, no es posible confirmar. <em>Recomendación: no extrapolar este mes como tendencia base.</em>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Effective take rate
    st.markdown('<div class="section-header">📊 Effective Take Rate Global</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    for i, (col, mes) in enumerate(zip([c1,c2,c3,c4], MESES)):
        with col:
            color = COLORS['success'] if DATA['eff_take_rate'][i] > 0.35 else COLORS['danger']
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size:1.8rem; font-weight:800; color:{color};">{DATA['eff_take_rate'][i]:.3f}%</div>
                <div class="metric-label">{mes}</div>
            </div>""", unsafe_allow_html=True)

    # Revenue por País
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">🌎 REVENUE POR PAÍS — IMPLICANCIAS PARA MÁRGENES</div>', unsafe_allow_html=True)

    col_chart, col_insight = st.columns([1, 1])
    with col_chart:
        paises = ['Chile', 'USA', 'Argentina', 'Colombia', 'Otros']
        pct_revenue = [40, 20, 10, 8, 22]
        colores_pais = ['#4a9eff', '#ff6b35', '#00d4aa', '#ffc048', '#8892a4']

        fig = go.Figure(go.Pie(
            labels=paises, values=pct_revenue, hole=0.55,
            marker=dict(colors=colores_pais, line=dict(color='#FFFFFF', width=2)),
            textinfo='percent+label', textfont=dict(size=14, family='Plus Jakarta Sans')
        ))
        fig = plotly_theme(fig, height=320)
        fig.update_layout(showlegend=False, annotations=[
            dict(text="<b>Revenue<br>Mix</b>", x=0.5, y=0.5,
                 font=dict(size=14, color='#2D3748'), showarrow=False)])
        st.plotly_chart(fig, use_container_width=True)

    with col_insight:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg, rgba(0, 102, 255, 0.06), rgba(0, 201, 167, 0.06));
                    border-radius:12px; padding:1.25rem; border:1px solid rgba(0, 102, 255, 0.15); height:100%;">
            <div style="display:flex; align-items:flex-start; gap:0.75rem;">
                <div style="font-size:1.3rem;">🌐</div>
                <div>
                    <div style="font-weight:600; color:#2D3748; margin-bottom:0.5rem; font-size:1.05rem;">Mix Geográfico y Márgenes</div>
                    <div style="font-size:0.95rem; color:#4A5568; line-height:1.6;">
                        Cada corredor tiene estructura de costos y márgenes distintos. La compresión observada en take rates
                        podría explicarse parcialmente por cambios en el mix geográfico — no necesariamente por presión competitiva.<br><br>
                        Al expandir a <strong>Perú, Bolivia y España</strong> (donde Vita ya tiene sociedades constituidas),
                        el mix cambiará nuevamente.<br><br>
                        <em>Clave: modelar márgenes por corredor, no solo a nivel consolidado.</em>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Tabla de países
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <table style="width:100%; border-collapse:collapse; font-size:1rem;">
        <thead>
            <tr style="background:#F7FAFC; border-bottom:2px solid #E2E8F0;">
                <th style="padding:0.8rem 1rem; text-align:left; font-weight:700; color:#2D3748;">País</th>
                <th style="padding:0.8rem 1rem; text-align:center; font-weight:700; color:#2D3748;">% Revenue</th>
                <th style="padding:0.8rem 1rem; text-align:left; font-weight:700; color:#2D3748;">Observación</th>
            </tr>
        </thead>
        <tbody>
            <tr style="border-bottom:1px solid #E2E8F0;">
                <td style="padding:0.7rem 1rem; color:#4a9eff; font-weight:600;">🇨🇱 Chile</td>
                <td style="padding:0.7rem 1rem; text-align:center; font-weight:700;">40%</td>
                <td style="padding:0.7rem 1rem; color:#4A5568;">Principal mercado. Intermediario de Instrumentos Financieros + Agencia de Valores</td>
            </tr>
            <tr style="border-bottom:1px solid #E2E8F0; background:#FAFAFA;">
                <td style="padding:0.7rem 1rem; color:#ff6b35; font-weight:600;">🇺🇸 USA</td>
                <td style="padding:0.7rem 1rem; text-align:center; font-weight:700;">20%</td>
                <td style="padding:0.7rem 1rem; color:#4A5568;">Holding + corredor de alto volumen</td>
            </tr>
            <tr style="border-bottom:1px solid #E2E8F0;">
                <td style="padding:0.7rem 1rem; color:#00d4aa; font-weight:600;">🇦🇷 Argentina</td>
                <td style="padding:0.7rem 1rem; text-align:center; font-weight:700;">10%</td>
                <td style="padding:0.7rem 1rem; color:#4A5568;">PSAV + PSP. Mercado volátil, potencial alto</td>
            </tr>
            <tr style="border-bottom:1px solid #E2E8F0; background:#FAFAFA;">
                <td style="padding:0.7rem 1rem; color:#ffc048; font-weight:600;">🇨🇴 Colombia</td>
                <td style="padding:0.7rem 1rem; text-align:center; font-weight:700;">8%</td>
                <td style="padding:0.7rem 1rem; color:#4A5568;">Sociedad operativa. En crecimiento</td>
            </tr>
            <tr>
                <td style="padding:0.7rem 1rem; color:#8892a4; font-weight:600;">🌍 Otros</td>
                <td style="padding:0.7rem 1rem; text-align:center; font-weight:700;">22%</td>
                <td style="padding:0.7rem 1rem; color:#4A5568;">Incluye México (transmisora de dinero). Perú, Bolivia y España con sociedades ya constituidas</td>
            </tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# PAGE 3: UNIT ECONOMICS
# ══════════════════════════════════════════════════════════════
with tab_unit:
    st.markdown('<div class="page-title">Unit Economics</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Los fundamentos del negocio son excepcionales — esta es la prueba</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-header">LTV vs CAC — B2B</div>', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(name='LTV', x=MESES, y=DATA['ltv_b2b'], marker_color=COLORS['primary'],
            text=[format_k(v) for v in DATA['ltv_b2b']], textposition='outside'))
        fig.add_trace(go.Bar(name='CAC', x=MESES, y=DATA['cac_b2b'], marker_color=COLORS['danger'],
            text=[f"${v:,.0f}" for v in DATA['cac_b2b']], textposition='outside'))
        fig = plotly_theme(fig, height=350)
        fig.update_layout(barmode='group', yaxis_title="USD")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('<div class="section-header">LTV/CAC vs Industria</div>', unsafe_allow_html=True)
        ltv_cac_avg = np.mean([l/c for l,c in zip(DATA['ltv_b2b'], DATA['cac_b2b'])])
        fig = go.Figure()
        for name, val, color in [
            ('Vita Wallet', ltv_cac_avg, COLORS['primary']),
            ('Top 10% Fintech', 15, COLORS['secondary']),
            ('Promedio SaaS', 5, COLORS['warning']),
            ('Mínimo viable', 3, COLORS['danger']),
        ]:
            fig.add_trace(go.Bar(y=[name], x=[val], orientation='h', marker_color=color,
                text=[f"{val:.0f}x"], textposition='outside',
                textfont=dict(size=16, color=color, family='Plus Jakarta Sans'), showlegend=False))
        fig = plotly_theme(fig, height=300)
        fig.update_layout(xaxis_title="LTV/CAC Ratio")
        fig.update_xaxes(range=[0, 35])
        st.plotly_chart(fig, use_container_width=True)
    
    # Key metrics
    st.markdown('<div class="section-header">Métricas de Retención y Eficiencia</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(metric_card("CAC Payback B2B", f"{np.mean(DATA['cac_payback_b2b']):.1f}", suffix=" meses",
            delta="<2 meses = excepcional", delta_dir="up"), unsafe_allow_html=True)
    with c2:
        churn_b2b_avg = np.mean(DATA['churn_b2b'])  # Promedio de los 4 meses = 0.95%
        st.markdown(metric_card("Churn B2B Avg", f"{churn_b2b_avg:.2f}", suffix="%",
            delta="Incluye M2 negativo (-1.3% = expansión)", delta_dir="up"), unsafe_allow_html=True)
    with c3:
        st.markdown(metric_card("Clientes B2B", f"{DATA['b2b_users_est'][3]}",
            delta=f"+{DATA['b2b_users_est'][3]-DATA['b2b_users_est'][0]} en 4 meses", delta_dir="up"), unsafe_allow_html=True)
    with c4:
        # ARPU solo Payouts B2B (consistente con base de clientes)
        st.markdown(metric_card("ARPU B2B", f"${BASE_ARPU_PAYOUTS_B2B:,.0f}",
            delta=f"+${BASE_ARPU_TOTAL_B2B-BASE_ARPU_PAYOUTS_B2B:.0f} cross-sell", delta_dir="up"), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Rule of 40
    st.markdown('<div class="section-header">Rule of 40 — Growth + Margin > 40%</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([3, 2])
    with col1:
        rule40_data = []
        for i in range(1, 4):
            growth = (DATA['revenue'][i]-DATA['revenue'][i-1])/DATA['revenue'][i-1]*100
            margin = DATA['op_margin'][i]
            rule40_data.append({'mes': MESES[i], 'growth': growth, 'margin': margin, 'total': growth+margin})
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Revenue Growth %', x=[d['mes'] for d in rule40_data],
            y=[d['growth'] for d in rule40_data], marker_color=COLORS['primary']))
        fig.add_trace(go.Bar(name='Op Margin %', x=[d['mes'] for d in rule40_data],
            y=[d['margin'] for d in rule40_data], marker_color=COLORS['secondary']))
        fig.add_hline(y=40, line_dash="dash", line_color=COLORS['success'], line_width=2,
            annotation_text="Target = 40", annotation_font_color=COLORS['success'])
        fig = plotly_theme(fig, height=350)
        fig.update_layout(barmode='stack', yaxis_title="Rule of 40 Score")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        for d in rule40_data:
            status = "✅" if d['total'] >= 40 else "❌"
            color = COLORS['success'] if d['total'] >= 40 else COLORS['danger']
            st.markdown(f"""
            <div style="background:#FFFFFF; border-radius:10px; padding:0.8rem; margin:0.5rem 0; border-left:3px solid {color};">
                <strong style="color:{color};">{d['mes']}: {d['total']:.0f} {status}</strong><br>
                <span style="color:#718096; font-size:1rem;">Growth {d['growth']:+.1f}% + Margin {d['margin']:.1f}%</span>
            </div>""", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background:#FFFFFF; border-radius:10px; padding:0.8rem; margin:0.8rem 0; border-left:3px solid {COLORS['warning']};">
            <span style="font-size:1.05rem; color:#4A5568;">
                <strong>Insight:</strong> Solo M3 ({rule40_data[1]['total']:.0f}) supera el target — impulsado por estacionalidad (Nov).
                M4 ({rule40_data[2]['total']:.0f}) es negativo por caída estacional (Dic). La estacionalidad es normal en pagos cross-border.
            </span>
        </div>""", unsafe_allow_html=True)

    # Unit economics evolution
    st.markdown('<div class="section-header">Evolución Unit Economics B2B</div>', unsafe_allow_html=True)
    fig = make_subplots(rows=1, cols=3, subplot_titles=("CAC Payback (meses)", "Churn Rate %", "ARPU Payouts B2B"))
    fig.add_trace(go.Scatter(x=MESES, y=DATA['cac_payback_b2b'], mode='lines+markers',
        marker=dict(size=10, color=COLORS['primary']), line=dict(width=3, color=COLORS['primary']), name='CAC Payback'), row=1, col=1)
    fig.add_trace(go.Scatter(x=MESES, y=DATA['churn_b2b'], mode='lines+markers',
        marker=dict(size=10, color=COLORS['accent']), line=dict(width=3, color=COLORS['accent']), name='Churn B2B'), row=1, col=2)
    # ARPU solo Payouts B2B (consistente con base de clientes)
    arpu_payouts_series = [DATA['rev_payouts_b2b'][i] / DATA['b2b_users_est'][i] for i in range(4)]
    fig.add_trace(go.Scatter(x=MESES, y=arpu_payouts_series, mode='lines+markers',
        marker=dict(size=10, color=COLORS['secondary']), line=dict(width=3, color=COLORS['secondary']), name='ARPU'), row=1, col=3)
    # Agregar anotación para M2 churn negativo
    fig.add_annotation(x='Mes 2', y=DATA['churn_b2b'][1], text="Expansión neta", showarrow=True, arrowhead=2,
        arrowcolor=COLORS['success'], font=dict(size=9, color=COLORS['success']), ax=0, ay=-30, row=1, col=2)
    fig = plotly_theme(fig, height=300)
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    # Metodología CLTV y MRR
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">📐 METODOLOGÍA — CLTV Y MRR</div>', unsafe_allow_html=True)

    # Variables para metodología CLTV/MRR
    # ARPU solo Payouts B2B (consistente con base de clientes)
    base_arpu_b2b = BASE_ARPU_PAYOUTS_B2B  # ~$872
    cltv_revenue = base_arpu_b2b / AVG_CHURN_B2B_SAFE  # ~$92K
    gross_margin_avg = 1 - np.mean(DATA['cogs']) / np.mean(DATA['revenue'])  # ~74.4%
    cltv_gross_profit = (base_arpu_b2b * gross_margin_avg) / AVG_CHURN_B2B_SAFE  # ~$68K

    ltv_cac_revenue = cltv_revenue / np.mean(DATA['cac_b2b'])  # ~69x
    ltv_cac_gp = cltv_gross_profit / np.mean(DATA['cac_b2b'])  # ~51x

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div style="background:{COLORS['card_bg']}; border-radius:12px; padding:1.2rem;
            border-top:4px solid {COLORS['primary']};">
            <div style="font-size:0.7rem; color:{COLORS['muted']}; text-transform:uppercase;
                letter-spacing:1px;">CLTV sobre Revenue</div>
            <div style="font-size:2rem; font-weight:800; color:{COLORS['primary']};">
                ${cltv_revenue/1000:,.0f}K</div>
            <div style="font-size:0.8rem; color:{COLORS['muted']}; margin-top:0.3rem;">
                ${base_arpu_b2b:,.0f} / {AVG_CHURN_B2B_SAFE*100:.2f}%</div>
            <div style="font-size:0.85rem; color:{COLORS['text']}; margin-top:0.5rem;">
                LTV/CAC: <b style="color:{COLORS['primary']};">{ltv_cac_revenue:.0f}x</b></div>
            <div style="font-size:0.75rem; color:{COLORS['muted']}; margin-top:0.5rem;">
                Método SaaS clásico. Comparable con industria pero no descuenta costos de servir al cliente.</div>
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="background:{COLORS['card_bg']}; border-radius:12px; padding:1.2rem;
            border-top:4px solid {COLORS['success']};">
            <div style="font-size:0.7rem; color:{COLORS['muted']}; text-transform:uppercase;
                letter-spacing:1px;">CLTV sobre Gross Profit ★</div>
            <div style="font-size:2rem; font-weight:800; color:{COLORS['success']};">
                ${cltv_gross_profit/1000:,.0f}K</div>
            <div style="font-size:0.8rem; color:{COLORS['muted']}; margin-top:0.3rem;">
                (${base_arpu_b2b:,.0f} × {gross_margin_avg*100:.0f}%) / {AVG_CHURN_B2B_SAFE*100:.2f}%</div>
            <div style="font-size:0.85rem; color:{COLORS['text']}; margin-top:0.5rem;">
                LTV/CAC: <b style="color:{COLORS['success']};">{ltv_cac_gp:.0f}x</b></div>
            <div style="font-size:0.75rem; color:{COLORS['muted']}; margin-top:0.5rem;">
                Conservador. Mide lo que el cliente deja en el bolsillo después de costos de procesamiento.
                Más apropiado para modelo transaccional con ARPU variable.</div>
        </div>""", unsafe_allow_html=True)

    # Nota de metodología
    st.markdown(f"""
    <div style="background:rgba(0, 102, 255, 0.08); border-radius:8px; padding:1rem; margin-top:1rem;
        border-left:3px solid {COLORS['secondary']};">
        <div style="font-size:0.85rem; color:#4A5568; line-height:1.6;">
            <strong style="color:{COLORS['secondary']};">📋 Metodología ARPU:</strong>
            ARPU calculado exclusivamente sobre Revenue Payouts B2B (${base_arpu_b2b:,.0f}/mes),
            consistente con la base de clientes derivada de Payouts ({BASE['users_b2b']:.0f} usuarios).
            Exchange (${BASE['rev_per_user_exchange_b2b']:,.0f}/mes) y Payins (${BASE['rev_per_user_payins_b2b']:,.0f}/mes)
            por cliente son oportunidad adicional de cross-sell pero no se incluyen en el cálculo base
            para evitar mezclar universos de datos.<br><br>
            <em style="color:{COLORS['success']};">Incluyendo Exchange y Payins, el ARPU total alcanza
            ${BASE_ARPU_TOTAL_B2B:,.0f}/mes — upside de {CROSS_SELL_UPSIDE:.0f}% sobre la base.</em>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # MRR Section
    col_mrr_single = st.columns(1)[0]
    with col_mrr_single:
        # Variables para MRR
        users_b2b_display = BASE['users_b2b']
        mrr_b2b_display = BASE_MRR_B2B

        st.markdown(f"""
        <div style="background:#FFFFFF; border-radius:12px; padding:1.25rem; border:1px solid #E2E8F0;
                    border-top:4px solid {COLORS['secondary']}; box-shadow: 0 1px 3px rgba(0,0,0,0.04);">
            <div style="font-weight:700; color:{COLORS['secondary']}; margin-bottom:0.8rem; font-size:1.1rem;">
                📈 Monthly Recurring Revenue (MRR)
            </div>
            <div style="background:#F7FAFC; border-radius:8px; padding:0.8rem; margin-bottom:1rem; font-family:monospace; font-size:0.95rem;">
                MRR = Σ (Usuarios activos × ARPU)
            </div>
            <div style="font-size:0.95rem; color:#4A5568; line-height:1.7;">
                <strong>Usuarios B2B activos:</strong> <span style="color:{COLORS['secondary']};">{users_b2b_display:.0f}</span> (promedio M1-M4)<br><br>
                <strong>ARPU B2B:</strong> <span style="color:{COLORS['secondary']};">${base_arpu_b2b:,.0f}/mes</span><br><br>
                <strong>MRR B2B</strong> = {users_b2b_display:.0f} × ${base_arpu_b2b:,.0f} = <span style="color:{COLORS['success']}; font-weight:700; font-size:1.1rem;">${mrr_b2b_display/1000:,.0f}K/mes</span><br><br>
                <div style="background:rgba(0, 102, 255, 0.1); border-radius:6px; padding:0.6rem; margin-top:0.5rem;">
                    <strong style="color:{COLORS['secondary']};">📋 Nota:</strong> El MRR de Vita incluye tanto revenue recurrente (clientes con volumen estable) como transaccional. La métrica más precisa sería separar clientes con >3 meses de actividad continua.
                </div>
                <div style="background:rgba(245, 166, 35, 0.1); border-radius:6px; padding:0.6rem; margin-top:0.5rem;">
                    <strong style="color:{COLORS['warning']};">⚠ Consideración:</strong> En cross-border payments, el "MRR" es menos estable que en SaaS tradicional por naturaleza transaccional del negocio.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════
    # CLIENTES B2B — EVOLUCIÓN Y DESGLOSE
    # ═══════════════════════════════════════════════════════════
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">👥 Clientes B2B — Evolución y Desglose por Línea</div>', unsafe_allow_html=True)

    col_tbl, col_chart = st.columns([3, 2])

    with col_tbl:
        # Tabla HTML estilizada de métricas por cliente
        table_html_ue = """<table style="width:100%; border-collapse:collapse; font-size:0.9rem; font-family:'JetBrains Mono', monospace;">
            <thead>
                <tr style="background:#F7FAFC; border-bottom:2px solid #E2E8F0;">
                    <th style="padding:0.5rem 0.4rem; text-align:left; font-weight:700; color:#2D3748;">Métrica</th>
                    <th style="padding:0.5rem 0.4rem; text-align:center; font-weight:700; color:#2D3748;">M1</th>
                    <th style="padding:0.5rem 0.4rem; text-align:center; font-weight:700; color:#2D3748;">M2</th>
                    <th style="padding:0.5rem 0.4rem; text-align:center; font-weight:700; color:#2D3748;">M3</th>
                    <th style="padding:0.5rem 0.4rem; text-align:center; font-weight:700; color:#2D3748;">M4</th>
                    <th style="padding:0.5rem 0.4rem; text-align:center; font-weight:700; color:#718096;">Promedio</th>
                </tr>
            </thead>
            <tbody>"""

        # Filas de datos
        rows_ue = [
            ("Clientes B2B activos", DATA['users_b2b'], '{:.0f}', COLORS['text']),
            ("Ticket mensual (GTV)", DATA['avg_gtv_user_b2b'], '${:,.0f}', COLORS['text']),
            ("Rev/Cliente — Payouts", DATA['rev_per_user_payouts_b2b'], '${:,.0f}', COLORS['payouts_b2b']),
            ("Rev/Cliente — Exchange", DATA['rev_per_user_exchange_b2b'], '${:,.0f}', COLORS['exchange']),
            ("Rev/Cliente — Payins", DATA['rev_per_user_payins_b2b'], '${:,.1f}', COLORS['payins_b2b']),
            ("Rev/Cliente — Total", DATA['rev_per_user_total_b2b'], '${:,.0f}', COLORS['success']),
            ("Take Rate por cliente", DATA['take_rate_per_user_b2b'], '{:.2f}%', COLORS['warning']),
        ]

        for i, (label, values, fmt, color) in enumerate(rows_ue):
            row_bg = "#FAFAFA" if i % 2 == 1 else "#FFFFFF"
            is_total = "Total" in label
            border_style = "border-top:2px solid #E2E8F0;" if is_total else "border-bottom:1px solid #E2E8F0;"
            font_weight = "font-weight:700;" if is_total else ""
            avg_val = sum(values) / 4

            table_html_ue += f'<tr style="background:{row_bg}; {border_style}">'
            table_html_ue += f'<td style="padding:0.4rem 0.3rem; {font_weight}">{label}</td>'
            for v in values:
                formatted = fmt.format(v) if '%' not in fmt else fmt.format(v)
                table_html_ue += f'<td style="padding:0.4rem 0.3rem; text-align:center; color:{color}; {font_weight}">{formatted}</td>'
            avg_formatted = fmt.format(avg_val) if '%' not in fmt else fmt.format(avg_val)
            table_html_ue += f'<td style="padding:0.4rem 0.3rem; text-align:center; color:#718096; {font_weight}">{avg_formatted}</td>'
            table_html_ue += '</tr>'

        table_html_ue += "</tbody></table>"
        st.markdown(table_html_ue, unsafe_allow_html=True)

    with col_chart:
        # Gráfico de barras apiladas: Revenue por cliente por línea
        fig_ue = go.Figure()
        fig_ue.add_trace(go.Bar(
            x=MESES, y=DATA['rev_per_user_payouts_b2b'],
            name='Payouts', marker_color=COLORS['payouts_b2b']))
        fig_ue.add_trace(go.Bar(
            x=MESES, y=DATA['rev_per_user_exchange_b2b'],
            name='Exchange', marker_color=COLORS['exchange']))
        fig_ue.add_trace(go.Bar(
            x=MESES, y=DATA['rev_per_user_payins_b2b'],
            name='Payins', marker_color=COLORS['payins_b2b']))
        fig_ue = plotly_theme(fig_ue, height=300)
        fig_ue.update_layout(
            barmode='stack',
            yaxis_title="Revenue/Cliente (USD)",
            yaxis_tickformat='$,.0f',
            title=dict(text='Revenue/Cliente B2B por Línea', font=dict(size=14, color=COLORS['text'])),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_ue, use_container_width=True)

    # Insight Box - Respuesta al Reto
    # Calcular variables para el insight box
    churn_avg = AVG_CHURN_B2B_SAFE * 100  # churn promedio como porcentaje
    arpu_payouts_display = BASE_ARPU_PAYOUTS_B2B  # ARPU solo Payouts
    cltv_b2b = BASE_CLTV_B2B
    vida_meses = 1 / AVG_CHURN_B2B_SAFE if AVG_CHURN_B2B_SAFE > 0 else 0
    mrr_b2b = BASE_MRR_B2B

    st.markdown(f"""
    <div style="background:linear-gradient(135deg, rgba(0, 201, 167, 0.06), rgba(0, 102, 255, 0.06));
                border-radius:12px; padding:1.25rem; margin-top:1rem; border:1px solid rgba(0, 201, 167, 0.2);">
        <div style="display:flex; align-items:flex-start; gap:0.75rem;">
            <div style="font-size:1.5rem;">💡</div>
            <div>
                <div style="font-weight:700; color:#2D3748; margin-bottom:0.5rem; font-size:1.05rem;">
                    Metodología CLTV/MRR — Respuesta al Reto (Punto 5)
                </div>
                <div style="font-size:0.92rem; color:#4A5568; line-height:1.7;">
                    <strong>¿Cómo estimo CLTV?</strong><br>
                    ARPU calculado exclusivamente sobre Revenue Payouts B2B (${arpu_payouts_display:,.0f}/mes),
                    consistente con la base de clientes derivada de Payouts ({BASE['users_b2b']:.0f} usuarios).
                    Dividido por el churn mensual promedio ({churn_avg:.2f}%) de los 4 meses analizados.
                    El CLTV de ${cltv_b2b/1000:,.0f}K implica una vida útil de ~{vida_meses:.0f} meses
                    ({vida_meses/12:.1f} años), consistente con los 6 años de operación de Vita.<br><br>
                    <strong>¿Por qué solo Payouts para CLTV?</strong><br>
                    Exchange (${BASE['rev_per_user_exchange_b2b']:,.0f}/mes) y Payins (${BASE['rev_per_user_payins_b2b']:,.1f}/mes)
                    son oportunidad de cross-sell pero no se incluyen en el cálculo base para evitar mezclar universos de datos.
                    <em style="color:{COLORS['success']};">Incluyendo todo, el ARPU total alcanza ${BASE_ARPU_TOTAL_B2B:,.0f}/mes — upside de {CROSS_SELL_UPSIDE:.0f}%.</em><br><br>
                    <strong>¿Por qué Rev/Cliente y no Rev/TX?</strong><br>
                    No tenemos número de transacciones individual, pero el ticket mensual acumulado
                    (${BASE['avg_gtv_user_b2b']/1000:,.0f}K GTV/cliente/mes) captura el comportamiento
                    completo. Un cliente que hace 3 TX de $50K o 1 TX de $150K genera revenue similar.<br><br>
                    <strong>Oportunidad de cross-sell:</strong>
                    Si el 30% de clientes B2B usa Payins a ${BASE['rev_per_user_payouts_b2b']*0.5:,.0f}/mes,
                    el MRR sube ~${BASE['users_b2b']*0.3*BASE['rev_per_user_payouts_b2b']*0.5/1000:,.0f}K adicionales.
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Nota de limitación de datos B2C
    st.markdown(f"""
    <div style="background:#1A1D23; border-radius:10px; padding:0.8rem; margin-top:1rem;
        border-left:4px solid {COLORS['warning']};">
        <span style="font-size:0.82rem; color:#DFE6E9;">
            <b style="color:{COLORS['warning']};">Nota:</b>
            Solo disponemos de GTV promedio por usuario para Payouts B2B —
            sin este dato para B2C, Exchange y Payins no es posible derivar
            usuarios activos, ARPU ni MRR para esas líneas.
        </span>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# PAGE 4: COST STRUCTURE & P&L
# ══════════════════════════════════════════════════════════════
with tab_costs:
    st.markdown('<div class="page-title">Cost Structure & P&L</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Disciplina financiera y palancas de eficiencia</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown('<div class="section-header">Waterfall P&L — Run-Rate (Promedio M1-M4)</div>', unsafe_allow_html=True)
        # Usar promedios M1-M4 en lugar de solo M4
        rev = np.mean(DATA['revenue'])
        cogs_v = np.mean(DATA['cogs'])
        gross = rev - cogs_v
        personal_avg = np.mean(DATA['personal'])
        marketing_avg = np.mean(DATA['marketing'])
        admin_avg = np.mean(DATA['admin'])
        tax_avg = np.mean(DATA['tax'])
        banking_avg = np.mean(DATA['banking'])
        inv_avg = np.mean(DATA['inversiones'])
        gastos_avg = np.mean(DATA['gastos'])
        net = rev - gastos_avg

        fig = go.Figure(go.Waterfall(
            name="P&L", orientation="v",
            measure=["absolute","relative","total","relative","relative","relative","relative","relative","relative","total"],
            x=["Revenue","COGS","Gross Profit","Personal","Marketing","Admin","Impuestos","Banking","Inversiones","Net Income"],
            y=[rev, -cogs_v, gross, -personal_avg, -marketing_avg, -admin_avg, -tax_avg, -banking_avg, -inv_avg, net],
            connector={"line":{"color":"#E2E8F0"}},
            increasing={"marker":{"color":COLORS['success']}},
            decreasing={"marker":{"color":COLORS['danger']}},
            totals={"marker":{"color":COLORS['primary']}},
            text=[format_k(v) for v in [rev, cogs_v, gross, personal_avg, marketing_avg, admin_avg, tax_avg, banking_avg, inv_avg, net]],
            textposition="outside", textfont=dict(size=15, family='Plus Jakarta Sans')))
        fig = plotly_theme(fig, height=420)
        fig.update_layout(showlegend=False)
        fig.update_yaxes(range=[-50000, 420000])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown(f"""
        <div style="background:#FFFFFF; border-radius:12px; padding:1.2rem; margin-top:2.5rem; border:1px solid #E2E8F0; box-shadow: 0 1px 3px rgba(0,0,0,0.04);">
            <div style="font-weight:700; margin-bottom:1rem; color:#2D3748;">📊 Run-Rate Breakdown (Promedio M1-M4)</div>
            <div style="display:flex; justify-content:space-between; padding:0.4rem 0; border-bottom:1px solid #E2E8F0;">
                <span style="color:#718096;">Revenue</span>
                <span style="color:#00D68F; font-weight:600;">{format_k(rev)}</span>
            </div>
            <div style="display:flex; justify-content:space-between; padding:0.4rem 0; border-bottom:1px solid #E2E8F0;">
                <span style="color:#718096;">COGS</span>
                <span style="color:#FF6B6B;">-{format_k(cogs_v)} ({cogs_v/rev*100:.0f}%)</span>
            </div>
            <div style="display:flex; justify-content:space-between; padding:0.4rem 0; border-bottom:1px solid #E2E8F0;">
                <span style="font-weight:600;">Gross Profit</span>
                <span style="color:#00D68F; font-weight:600;">{format_k(gross)} ({gross/rev*100:.0f}%)</span>
            </div>
            <div style="display:flex; justify-content:space-between; padding:0.4rem 0; border-bottom:1px solid #E2E8F0;">
                <span style="color:#718096;">Personal</span>
                <span style="color:#FF6B6B;">-{format_k(personal_avg)} ({personal_avg/rev*100:.0f}%)</span>
            </div>
            <div style="display:flex; justify-content:space-between; padding:0.4rem 0; border-bottom:1px solid #E2E8F0;">
                <span style="color:#718096;">Marketing</span>
                <span style="color:#FF6B6B;">-{format_k(marketing_avg)} ({marketing_avg/rev*100:.0f}%)</span>
            </div>
            <div style="display:flex; justify-content:space-between; padding:0.4rem 0; border-bottom:1px solid #E2E8F0;">
                <span style="color:#718096;">Admin + Tax + Bank</span>
                <span style="color:#FF6B6B;">-{format_k(admin_avg + tax_avg + banking_avg)}</span>
            </div>
            <div style="display:flex; justify-content:space-between; padding:0.6rem 0; margin-top:0.3rem;">
                <span style="font-weight:700; font-size:1.1rem;">Net Income</span>
                <span style="color:#00D68F; font-weight:700; font-size:1.1rem;">{format_k(net)} ({net/rev*100:.0f}%)</span>
            </div>
        </div>
        <div style="background:#FFFFFF; border-radius:12px; padding:1rem; margin-top:1rem; border:1px solid #E2E8F0; border-left:4px solid {COLORS['primary']}; box-shadow: 0 1px 3px rgba(0,0,0,0.04);">
            <div style="font-weight:700; color:{COLORS['primary']}; margin-bottom:0.3rem;">💡 Cash Conversion — Estructura de Fondos</div>
            <div style="font-size:0.95rem; color:#4A5568; line-height:1.6;">
                M3: P&L $94K pero Cash +$490K. La diferencia refleja el <strong>float operativo</strong> — fondos de clientes
                en tránsito que transitan por las cuentas de Vita.<br>
                Como entidad de pago regulada, estos fondos están <strong>segregados y no son invertibles</strong>.<br>
                <span style="color:#718096;">La oportunidad no es float income sino ofrecer remuneración de saldos como herramienta de retención.</span>
            </div>
        </div>""", unsafe_allow_html=True)
    
    # Cost evolution
    st.markdown('<div class="section-header">Estructura de Costos — Evolución</div>', unsafe_allow_html=True)
    fig = go.Figure()
    for name, values, color in [
        ('Personal', DATA['personal'], COLORS['primary']),
        ('COGS', DATA['cogs'], COLORS['danger']),
        ('Marketing', DATA['marketing'], COLORS['accent']),
        ('Admin', DATA['admin'], COLORS['secondary']),
        ('Impuestos', DATA['tax'], COLORS['warning']),
        ('Banking', DATA['banking'], COLORS['muted']),
    ]:
        fig.add_trace(go.Bar(name=name, x=MESES, y=values, marker_color=color))
    fig.update_layout(barmode='stack')
    fig = plotly_theme(fig, height=380)
    fig.update_layout(yaxis_title="USD/mes")
    st.plotly_chart(fig, use_container_width=True)
    
    # Efficiency - usando promedios M1-M4
    st.markdown('<div class="section-header">Métricas de Eficiencia (Run-Rate Promedio M1-M4)</div>', unsafe_allow_html=True)
    avg_rev = np.mean(DATA['revenue'])
    avg_gastos = np.mean(DATA['gastos'])
    avg_hc = np.mean(DATA['headcount'])
    avg_mktg = np.mean(DATA['marketing'])
    avg_net = avg_rev - avg_gastos  # ~$72K/mes

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(metric_card("Rev / Employee", format_k(avg_rev / avg_hc), delta="Target: $15K", delta_dir="down"), unsafe_allow_html=True)
    with c2:
        st.markdown(metric_card("Marketing Efficiency", f"{avg_rev / avg_mktg:.1f}x", delta="Target: >10x", delta_dir="down"), unsafe_allow_html=True)
    with c3:
        st.markdown(metric_card("OpEx Ratio", f"{avg_gastos / avg_rev * 100:.0f}%", delta="Target: <60%", delta_dir="down"), unsafe_allow_html=True)
    with c4:
        st.markdown(metric_card("Generación de Caja", format_k(avg_net) + "/mes", delta="Cash flow positivo 3 de 4 meses", delta_dir="up"), unsafe_allow_html=True)

    # Presupuesto por Área
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">📋 PRESUPUESTO POR ÁREA ORGANIZACIONAL</div>', unsafe_allow_html=True)

    col_chart, col_insight = st.columns([3, 2])
    with col_chart:
        areas = ['Growth', 'Desarrollo', 'Operaciones', 'Finanzas', 'Compliance', 'Legales', 'RRHH', 'BI']
        pct_area = [20, 20, 20, 20, 8, 5, 5, 2]
        colores_area = [COLORS['success'], COLORS['secondary'], COLORS['primary'], COLORS['warning'],
                        '#9F7AEA', '#ED8936', '#4FD1C5', '#A0AEC0']

        fig = go.Figure()
        for area, pct, color in zip(areas, pct_area, colores_area):
            fig.add_trace(go.Bar(
                y=[area], x=[pct], orientation='h', marker_color=color,
                text=[f"{pct}%"], textposition='inside', textfont=dict(size=14, color='white'),
                showlegend=False
            ))
        fig = plotly_theme(fig, height=350)
        fig.update_layout(
            xaxis_title="% del Presupuesto Total",
            yaxis=dict(autorange="reversed", categoryorder='array', categoryarray=areas),
            bargap=0.3
        )
        fig.update_xaxes(range=[0, 25])
        st.plotly_chart(fig, use_container_width=True)

    with col_insight:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg, rgba(0, 102, 255, 0.06), rgba(0, 201, 167, 0.06));
                    border-radius:12px; padding:1.25rem; border:1px solid rgba(0, 102, 255, 0.15);">
            <div style="display:flex; align-items:flex-start; gap:0.75rem;">
                <div style="font-size:1.3rem;">💡</div>
                <div>
                    <div style="font-weight:600; color:#2D3748; margin-bottom:0.5rem; font-size:1.05rem;">Distribución del Presupuesto</div>
                    <div style="font-size:0.95rem; color:#4A5568; line-height:1.6;">
                        Cuatro áreas concentran el <strong>80% del presupuesto</strong> en partes iguales
                        (Growth, Desarrollo, Operaciones, Finanzas). Esta distribución refleja la filosofía
                        de equilibrio entre crecimiento e infraestructura.<br><br>
                        <strong>Oportunidades:</strong><br>
                        <span style="color:{COLORS['warning']};">①</span> BI con solo 2% podría estar subinvertido dado el valor de data analytics
                        para decisiones de pricing y retención<br>
                        <span style="color:{COLORS['warning']};">②</span> Compliance al 8% es adecuado para el stage regulatorio actual pero
                        podría necesitar incremento con 3 nuevos países
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Gestión de Riesgos
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">⚠️ GESTIÓN DE RIESGOS AL ESCALAR — DE $51M A $150M+ GTV MENSUAL</div>', unsafe_allow_html=True)

    risk1, risk2, risk3 = st.columns(3)

    with risk1:
        st.markdown(f"""
        <div style="background:#FFFFFF; border-radius:12px; padding:1.25rem; border:1px solid #E2E8F0;
                    border-top:4px solid {COLORS['danger']}; box-shadow: 0 1px 3px rgba(0,0,0,0.04); height:100%;">
            <div style="font-weight:700; color:{COLORS['danger']}; margin-bottom:0.6rem; font-size:1.05rem;">
                💱 Descalce de Monedas
            </div>
            <div style="font-size:0.9rem; color:#4A5568; line-height:1.6;">
                Hoy Vita opera ~$51M/mes en GTV multi-moneda (CLP, COP, ARS, MXN, USD). Al triplicar volumen,
                la exposición a descalces crece de forma no lineal. Un movimiento adverso de 1% en tipo de cambio
                sobre $150M de GTV = <strong>$1.5M de exposición potencial</strong>.<br><br>
                <strong style="color:{COLORS['success']};">Mitigación:</strong><br>
                ① Calce intradiario estricto por moneda<br>
                ② Hedging con forwards sobre exposiciones netas<br>
                ③ Límites de exposición con alertas automatizadas<br>
                ④ Reducción del settlement window
            </div>
        </div>
        """, unsafe_allow_html=True)

    with risk2:
        st.markdown(f"""
        <div style="background:#FFFFFF; border-radius:12px; padding:1.25rem; border:1px solid #E2E8F0;
                    border-top:4px solid {COLORS['warning']}; box-shadow: 0 1px 3px rgba(0,0,0,0.04); height:100%;">
            <div style="font-weight:700; color:{COLORS['warning']}; margin-bottom:0.6rem; font-size:1.05rem;">
                💧 Gestión de Caja y Float
            </div>
            <div style="font-size:0.9rem; color:#4A5568; line-height:1.6;">
                El float operativo (fondos de clientes en tránsito) está segregado regulatoriamente, pero genera riesgo de liquidez.
                Al escalar, la caja para cubrir payouts crece proporcionalmente, pero los peaks son no lineales —
                un día de alto volumen puede requerir <strong>3-4x la liquidez promedio</strong>.<br><br>
                <strong style="color:{COLORS['success']};">Mitigación:</strong><br>
                ① Modelo de proyección de liquidez por corredor<br>
                ② Líneas de crédito pre-aprobadas como backstop<br>
                ③ Diversificación de proveedores por país<br>
                ④ Buffer mínimo basado en percentil 95
            </div>
        </div>
        """, unsafe_allow_html=True)

    with risk3:
        st.markdown(f"""
        <div style="background:#FFFFFF; border-radius:12px; padding:1.25rem; border:1px solid #E2E8F0;
                    border-top:4px solid {COLORS['secondary']}; box-shadow: 0 1px 3px rgba(0,0,0,0.04); height:100%;">
            <div style="font-weight:700; color:{COLORS['secondary']}; margin-bottom:0.6rem; font-size:1.05rem;">
                ⚙️ Complejidad Operacional
            </div>
            <div style="font-size:0.9rem; color:#4A5568; line-height:1.6;">
                Pasar de 4 países a 7, con 3× volumen, multiplica la complejidad: más contrapartes bancarias,
                más regulaciones, más puntos de falla. Las transacciones rechazadas ya muestran tendencia al alza
                (<strong>1,387 → 2,245</strong>).<br><br>
                <strong style="color:{COLORS['success']};">Mitigación:</strong><br>
                ① Automatización de compliance y reconciliación<br>
                ② Monitoreo real-time de tasas de rechazo<br>
                ③ Redundancia en proveedores por país<br>
                ④ Inversión en BI (hoy solo 2%) para detección temprana
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Insight box - La carta ganadora
    st.markdown(f"""
    <div style="background:linear-gradient(135deg, rgba(255, 107, 107, 0.08), rgba(0, 102, 255, 0.08));
                border-radius:12px; padding:1.25rem; border:1px solid rgba(255, 107, 107, 0.2);">
        <div style="display:flex; align-items:flex-start; gap:0.75rem;">
            <div style="font-size:1.5rem;">🎯</div>
            <div>
                <div style="font-weight:700; color:#2D3748; margin-bottom:0.4rem; font-size:1.05rem;">
                    El Rol Crítico del CFO en la Gestión de Riesgo a Escala
                </div>
                <div style="font-size:0.95rem; color:#4A5568; line-height:1.7;">
                    Esta es precisamente el área donde un CFO con experiencia en <strong>mercados financieros y derivados</strong>
                    agrega valor diferencial. La gestión de riesgo cambiario, liquidez y operacional a escala
                    <em>no es un problema contable — es un problema de trading desk y treasury</em>.<br><br>
                    Vita al triplicar volumen pasa de una operación manejable intuitivamente a una que requiere
                    <strong>frameworks formales de gestión de riesgo</strong>, límites, y monitoreo en tiempo real.
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# PAGE 5: PROPUESTAS ESTRATÉGICAS
# ══════════════════════════════════════════════════════════════
with tab_strat:
    st.markdown('<div class="page-title">Propuestas Estratégicas</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Plan concreto por línea de negocio — 12 meses de ejecución</div>', unsafe_allow_html=True)
    
    # ═══════════════════════════════════════════════════════════
    # PAYOUTS B2B - Sección personalizada
    # ═══════════════════════════════════════════════════════════
    st.markdown(f"""
    <div class="proposal-card" style="border-left:4px solid {COLORS['payouts_b2b']};">
        <div style="display:flex; align-items:center; gap:0.8rem; margin-bottom:0.5rem;">
            <span class="proposal-badge" style="background:{COLORS['payouts_b2b']}22; color:{COLORS['payouts_b2b']}; border:1px solid {COLORS['payouts_b2b']}44;">CORE · DEFENDER MARGEN · ×1.8</span>
            <span style="font-size:1.1rem; font-weight:700; color:{COLORS['payouts_b2b']};">Payouts B2B</span>
            <span style="margin-left:auto; font-size:1.05rem; color:#718096;">
                $265K/mes → <strong style="color:#2D3748;">$477K/mes</strong>
            </span>
        </div>
        <div style="font-size:1rem; color:#4A5568; margin-bottom:1rem; font-style:italic;">
            No competir en precio — hacer que el precio sea irrelevante con servicios de valor agregado para top 50 clientes.
        </div>
        <div style="display:grid; gap:0.5rem;">
            <div style="background:#F7FAFC; border-radius:8px; padding:0.6rem 1rem; border-left:3px solid {COLORS['primary']};">
                <strong style="color:{COLORS['primary']};">Forwards FX</strong> — Doble fuente de margen: spread en spot + spread en puntos forward. Los puntos forward tienen menor transparencia de mercado, permitiendo marginar con menos presión competitiva. Spread 0.15-0.25% total.
            </div>
            <div style="background:#F7FAFC; border-radius:8px; padding:0.6rem 1rem; border-left:3px solid {COLORS['secondary']};">
                <strong style="color:{COLORS['secondary']};">Reportería Treasury</strong> — Dashboard automático: posición por moneda, TC obtenido vs benchmark, resumen mensual.
            </div>
            <div style="background:#F7FAFC; border-radius:8px; padding:0.6rem 1rem; border-left:3px solid {COLORS['warning']};">
                <strong style="color:{COLORS['warning']};">Alertas FX</strong> — Notificación al cruzar umbrales de TC + ejecución automática opcional.
            </div>
            <div style="background:#F7FAFC; border-radius:8px; padding:0.6rem 1rem; border-left:3px solid {COLORS['success']};">
                <strong style="color:{COLORS['success']};">Pagos programados</strong> — Automatización de pagos recurrentes con TC spot o forward pre-acordado.
            </div>
            <div style="background:#F7FAFC; border-radius:8px; padding:0.6rem 1rem; border-left:3px solid {COLORS['muted']};">
                <strong style="color:#718096;">Corredores asiáticos</strong> — Evaluar corredor directo LatAm-CNY/JPY para importadores. Estudio de viabilidad meses 6-9.
            </div>
            <div style="background:#F7FAFC; border-radius:8px; padding:0.6rem 1rem; border-left:3px solid #A0AEC0;">
                <strong style="color:#718096;">Intermediación de saldos</strong> — Remuneración de saldos USD vía tercero. Revenue marginal, pero incentiva al cliente a mantener fondos en la plataforma y genera conversiones FX.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background:linear-gradient(135deg, rgba(0, 201, 167, 0.06), rgba(0, 102, 255, 0.06));
                border-radius:8px; padding:0.8rem 1rem; margin-bottom:1.5rem; border:1px solid rgba(0, 201, 167, 0.15);">
        <span style="font-size:0.9rem; color:#4A5568;">
            💡 <strong>Estos servicios son implementables con infraestructura existente.</strong> Bajo costo, alto impacto en retención y defensa de margen.
        </span>
    </div>
    """, unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════
    # PAYOUTS B2C - Sección personalizada
    # ═══════════════════════════════════════════════════════════
    st.markdown(f"""
    <div class="proposal-card" style="border-left:4px solid {COLORS['payouts_b2c']};">
        <div style="display:flex; align-items:center; gap:0.8rem; margin-bottom:0.5rem;">
            <span class="proposal-badge" style="background:{COLORS['payouts_b2c']}22; color:{COLORS['payouts_b2c']}; border:1px solid {COLORS['payouts_b2c']}44;">GROWTH · ESPAÑA GAME CHANGER · ×2.5</span>
            <span style="font-size:1.1rem; font-weight:700; color:{COLORS['payouts_b2c']};">Payouts B2C</span>
            <span style="margin-left:auto; font-size:1.05rem; color:#718096;">
                $40K/mes → <strong style="color:#2D3748;">$100K/mes</strong>
            </span>
        </div>
        <div style="font-size:1rem; color:#4A5568; margin-bottom:1rem;">
            Dos estrategias distintas según país:
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:1rem;">
            <div style="background:{COLORS['success']}11; border-radius:10px; padding:1rem; border:1px solid {COLORS['success']}33;">
                <div style="font-weight:700; color:{COLORS['success']}; margin-bottom:0.5rem;">🌎 Bolivia y Perú</div>
                <div style="font-size:0.9rem; color:#4A5568; line-height:1.5;">
                    <strong>Receptores complementarios.</strong> Sociedades ya constituidas. Amplían red de destino para usuarios existentes.
                </div>
            </div>
            <div style="background:{COLORS['accent']}11; border-radius:10px; padding:1rem; border:1px solid {COLORS['accent']}33;">
                <div style="font-weight:700; color:{COLORS['accent']}; margin-bottom:0.5rem;">🇪🇸 España — Game Changer</div>
                <div style="font-size:0.9rem; color:#4A5568; line-height:1.5;">
                    <strong>Corredor remesas Europa→LatAm.</strong> Comunidad latina masiva, envíos mensuales recurrentes.
                    Incumbentes cobran 5-8%, Vita puede ofrecer <strong>1-2%</strong>.
                    Licencia de entidad de pago ya constituida.
                    <em>Vita Card cierra el loop: remesa → app → gasto directo.</em>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════
    # PAYINS B2B - Sección personalizada
    # ═══════════════════════════════════════════════════════════
    st.markdown(f"""
    <div class="proposal-card" style="border-left:4px solid {COLORS['payins_b2b']};">
        <div style="display:flex; align-items:center; gap:0.8rem; margin-bottom:0.5rem;">
            <span class="proposal-badge" style="background:{COLORS['payins_b2b']}22; color:{COLORS['payins_b2b']}; border:1px solid {COLORS['payins_b2b']}44;">STAR · EXPORTADORES · ×18</span>
            <span style="font-size:1.1rem; font-weight:700; color:{COLORS['payins_b2b']};">Payins B2B</span>
            <span style="margin-left:auto; font-size:1.05rem; color:#718096;">
                $7K/mes → <strong style="color:#2D3748;">$120K/mes</strong>
            </span>
        </div>
        <div style="font-size:1rem; color:#4A5568; margin-bottom:1rem; font-style:italic;">
            Propuesta de valor: velocidad de acreditación, transparencia y costos menores que banca tradicional. El exportador recibe USD y puede operar desde la cuenta en USA.
        </div>
        <div style="display:grid; gap:0.5rem;">
            <div style="background:#F7FAFC; border-radius:8px; padding:0.6rem 1rem; border-left:3px solid {COLORS['success']};">
                <strong style="color:{COLORS['success']};">Monetización principal</strong> — Revenue viene cuando el exportador convierte USD → moneda local para gastos operativos (sueldos, impuestos, proveedores). Sin conversión FX, el margen es solo transaccional.
            </div>
            <div style="background:#F7FAFC; border-radius:8px; padding:0.6rem 1rem; border-left:3px solid {COLORS['primary']};">
                <strong style="color:{COLORS['primary']};">Cross-sell Forwards</strong> — Fijar TC para conversiones programadas. El exportador que sabe que necesita CLP cada mes es candidato natural. Acá se captura el doble margen (spot + forward points).
            </div>
            <div style="background:#F7FAFC; border-radius:8px; padding:0.6rem 1rem; border-left:3px solid {COLORS['warning']};">
                <strong style="color:{COLORS['warning']};">Riesgo a gestionar</strong> — Cliente que usa Vita solo como pasarela USD→USD genera volumen pero bajo margen. Clave: incentivar conversión dentro de la plataforma.
            </div>
            <div style="background:#F7FAFC; border-radius:8px; padding:0.6rem 1rem; border-left:3px solid {COLORS['muted']};">
                <strong style="color:{COLORS['muted']};">Sobre el multiplicador ×18</strong> — Multiplicador alto sobre base pequeña ($6.6K). El target real es $120K/mes — equivale a ~$18M de GTV mensual en Payins, plausible con exportadores de Chile y Colombia. El producto creció ×4.3 en su primer mes activo (M3→M4).
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background:linear-gradient(135deg, rgba(159, 122, 234, 0.08), rgba(0, 102, 255, 0.06));
                border-radius:8px; padding:0.8rem 1rem; margin-bottom:1.5rem; border:1px solid rgba(159, 122, 234, 0.2);">
        <span style="font-size:0.9rem; color:#4A5568;">
            💡 <strong>Payins B2B es una estrategia de adquisición de clientes de alto valor.</strong> La monetización no está en el payin mismo sino en la cadena de servicios posteriores: conversión FX, forwards, reportería. Un exportador que convierte $200K/mes a CLP genera ~$1,000-$1,300 en revenue recurrente.
        </span>
    </div>
    """, unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════
    # CRYPTO EXCHANGE - Sección personalizada
    # ═══════════════════════════════════════════════════════════
    st.markdown(f"""
    <div class="proposal-card" style="border-left:4px solid {COLORS['exchange']};">
        <div style="display:flex; align-items:center; gap:0.8rem; margin-bottom:0.5rem;">
            <span class="proposal-badge" style="background:{COLORS['exchange']}22; color:{COLORS['exchange']}; border:1px solid {COLORS['exchange']}44;">ESTRATÉGICO · GRANTS ECOSISTEMA · ×2.0</span>
            <span style="font-size:1.1rem; font-weight:700; color:{COLORS['exchange']};">Crypto Exchange</span>
            <span style="margin-left:auto; font-size:1.05rem; color:#718096;">
                $49K/mes → <strong style="color:#2D3748;">$98K/mes</strong>
            </span>
        </div>
        <div style="font-size:1rem; color:#4A5568; margin-bottom:1rem; font-style:italic;">
            Margen transaccional thin (0.08%), pero el volumen en USDC/USDT posiciona a Vita para acceder a grants de ecosistemas blockchain (Circle, Tether, Stellar, entre otros). Estos programas premian volumen y adopción con funding no-dilutivo.
        </div>
        <div style="display:grid; gap:0.5rem;">
            <div style="background:#F7FAFC; border-radius:8px; padding:0.6rem 1rem; border-left:3px solid {COLORS['success']};">
                <strong style="color:{COLORS['success']};">Grants como revenue</strong> — Ecosistemas crypto destinan fondos significativos a partners que mueven volumen. A mayor GTV crypto de Vita, mayor elegibilidad.
            </div>
            <div style="background:#F7FAFC; border-radius:8px; padding:0.6rem 1rem; border-left:3px solid {COLORS['secondary']};">
                <strong style="color:{COLORS['secondary']};">Stablecoin corridors B2B</strong> — Pagos corporativos cross-border vía USDC como alternativa al SWIFT. Más rápido, más barato, trazable. Crece el volumen y el caso de uso.
            </div>
            <div style="background:#F7FAFC; border-radius:8px; padding:0.6rem 1rem; border-left:3px solid {COLORS['primary']};">
                <strong style="color:{COLORS['primary']};">Estrategia dual</strong> — El exchange genera margen modesto por sí solo, pero habilita grants + partnerships preferenciales + mejor pricing de liquidez. Métrica clave: GTV crypto, no margen.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background:linear-gradient(135deg, rgba(237, 137, 54, 0.08), rgba(0, 201, 167, 0.06));
                border-radius:8px; padding:0.8rem 1rem; margin-bottom:1.5rem; border:1px solid rgba(237, 137, 54, 0.2);">
        <span style="font-size:0.9rem; color:#4A5568;">
            💡 <strong>No evaluar Exchange solo por su margen directo.</strong> Es la llave de acceso a un ecosistema de funding que puede aportar revenue no-dilutivo significativo.
        </span>
    </div>
    """, unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════
    # FORWARDS FX - Sección personalizada
    # ═══════════════════════════════════════════════════════════
    st.markdown(f"""
    <div class="proposal-card" style="border-left:4px solid {COLORS['forwards']};">
        <div style="display:flex; align-items:center; gap:0.8rem; margin-bottom:0.5rem;">
            <span class="proposal-badge" style="background:{COLORS['forwards']}22; color:{COLORS['forwards']}; border:1px solid {COLORS['forwards']}44;">🆕 NUEVO · DOBLE MARGEN · HIGH VALUE</span>
            <span style="font-size:1.1rem; font-weight:700; color:{COLORS['forwards']};">Forwards FX</span>
            <span style="margin-left:auto; font-size:1.05rem; color:#718096;">
                $0/mes → <strong style="color:#2D3748;">$45K/mes</strong>
            </span>
        </div>
        <div style="font-size:1rem; color:#4A5568; margin-bottom:1rem; font-style:italic;">
            Contratos forward para fijar tipo de cambio a 30-180 días. Modelo back-to-back con banco contraparte: Vita captura spread sin tomar posición propia de riesgo.
        </div>
        <div style="display:grid; gap:0.5rem;">
            <div style="background:#F7FAFC; border-radius:8px; padding:0.6rem 1rem; border-left:3px solid {COLORS['success']};">
                <strong style="color:{COLORS['success']};">Doble fuente de margen</strong> — Spread en spot + spread en puntos forward. Los puntos forward tienen menor transparencia de mercado, permitiendo marginar con menos presión competitiva. Total: 0.15-0.25%.
            </div>
            <div style="background:#F7FAFC; border-radius:8px; padding:0.6rem 1rem; border-left:3px solid {COLORS['secondary']};">
                <strong style="color:{COLORS['secondary']};">Clientes naturales</strong> — Importadores con pagos recurrentes + exportadores con conversiones programadas. Cross-sell directo desde Payouts B2B y Payins B2B.
            </div>
            <div style="background:#F7FAFC; border-radius:8px; padding:0.6rem 1rem; border-left:3px solid {COLORS['warning']};">
                <strong style="color:{COLORS['warning']};">Implementación</strong> — Regulatorio ya cubierto (Intermediario IF). Requiere +1 especialista en trading desk. Riesgo crédito del cliente mitigado con margen inicial + modelo DVP.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background:linear-gradient(135deg, rgba(52, 152, 219, 0.08), rgba(0, 201, 167, 0.06));
                border-radius:8px; padding:0.8rem 1rem; margin-bottom:1.5rem; border:1px solid rgba(52, 152, 219, 0.2);">
        <span style="font-size:0.9rem; color:#4A5568;">
            💡 <strong>Forwards FX es el producto de mayor margen por transacción.</strong> Diferenciador vs bancos: plataforma tech, mejor pricing, ejecución más rápida. El cliente B2B que ya usa Vita para pagos es el candidato natural.
        </span>
    </div>
    """, unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════
    # VITA CARD - Sección personalizada
    # ═══════════════════════════════════════════════════════════
    st.markdown(f"""
    <div class="proposal-card" style="border-left:4px solid {COLORS['vita_card']};">
        <div style="display:flex; align-items:center; gap:0.8rem; margin-bottom:0.5rem;">
            <span class="proposal-badge" style="background:{COLORS['vita_card']}22; color:{COLORS['vita_card']}; border:1px solid {COLORS['vita_card']}44;">🆕 NUEVO · ENGAGEMENT · CIERRA EL LOOP</span>
            <span style="font-size:1.1rem; font-weight:700; color:{COLORS['vita_card']};">Vita Card</span>
            <span style="margin-left:auto; font-size:1.05rem; color:#718096;">
                $0/mes → <strong style="color:#2D3748;">$40K/mes</strong>
            </span>
        </div>
        <div style="font-size:1rem; color:#4A5568; margin-bottom:1rem; font-style:italic;">
            Tarjeta para compras internacionales con comisión FX integrada. Cierra el loop del ecosistema: el usuario recibe remesa, mantiene saldo, y gasta directamente con la tarjeta.
        </div>
        <div style="display:grid; gap:0.5rem;">
            <div style="background:#F7FAFC; border-radius:8px; padding:0.6rem 1rem; border-left:3px solid {COLORS['success']};">
                <strong style="color:{COLORS['success']};">Reactivación B2C</strong> — Reactiva usuarios dormidos de Payouts B2C. Aumenta frecuencia de uso y lifetime value.
            </div>
            <div style="background:#F7FAFC; border-radius:8px; padding:0.6rem 1rem; border-left:3px solid {COLORS['secondary']};">
                <strong style="color:{COLORS['secondary']};">España synergy</strong> — Para el corredor de remesas Europa→LatAm, la tarjeta permite al receptor gastar sin necesidad de cuenta bancaria local. Diferenciador vs competencia.
            </div>
            <div style="background:#F7FAFC; border-radius:8px; padding:0.6rem 1rem; border-left:3px solid {COLORS['warning']};">
                <strong style="color:{COLORS['warning']};">Implementación</strong> — Requiere alianza con emisor (Visa/Mastercard partner). Timeline estimado: 6-9 meses. Producto de engagement más que de margen directo.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background:linear-gradient(135deg, rgba(229, 62, 62, 0.08), rgba(237, 137, 54, 0.06));
                border-radius:8px; padding:0.8rem 1rem; margin-bottom:1.5rem; border:1px solid rgba(229, 62, 62, 0.2);">
        <span style="font-size:0.9rem; color:#4A5568;">
            💡 <strong>Vita Card completa el ecosistema.</strong> Remesa → Saldo en app → Gasto con tarjeta. Sin salir de Vita. Aumenta retención, frecuencia y LTV del usuario B2C.
        </span>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# PAGE 6: SCENARIO BUILDER
# ══════════════════════════════════════════════════════════════
with tab_scenario:
    st.markdown('<div class="page-title">Scenario Builder</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Ajusta los parámetros en el panel lateral ← y observa los resultados aquí</div>', unsafe_allow_html=True)

    # Calculate (using variables from sidebar) - BASE = run-rate promedio M1-M4
    base_rev = BASE_REVENUE  # Run-rate promedio, no M4
    # rev_b2b_proj, rev_ex_proj, rev_payins_proj ya vienen calculados del sidebar
    rev_b2c_proj = BASE['rev_payouts_b2c'] * mult_b2c
    rev_pi_proj = rev_payins_proj  # Usa el valor derivado del sidebar (clientes × GTV × take rate)
    total_rev_proj = rev_b2b_proj + rev_b2c_proj + rev_ex_proj + rev_pi_proj + fwd_rev + card_rev

    # ═══════════════════════════════════════════════════════════
    # MODELO DE COSTOS FIJOS/VARIABLES
    # ═══════════════════════════════════════════════════════════

    # --- COSTOS FIJOS (no cambian con revenue) ---
    # Personal: equipo actual + hires nuevos (más caros: senior, nuevos países)
    current_team_cost = 58 * 1836  # equipo actual al costo actual
    new_hires_cost = max(0, hc_target - 58) * 2500  # hires nuevos son más caros
    personal_proj = current_team_cost + new_hires_cost

    # Admin: base fija + step por cada país nuevo
    admin_base = BASE_ADMIN  # promedio M1-M4
    admin_countries = new_countries * 5000  # oficinas, legal, regulatorio
    admin_proj = admin_base + admin_countries

    # Banking e inversiones: fijos
    bank_proj = 18000
    inv_proj = 8000

    # Ahorro AI Sales Agent
    ai_savings = 14000 if ai_on else 0

    # Costo Forwards (si está activo)
    fwd_cost = 4500 if fwd_on else 0

    total_fixed = personal_proj + admin_proj + bank_proj + inv_proj + fwd_cost - ai_savings

    # --- COSTOS VARIABLES (escalan con volumen/revenue) ---
    # COGS: anclado al GTV total (B2B + B2C + Payins)
    # GTV B2B viene del sidebar (gtv_b2b_m16), B2C crece con mult_b2c
    gtv_b2c_m16 = BASE_GTV_B2C * mult_b2c
    gtv_m16 = gtv_b2b_m16 + gtv_b2c_m16 + gtv_payins_m16  # GTV total M16
    cogs_rate = 0.0016  # ~0.16% del GTV (promedio M2-M4)
    cogs_proj = gtv_m16 * cogs_rate

    # Impuestos operativos: ~7.3% del revenue
    tax_proj = total_rev_proj * 0.073

    # Marketing: viene del slider
    mktg_proj = mktg_monthly * 1000

    total_variable = cogs_proj + tax_proj + mktg_proj

    # Total costos M16
    total_gastos_proj = total_fixed + total_variable

    # Ratio fijo/variable
    fixed_ratio = (total_fixed / total_gastos_proj * 100) if total_gastos_proj > 0 else 0
    variable_ratio = (total_variable / total_gastos_proj * 100) if total_gastos_proj > 0 else 0
    
    margin_proj = (total_rev_proj - total_gastos_proj) / total_rev_proj * 100 if total_rev_proj > 0 else 0
    multiple = total_rev_proj / base_rev
    rev_per_emp_proj = total_rev_proj / hc_target
    monthly_net = total_rev_proj - total_gastos_proj

    # Inversión requerida para el plan (CAC, infraestructura, nuevos hires)
    # Usar new_clients_b2b (derivado del sidebar) y clientes Payins
    cac_investment = new_clients_b2b * 1200 + 3000*(mult_b2c-1)*15 + clients_payins_m16 * 2000
    total_investment = cac_investment + 150000 + 150000 + (hc_target-58)*1900*12
    # Nota: cash_proj y gap se recalculan después de la trayectoria para reflejar el modo de contratación

    # Guardar en session_state para que Valuation pueda usarlos
    st.session_state['scenario_rev_m16'] = total_rev_proj
    st.session_state['scenario_margin_m16'] = margin_proj
    st.session_state['scenario_gastos_m16'] = total_gastos_proj
    st.session_state['scenario_multiple'] = multiple
    st.session_state['scenario_gtv_m16'] = gtv_m16
    st.session_state['scenario_ebitda_m16'] = total_rev_proj - total_gastos_proj
    st.session_state['scenario_rev_b2b'] = rev_b2b_proj
    st.session_state['scenario_rev_b2c'] = rev_b2c_proj
    st.session_state['scenario_rev_ex'] = rev_ex_proj
    st.session_state['scenario_rev_pi'] = rev_pi_proj
    st.session_state['scenario_fwd_rev'] = fwd_rev
    st.session_state['scenario_card_rev'] = card_rev
    st.session_state['scenario_clients_b2b'] = clients_b2b_m16
    st.session_state['scenario_clients_payins'] = clients_payins_m16

    # KPI cards
    color = COLORS['success'] if multiple >= 2.5 else COLORS['warning'] if multiple >= 2 else COLORS['danger']
    m_color = COLORS['success'] if margin_proj >= 30 else COLORS['warning'] if margin_proj >= 15 else COLORS['danger']
    re_color = COLORS['success'] if rev_per_emp_proj >= 12000 else COLORS['warning']

    r1, r2, r3 = st.columns(3)
    with r1:
        st.markdown(f"""
        <div class="scenario-output" style="text-align:center;">
            <div class="scenario-big">{format_k(total_rev_proj)}</div>
            <div style="color:#718096; font-size:0.8rem; text-transform:uppercase;">Revenue/mes</div>
            <div style="color:{color}; font-weight:700;">×{multiple:.1f}</div>
        </div>""", unsafe_allow_html=True)
    with r2:
        st.markdown(f"""
        <div class="scenario-output" style="text-align:center;">
            <div class="scenario-big">{margin_proj:.0f}%</div>
            <div style="color:#718096; font-size:0.8rem; text-transform:uppercase;">Margen</div>
            <div style="color:{m_color}; font-weight:700;">{'✅ >30%' if margin_proj >= 30 else '⚠️ <30%'}</div>
        </div>""", unsafe_allow_html=True)
    with r3:
        base_rev_emp_sb = BASE_REVENUE / DATA['headcount'][3]
        st.markdown(f"""
        <div class="scenario-output" style="text-align:center;">
            <div class="scenario-big">{format_k(rev_per_emp_proj)}</div>
            <div style="color:#718096; font-size:0.8rem; text-transform:uppercase;">Rev/Emp</div>
            <div style="color:{re_color}; font-weight:700;">vs {format_k(base_rev_emp_sb)} base</div>
        </div>""", unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════
    # RESUMEN DE CLIENTES — Base vs M16 con Target 3×
    # ═══════════════════════════════════════════════════════════
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">👥 RESUMEN DE CLIENTES</div>', unsafe_allow_html=True)

    # Clientes target 3× (triplicar base)
    target_clients_b2b = BASE['users_b2b'] * 3
    target_clients_payins = 100  # Target para producto nuevo
    pct_target_b2b = (clients_b2b_m16 / target_clients_b2b * 100) if target_clients_b2b > 0 else 0
    pct_target_payins = (clients_payins_m16 / target_clients_payins * 100) if target_clients_payins > 0 else 0

    col_cli1, col_cli2, col_cli3 = st.columns(3)

    with col_cli1:
        cli_color = COLORS['success'] if clients_b2b_m16 >= target_clients_b2b else COLORS['warning']
        st.markdown(f"""
        <div class="scenario-output" style="text-align:center;">
            <div style="font-size:0.75rem; color:{COLORS['muted']}; text-transform:uppercase;">PAYOUTS B2B</div>
            <div style="font-size:2rem; font-weight:800; color:{COLORS['dark']};">{clients_b2b_m16:.0f}</div>
            <div style="font-size:0.85rem; color:{COLORS['muted']};">vs {BASE['users_b2b']:.0f} hoy</div>
            <div style="font-size:0.75rem; color:{cli_color}; font-weight:700;">
                {pct_target_b2b:.0f}% del target 3× ({target_clients_b2b:.0f})
            </div>
        </div>""", unsafe_allow_html=True)

    with col_cli2:
        cli_pi_color = COLORS['success'] if clients_payins_m16 >= target_clients_payins else COLORS['warning']
        st.markdown(f"""
        <div class="scenario-output" style="text-align:center;">
            <div style="font-size:0.75rem; color:{COLORS['muted']}; text-transform:uppercase;">PAYINS B2B</div>
            <div style="font-size:2rem; font-weight:800; color:{COLORS['dark']};">{clients_payins_m16}</div>
            <div style="font-size:0.85rem; color:{COLORS['muted']};">vs ~2 hoy</div>
            <div style="font-size:0.75rem; color:{cli_pi_color}; font-weight:700;">
                {pct_target_payins:.0f}% del target ({target_clients_payins})
            </div>
        </div>""", unsafe_allow_html=True)

    with col_cli3:
        total_clients_m16 = clients_b2b_m16 + clients_payins_m16
        total_clients_base = BASE['users_b2b'] + 2  # ~2 Payins actuales
        client_mult = total_clients_m16 / total_clients_base if total_clients_base > 0 else 1
        mult_color = COLORS['success'] if client_mult >= 2.5 else COLORS['warning'] if client_mult >= 1.5 else COLORS['danger']
        st.markdown(f"""
        <div class="scenario-output" style="text-align:center;">
            <div style="font-size:0.75rem; color:{COLORS['muted']}; text-transform:uppercase;">TOTAL B2B</div>
            <div style="font-size:2rem; font-weight:800; color:{COLORS['dark']};">{total_clients_m16:.0f}</div>
            <div style="font-size:0.85rem; color:{COLORS['muted']};">vs {total_clients_base:.0f} hoy</div>
            <div style="font-size:0.75rem; color:{mult_color}; font-weight:700;">
                ×{client_mult:.1f} crecimiento
            </div>
        </div>""", unsafe_allow_html=True)

    # Revenue Mix donut - Base vs M16
    st.markdown("<br>", unsafe_allow_html=True)

    # Leyenda de colores
    st.markdown(f"""
    <div style="display:flex; justify-content:center; gap:1.5rem; flex-wrap:wrap; margin-bottom:1rem; padding:0.8rem; background:#F7FAFC; border-radius:8px;">
        <span style="display:flex; align-items:center; gap:0.4rem;">
            <span style="width:12px; height:12px; border-radius:50%; background:{COLORS['payouts_b2b']};"></span>
            <span style="font-size:0.85rem; color:#4A5568;">Payouts B2B</span>
        </span>
        <span style="display:flex; align-items:center; gap:0.4rem;">
            <span style="width:12px; height:12px; border-radius:50%; background:{COLORS['payouts_b2c']};"></span>
            <span style="font-size:0.85rem; color:#4A5568;">Payouts B2C</span>
        </span>
        <span style="display:flex; align-items:center; gap:0.4rem;">
            <span style="width:12px; height:12px; border-radius:50%; background:{COLORS['exchange']};"></span>
            <span style="font-size:0.85rem; color:#4A5568;">Exchange</span>
        </span>
        <span style="display:flex; align-items:center; gap:0.4rem;">
            <span style="width:12px; height:12px; border-radius:50%; background:{COLORS['payins_b2b']};"></span>
            <span style="font-size:0.85rem; color:#4A5568;">Payins B2B</span>
        </span>
        <span style="display:flex; align-items:center; gap:0.4rem;">
            <span style="width:12px; height:12px; border-radius:50%; background:{COLORS['forwards']};"></span>
            <span style="font-size:0.85rem; color:#4A5568;">Forwards FX</span>
        </span>
        <span style="display:flex; align-items:center; gap:0.4rem;">
            <span style="width:12px; height:12px; border-radius:50%; background:{COLORS['vita_card']};"></span>
            <span style="font-size:0.85rem; color:#4A5568;">Vita Card</span>
        </span>
    </div>
    """, unsafe_allow_html=True)

    col_mix_base, col_mix_m16 = st.columns(2)

    # Donut BASE (Promedio M1-M4)
    with col_mix_base:
        st.markdown(f"""
        <div style="text-align:center; padding:0.5rem; background:#F7FAFC; border-radius:8px; margin-bottom:0.5rem;">
            <span style="font-weight:700; font-size:1.1rem; color:#718096;">HOY (Avg M1-M4)</span><br>
            <span style="font-size:0.9rem; color:#A0AEC0;">{format_k(BASE_REVENUE)}/mes</span>
        </div>""", unsafe_allow_html=True)

        base_labels = ['Payouts B2B', 'Payouts B2C', 'Exchange', 'Payins B2B']
        base_values = [BASE['rev_payouts_b2b'], BASE['rev_payouts_b2c'], BASE['rev_exchange'], BASE['rev_payins_b2b']]
        base_colors = [COLORS['payouts_b2b'], COLORS['payouts_b2c'], COLORS['exchange'], COLORS['payins_b2b']]

        fig_base = go.Figure(go.Pie(labels=base_labels, values=base_values, hole=0.5,
            marker=dict(colors=base_colors, line=dict(color='#FFFFFF', width=2)),
            textinfo='percent', textfont=dict(size=14, family='Plus Jakarta Sans', color='#FFFFFF')))
        fig_base = plotly_theme(fig_base, height=350)
        b2b_pct_base = BASE['rev_payouts_b2b'] / BASE_REVENUE * 100
        fig_base.update_layout(showlegend=False,
            annotations=[dict(text=f"<b>{b2b_pct_base:.0f}%</b><br>B2B", x=0.5, y=0.5,
                 font=dict(size=16, color=COLORS['danger']), showarrow=False)])
        st.plotly_chart(fig_base, use_container_width=True)

    # Donut M16 (Proyectado)
    with col_mix_m16:
        st.markdown(f"""
        <div style="text-align:center; padding:0.5rem; background:{COLORS['success']}22; border-radius:8px; margin-bottom:0.5rem;">
            <span style="font-weight:700; font-size:1.1rem; color:{COLORS['success']};">MES 16 (Proyectado)</span><br>
            <span style="font-size:0.9rem; color:#718096;">{format_k(total_rev_proj)}/mes</span>
        </div>""", unsafe_allow_html=True)

        mix_labels = ['Payouts B2B', 'Payouts B2C', 'Exchange', 'Payins B2B']
        mix_values = [rev_b2b_proj, rev_b2c_proj, rev_ex_proj, rev_pi_proj]
        mix_colors = [COLORS['payouts_b2b'], COLORS['payouts_b2c'], COLORS['exchange'], COLORS['payins_b2b']]
        if fwd_rev > 0:
            mix_labels.append('Forwards FX'); mix_values.append(fwd_rev); mix_colors.append(COLORS['forwards'])
        if card_rev > 0:
            mix_labels.append('Vita Card'); mix_values.append(card_rev); mix_colors.append(COLORS['vita_card'])

        fig_m16 = go.Figure(go.Pie(labels=mix_labels, values=mix_values, hole=0.5,
            marker=dict(colors=mix_colors, line=dict(color='#FFFFFF', width=2)),
            textinfo='percent', textfont=dict(size=14, family='Plus Jakarta Sans', color='#FFFFFF')))
        fig_m16 = plotly_theme(fig_m16, height=350)
        b2b_pct = rev_b2b_proj / total_rev_proj * 100
        b2b_color = COLORS['success'] if b2b_pct < 60 else COLORS['warning']
        fig_m16.update_layout(showlegend=False,
            annotations=[dict(text=f"<b>{b2b_pct:.0f}%</b><br>B2B", x=0.5, y=0.5,
                 font=dict(size=16, color=b2b_color), showarrow=False)])
        st.plotly_chart(fig_m16, use_container_width=True)

    # Nota: Financing verdict se muestra después de calcular la trayectoria y el gap real

    # Trajectory chart with fixed/variable cost model
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">📈 Trayectoria de Revenue — 12 meses</div>', unsafe_allow_html=True)

    # Valores base = run-rate promedio M1-M4 (no M4 solo)
    rev_base = BASE_REVENUE
    # Fijos base: Personal + Admin + Banking + Inversiones (promedios)
    fixed_base = BASE_PERSONAL + BASE_ADMIN + BASE_BANKING + BASE_INVERSIONES
    # Variables base: COGS + Impuestos + Marketing (promedios)
    gtv_base_traj = BASE_GTV_B2B + BASE_GTV_B2C
    cogs_base_traj = BASE_COGS
    tax_base_traj = BASE_TAX
    mktg_base_traj = BASE_MARKETING
    variable_base = cogs_base_traj + tax_base_traj + mktg_base_traj

    # El primer punto de la trayectoria es M4 REAL
    rev_trajectory = [DATA['revenue'][3]]       # $360,467
    cost_trajectory = [DATA['gastos'][3]]       # $320,474
    fixed_trajectory = [DATA['gastos'][3] - DATA['cogs'][3] - DATA['tax'][3] - DATA['marketing'][3]]
    variable_trajectory = [DATA['cogs'][3] + DATA['tax'][3] + DATA['marketing'][3]]
    cash_trajectory = [DATA['cash'][3]]         # $3,231,872
    monthly_data = []

    # M4 = datos reales
    monthly_data.append({
        'mes': 'M4',
        'revenue': DATA['revenue'][3],
        'fixed': fixed_trajectory[0],
        'variable': variable_trajectory[0],
        'total_cost': DATA['gastos'][3],
        'net_income': DATA['revenue'][3] - DATA['gastos'][3],
        'margin': (DATA['revenue'][3] - DATA['gastos'][3]) / DATA['revenue'][3] * 100,
    })

    # A partir de M5 empieza la S-curve hacia M16
    months_proj = list(range(5, 17))  # M5 a M16 (12 meses)
    for i, m in enumerate(months_proj):
        f = (i + 1) / 12  # interpolation factor

        # Revenue: curva S desde M4 real hacia M16 proyectado
        s_curve = 1 / (1 + np.exp(-8 * (f - 0.4)))
        rev_m = DATA['revenue'][3] + (total_rev_proj - DATA['revenue'][3]) * s_curve

        # Costos fijos: step function con entrada gradual o inmediata
        new_positions_calc = max(0, hc_target - 58)
        if hiring_mode:
            # Gradual: 1 hire cada N meses
            hire_interval = 12 / new_positions_calc if new_positions_calc > 0 else 999
            hires_so_far = min(new_positions_calc, int((i + 1) / hire_interval)) if new_positions_calc > 0 else 0
        else:
            # Inmediato: todos desde mes 1 de proyección (mes 5 absoluto)
            hires_so_far = new_positions_calc
        pers_m = BASE_PERSONAL + hires_so_far * 2500
        # Países: cada uno entra en un trimestre diferente
        countries_active = min(new_countries, (i + 1) // 4 + (1 if i >= 2 else 0))
        admin_m = BASE_ADMIN + countries_active * 5000
        fixed_m = pers_m + admin_m + BASE_BANKING + BASE_INVERSIONES + (4500 if fwd_on else 0) - (ai_savings if i >= 3 else 0)

        # Costos variables: proporcionales al revenue del mes
        variable_ratio_base = variable_base / rev_base if rev_base > 0 else 0.40
        variable_ratio_m16 = total_variable / total_rev_proj if total_rev_proj > 0 else 0.35
        var_ratio_m = variable_ratio_base + (variable_ratio_m16 - variable_ratio_base) * f
        variable_m = rev_m * var_ratio_m

        cost_m = fixed_m + variable_m
        net_m = rev_m - cost_m

        rev_trajectory.append(rev_m)
        cost_trajectory.append(cost_m)
        fixed_trajectory.append(fixed_m)
        variable_trajectory.append(variable_m)
        cash_trajectory.append(cash_trajectory[-1] + net_m)

        monthly_data.append({
            'mes': f'M{m}',
            'revenue': rev_m,
            'fixed': fixed_m,
            'variable': variable_m,
            'total_cost': cost_m,
            'net_income': net_m,
            'margin': (rev_m - cost_m) / rev_m * 100 if rev_m > 0 else 0,
        })

    # Recalcular cash_proj usando la trayectoria real (no promedio)
    # rev_trajectory[0] = M4 real, rev_trajectory[1:] = M5-M16 proyectado
    cash_proj = DATA['cash'][3]
    for i in range(1, 13):  # índices 1-12 = M5-M16 (saltar M4 que ya está en cash inicial)
        cash_proj += rev_trajectory[i] - cost_trajectory[i]

    # Recalcular gap con el nuevo cash_proj basado en trayectoria
    gap = total_investment - cash_proj

    # Para gráficos: M1-M4 histórico + M5-M16 proyectado (sin duplicar M4)
    full_months = MESES + [f'Mes {m}' for m in months_proj]
    full_rev = DATA['revenue'] + rev_trajectory[1:]  # skip M4 en trajectory
    full_costs = DATA['gastos'] + cost_trajectory[1:]  # skip M4 en trajectory
    full_cash = list(DATA['cash']) + cash_trajectory[1:]

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=MESES, y=DATA['revenue'], name='Revenue (histórico)',
        marker_color=COLORS['primary'], opacity=0.8), secondary_y=False)
    fig.add_trace(go.Bar(x=[f'Mes {m}' for m in months_proj], y=rev_trajectory[1:],
        name='Revenue (proyectado)', marker_color=COLORS['secondary'], opacity=0.8), secondary_y=False)
    fig.add_trace(go.Scatter(x=full_months, y=full_costs, name='Gastos', mode='lines',
        line=dict(color=COLORS['danger'], width=2, dash='dot')), secondary_y=False)
    fig.add_trace(go.Scatter(x=full_months, y=full_cash, name='Cash Position', mode='lines+markers',
        line=dict(color=COLORS['warning'], width=2), marker=dict(size=4)), secondary_y=True)
    fig = plotly_theme(fig, height=400)
    fig.update_yaxes(title_text="Revenue & Gastos (USD)", secondary_y=False)
    fig.update_yaxes(title_text="Cash Position (USD)", secondary_y=True)
    fig.update_layout(legend=dict(y=1.15))
    fig.add_vline(x=3.5, line_dash="dash", line_color="#636E72", line_width=1,
        annotation_text="Hoy", annotation_font_color="#636E72")
    st.plotly_chart(fig, use_container_width=True)

    # Cash Position M16 y Financing Gap
    r4, r5 = st.columns(2)
    with r4:
        cash_color = COLORS['success'] if cash_proj > DATA['cash'][3] else COLORS['danger']
        st.markdown(f"""
        <div class="scenario-output" style="text-align:center;">
            <div class="scenario-big">{format_k(cash_proj)}</div>
            <div style="color:#636E72; font-size:0.75rem; text-transform:uppercase;
                letter-spacing:1px;">Cash Position M16</div>
            <div style="color:{cash_color}; font-weight:700; margin-top:0.3rem;">
                {'+' if cash_proj > DATA['cash'][3] else ''}{format_k(cash_proj - DATA['cash'][3])} vs hoy
            </div>
        </div>""", unsafe_allow_html=True)
    with r5:
        if gap < 0:
            gap_label = "✅ SURPLUS"
            gap_color = COLORS['success']
        else:
            gap_label = "⚠️ GAP"
            gap_color = COLORS['warning']
        st.markdown(f"""
        <div class="scenario-output" style="text-align:center;">
            <div class="scenario-big" style="font-size:2rem;">{format_k(abs(gap))}</div>
            <div style="color:#636E72; font-size:0.75rem; text-transform:uppercase;
                letter-spacing:1px;">Financiamiento</div>
            <div style="color:{gap_color}; font-weight:700; margin-top:0.3rem;">{gap_label}</div>
        </div>""", unsafe_allow_html=True)

    # Financing verdict (ahora usa gap calculado con trayectoria real)
    if gap < 0:
        verdict, v_color = "✅ CRECIMIENTO 100% ORGÁNICO", COLORS['success']
        v_detail = f"Surplus: {format_k(abs(gap))}"
    elif gap < 2000000:
        verdict, v_color = "⚠️ NECESITA LÍNEAS DE CRÉDITO", COLORS['warning']
        v_detail = f"Gap: {format_k(gap)}"
    else:
        verdict, v_color = "🔴 REQUIERE EQUITY", COLORS['danger']
        v_detail = f"Gap: {format_k(gap)}"

    st.markdown(f"""
    <div style="background:{v_color}11; border:2px solid {v_color}; border-radius:12px; padding:1rem; text-align:center; margin-top:1rem;">
        <div style="font-weight:800; font-size:1.1rem; color:{v_color};">{verdict}</div>
        <div style="font-size:0.95rem; color:#4A5568;">{v_detail}</div>
    </div>""", unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════
    # COMPARACIÓN BASE vs M16 — INGRESOS Y COSTOS
    # ═══════════════════════════════════════════════════════════
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">📊 COMPARACIÓN BASE vs M16 — INGRESOS Y COSTOS</div>', unsafe_allow_html=True)

    # Calcular valores para comparación
    net_income = total_rev_proj - total_gastos_proj
    net_color = COLORS['success'] if net_income > 0 else COLORS['danger']
    cogs_gtv_ratio = (cogs_proj / gtv_m16 * 100) if gtv_m16 > 0 else 0
    mult_color = COLORS['success'] if multiple >= 2.7 else COLORS['warning'] if multiple >= 2.0 else COLORS['danger']

    # Dos columnas para los gráficos
    col_rev, col_cost = st.columns(2)

    # ═══════════════════════════════════════════════════════════
    # GRÁFICO 1: REVENUE BASE vs M16
    # ═══════════════════════════════════════════════════════════
    with col_rev:
        st.markdown(f"""
        <div style="text-align:center; padding:0.5rem; background:#F7FAFC; border-radius:8px; margin-bottom:0.5rem;">
            <span style="font-weight:700; color:#2D3748;">💰 INGRESOS</span>
            <span style="color:{mult_color}; font-weight:800; margin-left:1rem;">×{multiple:.1f}</span>
        </div>""", unsafe_allow_html=True)

        # Datos para el gráfico de revenue
        rev_categories = ['Payouts B2B', 'Payouts B2C', 'Exchange', 'Payins B2B']
        rev_base_vals = [BASE['rev_payouts_b2b'], BASE['rev_payouts_b2c'], BASE['rev_exchange'], BASE['rev_payins_b2b']]
        rev_m16_vals = [rev_b2b_proj, rev_b2c_proj, rev_ex_proj, rev_pi_proj]

        # Agregar Forwards y Card si están activos
        if fwd_rev > 0:
            rev_categories.append('Forwards FX')
            rev_base_vals.append(0)  # No existía en base
            rev_m16_vals.append(fwd_rev)
        if card_rev > 0:
            rev_categories.append('Vita Card')
            rev_base_vals.append(0)  # No existía en base
            rev_m16_vals.append(card_rev)

        fig_rev = go.Figure()
        fig_rev.add_trace(go.Bar(
            name='Base (Avg M1-M4)',
            x=rev_categories,
            y=rev_base_vals,
            marker_color=COLORS['muted'],
            text=[format_k(v) for v in rev_base_vals],
            textposition='outside',
            textfont=dict(size=11)
        ))
        fig_rev.add_trace(go.Bar(
            name='Mes 16 (Proy.)',
            x=rev_categories,
            y=rev_m16_vals,
            marker_color=COLORS['primary'],
            text=[format_k(v) for v in rev_m16_vals],
            textposition='outside',
            textfont=dict(size=11)
        ))
        fig_rev = plotly_theme(fig_rev, height=350)
        fig_rev.update_layout(
            barmode='group',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
            yaxis_title="USD/mes",
            margin=dict(t=60, b=40)
        )
        st.plotly_chart(fig_rev, use_container_width=True)

        # Totales de revenue
        st.markdown(f"""
        <div style="display:flex; justify-content:space-around; padding:0.8rem; background:#F7FAFC; border-radius:8px;">
            <div style="text-align:center;">
                <div style="font-size:0.8rem; color:#718096;">Base</div>
                <div style="font-weight:700; color:#718096;">{format_k(BASE_REVENUE)}</div>
            </div>
            <div style="font-size:1.5rem; color:#CBD5E0;">→</div>
            <div style="text-align:center;">
                <div style="font-size:0.8rem; color:{COLORS['primary']};">M16</div>
                <div style="font-weight:700; color:{COLORS['primary']};">{format_k(total_rev_proj)}</div>
            </div>
        </div>""", unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════
    # GRÁFICO 2: COSTOS BASE vs M16
    # ═══════════════════════════════════════════════════════════
    with col_cost:
        cost_growth = ((total_gastos_proj / BASE_GASTOS) - 1) * 100 if BASE_GASTOS > 0 else 0
        cost_color = COLORS['success'] if cost_growth < (multiple - 1) * 100 else COLORS['warning']
        st.markdown(f"""
        <div style="text-align:center; padding:0.5rem; background:#F7FAFC; border-radius:8px; margin-bottom:0.5rem;">
            <span style="font-weight:700; color:#2D3748;">💸 COSTOS</span>
            <span style="color:{cost_color}; font-weight:800; margin-left:1rem;">+{cost_growth:.0f}%</span>
        </div>""", unsafe_allow_html=True)

        # Datos para el gráfico de costos (simplificado por categorías principales)
        cost_categories = ['Personal', 'Admin', 'COGS', 'Marketing', 'Impuestos', 'Otros']
        cost_base_vals = [
            BASE_PERSONAL,
            BASE_ADMIN,
            BASE_COGS,
            BASE_MARKETING,
            BASE_TAX,
            BASE_BANKING + BASE_INVERSIONES
        ]
        cost_m16_vals = [
            personal_proj,
            admin_proj,
            cogs_proj,
            mktg_proj,
            tax_proj,
            bank_proj + inv_proj + fwd_cost - ai_savings
        ]

        fig_cost = go.Figure()
        fig_cost.add_trace(go.Bar(
            name='Base (Avg M1-M4)',
            x=cost_categories,
            y=cost_base_vals,
            marker_color=COLORS['muted'],
            text=[format_k(v) for v in cost_base_vals],
            textposition='outside',
            textfont=dict(size=11)
        ))
        fig_cost.add_trace(go.Bar(
            name='Mes 16 (Proy.)',
            x=cost_categories,
            y=cost_m16_vals,
            marker_color=COLORS['danger'],
            text=[format_k(v) for v in cost_m16_vals],
            textposition='outside',
            textfont=dict(size=11)
        ))
        fig_cost = plotly_theme(fig_cost, height=350)
        fig_cost.update_layout(
            barmode='group',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
            yaxis_title="USD/mes",
            margin=dict(t=60, b=40)
        )
        st.plotly_chart(fig_cost, use_container_width=True)

        # Totales de costos y net income
        st.markdown(f"""
        <div style="display:flex; justify-content:space-around; padding:0.8rem; background:#F7FAFC; border-radius:8px;">
            <div style="text-align:center;">
                <div style="font-size:0.8rem; color:#718096;">Base</div>
                <div style="font-weight:700; color:#718096;">{format_k(BASE_GASTOS)}</div>
            </div>
            <div style="font-size:1.5rem; color:#CBD5E0;">→</div>
            <div style="text-align:center;">
                <div style="font-size:0.8rem; color:{COLORS['danger']};">M16</div>
                <div style="font-weight:700; color:{COLORS['danger']};">{format_k(total_gastos_proj)}</div>
            </div>
        </div>""", unsafe_allow_html=True)

    # Resumen de P&L
    st.markdown("<br>", unsafe_allow_html=True)
    base_net = BASE_REVENUE - BASE_GASTOS
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div style="background:#F7FAFC; border-radius:10px; padding:1rem; text-align:center; border-left:4px solid {COLORS['muted']};">
            <div style="font-size:0.85rem; color:#718096;">Net Income Base</div>
            <div style="font-size:1.3rem; font-weight:700; color:{COLORS['success'] if base_net > 0 else COLORS['danger']};">{format_k(base_net)}</div>
            <div style="font-size:0.8rem; color:#718096;">Margen: {BASE_OP_MARGIN:.1f}%</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div style="background:{net_color}11; border-radius:10px; padding:1rem; text-align:center; border:2px solid {net_color};">
            <div style="font-size:0.85rem; color:{net_color};">Net Income M16</div>
            <div style="font-size:1.3rem; font-weight:800; color:{net_color};">{format_k(net_income)}</div>
            <div style="font-size:0.8rem; color:#718096;">Margen: {margin_proj:.1f}%</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        net_growth = ((net_income / base_net) - 1) * 100 if base_net > 0 else 0
        st.markdown(f"""
        <div style="background:#F7FAFC; border-radius:10px; padding:1rem; text-align:center; border-left:4px solid {COLORS['secondary']};">
            <div style="font-size:0.85rem; color:#718096;">Crecimiento Net</div>
            <div style="font-size:1.3rem; font-weight:700; color:{COLORS['success']};">+{net_growth:.0f}%</div>
            <div style="font-size:0.8rem; color:#718096;">Ratio F/V: {fixed_ratio:.0f}%/{variable_ratio:.0f}%</div>
        </div>""", unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════
    # KPIs PROYECTADOS — MES 16 vs BASE (Run-Rate)
    # ═══════════════════════════════════════════════════════════
    st.markdown('<div class="section-header">📊 KPIs PROYECTADOS — BASE vs M16</div>', unsafe_allow_html=True)

    # Base values (run-rate promedio M1-M4)
    rev_base_kpi = BASE_REVENUE
    margin_base = BASE_OP_MARGIN
    rev_emp_base = BASE_REVENUE / DATA['headcount'][3]
    gross_base = BASE_GROSS_MARGIN
    conc_base = BASE['rev_payouts_b2b'] / BASE_REVENUE * 100
    mktg_eff_base = BASE_REVENUE / BASE_MARKETING
    emp_base = DATA['headcount'][3]  # Empleados actual
    rev_annual_base = BASE_REVENUE * 12
    val_base_calc = rev_annual_base * 7

    # COGS/GTV Base (promedio)
    gtv_base_total = BASE_GTV_B2B + BASE_GTV_B2C
    cogs_gtv_base = (BASE_COGS / gtv_base_total * 100) if gtv_base_total > 0 else 0.20

    # Ratio Fijo/Variable Base (calculado de promedios)
    fixed_base_kpi = BASE_PERSONAL + BASE_ADMIN + BASE_BANKING + BASE_INVERSIONES
    variable_base_kpi = BASE_COGS + BASE_TAX + BASE_MARKETING
    total_costs_base = fixed_base_kpi + variable_base_kpi
    fixed_ratio_base = (fixed_base_kpi / total_costs_base * 100) if total_costs_base > 0 else 0
    variable_ratio_base = (variable_base_kpi / total_costs_base * 100) if total_costs_base > 0 else 0

    # Mes 16 projected values
    gross_m16 = (total_rev_proj - cogs_proj) / total_rev_proj * 100 if total_rev_proj > 0 else 0
    conc_m16 = rev_b2b_proj / total_rev_proj * 100 if total_rev_proj > 0 else 0
    mktg_eff_m16 = total_rev_proj / mktg_proj if mktg_proj > 0 else 0
    rev_annual_m16 = total_rev_proj * 12
    val_m16_calc = rev_annual_m16 * 9

    # Color logic functions
    def kpi_color(m4, m16, higher_is_better=True):
        if higher_is_better:
            return COLORS['success'] if m16 > m4 else COLORS['danger'] if m16 < m4 else COLORS['warning']
        else:
            return COLORS['success'] if m16 < m4 else COLORS['danger'] if m16 > m4 else COLORS['warning']

    st.markdown(f"""
    <table style="width:100%; border-collapse:collapse; font-size:0.95rem;">
        <thead>
            <tr style="background:#F7FAFC; border-bottom:2px solid #E2E8F0;">
                <th style="padding:0.7rem 1rem; text-align:left; font-weight:700; color:#2D3748;">KPI</th>
                <th style="padding:0.7rem 1rem; text-align:center; font-weight:700; color:#718096;">Base (Avg M1-M4)</th>
                <th style="padding:0.7rem 1rem; text-align:center; font-weight:700; color:#2D3748;">Mes 16 (Proyectado)</th>
            </tr>
        </thead>
        <tbody>
            <tr style="border-bottom:1px solid #E2E8F0;">
                <td style="padding:0.6rem 1rem; font-weight:600;">Revenue mensual</td>
                <td style="padding:0.6rem 1rem; text-align:center; color:#718096;">{format_k(rev_base_kpi)}</td>
                <td style="padding:0.6rem 1rem; text-align:center; font-weight:700; color:{kpi_color(rev_base_kpi, total_rev_proj)};">{format_k(total_rev_proj)}</td>
            </tr>
            <tr style="border-bottom:1px solid #E2E8F0; background:#FAFAFA;">
                <td style="padding:0.6rem 1rem; font-weight:600;">Margen operativo</td>
                <td style="padding:0.6rem 1rem; text-align:center; color:#718096;">{margin_base:.1f}%</td>
                <td style="padding:0.6rem 1rem; text-align:center; font-weight:700; color:{kpi_color(margin_base, margin_proj)};">{margin_proj:.1f}%</td>
            </tr>
            <tr style="border-bottom:1px solid #E2E8F0;">
                <td style="padding:0.6rem 1rem; font-weight:600;">Revenue/Employee</td>
                <td style="padding:0.6rem 1rem; text-align:center; color:#718096;">${rev_emp_base:,.0f}</td>
                <td style="padding:0.6rem 1rem; text-align:center; font-weight:700; color:{kpi_color(rev_emp_base, rev_per_emp_proj)};">${rev_per_emp_proj:,.0f}</td>
            </tr>
            <tr style="border-bottom:1px solid #E2E8F0; background:#FAFAFA;">
                <td style="padding:0.6rem 1rem; font-weight:600;">Gross Margin</td>
                <td style="padding:0.6rem 1rem; text-align:center; color:#718096;">{gross_base:.1f}%</td>
                <td style="padding:0.6rem 1rem; text-align:center; font-weight:700; color:{kpi_color(gross_base, gross_m16)};">{gross_m16:.1f}%</td>
            </tr>
            <tr style="border-bottom:1px solid #E2E8F0;">
                <td style="padding:0.6rem 1rem; font-weight:600;">Concentración B2B Payouts</td>
                <td style="padding:0.6rem 1rem; text-align:center; color:#718096;">{conc_base:.0f}%</td>
                <td style="padding:0.6rem 1rem; text-align:center; font-weight:700; color:{kpi_color(conc_base, conc_m16, higher_is_better=False)};">{conc_m16:.0f}%</td>
            </tr>
            <tr style="border-bottom:1px solid #E2E8F0; background:#FAFAFA;">
                <td style="padding:0.6rem 1rem; font-weight:600;">Marketing Efficiency</td>
                <td style="padding:0.6rem 1rem; text-align:center; color:#718096;">{mktg_eff_base:.1f}×</td>
                <td style="padding:0.6rem 1rem; text-align:center; font-weight:700; color:{kpi_color(mktg_eff_base, mktg_eff_m16)};">{mktg_eff_m16:.1f}×</td>
            </tr>
            <tr style="border-bottom:1px solid #E2E8F0;">
                <td style="padding:0.6rem 1rem; font-weight:600;">COGS / GTV</td>
                <td style="padding:0.6rem 1rem; text-align:center; color:#718096;">{cogs_gtv_base:.2f}%</td>
                <td style="padding:0.6rem 1rem; text-align:center; font-weight:700; color:{kpi_color(cogs_gtv_base, cogs_gtv_ratio, higher_is_better=False)};">{cogs_gtv_ratio:.2f}%</td>
            </tr>
            <tr style="border-bottom:1px solid #E2E8F0; background:#FAFAFA;">
                <td style="padding:0.6rem 1rem; font-weight:600;">Ratio Fijo / Variable</td>
                <td style="padding:0.6rem 1rem; text-align:center; color:#718096;">{fixed_ratio_base:.0f}% / {variable_ratio_base:.0f}%</td>
                <td style="padding:0.6rem 1rem; text-align:center; font-weight:700; color:{COLORS['warning']};">{fixed_ratio:.0f}% / {variable_ratio:.0f}%</td>
            </tr>
            <tr style="border-bottom:1px solid #E2E8F0;">
                <td style="padding:0.6rem 1rem; font-weight:600;">Empleados</td>
                <td style="padding:0.6rem 1rem; text-align:center; color:#718096;">{emp_base}</td>
                <td style="padding:0.6rem 1rem; text-align:center; font-weight:700; color:{COLORS['warning']};">{hc_target}</td>
            </tr>
            <tr style="border-bottom:1px solid #E2E8F0; background:#FAFAFA;">
                <td style="padding:0.6rem 1rem; font-weight:600;">Revenue anualizado</td>
                <td style="padding:0.6rem 1rem; text-align:center; color:#718096;">${rev_annual_base/1e6:.1f}M</td>
                <td style="padding:0.6rem 1rem; text-align:center; font-weight:700; color:{kpi_color(rev_annual_base, rev_annual_m16)};">${rev_annual_m16/1e6:.1f}M</td>
            </tr>
            <tr style="background:{COLORS['success']}11; border-top:2px solid {COLORS['success']};">
                <td style="padding:0.7rem 1rem; font-weight:800; color:{COLORS['success']};">Valorización (base)</td>
                <td style="padding:0.7rem 1rem; text-align:center; color:#718096;">${val_base_calc/1e6:.0f}M (7×)</td>
                <td style="padding:0.7rem 1rem; text-align:center; font-weight:800; color:{COLORS['success']}; font-size:1.1rem;">${val_m16_calc/1e6:.0f}M (9×)</td>
            </tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════
    # EVOLUCIÓN MENSUAL — INGRESOS, COSTOS Y RESULTADO
    # ═══════════════════════════════════════════════════════════
    st.markdown('<div class="section-header">📈 EVOLUCIÓN MENSUAL — INGRESOS, COSTOS Y RESULTADO</div>', unsafe_allow_html=True)

    # Build monthly evolution data with S-curve interpolation
    meses_evol = [f'M{i}' for i in range(4, 17)]

    # M4 = valores REALES (no promedios)
    rev_b2b_m4 = DATA['rev_payouts_b2b'][3]
    rev_b2c_m4 = DATA['rev_payouts_b2c'][3]
    rev_ex_m4 = DATA['rev_exchange_b2b'][3]
    rev_pi_m4 = DATA['rev_payins_b2b'][3]
    costs_m4 = DATA['gastos'][3]
    cash_m4_evol = DATA['cash'][3]

    # Monthly arrays
    rev_b2b_evol, rev_b2c_evol, rev_ex_evol, rev_pi_evol = [], [], [], []
    fwd_evol, card_evol = [], []
    rev_total_evol, costs_total_evol, net_evol, margin_evol, cash_evol = [], [], [], [], []

    # Client tracking arrays
    clients_b2b_evol, clients_payins_evol = [], []
    arpu_b2b_evol = []

    # M4 clientes reales
    clients_b2b_m4 = DATA['b2b_users_est'][3]  # 396
    clients_payins_m4 = 2  # estimado

    for m in range(13):  # m=0 is M4 (real), m=1..12 is M5..M16 (S-curve)
        if m == 0:
            # M4 = datos REALES
            rb, rc, re, rp = rev_b2b_m4, rev_b2c_m4, rev_ex_m4, rev_pi_m4
            fwd_m, card_m = 0, 0  # Productos nuevos no existían en M4
            cost_m = costs_m4
            cli_b2b_m = clients_b2b_m4
            cli_pi_m = clients_payins_m4
        else:
            # M5-M16: S-curve desde M4 real hacia M16 proyectado
            f = m / 12
            s_factor = 1 / (1 + np.exp(-8 * (f - 0.4)))

            rb = rev_b2b_m4 + (rev_b2b_proj - rev_b2b_m4) * s_factor
            rc = rev_b2c_m4 + (rev_b2c_proj - rev_b2c_m4) * s_factor
            re = rev_ex_m4 + (rev_ex_proj - rev_ex_m4) * s_factor
            rp = rev_pi_m4 + (rev_pi_proj - rev_pi_m4) * s_factor

            fwd_m = fwd_rev * s_factor if fwd_rev > 0 else 0
            card_m = card_rev * s_factor if card_rev > 0 else 0

            cost_m = costs_m4 + (total_gastos_proj - costs_m4) * s_factor * 0.8

            # Clientes con S-curve
            cli_b2b_m = clients_b2b_m4 + (clients_b2b_m16 - clients_b2b_m4) * s_factor
            cli_pi_m = clients_payins_m4 + (clients_payins_m16 - clients_payins_m4) * s_factor

        rev_b2b_evol.append(rb)
        rev_b2c_evol.append(rc)
        rev_ex_evol.append(re)
        rev_pi_evol.append(rp)
        fwd_evol.append(fwd_m)
        card_evol.append(card_m)

        # Client tracking
        clients_b2b_evol.append(cli_b2b_m)
        clients_payins_evol.append(cli_pi_m)
        arpu_b2b_m = rb / cli_b2b_m if cli_b2b_m > 0 else 0
        arpu_b2b_evol.append(arpu_b2b_m)

        rev_tot = rb + rc + re + rp + fwd_m + card_m
        rev_total_evol.append(rev_tot)
        costs_total_evol.append(cost_m)

        net_m = rev_tot - cost_m
        net_evol.append(net_m)

        margin_m = (net_m / rev_tot * 100) if rev_tot > 0 else 0
        margin_evol.append(margin_m)

        # Cash accumulation
        if m == 0:
            cash_evol.append(cash_m4_evol)
        else:
            cash_evol.append(cash_evol[-1] + net_m)

    # 1. Stacked Area Chart - Revenue by Line
    # Helper to convert hex to rgba
    def hex_to_rgba(hex_color, alpha=0.6):
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        return f'rgba({r},{g},{b},{alpha})'

    fig_area = go.Figure()

    fig_area.add_trace(go.Scatter(
        x=meses_evol, y=rev_b2b_evol, name='Payouts B2B', mode='lines',
        line=dict(width=0.5, color=COLORS['payouts_b2b']),
        stackgroup='one', fillcolor=hex_to_rgba(COLORS['payouts_b2b'])
    ))
    fig_area.add_trace(go.Scatter(
        x=meses_evol, y=rev_b2c_evol, name='Payouts B2C', mode='lines',
        line=dict(width=0.5, color=COLORS['payouts_b2c']),
        stackgroup='one', fillcolor=hex_to_rgba(COLORS['payouts_b2c'])
    ))
    fig_area.add_trace(go.Scatter(
        x=meses_evol, y=rev_ex_evol, name='Exchange', mode='lines',
        line=dict(width=0.5, color=COLORS['exchange']),
        stackgroup='one', fillcolor=hex_to_rgba(COLORS['exchange'])
    ))
    fig_area.add_trace(go.Scatter(
        x=meses_evol, y=rev_pi_evol, name='Payins B2B', mode='lines',
        line=dict(width=0.5, color=COLORS['payins_b2b']),
        stackgroup='one', fillcolor=hex_to_rgba(COLORS['payins_b2b'])
    ))
    if fwd_rev > 0:
        fig_area.add_trace(go.Scatter(
            x=meses_evol, y=fwd_evol, name='Forwards FX', mode='lines',
            line=dict(width=0.5, color=COLORS['forwards']),
            stackgroup='one', fillcolor=hex_to_rgba(COLORS['forwards'])
        ))
    if card_rev > 0:
        fig_area.add_trace(go.Scatter(
            x=meses_evol, y=card_evol, name='Vita Card', mode='lines',
            line=dict(width=0.5, color=COLORS['vita_card']),
            stackgroup='one', fillcolor=hex_to_rgba(COLORS['vita_card'])
        ))

    fig_area = plotly_theme(fig_area, height=350)
    fig_area.update_layout(
        title=dict(text="Revenue por Línea de Negocio", font=dict(size=14)),
        yaxis_title="Revenue (USD/mes)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
    )
    st.plotly_chart(fig_area, use_container_width=True)

    # 2. Revenue vs Costs Line Chart with fill
    fig_lines = go.Figure()

    # Revenue line
    fig_lines.add_trace(go.Scatter(
        x=meses_evol, y=rev_total_evol, name='Revenue Total',
        mode='lines', line=dict(color=COLORS['secondary'], width=3),
        fill='tonexty', fillcolor='rgba(0, 201, 167, 0.15)'
    ))

    # Costs line (added first for fill reference)
    fig_lines.add_trace(go.Scatter(
        x=meses_evol, y=costs_total_evol, name='Costos Totales',
        mode='lines', line=dict(color=COLORS['danger'], width=3)
    ))

    # Net Income area (difference)
    fig_lines.add_trace(go.Scatter(
        x=meses_evol, y=net_evol, name='Net Income',
        mode='lines+markers', line=dict(color=COLORS['success'], width=2, dash='dot'),
        marker=dict(size=6)
    ))

    # Breakeven line
    fig_lines.add_hline(y=0, line_dash="dash", line_color="#636E72", line_width=1,
        annotation_text="Breakeven", annotation_position="right")

    fig_lines = plotly_theme(fig_lines, height=300)
    fig_lines.update_layout(
        title=dict(text="Revenue vs Costos — Evolución", font=dict(size=14)),
        yaxis_title="USD/mes",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
    )
    st.plotly_chart(fig_lines, use_container_width=True)

    # 3. Client Evolution Chart (PARTE 7)
    st.markdown("<br>", unsafe_allow_html=True)

    fig_clients = make_subplots(specs=[[{"secondary_y": True}]])

    # Clientes B2B
    fig_clients.add_trace(go.Bar(
        x=meses_evol, y=clients_b2b_evol, name='Clientes Payouts B2B',
        marker_color=COLORS['payouts_b2b'], opacity=0.8
    ), secondary_y=False)

    # Clientes Payins
    fig_clients.add_trace(go.Bar(
        x=meses_evol, y=clients_payins_evol, name='Clientes Payins B2B',
        marker_color=COLORS['payins_b2b'], opacity=0.8
    ), secondary_y=False)

    # ARPU B2B (linea secundaria)
    fig_clients.add_trace(go.Scatter(
        x=meses_evol, y=arpu_b2b_evol, name='ARPU B2B',
        mode='lines+markers', line=dict(color=COLORS['warning'], width=2),
        marker=dict(size=6)
    ), secondary_y=True)

    fig_clients = plotly_theme(fig_clients, height=300)
    fig_clients.update_layout(
        title=dict(text="Evolución de Clientes B2B y ARPU", font=dict(size=14)),
        barmode='group',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
    )
    fig_clients.update_yaxes(title_text="# Clientes", secondary_y=False)
    fig_clients.update_yaxes(title_text="ARPU (USD)", secondary_y=True)
    st.plotly_chart(fig_clients, use_container_width=True)

    # 4. Monthly Table - Build complete HTML with clients and ARPU (PARTE 8)
    table_html = """<table style="width:100%; border-collapse:collapse; font-size:0.78rem; font-family:'JetBrains Mono', monospace;">
        <thead>
            <tr style="background:#F7FAFC; border-bottom:2px solid #E2E8F0;">
                <th style="padding:0.5rem 0.3rem; text-align:center; font-weight:700; color:#2D3748;">Mes</th>
                <th style="padding:0.5rem 0.3rem; text-align:center; font-weight:700; color:#2D3748;">Clientes B2B</th>
                <th style="padding:0.5rem 0.3rem; text-align:center; font-weight:700; color:#2D3748;">ARPU</th>
                <th style="padding:0.5rem 0.3rem; text-align:center; font-weight:700; color:#2D3748;">Revenue</th>
                <th style="padding:0.5rem 0.3rem; text-align:center; font-weight:700; color:#2D3748;">Costos</th>
                <th style="padding:0.5rem 0.3rem; text-align:center; font-weight:700; color:#2D3748;">Net</th>
                <th style="padding:0.5rem 0.3rem; text-align:center; font-weight:700; color:#2D3748;">Margen</th>
                <th style="padding:0.5rem 0.3rem; text-align:center; font-weight:700; color:#2D3748;">Cash</th>
            </tr>
        </thead>
        <tbody>"""

    for i, mes in enumerate(meses_evol):
        rev = rev_total_evol[i]
        cost = costs_total_evol[i]
        net = net_evol[i]
        margin = margin_evol[i]
        cash = cash_evol[i]
        clients_b2b = clients_b2b_evol[i]
        arpu_b2b = arpu_b2b_evol[i]

        net_color = COLORS['success'] if net > 0 else COLORS['danger']
        margin_color = COLORS['success'] if margin > 20 else COLORS['warning'] if margin > 10 else COLORS['danger']
        row_bg = "#FAFAFA" if i % 2 == 1 else "#FFFFFF"

        table_html += f'<tr style="background:{row_bg}; border-bottom:1px solid #E2E8F0;">'
        table_html += f'<td style="padding:0.35rem 0.2rem; text-align:center; font-weight:600;">{mes}</td>'
        table_html += f'<td style="padding:0.35rem 0.2rem; text-align:center;">{clients_b2b:.0f}</td>'
        table_html += f'<td style="padding:0.35rem 0.2rem; text-align:center; color:{COLORS["warning"]}; font-weight:600;">${arpu_b2b:,.0f}</td>'
        table_html += f'<td style="padding:0.35rem 0.2rem; text-align:center;">{format_k(rev)}</td>'
        table_html += f'<td style="padding:0.35rem 0.2rem; text-align:center; color:{COLORS["danger"]};">{format_k(cost)}</td>'
        table_html += f'<td style="padding:0.35rem 0.2rem; text-align:center; color:{net_color}; font-weight:600;">{format_k(net)}</td>'
        table_html += f'<td style="padding:0.35rem 0.2rem; text-align:center; color:{margin_color}; font-weight:600;">{margin:.0f}%</td>'
        table_html += f'<td style="padding:0.35rem 0.2rem; text-align:center;">${cash/1e6:.1f}M</td>'
        table_html += '</tr>'

    table_html += "</tbody></table>"

    st.markdown(table_html, unsafe_allow_html=True)

    # ARPU summary note
    st.markdown(f"""<div style="font-size:0.78rem; color:{COLORS['muted']}; padding:0.5rem;">
ARPU Payouts M4: $669 (mes estacionalmente bajo). Promedio M1-M4: $883. Rango: $669-$1,102 por estacionalidad.</div>""", unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════
    # EVOLUCIÓN DE CLIENTES B2B — PROYECTADO A M16
    # ═══════════════════════════════════════════════════════════
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">👥 Métricas por Cliente B2B — Proyectado a M16</div>', unsafe_allow_html=True)

    # Usar clients_b2b_m16 derivado del sidebar (GTV ÷ avg GTV per client)
    users_b2b_m16 = clients_b2b_m16
    client_growth = users_b2b_m16 / BASE['users_b2b'] if BASE['users_b2b'] > 0 else 1
    ticket_m16 = gtv_b2b_m16 / users_b2b_m16 if users_b2b_m16 > 0 else BASE['avg_gtv_user_b2b']
    ticket_growth = ticket_m16 / BASE['avg_gtv_user_b2b'] if BASE['avg_gtv_user_b2b'] > 0 else 1

    # Revenue por cliente M16 (derivado de revenue ÷ clientes)
    rev_per_user_b2b_m16 = rev_b2b_proj / users_b2b_m16 if users_b2b_m16 > 0 else 0
    rev_per_user_ex_m16 = rev_ex_proj / users_b2b_m16 if users_b2b_m16 > 0 else 0
    rev_per_user_pi_m16 = rev_pi_proj / users_b2b_m16 if users_b2b_m16 > 0 else 0
    rev_per_user_total_m16 = rev_per_user_b2b_m16 + rev_per_user_ex_m16 + rev_per_user_pi_m16

    # MRR y CLTV proyectados
    mrr_m16 = users_b2b_m16 * rev_per_user_total_m16
    cltv_m16 = rev_per_user_total_m16 / AVG_CHURN_B2B_SAFE if AVG_CHURN_B2B_SAFE > 0 else 0

    # Guardar en session_state para usar en Valuation
    st.session_state['users_b2b_m16'] = users_b2b_m16
    st.session_state['rev_per_user_total_m16'] = rev_per_user_total_m16
    st.session_state['mrr_m16'] = mrr_m16
    st.session_state['cltv_m16'] = cltv_m16
    st.session_state['client_growth'] = client_growth
    st.session_state['ticket_growth'] = ticket_growth

    # Tabla comparativa Base vs M16
    col_clients_tbl, col_clients_insight = st.columns([3, 2])

    with col_clients_tbl:
        metrics_clients = [
            ("Clientes B2B activos", f"{BASE['users_b2b']:.0f}", f"{users_b2b_m16:.0f}", f"+{(client_growth-1)*100:.0f}%"),
            ("Ticket mensual (GTV/cliente)", f"${BASE['avg_gtv_user_b2b']/1000:,.0f}K", f"${ticket_m16/1000:,.0f}K", f"+{(ticket_growth-1)*100:.0f}%"),
            ("Rev/Cliente — Payouts", f"${BASE['rev_per_user_payouts_b2b']:,.0f}", f"${rev_per_user_b2b_m16:,.0f}", ""),
            ("Rev/Cliente — Exchange", f"${BASE['rev_per_user_exchange_b2b']:,.0f}", f"${rev_per_user_ex_m16:,.0f}", ""),
            ("Rev/Cliente — Payins", f"${BASE['rev_per_user_payins_b2b']:,.1f}", f"${rev_per_user_pi_m16:,.0f}", "⬆ Cross-sell"),
            ("Rev/Cliente — Total", f"${BASE['rev_per_user_total_b2b']:,.0f}", f"${rev_per_user_total_m16:,.0f}", f"+{(rev_per_user_total_m16/BASE['rev_per_user_total_b2b']-1)*100:.0f}%"),
            ("MRR B2B", f"${BASE_MRR_B2B/1000:,.0f}K", f"${mrr_m16/1000:,.0f}K", f"×{mrr_m16/BASE_MRR_B2B:.1f}"),
            ("CLTV B2B", f"${BASE_CLTV_B2B/1000:,.0f}K", f"${cltv_m16/1000:,.0f}K", f"×{cltv_m16/BASE_CLTV_B2B:.1f}"),
        ]

        table_clients_html = """<table style="width:100%; border-collapse:collapse; font-size:0.9rem; font-family:'JetBrains Mono', monospace;">
            <thead>
                <tr style="background:#F7FAFC; border-bottom:2px solid #E2E8F0;">
                    <th style="padding:0.5rem 0.4rem; text-align:left; font-weight:700; color:#2D3748;">Métrica</th>
                    <th style="padding:0.5rem 0.4rem; text-align:center; font-weight:700; color:#718096;">Base (Avg M1-M4)</th>
                    <th style="padding:0.5rem 0.4rem; text-align:center; font-weight:700; color:#2D3748;">Proyectado M16</th>
                    <th style="padding:0.5rem 0.4rem; text-align:center; font-weight:700; color:#2D3748;">Δ</th>
                </tr>
            </thead>
            <tbody>"""

        for i, (metric, base_val, m16_val, delta) in enumerate(metrics_clients):
            row_bg = "#FAFAFA" if i % 2 == 1 else "#FFFFFF"
            is_total = "Total" in metric or "MRR" in metric or "CLTV" in metric
            border_style = "border-top:2px solid #E2E8F0;" if is_total else "border-bottom:1px solid #E2E8F0;"
            font_weight = "font-weight:700;" if is_total else ""
            delta_color = COLORS['success'] if delta and ('+' in delta or '×' in delta or '⬆' in delta) else COLORS['text']

            table_clients_html += f'<tr style="background:{row_bg}; {border_style}">'
            table_clients_html += f'<td style="padding:0.4rem 0.3rem; {font_weight}">{metric}</td>'
            table_clients_html += f'<td style="padding:0.4rem 0.3rem; text-align:center; color:#718096;">{base_val}</td>'
            table_clients_html += f'<td style="padding:0.4rem 0.3rem; text-align:center; color:{COLORS["secondary"]}; {font_weight}">{m16_val}</td>'
            table_clients_html += f'<td style="padding:0.4rem 0.3rem; text-align:center; color:{delta_color}; {font_weight}">{delta}</td>'
            table_clients_html += '</tr>'

        table_clients_html += "</tbody></table>"
        st.markdown(table_clients_html, unsafe_allow_html=True)

    with col_clients_insight:
        # Insight sobre composición del crecimiento
        st.markdown(f"""
        <div style="background:linear-gradient(135deg, rgba(0, 201, 167, 0.06), rgba(0, 102, 255, 0.06));
                    border-radius:12px; padding:1rem; border:1px solid rgba(0, 201, 167, 0.2);">
            <div style="font-weight:700; color:#2D3748; margin-bottom:0.5rem; font-size:0.95rem;">
                📊 Composición del Crecimiento
            </div>
            <div style="font-size:0.9rem; color:#4A5568; line-height:1.6;">
                <strong>{pct_from_clients}% por más clientes</strong><br>
                De {BASE['users_b2b']:.0f} → {users_b2b_m16:.0f} clientes<br><br>
                <strong>{100-pct_from_clients}% por ticket mayor</strong><br>
                De ${BASE['avg_gtv_user_b2b']/1000:,.0f}K → ${ticket_m16/1000:,.0f}K/cliente<br><br>
                <div style="margin-top:0.5rem; padding-top:0.5rem; border-top:1px solid #E2E8F0;">
                    <strong style="color:{COLORS['secondary']};">MRR M16: ${mrr_m16/1000:,.0f}K</strong><br>
                    <span style="font-size:0.85rem; color:#718096;">
                        = {users_b2b_m16:.0f} clientes × ${rev_per_user_total_m16:,.0f}/mes
                    </span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Warning si el crecimiento de clientes es muy agresivo
        if client_growth > 2.5:
            st.markdown(f"""
            <div style="background:rgba(245, 166, 35, 0.1); border-radius:8px; padding:0.8rem; margin-top:0.8rem; border-left:4px solid {COLORS['warning']};">
                <strong style="color:{COLORS['warning']};">⚠️ Crecimiento agresivo de clientes</strong><br>
                <span style="font-size:0.85rem; color:#4A5568;">
                    Pasar de {BASE['users_b2b']:.0f} a {users_b2b_m16:.0f} clientes requiere una estrategia
                    de adquisición muy intensiva. Considera si es alcanzable con el CAC actual.
                </span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# PAGE 7: VALORIZACIÓN — Multi-Método Reactivo
# ══════════════════════════════════════════════════════════════
with tab_val:
    st.markdown('<div class="page-title">Valorización Multi-Método</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">6 metodologías independientes — Base vs M16 proyectado</div>', unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════
    # VALORES HEREDADOS DEL SCENARIO BUILDER (sidebar)
    # ═══════════════════════════════════════════════════════════
    v_rev_m16 = st.session_state.get('scenario_rev_m16', BASE_REVENUE * 2)
    v_gastos_m16 = st.session_state.get('scenario_gastos_m16', BASE_GASTOS * 1.5)
    v_gtv_m16 = st.session_state.get('scenario_gtv_m16', BASE_GTV_B2B * 2)
    v_multiple = st.session_state.get('scenario_multiple', 2.0)
    v_clients_b2b = st.session_state.get('scenario_clients_b2b', 600)
    v_clients_payins = st.session_state.get('scenario_clients_payins', 50)

    # Mostrar resumen del escenario heredado
    st.markdown(f"""<div style="background:#F0FFF4; border:1px solid {COLORS['success']}; border-radius:8px; padding:12px; margin-bottom:16px;">
<span style="font-size:0.9rem; font-weight:700; color:{COLORS['success']};">📊 Escenario del Scenario Builder (sidebar)</span><br>
<span style="font-size:0.85rem; color:{COLORS['text']};">
Revenue M16: <b>{format_k(v_rev_m16)}/mes</b> (×{v_multiple:.1f}) |
Clientes B2B: <b>{v_clients_b2b:.0f}</b> + Payins: <b>{v_clients_payins}</b>
</span></div>""", unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════
    # MOTOR DE CÁLCULO (usando valores del Scenario Builder)
    # ═══════════════════════════════════════════════════════════
    # Anualizados
    v_rev_annual_base = BASE_REVENUE * 12
    v_rev_annual_m16 = v_rev_m16 * 12

    # Crecimiento implícito
    v_growth_multiple = v_multiple
    v_annual_growth_pct = (v_growth_multiple - 1) * 100

    v_gtv_base = BASE_GTV_B2B + BASE_GTV_B2C
    v_gtv_annual_base = v_gtv_base * 12
    v_gtv_annual_m16 = v_gtv_m16 * 12

    # Márgenes
    v_ebitda_base = BASE_REVENUE - BASE_GASTOS
    v_ebitda_base_annual = v_ebitda_base * 12
    v_margin_base = v_ebitda_base / BASE_REVENUE * 100 if BASE_REVENUE > 0 else 0

    v_ebitda_m16 = v_rev_m16 - v_gastos_m16
    v_ebitda_m16_annual = v_ebitda_m16 * 12
    v_margin_m16 = v_ebitda_m16 / v_rev_m16 * 100 if v_rev_m16 > 0 else 0

    # Rule of 40
    v_rule40_base = 8 + v_margin_base  # ~8% growth MoM anualizado + margen
    v_rule40_m16 = v_annual_growth_pct + v_margin_m16

    # ═══════════════════════════════════════════════════════════
    # PASO 3: FUNCIÓN DCF
    # ═══════════════════════════════════════════════════════════
    def calc_dcf_val(base_rev_annual, base_ebitda_annual, growth_rates, margins, wacc, terminal_growth=0.03):
        rev = base_rev_annual
        fcfs = []
        for i in range(5):
            rev = rev * (1 + growth_rates[i])
            ebitda = rev * margins[i]
            pv = ebitda / ((1 + wacc) ** (i + 1))
            fcfs.append({'year': i + 1, 'revenue': rev, 'ebitda': ebitda, 'pv': pv})
        last_ebitda = fcfs[-1]['ebitda']
        terminal_value = last_ebitda * (1 + terminal_growth) / (wacc - terminal_growth) if wacc > terminal_growth else 0
        tv_pv = terminal_value / ((1 + wacc) ** 5)
        total_pv = sum(f['pv'] for f in fcfs) + tv_pv
        return total_pv, fcfs, tv_pv

    # ═══════════════════════════════════════════════════════════
    # PASO 4: CALCULAR 6 MÉTODOS
    # ═══════════════════════════════════════════════════════════

    # MÉTODO 1: EV/Revenue Multiple
    rev_multiples = {'Conservador': {'base': 5, 'm16': 6}, 'Base': {'base': 7, 'm16': 8}, 'Optimista': {'base': 9, 'm16': 11}}
    evrev = {}
    for scenario, mults in rev_multiples.items():
        evrev[scenario] = {'base': v_rev_annual_base * mults['base'], 'm16': v_rev_annual_m16 * mults['m16']}

    # MÉTODO 2: EV/EBITDA
    ebitda_multiples = [15, 20, 25]
    evebitda_base = {f'{m}x': v_ebitda_base_annual * m for m in ebitda_multiples}
    evebitda_m16 = {f'{m}x': v_ebitda_m16_annual * m for m in ebitda_multiples}

    # MÉTODO 3: DCF
    gr_from_base = [1.0, 0.50, 0.30, 0.20, 0.15]
    mg_from_base = [0.25, 0.35, 0.38, 0.40, 0.42]
    dcf_base_20, dcf_base_detail, dcf_base_tv = calc_dcf_val(v_rev_annual_base, v_ebitda_base_annual, gr_from_base, mg_from_base, 0.20)
    dcf_base_15, _, _ = calc_dcf_val(v_rev_annual_base, v_ebitda_base_annual, gr_from_base, mg_from_base, 0.15)

    gr_from_m16 = [0.30, 0.25, 0.20, 0.15, 0.10]
    mg_from_m16 = [v_margin_m16/100, min(0.40, v_margin_m16/100 + 0.03), min(0.42, v_margin_m16/100 + 0.05),
                   min(0.43, v_margin_m16/100 + 0.06), min(0.44, v_margin_m16/100 + 0.07)]
    dcf_m16_15, dcf_m16_detail, dcf_m16_tv = calc_dcf_val(v_rev_annual_m16, v_ebitda_m16_annual, gr_from_m16, mg_from_m16, 0.15)
    dcf_m16_20, _, _ = calc_dcf_val(v_rev_annual_m16, v_ebitda_m16_annual, gr_from_m16, mg_from_m16, 0.20)

    # MÉTODO 4: Volume-Based (GTV)
    v_take_rate_base = v_rev_annual_base / v_gtv_annual_base * 100 if v_gtv_annual_base > 0 else 0
    v_take_rate_m16 = v_rev_annual_m16 / v_gtv_annual_m16 * 100 if v_gtv_annual_m16 > 0 else 0
    gtv_check = "✅ Consistente" if v_take_rate_m16 < 1.2 else "⚠️ Take rate alto"
    vol_val_base = v_rev_annual_base * 7
    vol_val_m16 = v_rev_annual_m16 * 8 if v_take_rate_m16 < 1.2 else v_rev_annual_m16 * 5

    # MÉTODO 5: VC Method
    rev_year5 = v_rev_annual_m16 * 1.30 * 1.25 * 1.20 * 1.15
    exit_multiple = 6
    exit_value = rev_year5 * exit_multiple
    vc_vals = {}
    for irr_label, irr in [('25% IRR', 0.25), ('35% IRR', 0.35), ('45% IRR', 0.45)]:
        pv = exit_value / ((1 + irr) ** 5)
        vc_vals[irr_label] = pv

    # MÉTODO 6: Rule of 40 Adjusted
    r40_premium_base = 1.75 if v_rule40_base >= 40 else 1.0
    r40_val_base = v_rev_annual_base * 5 * r40_premium_base
    r40_premium_m16 = 1.75 if v_rule40_m16 >= 40 else 1.0
    r40_val_m16 = v_rev_annual_m16 * 6 * r40_premium_m16

    # ═══════════════════════════════════════════════════════════
    # VALIDACIÓN DE CONSISTENCIA CON PROYECCIÓN DE CLIENTES
    # ═══════════════════════════════════════════════════════════
    # Recuperar datos de session_state si existen (del Scenario Builder)
    users_b2b_m16_val = st.session_state.get('users_b2b_m16', BASE['users_b2b'] * 1.5)
    rev_per_user_m16_val = st.session_state.get('rev_per_user_total_m16', BASE['rev_per_user_total_b2b'] * 1.2)
    client_growth_val = st.session_state.get('client_growth', 1.5)

    # Revenue B2B (capturado por modelo de clientes) vs no-B2B
    rev_b2b_lines_m16 = v_rev_b2b_16 + v_rev_ex_16 + v_rev_pi_16  # solo líneas B2B
    rev_other_m16 = v_rev_b2c_16 + v_rev_new_16  # B2C + nuevos productos
    implied_rev_from_clients = users_b2b_m16_val * rev_per_user_m16_val

    # ARPU growth implícito (usando ARPU solo Payouts para consistencia)
    arpu_base = BASE_ARPU_PAYOUTS_B2B  # $872 (solo Payouts)
    arpu_m16 = rev_per_user_m16_val
    arpu_growth = (arpu_m16 / arpu_base - 1) * 100 if arpu_base > 0 else 0

    # ═══════════════════════════════════════════════════════════
    # PASO 5-6: TABLA CONSOLIDADA Y RANGO
    # ═══════════════════════════════════════════════════════════
    st.markdown('<div class="section-header">📊 Valorización Multi-Método</div>', unsafe_allow_html=True)

    methods_data = [
        ("EV/Revenue (7x/8x)", evrev['Base']['base'], evrev['Base']['m16'], "Método estándar fintech early-stage"),
        ("EV/EBITDA (20x)", evebitda_base.get('20x', 0), evebitda_m16.get('20x', 0), "Valida margen operativo"),
        ("DCF (WACC 20%/15%)", dcf_base_20, dcf_m16_15, "Sensible a terminal value"),
        ("Volume-Based (GTV)", vol_val_base, vol_val_m16, f"Take rate M16: {v_take_rate_m16:.2f}% {gtv_check}"),
        ("VC Method (35% IRR)", vc_vals.get('35% IRR', 0), None, "Exit a 5 años, perspectiva inversionista"),
        ("Rule of 40 Adjusted", r40_val_base, r40_val_m16, f"R40 Base: {v_rule40_base:.0f} | M16: {v_rule40_m16:.0f}"),
    ]

    # Tabla HTML
    table_html = """<table style="width:100%; border-collapse:collapse; font-size:0.95rem; margin-bottom:1rem;">
        <thead>
            <tr style="background:#F7FAFC; border-bottom:2px solid #E2E8F0;">
                <th style="padding:0.7rem 1rem; text-align:left; font-weight:700; color:#2D3748;">Método</th>
                <th style="padding:0.7rem 1rem; text-align:center; font-weight:700; color:#718096;">Base (Avg M1-M4)</th>
                <th style="padding:0.7rem 1rem; text-align:center; font-weight:700; color:#2D3748;">Mes 16 (Proy.)</th>
                <th style="padding:0.7rem 1rem; text-align:left; font-weight:700; color:#718096;">Notas</th>
            </tr>
        </thead>
        <tbody>"""

    for i, (method, val_base, val_m16, notes) in enumerate(methods_data):
        row_bg = "#FAFAFA" if i % 2 == 1 else "#FFFFFF"
        val_base_str = f"${val_base/1e6:.1f}M" if val_base else "—"
        val_m16_str = f"${val_m16/1e6:.1f}M" if val_m16 else "—"
        table_html += f'''<tr style="background:{row_bg}; border-bottom:1px solid #E2E8F0;">
            <td style="padding:0.6rem 1rem; font-weight:600;">{method}</td>
            <td style="padding:0.6rem 1rem; text-align:center; color:#718096; font-family:'JetBrains Mono', monospace;">{val_base_str}</td>
            <td style="padding:0.6rem 1rem; text-align:center; font-weight:700; color:{COLORS['success']}; font-family:'JetBrains Mono', monospace;">{val_m16_str}</td>
            <td style="padding:0.6rem 1rem; color:#718096; font-size:0.85rem;">{notes}</td>
        </tr>'''
    table_html += "</tbody></table>"
    st.markdown(table_html, unsafe_allow_html=True)

    # Rango de convergencia
    all_base_vals = [evrev['Base']['base'], evebitda_base.get('20x', 0), dcf_base_20, vol_val_base, vc_vals.get('35% IRR', 0), r40_val_base]
    all_base_vals = sorted([v for v in all_base_vals if v and v > 0])
    base_low = all_base_vals[1] if len(all_base_vals) > 2 else all_base_vals[0]
    base_high = all_base_vals[-2] if len(all_base_vals) > 2 else all_base_vals[-1]

    all_m16_vals = [evrev['Base']['m16'], evebitda_m16.get('20x', 0), dcf_m16_15, vol_val_m16, r40_val_m16]
    all_m16_vals = sorted([v for v in all_m16_vals if v and v > 0])
    m16_low = all_m16_vals[1] if len(all_m16_vals) > 2 else all_m16_vals[0]
    m16_high = all_m16_vals[-2] if len(all_m16_vals) > 2 else all_m16_vals[-1]

    st.markdown(f"""
    <div style="background:linear-gradient(135deg, rgba(0, 201, 167, 0.08), rgba(0, 102, 255, 0.08));
                border-radius:12px; padding:1.25rem; margin:1rem 0; border:1px solid rgba(0, 201, 167, 0.2);">
        <div style="font-weight:700; color:#2D3748; margin-bottom:0.5rem; font-size:1.1rem;">🎯 RANGO DE CONVERGENCIA</div>
        <div style="display:flex; gap:2rem; flex-wrap:wrap;">
            <div>
                <div style="font-size:0.85rem; color:#718096;">Base (Avg M1-M4)</div>
                <div style="font-size:1.3rem; font-weight:700; color:{COLORS['primary']};">${base_low/1e6:.0f}M — ${base_high/1e6:.0f}M</div>
            </div>
            <div>
                <div style="font-size:0.85rem; color:#718096;">Mes 16 (Proyectado)</div>
                <div style="font-size:1.3rem; font-weight:700; color:{COLORS['success']};">${m16_low/1e6:.0f}M — ${m16_high/1e6:.0f}M</div>
            </div>
            <div>
                <div style="font-size:0.85rem; color:#718096;">Múltiplo de valor</div>
                <div style="font-size:1.3rem; font-weight:700; color:{COLORS['secondary']};">×{((m16_low+m16_high)/2)/((base_low+base_high)/2):.1f}</div>
            </div>
        </div>
        <div style="font-size:0.9rem; color:#4A5568; margin-top:0.8rem;">
            La convergencia de múltiples metodologías independientes reduce el riesgo de sobre/sub-valorización.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Validación de consistencia con proyección de clientes B2B
    st.markdown(f"""
    <div style="background:{COLORS['card_bg']}; border-radius:12px; padding:1.2rem;
        border-left:4px solid {COLORS['secondary']};">
        <div style="font-weight:700; color:{COLORS['secondary']}; margin-bottom:0.5rem;">
            ✅ Validación de Consistencia — Revenue M16</div>
        <div style="font-size:0.82rem; color:#4A5568; line-height:1.7;">
            <b>Revenue total M16: {format_k(v_rev_m16)}</b><br><br>
            <b style="color:{COLORS['text']};">Capturado por modelo de clientes B2B:</b><br>
            {users_b2b_m16_val:.0f} clientes × ${rev_per_user_m16_val:,.0f}/mes =
            <b>{format_k(rev_b2b_lines_m16)}</b>
            ({rev_b2b_lines_m16/v_rev_m16*100:.0f}% del total)<br><br>
            <b style="color:{COLORS['text']};">No capturado (B2C + nuevos productos):</b><br>
            B2C: {format_k(v_rev_b2c_16)} | Nuevos: {format_k(v_rev_new_16)} =
            <b>{format_k(rev_other_m16)}</b>
            ({rev_other_m16/v_rev_m16*100:.0f}% del total)<br><br>
            <b style="color:{COLORS['text']};">Crecimiento ARPU implícito:</b><br>
            ${arpu_base:,.0f} → ${arpu_m16:,.0f}
            (<span style="color:{COLORS['success'] if arpu_growth < 40 else COLORS['warning']};">
            {'+' if arpu_growth > 0 else ''}{arpu_growth:.0f}%</span>)
            {' — plausible con cross-sell Payins y mayor volumen por cliente' if arpu_growth < 40
             else ' — ⚠️ crecimiento agresivo, revisar supuestos'}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════
    # EMPRESAS COMPARABLES
    # ═══════════════════════════════════════════════════════════
    st.markdown('<div class="section-header">🏢 Empresas Comparables — Cross-Border Payments LatAm</div>', unsafe_allow_html=True)

    comparables_html = f"""
    <div style="background:{COLORS['card_bg']}; border-radius:12px; padding:1.2rem; border:1px solid {COLORS['dark']};">
        <table style="width:100%; border-collapse:collapse;">
            <tr style="border-bottom:2px solid {COLORS['dark']};">
                <td style="color:{COLORS['muted']}; font-size:0.7rem; text-transform:uppercase; letter-spacing:1px; padding-bottom:8px;">Empresa</td>
                <td style="color:{COLORS['muted']}; font-size:0.7rem; text-transform:uppercase; letter-spacing:1px; text-align:center; padding-bottom:8px;">Revenue</td>
                <td style="color:{COLORS['muted']}; font-size:0.7rem; text-transform:uppercase; letter-spacing:1px; text-align:center; padding-bottom:8px;">EV/Rev</td>
                <td style="color:{COLORS['muted']}; font-size:0.7rem; text-transform:uppercase; letter-spacing:1px; padding-bottom:8px;">Nota</td>
            </tr>
            <tr style="border-bottom:1px solid {COLORS['dark']};">
                <td style="padding:8px 0; font-weight:600; color:{COLORS['text']}; font-size:0.85rem;">Wise</td>
                <td style="padding:8px; color:{COLORS['secondary']}; font-size:0.85rem; text-align:center;">$1.2B</td>
                <td style="padding:8px; color:{COLORS['primary']}; font-weight:700; font-size:0.85rem; text-align:center;">8-10x</td>
                <td style="padding:8px; color:{COLORS['muted']}; font-size:0.78rem;">Public. Líder global. Premium por escala y marca.</td>
            </tr>
            <tr style="border-bottom:1px solid {COLORS['dark']};">
                <td style="padding:8px 0; font-weight:600; color:{COLORS['text']}; font-size:0.85rem;">dLocal</td>
                <td style="padding:8px; color:{COLORS['secondary']}; font-size:0.85rem; text-align:center;">$660M</td>
                <td style="padding:8px; color:{COLORS['primary']}; font-weight:700; font-size:0.85rem; text-align:center;">5-7x</td>
                <td style="padding:8px; color:{COLORS['muted']}; font-size:0.78rem;">Public. LatAm puro. Compresión 2023-2024 por competencia.</td>
            </tr>
            <tr style="border-bottom:1px solid {COLORS['dark']};">
                <td style="padding:8px 0; font-weight:600; color:{COLORS['text']}; font-size:0.85rem;">Payoneer</td>
                <td style="padding:8px; color:{COLORS['secondary']}; font-size:0.85rem; text-align:center;">$870M</td>
                <td style="padding:8px; color:{COLORS['primary']}; font-weight:700; font-size:0.85rem; text-align:center;">3-5x</td>
                <td style="padding:8px; color:{COLORS['muted']}; font-size:0.78rem;">Public. Cross-border B2B. Múltiplo castigado por márgenes.</td>
            </tr>
            <tr style="border-bottom:1px solid {COLORS['dark']};">
                <td style="padding:8px 0; font-weight:600; color:{COLORS['text']}; font-size:0.85rem;">Remitly</td>
                <td style="padding:8px; color:{COLORS['secondary']}; font-size:0.85rem; text-align:center;">$950M</td>
                <td style="padding:8px; color:{COLORS['primary']}; font-weight:700; font-size:0.85rem; text-align:center;">4-6x</td>
                <td style="padding:8px; color:{COLORS['muted']}; font-size:0.78rem;">Public. B2C remesas. Alto crecimiento.</td>
            </tr>
            <tr style="border-bottom:1px solid {COLORS['dark']};">
                <td style="padding:8px 0; font-weight:600; color:{COLORS['text']}; font-size:0.85rem;">Nuvei</td>
                <td style="padding:8px; color:{COLORS['secondary']}; font-size:0.85rem; text-align:center;">$1.2B</td>
                <td style="padding:8px; color:{COLORS['primary']}; font-weight:700; font-size:0.85rem; text-align:center;">5-7x</td>
                <td style="padding:8px; color:{COLORS['muted']}; font-size:0.78rem;">Private (2024). Payments tech. Referencia de take-private.</td>
            </tr>
        </table>
        <div style="margin-top:10px; padding-top:8px; border-top:1px solid {COLORS['dark']}; text-align:center;">
            <span style="font-size:0.78rem; color:{COLORS['muted']};">
                Vita M4: <b style="color:{COLORS['primary']};">7x</b> (rango medio) →
                Vita M16: <b style="color:{COLORS['success']};">8x</b> (premium por ejecución demostrada y diversificación)
            </span>
        </div>
    </div>
    """
    st.markdown(comparables_html, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════
    # PASO 7: GRÁFICO DE BARRAS COMPARATIVO
    # ═══════════════════════════════════════════════════════════
    st.markdown('<div class="section-header">📈 Comparación Visual — Base vs M16</div>', unsafe_allow_html=True)

    method_names = [m[0] for m in methods_data]
    base_vals = [m[1]/1e6 if m[1] else 0 for m in methods_data]
    m16_vals = [m[2]/1e6 if m[2] else 0 for m in methods_data]

    fig_comp = go.Figure()
    fig_comp.add_trace(go.Bar(y=method_names, x=base_vals, name='Base (Avg M1-M4)',
        orientation='h', marker_color='#718096', text=[f"${v:.0f}M" for v in base_vals],
        textposition='outside', textfont=dict(size=12)))
    fig_comp.add_trace(go.Bar(y=method_names, x=m16_vals, name='M16 (Proyectado)',
        orientation='h', marker_color=COLORS['secondary'], text=[f"${v:.0f}M" if v > 0 else "—" for v in m16_vals],
        textposition='outside', textfont=dict(size=12)))
    fig_comp = plotly_theme(fig_comp, height=350)
    fig_comp.update_layout(barmode='group', xaxis_title="Enterprise Value ($M)",
        yaxis=dict(autorange="reversed"), legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center"))
    fig_comp.update_xaxes(range=[0, max(max(base_vals), max(m16_vals)) * 1.25])
    st.plotly_chart(fig_comp, use_container_width=True)

    # ═══════════════════════════════════════════════════════════
    # PASO 8: EXPANDERS DE DETALLE POR MÉTODO
    # ═══════════════════════════════════════════════════════════
    st.markdown('<div class="section-header">🔍 Detalle por Metodología</div>', unsafe_allow_html=True)

    with st.expander("📊 EV/Revenue — Escenarios"):
        cols = st.columns(3)
        for i, (scenario, vals) in enumerate(evrev.items()):
            mult_b = rev_multiples[scenario]['base']
            mult_m = rev_multiples[scenario]['m16']
            with cols[i]:
                st.markdown(f"""
                <div style="background:#F7FAFC; border-radius:8px; padding:1rem; text-align:center;">
                    <div style="font-weight:700; color:#2D3748;">{scenario}</div>
                    <div style="margin-top:0.5rem;">
                        <span style="color:#718096;">Base ({mult_b}x):</span>
                        <span style="font-weight:700;"> ${vals['base']/1e6:.1f}M</span>
                    </div>
                    <div>
                        <span style="color:#718096;">M16 ({mult_m}x):</span>
                        <span style="font-weight:700; color:{COLORS['success']};"> ${vals['m16']/1e6:.1f}M</span>
                    </div>
                </div>""", unsafe_allow_html=True)

    with st.expander("📊 EV/EBITDA — Múltiplos"):
        st.markdown(f"""
        <div style="display:flex; gap:1rem; flex-wrap:wrap;">
            {''.join([f'''<div style="background:#F7FAFC; border-radius:8px; padding:0.8rem; flex:1; min-width:120px; text-align:center;">
                <div style="font-weight:700;">{m}x</div>
                <div style="color:#718096; font-size:0.85rem;">Base: ${evebitda_base[m]/1e6:.1f}M</div>
                <div style="color:{COLORS['success']}; font-weight:600;">M16: ${evebitda_m16[m]/1e6:.1f}M</div>
            </div>''' for m in ['15x', '20x', '25x']])}
        </div>
        <div style="margin-top:0.8rem; color:#718096; font-size:0.9rem;">
            EBITDA Base: {format_k(v_ebitda_base_annual)}/año | EBITDA M16: {format_k(v_ebitda_m16_annual)}/año
        </div>""", unsafe_allow_html=True)

    with st.expander("📊 DCF — Proyección 5 Años"):
        dcf_table = "<table style='width:100%; font-size:0.85rem; border-collapse:collapse;'>"
        dcf_table += "<tr style='background:#F7FAFC;'><th style='padding:0.4rem;'>Año</th><th>Revenue</th><th>Margen</th><th>EBITDA</th><th>PV</th></tr>"
        for d in dcf_m16_detail:
            dcf_table += f"<tr style='border-bottom:1px solid #E2E8F0;'><td style='padding:0.4rem; text-align:center;'>{d['year']}</td><td style='text-align:right;'>${d['revenue']/1e6:.1f}M</td><td style='text-align:center;'>{d['ebitda']/d['revenue']*100:.0f}%</td><td style='text-align:right;'>${d['ebitda']/1e6:.1f}M</td><td style='text-align:right;'>${d['pv']/1e6:.1f}M</td></tr>"
        dcf_table += f"<tr style='background:#E8F5E9;'><td colspan='4' style='padding:0.4rem; font-weight:700;'>Terminal Value (PV)</td><td style='text-align:right; font-weight:700;'>${dcf_m16_tv/1e6:.1f}M</td></tr>"
        dcf_table += f"<tr style='background:{COLORS['success']}22;'><td colspan='4' style='padding:0.4rem; font-weight:800;'>TOTAL EV</td><td style='text-align:right; font-weight:800; color:{COLORS['success']};'>${dcf_m16_15/1e6:.0f}M</td></tr></table>"
        st.markdown(dcf_table, unsafe_allow_html=True)

    with st.expander("📊 VC Method — IRR Scenarios"):
        st.markdown(f"""
        <div style="margin-bottom:0.8rem; color:#4A5568;">
            <strong>Exit Value (Año 5):</strong> ${exit_value/1e6:.0f}M (Rev ${rev_year5/1e6:.0f}M × {exit_multiple}x)
        </div>
        <div style="display:flex; gap:1rem; flex-wrap:wrap;">
            {''.join([f'''<div style="background:#F7FAFC; border-radius:8px; padding:0.8rem; flex:1; min-width:100px; text-align:center;">
                <div style="font-weight:700;">{label}</div>
                <div style="color:{COLORS['success']}; font-weight:600; font-size:1.1rem;">${val/1e6:.0f}M</div>
                <div style="color:#718096; font-size:0.8rem;">PV hoy</div>
            </div>''' for label, val in vc_vals.items()])}
        </div>""", unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════
    # ESTRATEGIA DE FINANCIAMIENTO — 24 MESES
    # ═══════════════════════════════════════════════════════════
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">💰 Estrategia de Financiamiento — 24 Meses</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div style="background:{COLORS['card_bg']}; border-radius:16px; padding:1.5rem;
            border-top:4px solid {COLORS['success']}; height:100%;">
            <div style="font-size:0.7rem; color:#718096; text-transform:uppercase;
                letter-spacing:1.5px;">Fase 1</div>
            <div style="font-size:1.2rem; font-weight:700; color:{COLORS['success']};
                margin:0.3rem 0;">Meses 1-8</div>
            <div style="font-size:1rem; font-weight:600; color:{COLORS['text']};
                margin-bottom:0.8rem;">Orgánico + Líneas de Crédito</div>
            <div style="font-size:0.82rem; color:#4A5568; line-height:1.7;">
                Crecer con caja propia (${DATA['cash'][3]/1e6:.1f}M) y generación mensual
                (~{format_k(np.mean([r-g for r,g in zip(DATA['revenue'], DATA['gastos'])]))}).
                Líneas de crédito bancarias como backstop para peaks de liquidez
                al escalar GTV.<br><br>
                <b style="color:{COLORS['success']};">Sin dilución. Sin dependencia.</b><br>
                <span style="color:#718096;">Primero demostrar ejecución,
                después negociar desde fortaleza.</span>
            </div>
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="background:{COLORS['card_bg']}; border-radius:16px; padding:1.5rem;
            border-top:4px solid {COLORS['warning']}; height:100%;">
            <div style="font-size:0.7rem; color:#718096; text-transform:uppercase;
                letter-spacing:1.5px;">Fase 2</div>
            <div style="font-size:1.2rem; font-weight:700; color:{COLORS['warning']};
                margin:0.3rem 0;">Meses 9-16</div>
            <div style="font-size:1rem; font-weight:600; color:{COLORS['text']};
                margin-bottom:0.8rem;">Evaluar + Venture Debt</div>
            <div style="font-size:0.82rem; color:#4A5568; line-height:1.7;">
                Si el cash flow cubre el crecimiento, mantener orgánico.
                Si hay oportunidad de acelerar (competidor débil, país que
                se abre rápido), evaluar venture debt: $2-3M con dilución
                mínima.<br><br>
                <b style="color:{COLORS['warning']};">Ideal para fintech con revenue
                predecible.</b><br>
                <span style="color:#718096;">Venture debt no requiere
                ceder board seats ni control.</span>
            </div>
        </div>""", unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div style="background:{COLORS['card_bg']}; border-radius:16px; padding:1.5rem;
            border-top:4px solid {COLORS['primary']}; height:100%;">
            <div style="font-size:0.7rem; color:#718096; text-transform:uppercase;
                letter-spacing:1.5px;">Fase 3</div>
            <div style="font-size:1.2rem; font-weight:700; color:{COLORS['primary']};
                margin:0.3rem 0;">Meses 17-24</div>
            <div style="font-size:1rem; font-weight:600; color:{COLORS['text']};
                margin-bottom:0.8rem;">Equity desde Fortaleza</div>
            <div style="font-size:0.82rem; color:#4A5568; line-height:1.7;">
                Solo si hay oportunidad de aceleración que lo justifique.
                Con ejecución demostrada:<br><br>
                Pre-money: <b>$80-100M</b><br>
                Round: <b>$5-10M</b><br>
                Uso: aceleración, no sobrevivencia<br><br>
                <b style="color:{COLORS['primary']};">"Levantamos porque queremos,
                no porque necesitamos."</b><br>
                <span style="color:#718096;">Posición de negociación
                completamente distinta.</span>
            </div>
        </div>""", unsafe_allow_html=True)

    # Principio rector
    st.markdown(f"""
    <div style="background:linear-gradient(135deg, {COLORS['primary']}15, {COLORS['success']}15);
        border:1px solid {COLORS['primary']}33; border-radius:12px; padding:1rem;
        margin-top:1rem; text-align:center;">
        <span style="font-size:0.9rem; color:#4A5568;">
            <b style="color:{COLORS['text']};">Principio rector:</b>
            Alineado con la filosofía de los fundadores — disciplina financiera,
            cash flow positivo, crecimiento sostenible. Equity es una herramienta
            de aceleración, no un modelo de negocio.
        </span>
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {COLORS['primary']}22, {COLORS['secondary']}22);
                border: 1px solid {COLORS['primary']}44; border-radius:16px; padding:1.5rem; text-align:center;">
        <div style="font-size:1.3rem; font-weight:800; background: linear-gradient(135deg, #00C9A7, #0066FF); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            Discipline + Technology + Expertise = {v_growth_multiple:.1f}x Sostenible
        </div>
        <div style="color:#718096; margin-top:0.4rem; font-size:0.85rem;">
            Pablo Martinez — CFO Candidate | Febrero 2026
        </div>
    </div>""", unsafe_allow_html=True)
