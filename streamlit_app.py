import streamlit as st

def main():
    # Diccionario de esquemas de color
    colores_tema = {
        "Azul": {
            "background": "#E8F0FE",
            "text": "#0D47A1"
        },
        "Verde": {
            "background": "#E8F5E9",
            "text": "#1B5E20"
        },
        "Rosa": {
            "background": "#FCE4EC",
            "text": "#880E4F"
        }
    }

    # Configuración de la página
    st.set_page_config(page_title="Contador de Puntaje", layout="centered")

    # Selector de color
    color_elegido = st.radio("Elegí un tema de color:", list(colores_tema.keys()))

    # Estilo HTML dinámico
    estilo = f"""
        <style>
        .custom-container {{
            background-color: {colores_tema[color_elegido]["background"]};
            color: {colores_tema[color_elegido]["text"]};
            padding: 3em;
            border-radius: 10px;
            text-align: center;
        }}
        </style>
        <div class="custom-container">
            <h1>¡Bienvenido!</h1>
            <p>Gracias por visitar esta página hecha con Streamlit 😊</p>
        </div>
    """
    st.markdown(estilo, unsafe_allow_html=True)

# Ejecutar la función principal
if __name__ == "__main__":
    main()
