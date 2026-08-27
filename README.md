# 🌴 Operación Bikini - Río de Janeiro Edition 👙☀️

Aplicación web interactiva desarrollada con **Python** y **Streamlit** para el seguimiento y competencia de descenso de peso con estética playera de Río de Janeiro.

---

## ✨ Características Principales

- **👥 Registro de Participantes:** Formulario sencillo para sumar amigas con su apodo, peso inicial y peso objetivo.
- **⚖️ Carga Rápida de Pesaje Diario:** Registro con fecha automática. Si ya se cargó en el día, se actualiza automáticamente.
- **📊 Indicadores y Métricas Visuales:** Muestra peso actual, último cambio (con flechas de colores: verde si baja, roja si sube), total de kilos bajados y distancia al objetivo.
- **📈 Gráficos Interactivos con Plotly:**
  - Evolución individual con línea de meta.
  - Gráfico comparativo general de todas las participantes con líneas diarias y tooltips informativos con hover.
- **⏳ Cierre Automático el 17 de Noviembre:** Contador regresivo al gran día y bloqueo automático de nuevas cargas al expirar el plazo.
- **👑 Salón de la Gloria / Muro de la Fama:** Cartel de felicitaciones y animación de globos cuando una participante alcanza o supera su meta.
- **✏️ Corrección de Registros:** Pestaña para corregir o eliminar pesajes erróneos.
- **💾 Exportación y Backup:** Descarga de base de datos en formato CSV (Excel) y JSON en un solo clic.

---

## 🚀 Cómo Ejecutar en Localhost

### 1. Requisitos Previos
Asegúrate de tener instalado Python 3.9 o superior.

### 2. Instalar Dependencias
Abre una terminal en la carpeta del proyecto y ejecuta:
```bash
pip install -r requirements.txt
```

### 3. Iniciar la Aplicación
Ejecuta el siguiente comando:
```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador web en:
`http://localhost:8501`

---

## ☁️ Cómo Desplegar en Streamlit Cloud (Gratis)

1. Sube este proyecto a un repositorio en **GitHub** (por ejemplo: `operacion-bikini`).
2. Ingresa a [share.streamlit.io](https://share.streamlit.io/) e inicia sesión con tu cuenta de GitHub.
3. Haz clic en **"New app"**.
4. Selecciona tu repositorio, la rama `main` y en *Main file path* indica: `app.py`.
5. Haz clic en **"Deploy"**. ¡Listo! Tendrás un link público para compartir con todo el grupo por WhatsApp.

---

## 🌴 Estructura de Archivos

- `app.py`: Interfaz visual completa y lógica de presentación con Streamlit.
- `data_manager.py`: Módulo de gestión de datos, cálculos matemáticos y persistencia en JSON.
- `.streamlit/config.toml`: Configuración de estilos y paleta de colores Río de Janeiro.
- `data/operacion_bikini.json`: Archivo local autogenerado donde se almacenan las participantes y pesajes.
- `requirements.txt`: Lista de librerías necesarias.
