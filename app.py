import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import easyocr
from translate import Translator
from docx import Document
from io import BytesIO
from langdetect import detect

st.title("🌍 Traductor OCR (Detecta idioma automáticamente)")
st.markdown("Sube un PDF escaneado o una imagen. Detectamos el idioma y traducimos el texto a español 🇪🇸.")

uploaded_file = st.file_uploader("📤 Sube tu archivo (PDF o imagen)", type=["pdf", "png", "jpg", "jpeg"])

imagenes = []

if uploaded_file:
    if uploaded_file.type == "application/pdf":
        uploaded_file.seek(0)
        with st.spinner("Convirtiendo PDF a imágenes..."):
            doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            for page in doc:
                pix = page.get_pixmap(dpi=300)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                imagenes.append(img)
    else:
        imagen = Image.open(uploaded_file).convert("RGB")
        imagenes = [imagen]

    reader = easyocr.Reader(['en', 'es'], gpu=False)

    texto_extraido = ""
    with st.spinner("Aplicando OCR..."):
        for i, image in enumerate(imagenes):
            resultados = reader.readtext(image, detail=0)
            texto = "\n".join(resultados)
            texto_extraido += f"\n\n--- Página {i+1} ---\n\n{texto}"

    try:
        idioma_detectado = detect(texto_extraido)
    except:
        idioma_detectado = "desconocido"

    st.info(f"🌐 Idioma detectado: `{idioma_detectado}`")

    if idioma_detectado != "es":
        with st.spinner("Traduciendo al español..."):
            translator = Translator(from_lang=idioma_detectado, to_lang="es")
            texto_traducido = translator.translate(texto_extraido)
    else:
        texto_traducido = texto_extraido

    with st.spinner("Generando documento Word..."):
        docx = Document()
        docx.add_paragraph(texto_traducido)

        output = BytesIO()
        docx.save(output)
        output.seek(0)

    st.success("✅ Traducción completada.")
    st.download_button(
        label="📥 Descargar Word traducido",
        data=output,
        file_name="documento_traducido.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
