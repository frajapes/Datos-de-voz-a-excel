import streamlit as st
import speech_recognition as r
import pandas as pd
import io
import re

# Configuración de la página en el celular
st.set_page_config(page_title="Dictado a Excel", page_icon="📊", layout="centered")
st.title("🎙️ Dictado de Números a Excel")
st.write("Dicta tus números o sube un audio. Cada pausa creará una nueva hoja con datos enumerados.")

# Inicializar el estado de la aplicación si no existe
if "hojas_datos" not in st.session_state:
    st.session_state.hojas_datos = {}  # Diccionario para guardar {'Hoja 1': [números], 'Hoja 2': [...]}
if "contador_hojas" not in st.session_state:
    st.session_state.contador_hojas = 1

# Función para limpiar el texto y extraer solo números
def extraer_numeros(texto):
    # Diccionario básico para convertir números dictados en palabras a dígitos
    palabras_a_numeros = {
        "uno": "1", "dos": "2", "tres": "3", "cuatro": "4", "cinco": "5",
        "seis": "6", "siete": "7", "ocho": "8", "nueve": "9", "cero": "0"
    }
    
    texto_limpio = texto.lower()
    for palabra, digito in palabras_a_numeros.items():
        texto_limpio = texto_limpio.replace(palabra, digito)
    
    # Buscar todos los bloques numéricos en el texto
    numeros = re.findall(r'\d+', texto_limpio)
    return [int(n) for n in numeros]

# --- SECCIÓN 1: SUBIR O GRABAR AUDIO ---
archivo_audio = st.file_uploader("Sube tu archivo de audio (.wav o .mp3)", type=["wav", "mp3"])

# Botones de control de flujo
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔴 Procesar Bloque Actual"):
        if archivo_audio is not None:
            recognizer = r.Recognizer()
            with r.AudioFile(archivo_audio) as source:
                audio_data = recognizer.record(source)
                try:
                    # Transcripción usando el servicio gratuito de Google en español
                    texto_transcrito = recognizer.recognize_google(audio_data, language="es-ES")
                    numeros_obtenidos = extraer_numeros(texto_transcrito)
                    
                    if numeros_obtenidos:
                        nombre_hoja = f"Hoja {st.session_state.contador_hojas}"
                        st.session_state.hojas_datos[nombre_hoja] = numeros_obtenidos
                        st.success(f"¡Procesado! Se encontraron {len(numeros_obtenidos)} números en la {nombre_hoja}.")
                    else:
                        st.warning("No se detectaron números en el audio.")
                except Exception as e:
                    st.error("No se pudo entender el audio o el formato no es compatible.")
        else:
            st.warning("Por favor, sube un archivo de audio primero.")

with col2:
    if st.button("⏸️ Pausar y Siguiente Hoja"):
        st.session_state.contador_hojas += 1
        st.info(f"Audio pausado. Al continuar, los datos irán en la **Hoja {st.session_state.contador_hojas}**")

with col3:
    if st.button("🔄 Reiniciar Todo"):
        st.session_state.hojas_datos = {}
        st.session_state.contador_hojas = 1
        st.rerun()

# --- SECCIÓN 2: VISTA PREVIA Y DESCARGA ---
if st.session_state.hojas_datos:
    st.write("---")
    st.subheader("📋 Vista previa del Libro de Excel")
    
    for hoja, datos in st.session_state.hojas_datos.items():
        st.write(f"**{hoja}** ({len(datos)} elementos):")
        # Creamos la enumeración partiendo desde 1
        indices = list(range(1, len(datos) + 1))
        df_vista = pd.DataFrame({"Índice": indices, "Números": datos})
        st.dataframe(df_vista, hide_index=True)

    # Generar el archivo Excel en memoria para la descarga
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        for hoja, datos in st.session_state.hojas_datos.items():
            indices = list(range(1, len(datos) + 1))
            df_excel = pd.DataFrame({"Índice": indices, "Números": datos})
            # index=False evita que se guarde la columna por defecto de pandas y use nuestra columna "Índice"
            df_excel.to_excel(writer, sheet_name=hoja, index=False)
    
    excel_data = output.getvalue()

    st.download_button(
        label="📥 Descargar Archivo Excel",
        data=excel_data,
        file_name="datos_dictados_enumerados.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
import streamlit as st
import speech_recognition as r
import pandas as pd
import io
import re

# Configuración de la página en el celular
st.set_page_config(page_title="Dictado a Excel", page_icon="📊", layout="centered")
st.title("🎙️ Dictado de Números a Excel")
st.write("Dicta tus números o sube un audio. Cada pausa creará una nueva hoja con datos enumerados.")

# Inicializar el estado de la aplicación si no existe
if "hojas_datos" not in st.session_state:
    st.session_state.hojas_datos = {}  # Diccionario para guardar {'Hoja 1': [números], 'Hoja 2': [...]}
if "contador_hojas" not in st.session_state:
    st.session_state.contador_hojas = 1

# Función para limpiar el texto y extraer solo números
def extraer_numeros(texto):
    # Diccionario básico para convertir números dictados en palabras a dígitos
    palabras_a_numeros = {
        "uno": "1", "dos": "2", "tres": "3", "cuatro": "4", "cinco": "5",
        "seis": "6", "siete": "7", "ocho": "8", "nueve": "9", "cero": "0"
    }
    
    texto_limpio = texto.lower()
    for palabra, digito in palabras_a_numeros.items():
        texto_limpio = texto_limpio.replace(palabra, digito)
    
    # Buscar todos los bloques numéricos en el texto
    numeros = re.findall(r'\d+', texto_limpio)
    return [int(n) for n in numeros]

# --- SECCIÓN 1: SUBIR O GRABAR AUDIO ---
archivo_audio = st.file_uploader("Sube tu archivo de audio (.wav o .mp3)", type=["wav", "mp3"])

# Botones de control de flujo
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔴 Procesar Bloque Actual"):
        if archivo_audio is not None:
            recognizer = r.Recognizer()
            with r.AudioFile(archivo_audio) as source:
                audio_data = recognizer.record(source)
                try:
                    # Transcripción usando el servicio gratuito de Google en español
                    texto_transcrito = recognizer.recognize_google(audio_data, language="es-ES")
                    numeros_obtenidos = extraer_numeros(texto_transcrito)
                    
                    if numeros_obtenidos:
                        nombre_hoja = f"Hoja {st.session_state.contador_hojas}"
                        st.session_state.hojas_datos[nombre_hoja] = numeros_obtenidos
                        st.success(f"¡Procesado! Se encontraron {len(numeros_obtenidos)} números en la {nombre_hoja}.")
                    else:
                        st.warning("No se detectaron números en el audio.")
                except Exception as e:
                    st.error("No se pudo entender el audio o el formato no es compatible.")
        else:
            st.warning("Por favor, sube un archivo de audio primero.")

with col2:
    if st.button("⏸️ Pausar y Siguiente Hoja"):
        st.session_state.contador_hojas += 1
        st.info(f"Audio pausado. Al continuar, los datos irán en la **Hoja {st.session_state.contador_hojas}**")

with col3:
    if st.button("🔄 Reiniciar Todo"):
        st.session_state.hojas_datos = {}
        st.session_state.contador_hojas = 1
        st.rerun()

# --- SECCIÓN 2: VISTA PREVIA Y DESCARGA ---
if st.session_state.hojas_datos:
    st.write("---")
    st.subheader("📋 Vista previa del Libro de Excel")
    
    for hoja, datos in st.session_state.hojas_datos.items():
        st.write(f"**{hoja}** ({len(datos)} elementos):")
        # Creamos la enumeración partiendo desde 1
        indices = list(range(1, len(datos) + 1))
        df_vista = pd.DataFrame({"Índice": indices, "Números": datos})
        st.dataframe(df_vista, hide_index=True)

    # Generar el archivo Excel en memoria para la descarga
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        for hoja, datos in st.session_state.hojas_datos.items():
            indices = list(range(1, len(datos) + 1))
            df_excel = pd.DataFrame({"Índice": indices, "Números": datos})
            # index=False evita que se guarde la columna por defecto de pandas y use nuestra columna "Índice"
            df_excel.to_excel(writer, sheet_name=hoja, index=False)
    
    excel_data = output.getvalue()

    st.download_button(
        label="📥 Descargar Archivo Excel",
        data=excel_data,
        file_name="datos_dictados_enumerados.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
