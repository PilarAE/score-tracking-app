import streamlit as st

# Configuración de la página
st.set_page_config(page_title="App Interactiva", layout="centered")

# Título general
st.title("🏆 App de Conteo de Puntajes")

# Inicializar listas y variables en la sesión
if "participantes" not in st.session_state:
    st.session_state.participantes = []
if "puntajes" not in st.session_state:
    st.session_state.puntajes = {}
if "permitir_negativos" not in st.session_state:
    st.session_state.permitir_negativos = False
if "puntaje_base" not in st.session_state:
    st.session_state.puntaje_base = 0

# Crear las pestañas
tab1, tab2, tab3, tab4 = st.tabs([
    "📖 Instrucciones", "👥 Ingresa Participantes", "🎯 Ingresa Puntaje", "🏅 Puntajes con Dos Contadores"
])

# ----------------------
# 📖 Pestaña 1: Instrucciones
# ----------------------
with tab1:
    st.header("📖 ¿Cómo usar esta app?")
    st.markdown("""
    Esta aplicación tiene cuatro secciones:
    
    1. **Ingresa Participantes:** Aquí puedes agregar los nombres de los participantes. También puedes permitir que los puntajes bajen (valores negativos) y definir puntaje base.
    2. **Ingresa Puntajes:** Aquí ingresas el puntaje de cada ronda por jugador, y llevas el total.
    3. **Puntajes A y B:** Aquí puedes llevar dos puntajes por jugador (por ejemplo, ataque y defensa).
    """)

# ----------------------
# 👥 Pestaña 2: Participantes
# ----------------------
with tab2:
    # ----------------------
    # ⚙️ Configuración global
    # ----------------------
    st.header("👥 Agregar Participantes")
    st.subheader("⚙️ Configuración de Puntajes")

    puntaje_base = st.number_input(
        "Define el puntaje base con el que parten todos los jugadores (dejar en 0 para comenzar en 0):",
        value=st.session_state.puntaje_base, step=1
    )
    st.session_state.puntaje_base = puntaje_base

    st.session_state.permitir_negativos = st.toggle(
        "¿Permitir que los puntajes bajen (valores negativos)?",
        value=st.session_state.permitir_negativos
    )

    st.markdown("---")
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
                st.session_state.puntajes[nombre_limpio] = {"A": puntaje_base, "B": puntaje_base}
                st.success(f"Agregado: {nombre_limpio} con puntaje base {puntaje_base}")

    with col2:
        if st.session_state.participantes:
            st.markdown("### 🧑‍🤝‍🧑 Lista actual:")
            for i, p in enumerate(st.session_state.participantes, start=1):
                st.markdown(f"- {i}. {p}")

            if st.button("🗑️ Limpiar lista"):
                st.session_state.participantes = []
                st.session_state.puntajes = {}
                st.info("Lista de participantes y puntajes vaciada.")

    

st.markdown("---")

# ----------------------
# 🎯 Pestaña 3: Puntaje único
# ----------------------
with tab3:
    st.header("🎯 Registrar Puntajes")

    if not st.session_state.participantes:
        st.warning("Primero agrega participantes en la pestaña anterior.")
    else:
        for nombre in st.session_state.participantes:
            if nombre not in st.session_state.puntajes:
                st.session_state.puntajes[nombre] = {"A": puntaje_base, "B": puntaje_base}
            elif isinstance(st.session_state.puntajes[nombre], int):
                st.session_state.puntajes[nombre] = {"A": st.session_state.puntajes[nombre], "B": puntaje_base}
            else:
                if "A" not in st.session_state.puntajes[nombre]:
                    st.session_state.puntajes[nombre]["A"] = puntaje_base

        # Aquí usamos columnas para poner selector y input en la misma fila
        col_jugador, col_puntaje = st.columns([2, 2])

        with col_jugador:
            jugador = st.radio("Selecciona un jugador:", st.session_state.participantes)

        with col_puntaje:
            if st.session_state.permitir_negativos:
                nuevo_puntaje = st.number_input("Puntaje a agregar o restar:", step=1, value=0)
            else:
                nuevo_puntaje = st.number_input("Puntaje a agregar:", min_value=0, step=1, value=0)

        if st.button("➕ Sumar puntaje") and jugador:
            st.session_state.puntajes[jugador]["A"] += nuevo_puntaje
            st.success(f"{jugador} ahora tiene {st.session_state.puntajes[jugador]['A']} puntos (puntaje total).")

        st.subheader("📊 Puntajes Totales (A):")
        for nombre, p in st.session_state.puntajes.items():
            st.markdown(f"- **{nombre}**: {p['A']} puntos")

        if st.button("🔄 Reiniciar puntajes"):
            for nombre in st.session_state.puntajes:
                st.session_state.puntajes[nombre]["A"] = puntaje_base
            st.info(f"Todos los puntajes fueron reiniciados a {puntaje_base}.")


# ----------------------
# 🏅 Pestaña 4: Puntajes A y B
# ----------------------
with tab4:
    st.header("🏅 Puntajes con Dos Contadores")

    if not st.session_state.participantes:
        st.warning("Primero agrega participantes en la pestaña anterior.")
    else:
        # Sección de puntajes iniciales específicos para A y B
        col_a, col_b = st.columns(2)
        with col_a:
            puntaje_inicial_a = st.number_input("Puntaje inicial para A:", step=1, value=0, key="puntaje_inicial_a")
        with col_b:
            puntaje_inicial_b = st.number_input("Puntaje inicial para B:", step=1, value=0, key="puntaje_inicial_b")

        # Inicializar puntajes A y B por separado
        for nombre in st.session_state.participantes:
            if nombre not in st.session_state.puntajes:
                st.session_state.puntajes[nombre] = {
                    "A": puntaje_inicial_a,
                    "B": puntaje_inicial_b
                }
            else:
                if "A" not in st.session_state.puntajes[nombre]:
                    st.session_state.puntajes[nombre]["A"] = puntaje_inicial_a
                if "B" not in st.session_state.puntajes[nombre]:
                    st.session_state.puntajes[nombre]["B"] = puntaje_inicial_b

        # Selección de jugador y tipo de puntaje a modificar
        col_jugador, col_puntaje = st.columns([2, 2])

        with col_jugador:
            jugador = st.radio("Selecciona un jugador:", st.session_state.participantes)

        with col_puntaje:
            tipo_puntaje = st.radio("¿Qué puntaje deseas modificar?", ["A", "B"], horizontal=True)
            if st.session_state.permitir_negativos:
                nuevo_puntaje = st.number_input("Puntaje a agregar o restar:", step=1, value=0, key="puntaje_doble")
            else:
                nuevo_puntaje = st.number_input("Puntaje a agregar:", min_value=0, step=1, value=0, key="puntaje_doble")

        if st.button("➕ Sumar a puntaje A/B"):
            st.session_state.puntajes[jugador][tipo_puntaje] += nuevo_puntaje
            st.success(f"{jugador} ahora tiene {st.session_state.puntajes[jugador][tipo_puntaje]} puntos en el puntaje {tipo_puntaje}.")

        # Mostrar puntajes como tabla
        st.subheader("📊 Puntajes Totales A y B:")
        import pandas as pd

        data = {
            "Participante": [],
            "Puntaje A": [],
            "Puntaje B": []
        }

        for nombre, p in st.session_state.puntajes.items():
            data["Participante"].append(nombre)
            data["Puntaje A"].append(p.get("A", 0))
            data["Puntaje B"].append(p.get("B", 0))

        df_puntajes = pd.DataFrame(data)
        st.table(df_puntajes)

        # Botón para reiniciar A y B
        if st.button("🔄 Reiniciar A y B"):
            for nombre in st.session_state.puntajes:
                st.session_state.puntajes[nombre]["A"] = puntaje_inicial_a
                st.session_state.puntajes[nombre]["B"] = puntaje_inicial_b
            st.info(f"Todos los puntajes A y B fueron reiniciados.")



# ----------------------
# 📌 Pie de página global
# ----------------------
st.markdown("""
<hr style="margin-top: 2em; margin-bottom: 1em;">
<center>
    <small>Desarrollado por Rodrigo López, Innovación CVD, usando ChatGPT + GitHub + Streamlit · © 2025</small>
</center>
""", unsafe_allow_html=True)
