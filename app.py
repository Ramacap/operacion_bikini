"""
app.py - Operación Bikini 🌴👙☀️
Aplicación de seguimiento y competencia de descenso de peso con temática de Río de Janeiro.
Diseño adaptable (responsive) para PC y smartphones con menú estilo botones 3D y gráficos interactivos de alto contraste.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import data_manager as dm

# Colores temáticos Río de Janeiro
COLORS = {
    "coral":       "#FF6B6B",
    "coral_dark":  "#E63946",
    "sunset":      "#FF8E53",
    "gold":        "#FFBE0B",
    "gold_dark":   "#F6AD55",
    "sand":        "#FFF3E2",
    "sand_light":  "#FFFDF9",
    "turquoise":   "#00F5D4",
    "teal":        "#06D6A0",
    "teal_dark":   "#058C68",
    "ocean":       "#0077B6",
    "navy":        "#1A202C",
    "gray":        "#4A5568",
}

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
       FORZAR TEMA CLARO Y TIPOGRAFÍAS DE ALTO CONTRASTE
       Evita que el modo oscuro del sistema ponga textos o fondos invisibles
       ========================================================= */
    .stApp, .stApp > div, [data-testid="stAppViewContainer"], [data-testid="block-container"] {
        background-color: #FFFDF9 !important;
        color: #1A202C !important;
    }
    
    /* Tipografía general */
    p, span, label, div, small, strong, b {
        color: #1A202C;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #1A202C !important;
        font-weight: 800 !important;
    }
    .stCaption, [data-testid="stCaptionContainer"] * {
        color: #4A5568 !important;
        font-weight: 500 !important;
    }

    /* Encabezado Principal */
    .main-header {
        background: linear-gradient(135deg, #FF6B6B 0%, #FFBE0B 50%, #00F5D4 100%);
        padding: 26px 16px;
        border-radius: 20px;
        color: white !important;
        text-align: center;
        margin-bottom: 18px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        position: relative;
        overflow: hidden;
    }
    .main-header * {
        color: white !important;
    }
    .main-header h1 {
        color: white !important;
        font-size: 2.4rem;
        font-weight: 900;
        margin: 0;
        letter-spacing: 1.5px;
        text-shadow: 2px 3px 6px rgba(0,0,0,0.25);
    }
    .main-header p {
        color: white !important;
        font-size: 1.05rem;
        margin-top: 6px;
        margin-bottom: 0;
        font-weight: 600;
    }
    
    /* Banner de Cuenta Regresiva */
    .countdown-card {
        background: linear-gradient(90deg, #FFF3E2 0%, #FFECD2 100%);
        border-left: 6px solid #FF6B6B;
        padding: 16px 20px;
        border-radius: 12px;
        margin-bottom: 18px;
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: space-between;
        gap: 10px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.06);
    }
    .countdown-card * {
        color: #1A202C;
    }
    .countdown-days {
        font-size: 2rem;
        font-weight: 900;
        color: #FF6B6B !important;
        line-height: 1;
    }
    .countdown-days small {
        font-size: 0.9rem;
        font-weight: 700;
        display: block;
        color: #E63946 !important;
    }
    
    /* Salón de la Gloria */
    .hall-of-fame-card {
        background: linear-gradient(120deg, #FFF9E6 0%, #FFE8B8 50%, #FFF3CC 100%);
        border: 2px solid #F39C12;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 22px;
        box-shadow: 0 6px 16px rgba(243, 156, 18, 0.22);
    }
    .hall-of-fame-card h3 {
        color: #B7791F !important;
        margin: 0 0 8px 0;
    }
    .hall-of-fame-card p {
        color: #744210 !important;
        margin: 0;
        font-size: 0.95rem;
    }

    /* =========================================================
       BOTONES DE NAVEGACIÓN PRINCIPAL EN 3D (TEXTO SIEMPRE VISIBLE)
       ========================================================= */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px !important;
        padding: 8px 4px 22px 4px !important;
        border-bottom: none !important;
        display: flex !important;
        flex-wrap: wrap !important;
        justify-content: center !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(180deg, #FFFFFF 0%, #FFF0D4 100%) !important;
        border: 2px solid #F6AD55 !important;
        border-bottom: 4px solid #DD6B20 !important;
        border-radius: 35px !important;
        padding: 12px 22px !important;
        box-shadow: 0 6px 0 #DD6B20, 0 8px 14px rgba(221, 107, 32, 0.25) !important;
        transition: all 0.12s cubic-bezier(0.4, 0, 0.2, 1) !important;
        cursor: pointer !important;
        white-space: nowrap !important;
        position: relative !important;
        top: 0px !important;
    }
    
    /* Forzar color oscuro en TODOS los textos e iconos de pestañas inactivas */
    .stTabs [data-baseweb="tab"] * {
        color: #1A202C !important;
        font-weight: 800 !important;
        font-size: 0.95rem !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: linear-gradient(180deg, #FFF9F0 0%, #FFE2B8 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 0 #DD6B20, 0 12px 18px rgba(221, 107, 32, 0.3) !important;
    }
    
    .stTabs [data-baseweb="tab"]:active {
        top: 5px !important;
        transform: translateY(5px) !important;
        box-shadow: 0 1px 0 #DD6B20, inset 0 2px 4px rgba(0,0,0,0.15) !important;
        border-bottom: 2px solid #DD6B20 !important;
    }
    
    /* Pestaña activa (fondo coral + texto blanco nítido) */
    .stTabs [aria-selected="true"] {
        background: linear-gradient(180deg, #FF6B6B 0%, #EE5253 100%) !important;
        border: 2px solid #C53030 !important;
        border-bottom: 4px solid #9B2C2C !important;
        box-shadow: 0 6px 0 #9B2C2C, 0 10px 20px rgba(238, 82, 83, 0.4) !important;
        transform: scale(1.02) !important;
    }
    .stTabs [aria-selected="true"] * {
        color: #FFFFFF !important;
        font-weight: 800 !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.25);
    }
    
    .stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] {
        display: none !important;
    }

    /* =========================================================
       TARJETAS DE MÉTRICAS CON MÁXIMO CONTRASTE
       ========================================================= */
    div[data-testid="stMetric"] {
        background: #FFFFFF !important;
        padding: 16px !important;
        border-radius: 16px !important;
        border: 1.5px solid #FFD166 !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06) !important;
    }
    div[data-testid="stMetricLabel"] * {
        font-size: 0.92rem !important;
        font-weight: 700 !important;
        color: #4A5568 !important;
    }
    div[data-testid="stMetricValue"] * {
        font-size: 1.75rem !important;
        font-weight: 900 !important;
        color: #1A202C !important;
    }

    /* =========================================================
       INPUTS, SELECTS Y FORMULARIOS CLAROS
       ========================================================= */
    label, label * {
        color: #1A202C !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
    }
    .stSelectbox > div[data-baseweb="select"] > div,
    .stTextInput > div > div,
    .stNumberInput > div > div {
        background-color: #FFFFFF !important;
        border: 1.5px solid #CBD5E0 !important;
        border-radius: 10px !important;
    }
    .stSelectbox [data-baseweb="select"] * {
        color: #1A202C !important;
        font-weight: 600 !important;
    }
    
    /* Botones de acción 3D en la interfaz */
    .stButton>button, .stDownloadButton>button {
        border-radius: 28px !important;
        font-weight: 700 !important;
        border-bottom: 3px solid rgba(0,0,0,0.15) !important;
        box-shadow: 0 4px 0 rgba(0,0,0,0.10), 0 6px 12px rgba(0,0,0,0.06) !important;
        transition: all 0.12s ease !important;
    }
    .stButton>button:hover, .stDownloadButton>button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 5px 0 rgba(0,0,0,0.10), 0 8px 16px rgba(0,0,0,0.1) !important;
    }
    .stButton>button:active, .stDownloadButton>button:active {
        transform: translateY(3px) !important;
        box-shadow: 0 1px 0 rgba(0,0,0,0.12) !important;
    }

    /* Tarjeta vacía de bienvenida */
    .welcome-empty {
        text-align: center;
        padding: 40px 20px;
        background: #FFFFFF;
        border-radius: 16px;
        border: 2px dashed #FFD166;
        margin-top: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
    }
    .welcome-empty .emoji-big { font-size: 3.5rem; }
    .welcome-empty h3 { color: #FF6B6B !important; margin-top: 12px; }
    .welcome-empty p { color: #4A5568 !important; max-width: 520px; margin: 8px auto 0; font-size: 0.95rem; font-weight: 500; }

    /* Pie de página */
    .footer-rio {
        text-align: center;
        padding: 20px 10px;
        margin-top: 30px;
        color: #718096 !important;
        font-size: 0.85rem;
        font-weight: 600;
        border-top: 1px solid #E2E8F0;
    }

    /* Adaptación Responsive para Móviles */
    @media (max-width: 768px) {
        .main-header { padding: 16px 12px; }
        .main-header h1 { font-size: 1.5rem !important; }
        .main-header p { font-size: 0.85rem !important; }
        .stTabs [data-baseweb="tab"] {
            padding: 8px 14px !important;
            font-size: 0.82rem !important;
            border-radius: 25px !important;
            box-shadow: 0 4px 0 #DD6B20, 0 6px 10px rgba(221, 107, 32, 0.2) !important;
        }
        div[data-testid="stMetricValue"] * { font-size: 1.35rem !important; }
        .countdown-card {
            font-size: 0.88rem;
            flex-direction: column;
            text-align: center;
        }
        .countdown-days { font-size: 1.5rem; }
    }
</style>
""", unsafe_allow_html=True)


# --- ENCABEZADO Y ESTADO DE COMPETENCIA ---
is_closed, days_left, deadline_str = dm.get_competition_status()

st.markdown("""
<div class="main-header">
    <h1>🌴 OPERACIÓN BIKINI 👙</h1>
    <p>🏖️ Edición Río de Janeiro • ¡Rumbo al verano en forma, saludables y fabulosas! 🍹☀️</p>
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
        <h3 style="margin: 0 0 10px 0; color: #B7791F;">👑 SALÓN DE LA GLORIA: ¡CHICAS BIKINI DE ORO! 👑</h3>
        <p style="margin: 0; font-size: 0.95rem; color: #744210;">
            ¡Un aplauso gigante para las participantes que ya alcanzaron o superaron su peso objetivo! 👏🎉🍾
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    cols = st.columns(min(len(hall_of_fame), 4))
    for idx, champ in enumerate(hall_of_fame):
        with cols[idx % 4]:
            st.success(f"🏆 **{champ['nickname']}**\n\n🎯 Meta: {champ['target_weight']} kg\n\n⚖️ Actual: **{champ['current_weight']} kg**\n\n📉 Bajó: **{champ['total_lost']} kg** 🎉")


# --- MENÚ DE PESTAÑAS ESTILO BOTONES 3D ---
tab_mi_progreso, tab_general, tab_nuevo_usuario, tab_historial, tab_datos = st.tabs([
    "🏖️ Mi Progreso & Cargar Peso",
    "📊 Competencia General",
    "➕ Nueva Participante",
    "✏️ Historial & Corrección",
    "💾 Copia de Seguridad"
])

all_users = dm.get_all_users()


# =========================================================
# PESTAÑA 1: MI PROGRESO & CARGAR PESO
# =========================================================
with tab_mi_progreso:
    if not all_users:
        st.info("👋 ¡Aún no hay participantes registradas! Ve a la pestaña **➕ Nueva Participante** para comenzar.")
    else:
        # Manejo de estado de selección de apodo
        if "selected_nickname" not in st.session_state:
            st.session_state.selected_nickname = None

        # Contenedor limpio y nativo para el selector de apodo
        with st.container(border=True):
            def clear_user_selection_callback():
                st.session_state.selected_nickname = None
                st.session_state["select_user_progress_dropdown"] = "-- Elige tu Apodo en la lista --"

            col_sel_text, col_sel_btn = st.columns([3, 1])
            with col_sel_text:
                st.markdown("### 👤 Selecciona tu Apodo:")
            with col_sel_btn:
                st.button("❌ Borrar Selección", key="btn_clear_user_selection", on_click=clear_user_selection_callback, use_container_width=True)

            options = ["-- Elige tu Apodo en la lista --"] + all_users
            
            # Inicializar valor si no existe o si el apodo guardado ya no está en la lista
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

        # Si NO hay apodo seleccionado, mostramos tarjeta de bienvenida
        if not st.session_state.selected_nickname:
            st.markdown("""
            <div class="welcome-empty">
                <span class="emoji-big">🌴👙</span>
                <h3>¡Hola! Elige tu apodo arriba para ver tu progreso</h3>
                <p>
                    Selecciona tu nombre en el menú superior para ver tus kilos bajados,
                    registrar tu pesaje de hoy y visualizar tu gráfico hacia el objetivo.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            selected_user = st.session_state.selected_nickname
            stats = dm.get_user_stats(selected_user)
            
            if stats:
                st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
                col_form, col_metrics = st.columns([1, 2])
                
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
                                        st.success(f"🎉🎉 ¡FELICITACIONES {selected_user.upper()}! ¡ALCANZASTE TU PESO OBJETIVO DE {stats['target_weight']} kg! 🍾👙☀️")
                                    else:
                                        st.success(msg)
                                    st.rerun()
                                else:
                                    st.error(msg)
                                    
                with col_metrics:
                    st.subheader(f"📊 Estadísticas de {selected_user}")
                    
                    m1, m2, m3, m4 = st.columns(4)
                    
                    with m1:
                        st.metric(
                            label="Peso Actual",
                            value=f"{stats['current_weight']} kg"
                        )
                    with m2:
                        delta_val = stats['last_delta']
                        st.metric(
                            label="Último Cambio",
                            value=f"{stats['current_weight']} kg",
                            delta=f"{delta_val:+.1f} kg" if len(stats["history"]) > 1 else "Inicio",
                            delta_color="inverse"
                        )
                    with m3:
                        st.metric(
                            label="Total Bajado",
                            value=f"{stats['total_lost']} kg",
                            delta=f"{-stats['total_delta']:+.1f} kg",
                            delta_color="normal"
                        )
                    with m4:
                        if stats["goal_achieved"]:
                            st.metric(
                                label="Meta",
                                value="¡Cumplida! 👑",
                                delta="Superada 🌟"
                            )
                        else:
                            st.metric(
                                label="Faltan para la Meta",
                                value=f"{stats['remaining_to_goal']} kg",
                                delta=f"Objetivo: {stats['target_weight']} kg",
                                delta_color="off"
                            )
                    
                    # Barra de progreso motivacional
                    prog_pct = min(max(stats["progress_pct"], 0.0), 100.0)
                    st.markdown(f"**Progreso hacia el objetivo ({stats['target_weight']} kg): {stats['progress_pct']}%**")
                    st.progress(prog_pct / 100.0)
                
                # Gráfico de evolución individual con fondo blanco explícito y etiquetas oscuras
                st.markdown("---")
                st.subheader(f"📈 Evolución de Peso — {selected_user}")
                
                df_user = pd.DataFrame(stats["history"])
                df_user["Fecha_dt"] = pd.to_datetime(df_user["date"])
                df_user = df_user.sort_values(by="Fecha_dt")
                
                fig_user = go.Figure()
                
                # Área degradada debajo de la curva
                fig_user.add_trace(go.Scatter(
                    x=df_user["Fecha_dt"],
                    y=df_user["weight"],
                    mode='lines',
                    line=dict(width=0),
                    showlegend=False,
                    hoverinfo='skip',
                    fill='tozeroy',
                    fillcolor='rgba(255, 107, 107, 0.12)'
                ))
                
                # Línea de peso real del usuario
                fig_user.add_trace(go.Scatter(
                    x=df_user["Fecha_dt"],
                    y=df_user["weight"],
                    mode='lines+markers',
                    name=f'{selected_user}',
                    line=dict(color=COLORS["coral"], width=3.5, shape='spline'),
                    marker=dict(size=10, color=COLORS["coral_dark"], line=dict(color='white', width=2)),
                    hovertemplate="<b>%{x|%d/%m/%Y}</b><br>Peso: <b>%{y:.1f} kg</b><extra></extra>"
                ))
                
                # Línea del peso inicial (referencia)
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
                    line_color=COLORS["teal"],
                    line_width=3,
                    annotation_text=f"🎯 Meta: {stats['target_weight']} kg",
                    annotation_position="bottom right",
                    annotation_font=dict(size=12, color=COLORS["teal_dark"], family="Poppins")
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
                        tickfont=dict(color='#1A202C', size=11, family='Poppins'),
                        title_font=dict(color='#1A202C', size=13, family='Poppins')
                    ),
                    xaxis=dict(
                        gridcolor='#E2E8F0',
                        tickfont=dict(color='#1A202C', size=11, family='Poppins'),
                        title_font=dict(color='#1A202C', size=13, family='Poppins')
                    ),
                    hovermode="x unified",
                    hoverlabel=dict(
                        bgcolor="#FFFFFF",
                        font_color="#1A202C",
                        font_size=12,
                        font_family="Poppins",
                        bordercolor="#CBD5E0"
                    ),
                    template="plotly_white",
                    height=420,
                    margin=dict(l=20, r=20, t=30, b=20),
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
                
                st.plotly_chart(fig_user, use_container_width=True)


# =========================================================
# PESTAÑA 2: COMPETENCIA GENERAL
# =========================================================
with tab_general:
    st.subheader("🏖️ Gráfico Comparativo del Grupo")
    df_all = dm.get_all_weights_dataframe()
    
    if df_all.empty:
        st.info("Aún no hay pesajes cargados para graficar.")
    else:
        # Inicialización de estado de participantes seleccionadas
        if "multiselect_group_users_widget" not in st.session_state:
            st.session_state["multiselect_group_users_widget"] = all_users.copy()
        else:
            # Sincronizar: solo contener usuarias que existen
            st.session_state["multiselect_group_users_widget"] = [
                u for u in st.session_state["multiselect_group_users_widget"] if u in all_users
            ]

        # Callbacks de selección rápida
        def select_all_group_callback():
            st.session_state["multiselect_group_users_widget"] = all_users.copy()

        def clear_all_group_callback():
            st.session_state["multiselect_group_users_widget"] = []

        col_btn1, col_btn2, col_radio = st.columns([1, 1, 2])
        with col_btn1:
            st.button("🔘 Seleccionar Todos", key="btn_select_all_group_users", on_click=select_all_group_callback, use_container_width=True)
        with col_btn2:
            st.button("❌ Borrar Selección", key="btn_clear_all_group_users", on_click=clear_all_group_callback, use_container_width=True)
        with col_radio:
            view_metric = st.radio(
                "Métrica a graficar:",
                options=["Peso Actual (kg)", "Kilos Bajados (kg)"],
                horizontal=True,
                key="radio_group_metric_choice"
            )
            
        selected_participants = st.multiselect(
            "Participantes visibles en el gráfico:",
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
                title=f"Evolución Diaria del Grupo — {view_metric}",
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
                hoverlabel=dict(
                    bgcolor="#FFFFFF",
                    font_color="#1A202C",
                    font_size=12,
                    font_family="Poppins",
                    bordercolor="#CBD5E0"
                ),
                template="plotly_white",
                height=500,
                margin=dict(l=20, r=20, t=50, b=20),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="center",
                    x=0.5,
                    font=dict(color="#1A202C", size=12, family="Poppins")
                ),
                paper_bgcolor='#FFFFFF',
                plot_bgcolor='#FFFFFF',
                yaxis=dict(
                    gridcolor='#E2E8F0',
                    tickfont=dict(color='#1A202C', size=11, family='Poppins'),
                    title_font=dict(color='#1A202C', size=13, family='Poppins')
                ),
                xaxis=dict(
                    gridcolor='#E2E8F0',
                    tickfont=dict(color='#1A202C', size=11, family='Poppins'),
                    title_font=dict(color='#1A202C', size=13, family='Poppins')
                ),
                font=dict(color='#1A202C', family='Poppins'),
                title=dict(font=dict(color='#1A202C', size=15, family='Poppins'))
            )
            fig_group.update_xaxes(dtick="D1", tickformat="%d/%m")
            
            st.plotly_chart(fig_group, use_container_width=True)
        else:
            st.warning("Selecciona al menos una participante para visualizar el gráfico.")
            
        # Ranking del Verano ordenado por % hacia la meta
        st.markdown("---")
        st.subheader("🏆 Ranking del Verano")
        all_stats = dm.get_all_stats()
        
        if all_stats:
            all_stats.sort(key=lambda x: (x["progress_pct"], x["total_lost"]), reverse=True)
            
            # Renderizar ranking con tarjetas estilizadas
            for rank, s in enumerate(all_stats, 1):
                if rank == 1:
                    medal = "🥇"
                    bg = "linear-gradient(90deg, #FFF9E6, #FFE8B8)"
                    border_col = "#F6AD55"
                elif rank == 2:
                    medal = "🥈"
                    bg = "linear-gradient(90deg, #F7FAFC, #EDF2F7)"
                    border_col = "#A0AEC0"
                elif rank == 3:
                    medal = "🥉"
                    bg = "linear-gradient(90deg, #FFFAF0, #FEEBC8)"
                    border_col = "#DD6B20"
                else:
                    medal = f"#{rank}"
                    bg = "#FFFDF9"
                    border_col = "#E2E8F0"
                    
                prog_bar_width = min(max(s['progress_pct'], 0), 100)
                prog_color = COLORS["teal"] if s["goal_achieved"] else COLORS["coral"]
                status_text = "👑 ¡Meta Lograda!" if s["goal_achieved"] else f"Faltan {s['remaining_to_goal']} kg"
                
                st.markdown(f"""
                <div style="
                    background: {bg};
                    border-left: 5px solid {border_col};
                    border-radius: 12px;
                    padding: 14px 18px;
                    margin-bottom: 10px;
                    display: flex;
                    flex-wrap: wrap;
                    align-items: center;
                    gap: 16px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
                ">
                    <div style="font-size: 1.8rem; min-width: 45px; text-align: center; color: #1A202C;">{medal}</div>
                    <div style="flex: 1; min-width: 120px;">
                        <div style="font-weight: 800; font-size: 1.1rem; color: #1A202C;">{s['nickname']}</div>
                        <div style="font-size: 0.82rem; color: #4A5568;">{s['start_weight']} → {s['current_weight']} kg (meta: {s['target_weight']})</div>
                    </div>
                    <div style="flex: 2; min-width: 200px;">
                        <div style="display: flex; justify-content: space-between; font-size: 0.82rem; color: #1A202C; margin-bottom: 4px;">
                            <span>Bajó <b style="color:#1A202C;">{s['total_lost']} kg</b></span>
                            <span><b style="color:#1A202C;">{s['progress_pct']}%</b> del objetivo</span>
                        </div>
                        <div style="background: #E2E8F0; border-radius: 10px; height: 10px; overflow: hidden;">
                            <div style="background: {prog_color}; width: {prog_bar_width}%; height: 100%; border-radius: 10px; transition: width 0.5s;"></div>
                        </div>
                    </div>
                    <div style="min-width: 130px; text-align: right; font-size: 0.85rem; font-weight: 700; color: {'#058C68' if s['goal_achieved'] else '#4A5568'};">
                        {status_text}
                    </div>
                </div>
                """, unsafe_allow_html=True)


# =========================================================
# PESTAÑA 3: NUEVA PARTICIPANTE
# =========================================================
with tab_nuevo_usuario:
    st.subheader("➕ Registrar Nueva Participante")
    st.markdown("Suma una amiga al desafío de **Operación Bikini**. El peso inicial quedará registrado automáticamente como su primer pesaje de partida.")
    
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
                    # Agregar al multiselect de competencia general
                    if "multiselect_group_users_widget" in st.session_state:
                        current_list = list(st.session_state["multiselect_group_users_widget"])
                        if clean_nick not in current_list:
                            current_list.append(clean_nick)
                            st.session_state["multiselect_group_users_widget"] = current_list
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)


# =========================================================
# PESTAÑA 4: HISTORIAL & CORRECCIÓN
# =========================================================
with tab_historial:
    st.subheader("✏️ Modificar o Eliminar Pesajes Erróneos")
    st.caption("Si cargaste mal un número o quieres corregir un pesaje anterior, puedes gestionarlo aquí de manera sencilla.")
    
    if not all_users:
        st.info("No hay participantes cargadas.")
    else:
        # Asegurar que la participante en session_state siga existiendo
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
                
                # Validar que la fecha seleccionada exista
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
                if st.button(f"🗑️ Eliminar pesaje del {selected_date}", key=f"btn_delete_entry_{user_to_edit}_{selected_date}", type="secondary"):
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
        st.markdown("### ⚠️ Zona de Peligro")
        
        # Inicializar estado de confirmación de borrado
        confirm_key = f"confirm_delete_user_{user_to_edit}"
        if confirm_key not in st.session_state:
            st.session_state[confirm_key] = False

        if not st.session_state[confirm_key]:
            # Primer paso: botón inicial
            if st.button(
                f"🗑️ Eliminar participante '{user_to_edit}' (borra todos sus datos)",
                key=f"btn_delete_user_initial_{user_to_edit}",
                type="secondary"
            ):
                st.session_state[confirm_key] = True
                st.rerun()
        else:
            # Segundo paso: panel de confirmación
            st.markdown(
                f"""
                <div style="background:#FFF5F5; border:2px solid #FC8181; border-radius:14px; padding:18px 20px; margin-top:8px;">
                    <p style="color:#C53030 !important; font-weight:800; font-size:1.05rem; margin:0 0 8px 0;">
                        🚨 ¿Estás segura de que querés eliminar a <em>'{user_to_edit}'</em>?
                    </p>
                    <p style="color:#742A2A !important; font-size:0.9rem; margin:0;">
                        Esta acción borrará <strong>todos sus pesajes e historial</strong> de forma permanente.
                        No hay forma de deshacer esta operación.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

            col_confirm, col_cancel = st.columns(2)
            with col_confirm:
                if st.button(
                    "✅ Sí, eliminar definitivamente",
                    key=f"btn_confirm_delete_user_{user_to_edit}",
                    type="primary",
                    use_container_width=True
                ):
                    succ, msg = dm.delete_user(user_to_edit)
                    if succ:
                        # Limpiar todo el estado de session_state para evitar errores de selección inexistente
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
                        st.success(f"✅ '{user_to_edit}' fue eliminada del sistema correctamente.")
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
# PESTAÑA 5: COPIA DE SEGURIDAD & DATOS
# =========================================================
with tab_datos:
    st.subheader("💾 Copia de Seguridad y Exportación")
    st.markdown("Puedes descargar los datos en cualquier momento para tener un respaldo en tu computadora.")
    
    col_d1, col_d2 = st.columns(2)
    
    with col_d1:
        csv_data = dm.export_data_csv()
        st.download_button(
            label="📥 Descargar todos los datos en CSV (Excel)",
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
            label="📥 Descargar copia de seguridad en JSON",
            data=raw_json,
            file_name=f"operacion_bikini_backup_{date.today().strftime('%Y%m%d')}.json",
            mime="application/json",
            key="btn_download_json_backup",
            use_container_width=True
        )
        
    st.markdown("---")
    st.subheader("🎲 Datos de Prueba para Demostración")
    st.caption("Si quieres probar cómo se ve la app con participantes de ejemplo, haz clic en el siguiente botón:")
    
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
        st.success("¡Datos de prueba cargados con éxito! 🏖️💃")
        st.rerun()


# --- PIE DE PÁGINA ---
st.markdown("""
<div class="footer-rio">
    🌴 Operación Bikini — Edición Río de Janeiro 2026 👙 — Hecho con ☀️ y buena onda
</div>
""", unsafe_allow_html=True)
