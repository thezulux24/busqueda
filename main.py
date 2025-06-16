import streamlit as st
from cryptography.fernet import Fernet
import pandas as pd
from io import StringIO


st.set_page_config(page_title="Búsqueda Inscritos Carrera CALOTO RUN 2025", layout="centered")

@st.cache_data  
def load_data(file_name, key):
    try:
        f = Fernet(key)
        with open(file_name, "rb") as file:
            encrypted_data = file.read()
        decrypted_data = f.decrypt(encrypted_data)
        df = pd.read_csv(StringIO(decrypted_data.decode()), delimiter=';')
        df['Cedula'] = df['Cedula'].astype(str).str.strip()
        df['Celular'] = df['Celular'].astype(str).str.strip()
        return df
    except Exception as e:
        st.error(f"Error al cargar datos: {str(e)}")
        return None

# Cargar datos con caché
key = st.secrets["key"]
df = load_data('data/data.csv', key)

if df is not None:
    st.title('Búsqueda Inscritos')
    
    search_option = st.radio('Seleccione el método de búsqueda', ('Cédula', 'Teléfono'))
    
    resultado = None

    if search_option == 'Cédula':
        cedula_input = st.text_input('Ingrese el número de cédula', '')
        if st.button('Buscar'):
            if cedula_input:
                cedula_input = str(cedula_input).strip()
                resultado = df[df["Cedula"] == cedula_input]  # Búsqueda exacta
            else:
                resultado = pd.DataFrame()

    elif search_option == 'Teléfono':
        celular_input = st.text_input('Ingrese el número de teléfono', '')
        if st.button('Buscar'):
            if celular_input:
                celular_input = str(celular_input).strip()
                resultado = df[df['Celular'] == celular_input]  # Búsqueda exacta
            else:
                resultado = pd.DataFrame()

    if resultado is not None:
        if not resultado.empty:
            st.success('Te encuentras inscrito.')
            st.toast('Te encuentras inscrito.', icon="✅")
            st.write(f"Nombre: {resultado.iloc[0]['Nombre']}")
            st.write(f"Distancia: {resultado.iloc[0]['Distancia']}")
            st.write(f"Sexo: {resultado.iloc[0]['Sexo']}")
            st.write(f"Talle: {resultado.iloc[0]['Talle']}")
            st.write(f"Celular: {resultado.iloc[0]['Celular']}")
            st.write(f"Correo: {resultado.iloc[0]['Correo']}")

        else:
            st.error('Cédula o teléfono no encontrado. No te encuentras inscrito.')
            st.toast('Cédula o teléfono no encontrado. No te encuentras inscrito.', icon="❌")