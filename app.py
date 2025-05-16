from pathlib import Path
import zipfile

# Nueva ruta para versión extendida
base_path = Path("/mnt/data/ocr_traductor_idioma_imagen")
base_path.mkdir(parents=True, exist_ok=True)

# app.py extendido con detección de idioma y soporte de imágenes
app_code_extended = """
import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
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
        with st.spinner("Convirtiendo PDF a imágenes..."):
            doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            for page in doc:
                pix = page.get_pixmap(dpi=300)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                imagenes.append(img)
    else:
        imagen = Image.open(uploaded_file).convert("RGB")
        imagenes = [imagen]

    texto_extraido = ""
    with st.spinner("Aplicando OCR..."):
        for i, image in enumerate(imagenes):
            texto = pytesseract.image_to_string(image)
            texto_extraido += f"\\n\\n--- Página {i+1} ---\\n\\n{texto}"

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
"""

# requirements.txt extendido
requirements_extended = """
streamlit
pytesseract
pillow
python-docx
translate
PyMuPDF
langdetect
"""

# README.md actualizado
readme_extended = """
# Traductor OCR con Detección Automática de Idioma (PDF/Imágenes)

Esta app convierte archivos PDF escaneados o imágenes (JPG, PNG) en texto traducido al español, detectando automáticamente el idioma original.

## 🚀 Cómo usar

1. Sube este repositorio a tu cuenta de GitHub.
2. Ve a [https://streamlit.io/cloud](https://streamlit.io/cloud) y conéctalo a tu GitHub.
3. Haz clic en "New App", selecciona este repo, y el archivo `app.py`.
4. ¡Listo! Streamlit te dará una URL pública para usar tu app.

## ✅ Funciones

- OCR con Tesseract
- Traducción automática al español
- Detección de idioma original (`langdetect`)
- Compatible con PDFs e imágenes
"""

# Guardar archivos
(base_path / "app.py").write_text(app_code_extended.strip())
(base_path / "requirements.txt").write_text(requirements_extended.strip())
(base_path / "README.md").write_text(readme_extended.strip())

# Crear ZIP
zip_path_extended = Path("/mnt/data/ocr_traductor_idioma_imagen.zip")
with zipfile.ZipFile(zip_path_extended, 'w') as zipf:
    for file in base_path.iterdir():
        zipf.write(file, arcname=file.name)

zip_path_extended.name
