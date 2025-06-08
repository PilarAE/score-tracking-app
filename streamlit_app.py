import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="App Interactiva", layout="centered")

# Título general
st.title("🏆 App de Conteo de Puntajes")

# Inicializar variables de sesión
if "participantes" not in st.session_state:
    st.session_state.participantes = []
if "puntajes" not in st.session_state:
    st.session_state.puntajes = {}
if "permitir_negativos" not in st.session_state:
    st.session_state.permitir_negativos = False
if "puntaje_base_a" not in st.session_state:
    st.session_state.puntaje_base_a = 0
if "puntaje_base_b" not in st.session_state:
    st.session_state.puntaje_base_b = 0

# Crear las pestañas
tab1, tab2, tab3, tab4 = st.tabs([
    "📖 Instrucciones", "👥 Configura el Juego", "🎯 Puntaje Único", "🏅 Dos Contadores"
])

# ----------------------
# 📖 Pestaña 1: Instrucciones
# ----------------------
with tab1:
    st.header("📖 ¿Cómo usar esta app?")
    st.markdown("""
    Esta aplicación tiene tres secciones:
    
    1. **Configura el Juego:** Define puntajes base A y B, agrega participantes y permite puntajes negativos si se desea.
    2. **Puntaje Único:** Registra puntajes individuales (solo A).
    3. **Dos Contadores:** Lleva dos puntajes por jugador (A y B).
    """)

# ----------------------
# 👥 Pestaña 2: Configuración del Juego
# ----------------------
with tab2:
    st.header("👥 Configura el Juego")
    st.subheader("⚙️ Puntajes Base")

    col1, col2 = st.columns(2)
    with col1:
        st.session_state.puntaje_base_a = st.number_input("Puntaje base A (puede ser único):", step=1, value=st.session_state.puntaje_base_a)
    with col2:
        st.session_state.puntaje_base_b = st.number_input("Puntaje base B (si necesitas dos contadores):", step=1, value=st.session_state.puntaje_base_b)

    st.session_state.permitir_negativos = st.toggle(
        "¿Permitir que los puntajes bajen (valores negativos)?",
        value=st.session_state.permitir_negativos
    )

    st.markdown("---")
    st.subheader("👥 Agrega Participantes")
    col1, col2 = st.columns(2)
    with col1:
        nombre = st.text_input("✍️ Escribe un nombre:")

        if st.button("➕ Agregar"):
            nombre_limpio = nombre.strip()
            if nombre_limpio == "":
                st.warning("Por favor, escribe un nombre válido.")
            elif nombre_limpio in st.session_state.participantes:
                st.warning("Este nombre ya fue ingresado.")
            else:
                st.session_state.participantes.append(nombre_limpio)
                st.session_state.puntajes[nombre_limpio] = {
                    "A": st.session_state.puntaje_base_a,
                    "B": st.session_state.puntaje_base_b
                }
                st.success(f"Agregado: {nombre_limpio} con A={st.session_state.puntaje_base_a}, B={st.session_state.puntaje_base_b}")

    with col2:
        if st.session_state.participantes:
            st.markdown("### 🧑‍🤝‍🧑 Lista actual:")
            for i, p in enumerate(st.session_state.participantes, start=1):
                st.markdown(f"- {i}. {p}")

            if st.button("🗑️ Limpiar lista"):
                st.session_state.participantes = []
                st.session_state.puntajes = {}
                st.info("Lista de participantes y puntajes vaciada.")

# ----------------------
# 🎯 Pestaña 3: Puntaje único (solo A)
# ----------------------
with tab3:
    st.header("🎯 Puntaje Único (A)")

    if not st.session_state.participantes:
        st.warning("Primero agrega participantes en la pestaña anterior.")
    else:
        col_, col_puntaje = st.columns([2, 2])
        with col_:
            jugador = st.radio("Selecciona un jugador:", st.session_state.participantes, key="jugador_tab3")
        with col_puntaje:
            if st.session_state.permitir_negativos:
                nuevo_puntaje = st.number_input("Puntaje a agregar o restar:", step=1, value=0)
            else:
                nuevo_puntaje = st.number_input("Puntaje a agregar:", min_value=0, step=1, value=0)

        if st.button("➕ Sumar puntaje"):
            st.session_state.puntajes[jugador]["A"] += nuevo_puntaje
            st.success(f"{jugador} ahora tiene {st.session_state.puntajes[jugador]['A']} puntos.")

        st.subheader("📊 Puntajes Totales (A):")
        for nombre, p in st.session_state.puntajes.items():
            st.markdown(f"- **{nombre}**: {p['A']} puntos")

        if st.button("🔄 Reiniciar puntajes A"):
            for nombre in st.session_state.puntajes:
                st.session_state.puntajes[nombre]["A"] = st.session_state.puntaje_base_a
            st.info("Todos los puntajes A fueron reiniciados.")

# ----------------------
# 🏅 Pestaña 4: Dos Contadores (A y B)
# ----------------------
with tab4:
    st.header("🏅 Puntajes con Dos Contadores (A y B)")

    if not st.session_state.participantes:
        st.warning("Primero agrega participantes en la pestaña anterior.")
    else:
        col_jugador, col_tipo = st.columns([2, 2])
        with col_jugador:
            jugador = st.radio("Selecciona un jugador:", st.session_state.participantes, key="jugador_tab4")
        with col_tipo:
            tipo_puntaje = st.radio("¿Qué puntaje deseas modificar?", ["A", "B"], horizontal=True)
            if st.session_state.permitir_negativos:
                nuevo_puntaje = st.number_input("Puntaje a agregar o restar:", step=1, value=0, key="puntaje_doble")
            else:
                nuevo_puntaje = st.number_input("Puntaje a agregar:", min_value=0, step=1, value=0, key="puntaje_doble")

        if st.button("➕ Sumar a puntaje A/B"):
            st.session_state.puntajes[jugador][tipo_puntaje] += nuevo_puntaje
            st.success(f"{jugador} ahora tiene {st.session_state.puntajes[jugador][tipo_puntaje]} puntos en el puntaje {tipo_puntaje}.")

        # Mostrar como tabla
        st.subheader("📊 Puntajes Totales A y B:")
        data = {
            "Participante": [],
            "Puntaje A": [],
            "Puntaje B": []
        }
        for nombre, p in st.session_state.puntajes.items():
            data["Participante"].append(nombre)
            data["Puntaje A"].append(p.get("A", 0))
            data["Puntaje B"].append(p.get("B", 0))
        df = pd.DataFrame(data)
        st.table(df)

        if st.button("🔄 Reiniciar A y B"):
            for nombre in st.session_state.puntajes:
                st.session_state.puntajes[nombre]["A"] = st.session_state.puntaje_base_a
                st.session_state.puntajes[nombre]["B"] = st.session_state.puntaje_base_b
            st.info("Todos los puntajes A y B fueron reiniciados.")

# ----------------------
# 📌 Pie de página global
# ----------------------
st.markdown("""
<hr style="margin-top: 2em; margin-bottom: 1em;">
<center>
    <small>Desarrollado por Rodrigo López, Innovación CVD, usando ChatGPT + GitHub + Streamlit · © 2025</small>
</center>
""", unsafe_allow_html=True)
