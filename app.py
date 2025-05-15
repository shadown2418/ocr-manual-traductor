
import streamlit as st
import os
from pdf2image import convert_from_bytes
from PIL import Image
import pytesseract
from translate import Translator
from docx import Document
from io import BytesIO

# Configuración
st.title("🧠 Traductor de PDF Escaneado (Inglés ➝ Español)")
st.markdown("Sube un PDF escaneado en inglés y obtén un documento Word traducido al español.")

uploaded_file = st.file_uploader("📤 Sube tu archivo PDF", type=["pdf"])

if uploaded_file:
    with st.spinner("Convirtiendo PDF a imágenes..."):
        images = convert_from_bytes(uploaded_file.read(), dpi=300)

    texto_extraido = ""
    with st.spinner("Aplicando OCR a cada página..."):
        for i, image in enumerate(images):
            texto = pytesseract.image_to_string(image, lang="eng")
            texto_extraido += f"\n\n--- Página {i+1} ---\n\n{texto}"

    with st.spinner("Traduciendo al español..."):
        translator = Translator(from_lang="en", to_lang="es")
        texto_traducido = translator.translate(texto_extraido)

    with st.spinner("Creando documento Word..."):
        doc = Document()
        doc.add_paragraph(texto_traducido)

        output = BytesIO()
        doc.save(output)
        output.seek(0)

    st.success("✅ Traducción completada.")
    st.download_button(
        label="📥 Descargar Word traducido",
        data=output,
        file_name="documento_traducido.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
