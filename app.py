import streamlit as st
import pandas as pd
import speech_recognition as sr
from pydub import AudioSegment
import io

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
st.subheader("Sube tu archivo de audio (.wav o .mp3)")
archivo_audio = st.file_uploader("Selecciona un archivo", type=["wav", "mp3"], label_visibility="collapsed")

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

# Lógica de simulación o procesamiento (puedes adaptarla según tu función de transcripción)
if archivo_audio and procesar:
    nombre_hoja = f"Hoja {st.session_state.contador_hojas}"
    # Ejemplo de datos simulados (reemplazar con tu lógica de SpeechRecognition)
    nuevos_datos = ["123", "456", "789"] 
    
    if nombre_hoja not in st.session_state.hojas_datos:
        st.session_state.hojas_datos[nombre_hoja] = []
    
    st.session_state.hojas_datos[nombre_hoja].extend(nuevos_datos)
    st.success(f"Datos agregados a la {nombre_hoja}")

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
