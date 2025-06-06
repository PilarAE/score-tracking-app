import streamlit as st
import speech_recognition as sr
import pandas as pd
import re
from typing import List, Dict, Tuple
import uuid

import streamlit as st

# Título de la aplicación
st.title("CP - Contador de Puntajes")

# Texto de bienvenida
st.write("Bienvenido!")

# Opciones de color
color = st.radio("Selecciona un color de fondo:", ('Rojo', 'Verde', 'Azul'))

# Cambiando el color de fondo según la selección
if color == 'Rojo':
    st.markdown(
        """
        <style>
        .reportview-container {
            background-color: red;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
elif color == 'Verde':
    st.markdown(
        """
        <style>
        .reportview-container {
            background-color: green;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
elif color == 'Azul':
    st.markdown(
        """
        <style>
        .reportview-container {
            background-color: blue;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Ejecutar la aplicación
if __name__ == "__main__":
    st.write("¡Elige un color para personalizar tu aplicación!")
