import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="App Interactiva", layout="centered")

# Estilo visual personalizado
st.markdown("""
<style>
body {
    background-color: #2b2b2b;
    color: white;
}

h1, h2, h3, h4 {
    color: #f9f9f9;
    font-size: 1.6em;
}

small, .markdown-text-container {
    color: #cccccc;
}

button {
    background-color: #f4b400 !important;
    color: black !important;
    border-radius: 12px !important;
    font-weight: bold !important;
}

/* Estilo tabla */
div[data-testid="stTable"] table {
    background-color: #3a3a3a;
    color: white;
    border-radius: 10px;
}

/* Tarjetas para jugadores */
.card {
    background-color: #444;
    border: 1px solid #666;
    border-radius: 12px;
    padding: 16px;
    margin: 8px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.2);
    text-align: center;
    color: white;
}
</style>
""", unsafe_allow_html=True)

#########################################


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
if "orden_personalizado" not in st.session_state:
    st.session_state.orden_personalizado = []

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
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("👥 Agrega Participantes")
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

    # Reordenar participantes (añadido aquí)
    with col2:
        if st.session_state.participantes:
            st.subheader("🔀 Reordenar turnos")

            jugadores_disponibles = st.session_state.participantes.copy()
            nuevo_orden = []

            for i in range(len(jugadores_disponibles)):
                opciones_restantes = [j for j in jugadores_disponibles if j not in nuevo_orden]
                seleccion = st.selectbox(f"Turno #{i+1}", opciones_restantes, key=f"orden_turno_{i}")
                nuevo_orden.append(seleccion)

            if st.button("✅ Confirmar nuevo orden"):
                st.session_state.orden_personalizado = nuevo_orden
                st.success("Se actualizó el orden de los turnos.")

    with col1:
            if st.button("🗑️ Limpiar lista"):
                st.session_state.participantes = []
                st.session_state.puntajes = {}
                st.session_state.orden_personalizado = []
                st.info("Lista de participantes y puntajes vaciada.")


# ----------------------
# 🎯 Pestaña 3: Puntaje único (solo A)
# ----------------------
with tab3:
    st.header("🎯 Puntaje Único")

    participantes_visibles_tab3 = st.session_state.orden_personalizado if st.session_state.orden_personalizado else st.session_state.participantes

    if not participantes_visibles_tab3:
        st.warning("Primero agrega participantes en la pestaña anterior.")
    else:
        col_, col_puntaje = st.columns([2, 2])
        with col_:
            jugador = st.radio("Selecciona un jugador:", participantes_visibles_tab3, key="jugador_tab3")
        with col_puntaje:
            if st.session_state.permitir_negativos:
                nuevo_puntaje = st.number_input("Puntaje a agregar o restar:", step=1, value=0, key="ptje_tab3")
            else:
                nuevo_puntaje = st.number_input("Puntaje a agregar:", min_value=0, step=1, value=0, key="ptje_tab3")

        if st.button("➕ Sumar puntaje"):
            st.session_state.puntajes[jugador]["A"] += nuevo_puntaje
            st.success(f"{jugador} ahora tiene {st.session_state.puntajes[jugador]['A']} puntos.")

        # Mostrar como tarjetas
        st.subheader("🎯 Puntajes Totales:")
        cols = st.columns(4)
        for idx, nombre in enumerate(participantes_visibles_tab3):
            with cols[idx % 4]:
                st.markdown(f"""
                <div class="card">
                <h4>{nombre}</h4>
                <p>Puntaje: <strong>{st.session_state.puntajes[nombre].get("A", 0)}</strong></p>
                </div>
                """, unsafe_allow_html=True)
        
        if st.button("🔄 Reiniciar puntajes", key="reiniciar_tab3"):
            for nombre in st.session_state.puntajes:
                st.session_state.puntajes[nombre]["A"] = st.session_state.puntaje_base_a
            st.info("Todos los puntajes fueron reiniciados.")

# ----------------------
# 🏅 Pestaña 4: Dos Contadores (A y B)
# ----------------------
with tab4:
    st.header("🏅 Puntajes con Dos Contadores (A y B)")

    participantes_visibles_tab4 = st.session_state.orden_personalizado if st.session_state.orden_personalizado else st.session_state.participantes

    if not participantes_visibles_tab4:
        st.warning("Primero agrega participantes en la pestaña anterior.")
    else:
        col_jugador, col_tipo = st.columns([2, 2])
        with col_jugador:
            jugador = st.radio("Selecciona un jugador:", participantes_visibles_tab4, key="jugador_tab4")
        with col_tipo:
            tipo_puntaje = st.radio("¿Qué puntaje deseas modificar?", ["A", "B"], horizontal=True, key="puntaje_tab4")
            if st.session_state.permitir_negativos:
                nuevo_puntaje = st.number_input("Puntaje a agregar o restar:", step=1, value=0, key="puntaje_doble")
            else:
                nuevo_puntaje = st.number_input("Puntaje a agregar:", min_value=0, step=1, value=0, key="puntaje_doble")

        if st.button("➕ Sumar a puntaje A ó B"):
            st.session_state.puntajes[jugador][tipo_puntaje] += nuevo_puntaje
            st.success(f"{jugador} ahora tiene {st.session_state.puntajes[jugador][tipo_puntaje]} puntos en el puntaje {tipo_puntaje}.")

        # Mostrar como tarjetas
        st.subheader("📊 Puntajes Totales:")
        cols = st.columns(4)
        for idx, nombre in enumerate(participantes_visibles_tab4):
            with cols[idx % 4]:
                st.markdown(f"""
                <div class="card">
                <h4>{nombre}</h4>
                <p>A: <strong>{st.session_state.puntajes[nombre].get("A", 0)}</strong></p>
                <p>B: <strong>{st.session_state.puntajes[nombre].get("B", 0)}</strong></p>
                </div>
                """, unsafe_allow_html=True)
        
        if st.button("🔄 Reiniciar puntajes", key="reiniciar_tab4"):
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
