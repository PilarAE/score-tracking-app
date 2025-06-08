import streamlit as st

# Configuración de la página
st.set_page_config(page_title="App Interactiva", layout="centered")

# Título general
st.title("🏆 App de Conteo de Puntajes")

# Inicializar listas en la sesión
if "participantes" not in st.session_state:
    st.session_state.participantes = []
if "puntajes" not in st.session_state:
    st.session_state.puntajes = {}

# Crear las pestañas
tab1, tab2, tab3 tab4 = st.tabs(["📖 Instrucciones", "👥 Ingresa Participantes", "🎯 Ingresa Puntajes" "🎯 Ingresa 2 Puntajes"])

# ----------------------
# 📖 Pestaña 1: Instrucciones
# ----------------------
with tab1:
    st.header("📖 ¿Cómo usar esta app?")
    st.markdown("""
    Esta aplicación tiene tres secciones:
    
    1. **Ingresa Participantes:** Aquí puedes agregar los nombres de los participantes.
    2. **Ingresa Puntajes:** Puedes llevar dos tipos de puntaje por persona (A y B).
    3. **Pásalo bien:** Esta app está pensada para actividades grupales como juegos, concursos, dinámicas educativas o team building.
    
    ---
    """)

# ----------------------
# 👥 Pestaña 2: Participantes
# ----------------------
with tab2:
    st.header("👥 Agregar Participantes")

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
                st.session_state.puntajes[nombre_limpio] = {"A": 0, "B": 0}
                st.success(f"Agregado: {nombre_limpio}")

    with col2:
        if st.session_state.participantes:
            st.markdown("### 🧑‍🤝‍🧑 Lista actual:")
            for i, p in enumerate(st.session_state.participantes, start=1):
                st.markdown(f"- {i}. {p}")

            if st.button("🗑️ Limpiar lista"):
                st.session_state.participantes = []
                st.session_state.puntajes = {}
                st.info("Lista de participantes y puntajes vaciada.")

    st.markdown("""---""")


# ----------------------
# 🎯 Pestaña 3: Puntajes
# ----------------------
with tab3:
    st.header("🎯 Registrar Puntajes")

    if not st.session_state.participantes:
        st.warning("Primero agrega participantes en la pestaña anterior.")
    else:
        # Inicializar puntajes si no existen
        for nombre in st.session_state.participantes:
            if nombre not in st.session_state.puntajes:
                st.session_state.puntajes[nombre] = 0

        # Mostrar los jugadores como radio buttons
        jugador = st.radio("Selecciona un jugador:", st.session_state.participantes)

        # Ingresar puntaje nuevo
        nuevo_puntaje = st.number_input("Puntaje a agregar:", min_value=0, step=1)

        # Botón para agregar puntaje
        if st.button("➕ Sumar puntaje") and jugador:
            st.session_state.puntajes[jugador] += nuevo_puntaje
            st.success(f"{jugador} ahora tiene {st.session_state.puntajes[jugador]} puntos.")

        # Mostrar tabla de puntajes actualizados
        st.subheader("📊 Puntajes Totales:")
        for nombre, puntaje in st.session_state.puntajes.items():
            st.markdown(f"- **{nombre}**: {puntaje} puntos")

        # Botón para reiniciar todos los puntajes
        if st.button("🔄 Reiniciar puntajes"):
            for nombre in st.session_state.puntajes:
                st.session_state.puntajes[nombre] = 0
            st.info("Todos los puntajes fueron reiniciados a 0.")

    st.markdown("""---""")


# ----------------------
# 🎯 Pestaña 4: Puntajes
# ----------------------
with tab3:
    st.header("🎯 Registrar Puntajes")

    if not st.session_state.participantes:
        st.warning("Primero agrega participantes en la pestaña anterior.")
    else:
        # Asegurar que todos los participantes tengan ambos tipos de puntajes
        for nombre in st.session_state.participantes:
            if nombre not in st.session_state.puntajes:
                st.session_state.puntajes[nombre] = {"A": 0, "B": 0}
            else:
                if "A" not in st.session_state.puntajes[nombre]:
                    st.session_state.puntajes[nombre]["A"] = 0
                if "B" not in st.session_state.puntajes[nombre]:
                    st.session_state.puntajes[nombre]["B"] = 0

        jugador = st.radio("Selecciona un jugador:", st.session_state.participantes)
        tipo_puntaje = st.radio("¿Qué puntaje deseas sumar?", ["A", "B"], horizontal=True)
        nuevo_puntaje = st.number_input("Puntaje a agregar:", min_value=0, step=1)

        if st.button("➕ Sumar puntaje") and jugador:
            st.session_state.puntajes[jugador][tipo_puntaje] += nuevo_puntaje
            st.success(f"{jugador} ahora tiene {st.session_state.puntajes[jugador][tipo_puntaje]} puntos en el puntaje {tipo_puntaje}.")

        st.subheader("📊 Puntajes Totales:")
        for nombre, p in st.session_state.puntajes.items():
            st.markdown(f"- **{nombre}**: A = {p['A']} puntos | B = {p['B']} puntos")

        if st.button("🔄 Reiniciar puntajes"):
            for nombre in st.session_state.puntajes:
                st.session_state.puntajes[nombre] = {"A": 0, "B": 0}
            st.info("Todos los puntajes fueron reiniciados a 0.")

    st.markdown("""---""")




# Footer divertido
st.markdown("Hecho por Rodrigo López de inovación")

