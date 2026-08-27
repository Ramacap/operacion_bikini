"""
app.py - Operación Bikini 🌴👙☀️
Aplicación de seguimiento y competencia de descenso de peso con temática de Río de Janeiro.
Diseño adaptable (responsive) con menú de botones 2x2 para móviles, tipografías oscuras de alto contraste
y gráficos fijos sin zoom accidental para celulares.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import data_manager as dm

# Paleta de colores vibrantes para gráfico grupal (estilo Copacabana)
TROPICAL_PALETTE = [
    "#FF6B6B",  # Coral
    "#0077B6",  # Océano
    "#06D6A0",  # Teal
    "#FFBE0B",  # Sol
    "#E63946",  # Rojo arena
    "#7209B7",  # Violeta tropical
    "#FF8E53",  # Atardecer
    "#00B4D8",  # Cielo
    "#F72585",  # Fucsia
    "#4361EE",  # Azul eléctrico
]

# Configuración de página
st.set_page_config(
    page_title="Operación Bikini 🌴 Río Edition",
    page_icon="👙",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inyección de estilos CSS personalizados con ALTO CONTRASTE y compatibilidad móvil total
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    /* =========================================================
       FORZAR TEMA CLARO Y TIPOGRAFÍAS EN NEGRO / OSCURO
       Evita que el modo oscuro del móvil ponga textos o fondos invisibles
       ========================================================= */
    .stApp, .stApp > div, [data-testid="stAppViewContainer"], [data-testid="block-container"] {
        background-color: #FFFDF9 !important;
        color: #1A202C !important;
    }
    
    /* Tipografía general */
    p, span, label, div, small, strong, b, li {
        color: #1A202C !important;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #1A202C !important;
        font-weight: 800 !important;
    }
    .stCaption, [data-testid="stCaptionContainer"] * {
        color: #4A5568 !important;
        font-weight: 600 !important;
    }

    /* =========================================================
       INPUTS, SELECTBOXES Y FORMULARIOS — TEXTO SIEMPRE NEGRO
       ========================================================= */
    input, input[type="text"], input[type="number"], textarea {
        color: #1A202C !important;
        -webkit-text-fill-color: #1A202C !important;
        background-color: #FFFFFF !important;
        border: 2px solid #CBD5E0 !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
    }
    input:focus, textarea:focus {
        border-color: #FF8E53 !important;
        box-shadow: 0 0 0 2px rgba(255, 142, 83, 0.25) !important;
    }
    
    /* Selectboxes y Dropdowns */
    div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        border-radius: 12px !important;
    }
    div[data-baseweb="select"] * {
        color: #1A202C !important;
        -webkit-text-fill-color: #1A202C !important;
        font-weight: 600 !important;
    }
    div[data-baseweb="popover"], div[data-baseweb="popover"] * {
        background-color: #FFFFFF !important;
        color: #1A202C !important;
    }
    ul[role="listbox"] {
        background-color: #FFFFFF !important;
    }
    li[role="option"] {
        background-color: #FFFFFF !important;
        color: #1A202C !important;
    }
    li[role="option"] * {
        color: #1A202C !important;
    }
    li[role="option"]:hover, li[role="option"][aria-selected="true"] {
        background-color: #FFE3C2 !important;
        color: #1A202C !important;
    }

    /* Encabezado Principal */
    .main-header {
        background: linear-gradient(135deg, #FF6B6B 0%, #FFBE0B 50%, #00F5D4 100%);
        padding: 22px 16px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 16px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.12);
    }
    .main-header h1 {
        color: white !important;
        font-size: 2.2rem;
        font-weight: 900;
        margin: 0;
        letter-spacing: 1.5px;
        text-shadow: 2px 2px 5px rgba(0,0,0,0.25);
    }
    .main-header p {
        color: white !important;
        font-size: 1rem;
        margin-top: 5px;
        margin-bottom: 0;
        font-weight: 600;
    }
    
    /* Banner de Cuenta Regresiva */
    .countdown-card {
        background: #FFF3E2;
        border-left: 6px solid #FF6B6B;
        padding: 14px 18px;
        border-radius: 12px;
        margin-bottom: 16px;
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: space-between;
        gap: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .countdown-card * {
        color: #1A202C !important;
    }
    .countdown-days {
        font-size: 1.8rem;
        font-weight: 900;
        color: #E63946 !important;
        line-height: 1;
    }
    .countdown-days small {
        font-size: 0.85rem;
        font-weight: 700;
        display: block;
        color: #E63946 !important;
    }
    
    /* Salón de la Gloria */
    .hall-of-fame-card {
        background: #FFF9E6;
        border: 2px solid #F39C12;
        border-radius: 16px;
        padding: 16px 20px;
        margin-bottom: 18px;
        box-shadow: 0 4px 12px rgba(243, 156, 18, 0.18);
    }
    .hall-of-fame-card h3 {
        color: #B7791F !important;
        margin: 0 0 6px 0;
    }
    .hall-of-fame-card p {
        color: #744210 !important;
        margin: 0;
        font-size: 0.95rem;
    }

    /* =========================================================
       BOTONES DEL MENÚ DE NAVEGACIÓN (3D, VISIBLES, 2x2 EN MÓVIL)
       ========================================================= */
    .nav-btn-active button {
        background: linear-gradient(180deg, #FF6B6B 0%, #EE5253 100%) !important;
        border: 2px solid #C53030 !important;
        border-bottom: 4px solid #9B2C2C !important;
        color: #FFFFFF !important;
        font-weight: 800 !important;
        font-size: 0.95rem !important;
        border-radius: 20px !important;
        box-shadow: 0 4px 0 #9B2C2C, 0 6px 12px rgba(238, 82, 83, 0.35) !important;
        padding: 12px 10px !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.2) !important;
    }
    .nav-btn-inactive button {
        background: linear-gradient(180deg, #FFFFFF 0%, #FFF0D4 100%) !important;
        border: 2px solid #F6AD55 !important;
        border-bottom: 4px solid #DD6B20 !important;
        color: #1A202C !important;
        font-weight: 800 !important;
        font-size: 0.95rem !important;
        border-radius: 20px !important;
        box-shadow: 0 4px 0 #DD6B20, 0 6px 10px rgba(221, 107, 32, 0.15) !important;
        padding: 12px 10px !important;
    }
    .nav-btn-inactive button:hover {
        background: #FFE2B8 !important;
        transform: translateY(-2px);
    }
    .nav-btn-active button:active, .nav-btn-inactive button:active {
        transform: translateY(3px) !important;
        box-shadow: 0 1px 0 #DD6B20 !important;
    }

    /* Botones de acción estándar (3D Naranja/Pastel) */
    .stButton>button {
        background: linear-gradient(180deg, #FFF6EC 0%, #FFE5CE 100%) !important;
        border: 2px solid #F6AD55 !important;
        border-bottom: 3px solid #DD6B20 !important;
        color: #1A202C !important;
        font-weight: 800 !important;
        border-radius: 22px !important;
        box-shadow: 0 3px 0 #DD6B20, 0 4px 8px rgba(0,0,0,0.06) !important;
        padding: 8px 16px !important;
    }
    .stButton>button:hover {
        background: #FFD9B8 !important;
        color: #1A202C !important;
    }
    .stButton>button:active {
        transform: translateY(2px) !important;
        box-shadow: 0 1px 0 #DD6B20 !important;
    }
    
    /* Botones primarios (formularios / confirmar) */
    div[data-testid="stForm"] button[kind="primaryFormSubmit"], button[kind="primary"] {
        background: linear-gradient(180deg, #FF6B6B 0%, #EE5253 100%) !important;
        border: 2px solid #C53030 !important;
        border-bottom: 4px solid #9B2C2C !important;
        color: #FFFFFF !important;
        font-weight: 800 !important;
        border-radius: 25px !important;
        box-shadow: 0 4px 0 #9B2C2C !important;
    }

    /* =========================================================
       TARJETAS DE MÉTRICAS (2x2) CON MÁXIMO CONTRASTE
       ========================================================= */
    div[data-testid="stMetric"] {
        background: #FFFFFF !important;
        padding: 12px 14px !important;
        border-radius: 14px !important;
        border: 2px solid #FFD166 !important;
        box-shadow: 0 3px 8px rgba(0,0,0,0.04) !important;
        text-align: center !important;
    }
    div[data-testid="stMetricLabel"] * {
        font-size: 0.88rem !important;
        font-weight: 700 !important;
        color: #4A5568 !important;
    }
    div[data-testid="stMetricValue"] * {
        font-size: 1.55rem !important;
        font-weight: 900 !important;
        color: #1A202C !important;
    }

    /* Tarjeta vacía de bienvenida */
    .welcome-empty {
        text-align: center;
        padding: 30px 20px;
        background: #FFFFFF;
        border-radius: 16px;
        border: 2px dashed #FFD166;
        margin-top: 12px;
        box-shadow: 0 3px 8px rgba(0,0,0,0.03);
    }
    .welcome-empty .emoji-big { font-size: 3rem; }
    .welcome-empty h3 { color: #FF6B6B !important; margin-top: 10px; }
    .welcome-empty p { color: #4A5568 !important; max-width: 500px; margin: 6px auto 0; font-size: 0.92rem; font-weight: 600; }

    /* Pie de página */
    .footer-rio {
        text-align: center;
        padding: 18px 10px;
        margin-top: 25px;
        color: #718096 !important;
        font-size: 0.82rem;
        font-weight: 600;
        border-top: 1px solid #E2E8F0;
    }

    /* Adaptación Responsive para Móviles */
    @media (max-width: 768px) {
        .main-header { padding: 14px 10px; }
        .main-header h1 { font-size: 1.4rem !important; }
        .main-header p { font-size: 0.82rem !important; }
        div[data-testid="stMetricValue"] * { font-size: 1.3rem !important; }
        .countdown-card {
            font-size: 0.85rem;
            flex-direction: column;
            text-align: center;
        }
        .countdown-days { font-size: 1.4rem; }
    }
</style>
""", unsafe_allow_html=True)


# --- ENCABEZADO Y ESTADO DE COMPETENCIA ---
is_closed, days_left, deadline_str = dm.get_competition_status()

st.markdown("""
<div class="main-header">
    <h1>🌴 OPERACIÓN BIKINI 👙</h1>
    <p>🏖️ Edición Río de Janeiro • ¡Rumbo al verano en forma y fabulosas! 🍹☀️</p>
</div>
""", unsafe_allow_html=True)

# Banner de cuenta regresiva
if is_closed:
    st.error(f"🏁 **¡La competencia finalizó el {deadline_str}!** Ya no se aceptan nuevos pesajes. ¡Felicitaciones a todas por participar! 🏆🍹")
else:
    st.markdown(f"""
    <div class="countdown-card">
        <div>
            <span style="font-size: 1.3rem;">⏳</span> 
            <strong>Gran Final: {deadline_str}</strong> — Cierre definitivo de cargas.
        </div>
        <div class="countdown-days">
            {days_left} <small>☀️ días para el verano</small>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- MURO DE LA GLORIA / META CUMPLIDA ---
hall_of_fame = dm.get_hall_of_fame()
if hall_of_fame:
    st.markdown("""
    <div class="hall-of-fame-card">
        <h3 style="margin: 0 0 6px 0; color: #B7791F;">👑 SALÓN DE LA GLORIA: ¡CHICAS BIKINI DE ORO! 👑</h3>
        <p style="margin: 0; font-size: 0.92rem; color: #744210;">
            ¡Un aplauso gigante para las participantes que ya alcanzaron su peso objetivo! 👏🎉🍾
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    cols = st.columns(min(len(hall_of_fame), 4))
    for idx, champ in enumerate(hall_of_fame):
        with cols[idx % 4]:
            st.success(f"🏆 **{champ['nickname']}**\n\n🎯 Meta: {champ['target_weight']} kg\n\n⚖️ Actual: **{champ['current_weight']} kg**\n\n📉 Bajó: **{champ['total_lost']} kg** 🎉")


# =========================================================
# MENÚ PRINCIPAL TIPO BOTONES (DISPUESTO EN GRILLA 2x2 PARA CELULAR)
# =========================================================
if "active_nav_tab" not in st.session_state:
    st.session_state.active_nav_tab = "🏖️ Mi Progreso"

# Fila 1 del Menú (2 botones)
nav_r1_c1, nav_r1_c2 = st.columns(2)
with nav_r1_c1:
    btn_class1 = "nav-btn-active" if st.session_state.active_nav_tab == "🏖️ Mi Progreso" else "nav-btn-inactive"
    st.markdown(f'<div class="{btn_class1}">', unsafe_allow_html=True)
    if st.button("🏖️ Mi Progreso", key="btn_nav_progreso", use_container_width=True):
        st.session_state.active_nav_tab = "🏖️ Mi Progreso"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with nav_r1_c2:
    btn_class2 = "nav-btn-active" if st.session_state.active_nav_tab == "📊 Competencia" else "nav-btn-inactive"
    st.markdown(f'<div class="{btn_class2}">', unsafe_allow_html=True)
    if st.button("📊 Competencia", key="btn_nav_competencia", use_container_width=True):
        st.session_state.active_nav_tab = "📊 Competencia"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# Fila 2 del Menú (2 botones)
nav_r2_c1, nav_r2_c2 = st.columns(2)
with nav_r2_c1:
    btn_class3 = "nav-btn-active" if st.session_state.active_nav_tab == "➕ Nueva Participante" else "nav-btn-inactive"
    st.markdown(f'<div class="{btn_class3}">', unsafe_allow_html=True)
    if st.button("➕ Nueva Amiga", key="btn_nav_nueva", use_container_width=True):
        st.session_state.active_nav_tab = "➕ Nueva Participante"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with nav_r2_c2:
    btn_class4 = "nav-btn-active" if st.session_state.active_nav_tab == "✏️ Historial" else "nav-btn-inactive"
    st.markdown(f'<div class="{btn_class4}">', unsafe_allow_html=True)
    if st.button("✏️ Historial", key="btn_nav_historial", use_container_width=True):
        st.session_state.active_nav_tab = "✏️ Historial"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# Fila 3 del Menú (1 botón centrado / ancho)
nav_r3_c1, nav_r3_c2, nav_r3_c3 = st.columns([1, 2, 1])
with nav_r3_c2:
    btn_class5 = "nav-btn-active" if st.session_state.active_nav_tab == "💾 Copia de Seguridad" else "nav-btn-inactive"
    st.markdown(f'<div class="{btn_class5}">', unsafe_allow_html=True)
    if st.button("💾 Copia de Seguridad", key="btn_nav_backup", use_container_width=True):
        st.session_state.active_nav_tab = "💾 Copia de Seguridad"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

all_users = dm.get_all_users()


# =========================================================
# VISTA 1: MI PROGRESO & CARGAR PESO
# =========================================================
if st.session_state.active_nav_tab == "🏖️ Mi Progreso":
    if not all_users:
        st.info("👋 ¡Aún no hay participantes registradas! Toca arriba en **➕ Nueva Amiga** para comenzar.")
    else:
        if "selected_nickname" not in st.session_state:
            st.session_state.selected_nickname = None

        # Contenedor limpio para el selector de apodo
        with st.container(border=True):
            def clear_user_selection_callback():
                st.session_state.selected_nickname = None
                st.session_state["select_user_progress_dropdown"] = "-- Elige tu Apodo en la lista --"

            col_sel_text, col_sel_btn = st.columns([3, 1])
            with col_sel_text:
                st.markdown("### 👤 Selecciona tu Apodo:")
            with col_sel_btn:
                st.button("❌ Borrar", key="btn_clear_user_selection", on_click=clear_user_selection_callback, use_container_width=True)

            options = ["-- Elige tu Apodo en la lista --"] + all_users
            
            if "select_user_progress_dropdown" not in st.session_state or st.session_state["select_user_progress_dropdown"] not in options:
                if st.session_state.selected_nickname and st.session_state.selected_nickname in all_users:
                    st.session_state["select_user_progress_dropdown"] = st.session_state.selected_nickname
                else:
                    st.session_state["select_user_progress_dropdown"] = "-- Elige tu Apodo en la lista --"

            chosen_option = st.selectbox(
                "Elige tu apodo:",
                options=options,
                label_visibility="collapsed",
                key="select_user_progress_dropdown"
            )

            if chosen_option != "-- Elige tu Apodo en la lista --":
                st.session_state.selected_nickname = chosen_option
            else:
                st.session_state.selected_nickname = None

        # Si NO hay apodo seleccionado
        if not st.session_state.selected_nickname:
            st.markdown("""
            <div class="welcome-empty">
                <span class="emoji-big">🌴👙</span>
                <h3>¡Hola! Elige tu apodo arriba para ver tu progreso</h3>
                <p>
                    Selecciona tu nombre en la lista para ver tus kilos bajados,
                    registrar tu pesaje de hoy y visualizar tu gráfico hacia el objetivo.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            selected_user = st.session_state.selected_nickname
            stats = dm.get_user_stats(selected_user)
            
            if stats:
                st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
                
                # Formulario de Carga y Estadísticas (2x2 cuadrado)
                col_form, col_metrics = st.columns([1, 1.2])
                
                with col_form:
                    st.subheader("⚖️ Cargar Peso de Hoy")
                    today_display = date.today().strftime("%d/%m/%Y")
                    st.caption(f"📅 Fecha: **{today_display}** (si ya cargaste hoy, se actualizará)")
                    
                    if is_closed:
                        st.warning("⚠️ La competencia finalizó. No es posible registrar nuevos pesajes.")
                    else:
                        with st.form("form_log_weight", clear_on_submit=False):
                            new_weight = st.number_input(
                                f"Nuevo peso de {selected_user} (kg):",
                                min_value=30.0,
                                max_value=250.0,
                                value=float(stats["current_weight"]),
                                step=0.1,
                                format="%.1f",
                                key="input_log_new_weight"
                            )
                            btn_log = st.form_submit_button("🌴 Guardar Pesaje", use_container_width=True)
                            
                            if btn_log:
                                success, msg = dm.log_weight(selected_user, new_weight)
                                if success:
                                    if new_weight <= stats["target_weight"]:
                                        st.balloons()
                                        st.success(f"🎉🎉 ¡FELICITACIONES {selected_user.upper()}! ¡ALCANZASTE TU META DE {stats['target_weight']} kg! 🍾👙☀️")
                                    else:
                                        st.success(msg)
                                    st.rerun()
                                else:
                                    st.error(msg)
                                    
                with col_metrics:
                    st.subheader(f"📊 Métricas de {selected_user}")
                    
                    # Cuadrado 2x2 de métricas para celular y PC
                    m_r1_c1, m_r1_c2 = st.columns(2)
                    with m_r1_c1:
                        st.metric(
                            label="Peso Actual",
                            value=f"{stats['current_weight']} kg"
                        )
                    with m_r1_c2:
                        delta_val = stats['last_delta']
                        st.metric(
                            label="Último Cambio",
                            value=f"{stats['current_weight']} kg",
                            delta=f"{delta_val:+.1f} kg" if len(stats["history"]) > 1 else "Inicio",
                            delta_color="inverse"
                        )
                        
                    m_r2_c1, m_r2_c2 = st.columns(2)
                    with m_r2_c1:
                        st.metric(
                            label="Total Bajado",
                            value=f"{stats['total_lost']} kg",
                            delta=f"{-stats['total_delta']:+.1f} kg",
                            delta_color="normal"
                        )
                    with m_r2_c2:
                        if stats["goal_achieved"]:
                            st.metric(label="Meta", value="¡Cumplida! 👑", delta="Superada 🌟")
                        else:
                            st.metric(
                                label="Faltan para Meta",
                                value=f"{stats['remaining_to_goal']} kg",
                                delta=f"Meta: {stats['target_weight']} kg",
                                delta_color="off"
                            )
                    
                    # Barra de progreso motivacional
                    prog_pct = min(max(stats["progress_pct"], 0.0), 100.0)
                    st.markdown(f"**Progreso hacia la meta ({stats['target_weight']} kg): {stats['progress_pct']}%**")
                    st.progress(prog_pct / 100.0)
                
                # Gráfico individual sin zoom accidental (fijo para móvil)
                st.markdown("---")
                st.subheader(f"📈 Evolución de Peso — {selected_user}")
                
                df_user = pd.DataFrame(stats["history"])
                df_user["Fecha_dt"] = pd.to_datetime(df_user["date"])
                df_user = df_user.sort_values(by="Fecha_dt")
                
                fig_user = go.Figure()
                
                # Área degradada
                fig_user.add_trace(go.Scatter(
                    x=df_user["Fecha_dt"],
                    y=df_user["weight"],
                    mode='lines',
                    line=dict(width=0),
                    showlegend=False,
                    hoverinfo='skip',
                    fill='tozeroy',
                    fillcolor='rgba(255, 107, 107, 0.10)'
                ))
                
                # Línea de peso real del usuario
                fig_user.add_trace(go.Scatter(
                    x=df_user["Fecha_dt"],
                    y=df_user["weight"],
                    mode='lines+markers',
                    name=f'{selected_user}',
                    line=dict(color="#FF6B6B", width=3.5, shape='spline'),
                    marker=dict(size=10, color="#E63946", line=dict(color='white', width=2)),
                    hovertemplate="<b>%{x|%d/%m/%Y}</b><br>Peso: <b>%{y:.1f} kg</b><extra></extra>"
                ))
                
                # Línea del peso inicial
                fig_user.add_hline(
                    y=stats["start_weight"],
                    line_dash="dot",
                    line_color="#A0AEC0",
                    line_width=1.5,
                    annotation_text=f"Inicio: {stats['start_weight']} kg",
                    annotation_position="top left",
                    annotation_font=dict(size=11, color="#4A5568", family="Poppins")
                )
                
                # Línea de meta punteada
                fig_user.add_hline(
                    y=stats["target_weight"],
                    line_dash="dash",
                    line_color="#06D6A0",
                    line_width=3,
                    annotation_text=f"🎯 Meta: {stats['target_weight']} kg",
                    annotation_position="bottom right",
                    annotation_font=dict(size=12, color="#058C68", family="Poppins")
                )
                
                # Ajuste de límites del eje Y
                all_weights_vals = [item["weight"] for item in stats["history"]] + [stats["target_weight"], stats["start_weight"]]
                y_min = min(all_weights_vals) - 2.0
                y_max = max(all_weights_vals) + 2.0
                
                fig_user.update_layout(
                    xaxis_title="Fecha",
                    yaxis_title="Peso (kg)",
                    yaxis=dict(
                        range=[y_min, y_max],
                        gridcolor='#E2E8F0',
                        fixedrange=True,  # Desactiva zoom accidental en móvil
                        tickfont=dict(color='#1A202C', size=11, family='Poppins'),
                        title_font=dict(color='#1A202C', size=13, family='Poppins')
                    ),
                    xaxis=dict(
                        gridcolor='#E2E8F0',
                        fixedrange=True,  # Desactiva zoom accidental en móvil
                        tickfont=dict(color='#1A202C', size=11, family='Poppins'),
                        title_font=dict(color='#1A202C', size=13, family='Poppins')
                    ),
                    hovermode="x unified",
                    dragmode=False,       # Desactiva arrastrar/pan en móvil
                    hoverlabel=dict(
                        bgcolor="#FFFFFF",
                        font_color="#1A202C",
                        font_size=12,
                        font_family="Poppins",
                        bordercolor="#CBD5E0"
                    ),
                    template="plotly_white",
                    height=400,
                    margin=dict(l=10, r=10, t=30, b=20),
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1,
                        font=dict(color="#1A202C", size=11, family="Poppins")
                    ),
                    paper_bgcolor='#FFFFFF',
                    plot_bgcolor='#FFFFFF',
                    font=dict(color='#1A202C', family='Poppins')
                )
                fig_user.update_xaxes(dtick="D1", tickformat="%d/%m")
                
                st.plotly_chart(
                    fig_user,
                    use_container_width=True,
                    config={'displayModeBar': False, 'scrollZoom': False, 'doubleClick': False}
                )


# =========================================================
# VISTA 2: COMPETENCIA GENERAL
# =========================================================
elif st.session_state.active_nav_tab == "📊 Competencia":
    st.subheader("🏖️ Gráfico Comparativo del Grupo")
    df_all = dm.get_all_weights_dataframe()
    
    if df_all.empty:
        st.info("Aún no hay pesajes cargados para graficar.")
    else:
        if "multiselect_group_users_widget" not in st.session_state:
            st.session_state["multiselect_group_users_widget"] = all_users.copy()
        else:
            st.session_state["multiselect_group_users_widget"] = [
                u for u in st.session_state["multiselect_group_users_widget"] if u in all_users
            ]

        def select_all_group_callback():
            st.session_state["multiselect_group_users_widget"] = all_users.copy()

        def clear_all_group_callback():
            st.session_state["multiselect_group_users_widget"] = []

        col_btn1, col_btn2, col_radio = st.columns([1, 1, 2])
        with col_btn1:
            st.button("🔘 Todos", key="btn_select_all_group_users", on_click=select_all_group_callback, use_container_width=True)
        with col_btn2:
            st.button("❌ Ninguno", key="btn_clear_all_group_users", on_click=clear_all_group_callback, use_container_width=True)
        with col_radio:
            view_metric = st.radio(
                "Métrica:",
                options=["Peso Actual (kg)", "Kilos Bajados (kg)"],
                horizontal=True,
                key="radio_group_metric_choice"
            )
            
        selected_participants = st.multiselect(
            "Participantes visibles:",
            options=all_users,
            key="multiselect_group_users_widget"
        )
        
        df_filtered = df_all[df_all["Participante"].isin(selected_participants)]
        
        if not df_filtered.empty:
            y_col = "Peso (kg)" if view_metric == "Peso Actual (kg)" else "Kilos Bajados"
            
            fig_group = px.line(
                df_filtered,
                x="Fecha_dt",
                y=y_col,
                color="Participante",
                markers=True,
                title=f"Evolución Diaria — {view_metric}",
                labels={"Fecha_dt": "Fecha", y_col: view_metric},
                color_discrete_sequence=TROPICAL_PALETTE
            )
            
            fig_group.update_traces(
                line=dict(width=3, shape='spline'),
                marker=dict(size=9, line=dict(color='white', width=1.5)),
                hovertemplate="<b>%{data.name}</b><br>Fecha: %{x|%d/%m/%Y}<br>" + view_metric + ": <b>%{y:.1f} kg</b><extra></extra>"
            )
            
            fig_group.update_layout(
                xaxis_title="Fecha",
                yaxis_title=view_metric,
                hovermode="x unified",
                dragmode=False,       # Desactiva arrastrar/pan en móvil
                hoverlabel=dict(
                    bgcolor="#FFFFFF",
                    font_color="#1A202C",
                    font_size=12,
                    font_family="Poppins",
                    bordercolor="#CBD5E0"
                ),
                template="plotly_white",
                height=480,
                margin=dict(l=10, r=10, t=40, b=20),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="center",
                    x=0.5,
                    font=dict(color="#1A202C", size=11, family="Poppins")
                ),
                paper_bgcolor='#FFFFFF',
                plot_bgcolor='#FFFFFF',
                yaxis=dict(
                    gridcolor='#E2E8F0',
                    fixedrange=True,  # Desactiva zoom accidental en móvil
                    tickfont=dict(color='#1A202C', size=11, family='Poppins'),
                    title_font=dict(color='#1A202C', size=13, family='Poppins')
                ),
                xaxis=dict(
                    gridcolor='#E2E8F0',
                    fixedrange=True,  # Desactiva zoom accidental en móvil
                    tickfont=dict(color='#1A202C', size=11, family='Poppins'),
                    title_font=dict(color='#1A202C', size=13, family='Poppins')
                ),
                font=dict(color='#1A202C', family='Poppins'),
                title=dict(font=dict(color='#1A202C', size=14, family='Poppins'))
            )
            fig_group.update_xaxes(dtick="D1", tickformat="%d/%m")
            
            st.plotly_chart(
                fig_group,
                use_container_width=True,
                config={'displayModeBar': False, 'scrollZoom': False, 'doubleClick': False}
            )
        else:
            st.warning("Selecciona al menos una participante para visualizar el gráfico.")
            
        # Ranking del Verano ordenado por % hacia la meta
        st.markdown("---")
        st.subheader("🏆 Ranking del Verano")
        all_stats = dm.get_all_stats()
        
        if all_stats:
            all_stats.sort(key=lambda x: (x["progress_pct"], x["total_lost"]), reverse=True)
            
            for rank, s in enumerate(all_stats, 1):
                if rank == 1:
                    medal = "🥇"
                    bg = "#FFF9E6"
                    border_col = "#F6AD55"
                elif rank == 2:
                    medal = "🥈"
                    bg = "#F7FAFC"
                    border_col = "#A0AEC0"
                elif rank == 3:
                    medal = "🥉"
                    bg = "#FFFAF0"
                    border_col = "#DD6B20"
                else:
                    medal = f"#{rank}"
                    bg = "#FFFFFF"
                    border_col = "#E2E8F0"
                    
                prog_bar_width = min(max(s['progress_pct'], 0), 100)
                prog_color = "#06D6A0" if s["goal_achieved"] else "#FF6B6B"
                status_text = "👑 ¡Meta Lograda!" if s["goal_achieved"] else f"Faltan {s['remaining_to_goal']} kg"
                
                st.markdown(f"""
                <div style="
                    background: {bg};
                    border-left: 5px solid {border_col};
                    border-radius: 12px;
                    padding: 12px 14px;
                    margin-bottom: 8px;
                    display: flex;
                    flex-wrap: wrap;
                    align-items: center;
                    gap: 12px;
                    box-shadow: 0 2px 6px rgba(0,0,0,0.04);
                ">
                    <div style="font-size: 1.6rem; min-width: 40px; text-align: center; color: #1A202C;">{medal}</div>
                    <div style="flex: 1; min-width: 110px;">
                        <div style="font-weight: 800; font-size: 1.05rem; color: #1A202C;">{s['nickname']}</div>
                        <div style="font-size: 0.8rem; color: #4A5568;">{s['start_weight']} → {s['current_weight']} kg (meta: {s['target_weight']})</div>
                    </div>
                    <div style="flex: 2; min-width: 180px;">
                        <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: #1A202C; margin-bottom: 4px;">
                            <span>Bajó <b style="color:#1A202C;">{s['total_lost']} kg</b></span>
                            <span><b style="color:#1A202C;">{s['progress_pct']}%</b></span>
                        </div>
                        <div style="background: #E2E8F0; border-radius: 10px; height: 8px; overflow: hidden;">
                            <div style="background: {prog_color}; width: {prog_bar_width}%; height: 100%; border-radius: 10px;"></div>
                        </div>
                    </div>
                    <div style="min-width: 120px; text-align: right; font-size: 0.82rem; font-weight: 700; color: {'#058C68' if s['goal_achieved'] else '#4A5568'};">
                        {status_text}
                    </div>
                </div>
                """, unsafe_allow_html=True)


# =========================================================
# VISTA 3: NUEVA PARTICIPANTE
# =========================================================
elif st.session_state.active_nav_tab == "➕ Nueva Participante":
    st.subheader("➕ Registrar Nueva Participante")
    st.markdown("Suma una amiga al desafío de **Operación Bikini**. Su peso inicial quedará registrado como el punto de partida.")
    
    with st.form("form_new_user", clear_on_submit=True):
        col_n1, col_n2, col_n3 = st.columns(3)
        with col_n1:
            new_nickname = st.text_input("Apodo / Nombre:", placeholder="Ej: Caro, Lucre, Mari...", key="input_new_nickname")
        with col_n2:
            new_start_weight = st.number_input("Peso Inicial (kg):", min_value=30.0, max_value=250.0, value=70.0, step=0.1, format="%.1f", key="input_new_start_weight")
        with col_n3:
            new_target_weight = st.number_input("Peso Objetivo (kg):", min_value=30.0, max_value=250.0, value=65.0, step=0.1, format="%.1f", key="input_new_target_weight")
            
        btn_add_user = st.form_submit_button("🍹 Registrar Participante", use_container_width=True)
        
        if btn_add_user:
            if not new_nickname:
                st.error("Por favor ingresa un apodo.")
            else:
                success, msg = dm.add_user(new_nickname, new_start_weight, new_target_weight)
                if success:
                    clean_nick = new_nickname.strip()
                    st.session_state.selected_nickname = clean_nick
                    st.session_state["select_user_progress_dropdown"] = clean_nick
                    if "multiselect_group_users_widget" in st.session_state:
                        current_list = list(st.session_state["multiselect_group_users_widget"])
                        if clean_nick not in current_list:
                            current_list.append(clean_nick)
                            st.session_state["multiselect_group_users_widget"] = current_list
                    st.session_state.active_nav_tab = "🏖️ Mi Progreso"
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)


# =========================================================
# VISTA 4: HISTORIAL & CORRECCIÓN
# =========================================================
elif st.session_state.active_nav_tab == "✏️ Historial":
    st.subheader("✏️ Modificar o Eliminar Pesajes")
    st.caption("Si cargaste mal un número o quieres corregir un pesaje anterior, puedes gestionarlo aquí.")
    
    if not all_users:
        st.info("No hay participantes cargadas.")
    else:
        if "select_user_to_edit_history" in st.session_state and st.session_state["select_user_to_edit_history"] not in all_users:
            st.session_state.pop("select_user_to_edit_history", None)

        user_to_edit = st.selectbox("Selecciona participante:", options=all_users, key="select_user_to_edit_history")
        user_stats = dm.get_user_stats(user_to_edit)
        
        if user_stats:
            history = user_stats["history"]
            
            col_tbl, col_actions = st.columns([1, 1])
            with col_tbl:
                st.markdown(f"**Historial de pesajes de {user_to_edit}:**")
                df_hist = pd.DataFrame(history)
                df_hist["Fecha"] = pd.to_datetime(df_hist["date"]).dt.strftime("%d/%m/%Y")
                df_hist["Peso (kg)"] = df_hist["weight"]
                st.dataframe(df_hist[["Fecha", "Peso (kg)"]], use_container_width=True, hide_index=True)
                
            with col_actions:
                st.markdown("**Acciones de corrección:**")
                dates_available = [item["date"] for item in history]
                
                if "select_date_to_edit_history" in st.session_state and st.session_state["select_date_to_edit_history"] not in dates_available:
                    st.session_state.pop("select_date_to_edit_history", None)

                selected_date = st.selectbox("Selecciona la fecha a modificar o eliminar:", options=dates_available, key="select_date_to_edit_history")
                current_val = next((item["weight"] for item in history if item["date"] == selected_date), 70.0)
                
                with st.form("form_edit_weight"):
                    corrected_weight = st.number_input(
                        f"Nuevo peso para {selected_date} (kg):",
                        min_value=30.0,
                        max_value=250.0,
                        value=float(current_val),
                        step=0.1,
                        format="%.1f",
                        key="input_corrected_weight_val"
                    )
                    btn_update = st.form_submit_button("💾 Guardar Corrección")
                    
                    if btn_update:
                        succ, msg = dm.update_weight_entry(user_to_edit, selected_date, corrected_weight)
                        if succ:
                            st.success(msg)
                            st.rerun()
                        else:
                            st.error(msg)
                
                st.markdown("---")
                if st.button(f"🗑️ Eliminar pesaje del {selected_date}", key=f"btn_delete_entry_{user_to_edit}_{selected_date}"):
                    succ, msg = dm.delete_weight_entry(user_to_edit, selected_date)
                    if succ:
                        st.session_state.pop("select_date_to_edit_history", None)
                        st.session_state.pop("input_corrected_weight_val", None)
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)

        # --------------------------------------------------
        # ZONA DE PELIGRO: Eliminar Participante Completa
        # --------------------------------------------------
        st.markdown("---")
        st.markdown("### ⚠️ Eliminar Participante")
        
        confirm_key = f"confirm_delete_user_{user_to_edit}"
        if confirm_key not in st.session_state:
            st.session_state[confirm_key] = False

        if not st.session_state[confirm_key]:
            if st.button(
                f"🗑️ Eliminar a '{user_to_edit}' y todos sus datos",
                key=f"btn_delete_user_initial_{user_to_edit}"
            ):
                st.session_state[confirm_key] = True
                st.rerun()
        else:
            st.markdown(
                f"""
                <div style="background:#FFF5F5; border:2px solid #FC8181; border-radius:14px; padding:16px 18px; margin-top:6px;">
                    <p style="color:#C53030 !important; font-weight:800; font-size:1rem; margin:0 0 6px 0;">
                        🚨 ¿Estás segura de que querés eliminar a <em>'{user_to_edit}'</em>?
                    </p>
                    <p style="color:#742A2A !important; font-size:0.88rem; margin:0;">
                        Esta acción borrará todos sus pesajes permanentemente.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

            col_confirm, col_cancel = st.columns(2)
            with col_confirm:
                if st.button(
                    "✅ Sí, eliminar definitivamente",
                    key=f"btn_confirm_delete_user_{user_to_edit}",
                    use_container_width=True
                ):
                    succ, msg = dm.delete_user(user_to_edit)
                    if succ:
                        st.session_state.pop(confirm_key, None)
                        st.session_state.pop("select_user_to_edit_history", None)
                        st.session_state.pop("select_date_to_edit_history", None)
                        st.session_state.pop("input_corrected_weight_val", None)
                        
                        if st.session_state.get("selected_nickname") == user_to_edit:
                            st.session_state.selected_nickname = None
                            st.session_state["select_user_progress_dropdown"] = "-- Elige tu Apodo en la lista --"
                            
                        if "multiselect_group_users_widget" in st.session_state:
                            st.session_state["multiselect_group_users_widget"] = [
                                u for u in st.session_state["multiselect_group_users_widget"]
                                if u != user_to_edit
                            ]
                        st.success(f"✅ '{user_to_edit}' fue eliminada correctamente.")
                        st.rerun()
                    else:
                        st.error(msg)
            with col_cancel:
                if st.button(
                    "❌ Cancelar",
                    key=f"btn_cancel_delete_user_{user_to_edit}",
                    use_container_width=True
                ):
                    st.session_state[confirm_key] = False
                    st.rerun()


# =========================================================
# VISTA 5: COPIA DE SEGURIDAD & DATOS
# =========================================================
elif st.session_state.active_nav_tab == "💾 Copia de Seguridad":
    st.subheader("💾 Copia de Seguridad y Exportación")
    st.markdown("Descarga los datos en cualquier momento para tener un respaldo en tu computadora o teléfono.")
    
    col_d1, col_d2 = st.columns(2)
    
    with col_d1:
        csv_data = dm.export_data_csv()
        st.download_button(
            label="📥 Descargar datos en CSV (Excel)",
            data=csv_data,
            file_name=f"operacion_bikini_pesajes_{date.today().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            key="btn_download_csv_backup",
            use_container_width=True
        )
        
    with col_d2:
        import json
        raw_json = json.dumps(dm.load_data(), indent=2, ensure_ascii=False)
        st.download_button(
            label="📥 Descargar respaldo en JSON",
            data=raw_json,
            file_name=f"operacion_bikini_backup_{date.today().strftime('%Y%m%d')}.json",
            mime="application/json",
            key="btn_download_json_backup",
            use_container_width=True
        )
        
    st.markdown("---")
    st.subheader("🎲 Datos de Prueba para Demostración")
    st.caption("Si quieres probar la app con participantes de ejemplo:")
    
    if st.button("🌴 Cargar Participantes de Demostración (Demo)", key="btn_load_demo_sample_data"):
        demo_users = {
            "Valeria":  {"start": 74.5, "target": 68.0, "logs": [("2026-08-15", 74.5), ("2026-08-18", 74.0), ("2026-08-20", 73.2), ("2026-08-23", 72.6), ("2026-08-27", 72.0)]},
            "Claudia":  {"start": 69.0, "target": 64.0, "logs": [("2026-08-15", 69.0), ("2026-08-18", 68.5), ("2026-08-21", 68.1), ("2026-08-24", 67.8), ("2026-08-27", 67.3)]},
            "Silvina":  {"start": 80.0, "target": 72.0, "logs": [("2026-08-15", 80.0), ("2026-08-18", 79.0), ("2026-08-22", 76.5), ("2026-08-25", 73.2), ("2026-08-27", 71.8)]},
            "Mariana":  {"start": 65.0, "target": 60.0, "logs": [("2026-08-16", 65.0), ("2026-08-19", 65.2), ("2026-08-23", 65.4), ("2026-08-25", 64.9), ("2026-08-27", 64.6)]},
        }
        for nick, data in demo_users.items():
            dm.add_user(nick, data["start"], data["target"], entry_date=data["logs"][0][0])
            for d_str, w_val in data["logs"][1:]:
                dm.log_weight(nick, w_val, entry_date=d_str)
        st.session_state.selected_nickname = "Valeria"
        st.session_state["select_user_progress_dropdown"] = "Valeria"
        st.session_state["multiselect_group_users_widget"] = list(demo_users.keys())
        st.session_state.active_nav_tab = "🏖️ Mi Progreso"
        st.success("¡Datos de prueba cargados con éxito! 🏖️💃")
        st.rerun()


# --- PIE DE PÁGINA ---
st.markdown("""
<div class="footer-rio">
    🌴 Operación Bikini — Edición Río de Janeiro 2026 👙 — Hecho con ☀️ y buena onda
</div>
""", unsafe_allow_html=True)
