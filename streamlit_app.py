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
tab1, tab2, tab3 = st.tabs(["📖 Instrucciones", "👥 Ingresa Participantes", "🎯 Ingresa Puntajes"])

# ----------------------
# 📖 Pestaña 1: Instrucciones
# ----------------------
with tab1:
    st.header("📖 ¿Cómo usar esta app?")
    st.markdown("""
    Esta aplicación tiene tres secciones:
    
    1. **Ingresa Participantes:** Aquí puedes agregar los nombres de los participantes.
    2. **Ingresa Puntajes:** Una vez que tengas la lista de participantes, puedes empezar a jugar y registrar sus puntajes.
    3. **Pásalo bien:** Esta app está pensada para actividades grupales como juegos, concursos, dinámicas educativas o team building.
    
    ---
    """)

# ----------------------
# 👥 Pestaña 2: Participantes
# ----------------------
with tab2:
    st.header("👥 Agregar Participantes")

    nombre = st.text_input("✍️ Escribe un nombre:")

    if st.button("➕ Agregar"):
        if nombre.strip() != "":
            st.session_state.participantes.append(nombre.strip())
            st.success(f"Agregado: {nombre}")
        else:
            st.warning("Por favor, escribe un nombre válido.")

    if st.session_state.participantes:
        st.markdown("### 🧑‍🤝‍🧑 Lista actual:")
        for i, p in enumerate(st.session_state.participantes, start=1):
            st.markdown(f"- {i}. {p}")

        if st.button("🗑️ Limpiar lista"):
            st.session_state.participantes = []
            st.info("Lista vaciada.")

# ----------------------
# 🎯 Pestaña 3: Puntajes
# ----------------------
with tab3:
    st.header("🎯 Registrar Puntajes")

    if not st.session_state.participantes:
        st.warning("Primero agrega participantes en la pestaña anterior.")
    else:
        for nombre in st.session_state.participantes:
            puntaje = st.number_input(f"Ingresa el puntaje para {nombre}:", min_value=0, step=1)
            st.session_state.puntajes[nombre] = puntaje

        st.markdown("---")
        st.subheader("📊 Puntajes registrados:")
        for nombre, puntaje in st.session_state.puntajes.items():
            st.markdown(f"**{nombre}**: {puntaje} puntos")



# Footer divertido
st.markdown("Hecho por Rodrigo López de inovación")

