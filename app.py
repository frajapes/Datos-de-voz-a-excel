import streamlit as st
import pandas as pd
import speech_recognition as sr
from pydub import AudioSegment
import io
import re

# Configuración de la página
st.set_page_config(page_title="Dictado de Números a Excel", page_icon="🎙️")

st.title("🎙️ Dictado de Números a Excel")
st.write("Dicta tus números o sube un audio. Cada pausa creará una nueva hoja con datos enumerados.")

# Inicializar estados de la sesión si no existen
if "hojas_datos" not in st.session_state:
    st.session_state.hojas_datos = {}
if "contador_hojas" not in st.session_state:
    st.session_state.contador_hojas = 1

# --- SECCIÓN 1: SUBIDA Y PROCESAMIENTO DE AUDIO ---
st.subheader("Sube tu archivo de audio (.wav, .mp3 o .m4a)")
archivo_audio = st.file_uploader("Selecciona un archivo", type=["wav", "mp3", "m4a"], label_visibility="collapsed")

col1, col2, col3 = st.columns(3)

with col1:
    procesar = st.button("🔴 Procesar Bloque Actual")
with col2:
    pausar = st.button("⏸️ Pausar y Siguiente Hoja")
with col3:
    reiniciar = st.button("🔄 Reiniciar Todo")

# Lógica del botón Reiniciar
if reiniciar:
    st.session_state.hojas_datos = {}
    st.session_state.contador_hojas = 1
    st.rerun()

# Lógica de procesamiento de audio REAL
if archivo_audio and procesar:
    with st.spinner("Procesando y transformando audio a texto..."):
        try:
            # Leer el archivo subido en memoria
            audio_bytes = archivo_audio.read()
            audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes))
            
            # Convertir obligatoriamente a WAV (formato que requiere SpeechRecognition)
            wav_io = io.BytesIO()
            audio_segment.export(wav_io, format="wav")
            wav_io.seek(0)
            
            # Reconocimiento de voz
            recognizer = sr.Recognizer()
            with sr.AudioFile(wav_io) as source:
                audio_data = recognizer.record(source)
                # Cambiado a español para que entienda bien los números dictados
                texto_transcrito = recognizer.recognize_google(audio_data, language="es-ES")
            
            # Buscar todos los números en el texto transcrito
            nuevos_datos = re.findall(r'\d+', texto_transcrito)
            
            if nuevos_datos:
                nombre_hoja = f"Hoja {st.session_state.contador_hojas}"
                if nombre_hoja not in st.session_state.hojas_datos:
                    st.session_state.hojas_datos[nombre_hoja] = []
                
                st.session_state.hojas_datos[nombre_hoja].extend(nuevos_datos)
                st.success(f"¡Éxito! Se encontraron {len(nuevos_datos)} números y se agregaron a la {nombre_hoja}")
            else:
                st.warning("El audio se procesó, pero no se lograron detectar números claros en la transcripción.")
                
        except Exception as e:
            st.error(f"Hubo un problema al procesar el audio: {e}")

if pausar:
    st.session_state.contador_hojas += 1
    st.info(f"Preparado para la Hoja {st.session_state.contador_hojas}")

# --- SECCIÓN 2: VISTA PREVIA Y DESCARGA ---
if st.session_state.hojas_datos:
    st.write("---")
    st.subheader("📋 Vista previa del Libro de Excel")
    
    for hoja, datos in st.session_state.hojas_datos.items():
        st.write(f"**{hoja}** ({len(datos)} elementos)")
        indices = list(range(1, len(datos) + 1))
        df_vista = pd.DataFrame({"Índice": indices, "Datos": datos})
        st.dataframe(df_vista, hide_index=True)
        
    # Generar el archivo Excel en memoria
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        for hoja, datos in st.session_state.hojas_datos.items():
            indices = list(range(1, len(datos) + 1))
            df_excel = pd.DataFrame({"Índice": indices, "Datos": datos})
            df_excel.to_excel(writer, sheet_name=hoja, index=False)
            
    excel_data = output.getvalue()
    
    st.download_button(
        label="📥 Descargar Archivo Excel",
        data=excel_data,
        file_name="datos_dictados_enumerados.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
