import streamlit as st

# Configuración inicial
st.set_page_config(page_title="Bienvenido", layout="centered")

# Título principal
st.title("🎉 Bienvenido a la App Interactiva 🎉")

# Instrucciones
st.markdown("Ingresá los nombres de quienes participarán. ¡Usá el campo de texto y divertite!")

# Inicializar lista de participantes
if "participantes" not in st.session_state:
    st.session_state.participantes = []

# Campo para ingresar nombre
nombre = st.text_input("✍️ Escribí un nombre:")

# Botón para agregar nombre
if st.button("➕ Agregar"):
    if nombre.strip() != "":
        st.session_state.participantes.append(nombre.strip())
        st.success(f"Agregado: {nombre}")
    else:
        st.warning("Por favor, escribí un nombre antes de hacer clic.")

# Mostrar lista actual
if st.session_state.participantes:
    st.markdown("### 🧑‍🤝‍🧑 Lista de Participantes:")
    for i, p in enumerate(st.session_state.participantes, start=1):
        st.markdown(f"- {i}. {p}")

# Botón para reiniciar la lista
if st.button("🗑️ Limpiar lista"):
    st.session_state.participantes = []
    st.info("Lista vaciada.")

# Divisor
st.markdown("---")

# Footer divertido
st.markdown("Hecho con 💻 y ❤️ usando Streamlit")

