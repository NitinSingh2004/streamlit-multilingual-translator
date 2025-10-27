import streamlit as st
from mtranslate import translate
from PyPDF2 import PdfReader
import cv2
import pytesseract
import tempfile
import numpy as np

st.set_page_config(page_title="🌍 Multilingual Translator", page_icon="🌐", layout="wide")

st.title("🌍 Multilingual Text, PDF & Camera Translator")
st.write("Translate text from text input, uploaded PDFs, or real-time camera feed using OpenCV + mtranslate.")

# ---------------------------------------------------
# Language Dictionary
# ---------------------------------------------------
languages = {
    "English": "en", "Hindi": "hi", "French": "fr", "German": "de", "Spanish": "es",
    "Italian": "it", "Japanese": "ja", "Korean": "ko", "Chinese (Simplified)": "zh-CN",
    "Arabic": "ar", "Russian": "ru", "Portuguese": "pt"
}

mode = st.radio("Choose input type:", ["📝 Text", "📄 PDF", "📷 Live Camera Text"])
target_lang = st.selectbox("🌐 Choose target language:", list(languages.keys()), index=1)

# ---------------------------------------------------
# TEXT MODE
# ---------------------------------------------------
if mode == "📝 Text":
    text = st.text_area("Enter text:", placeholder="Type something here...")
    if st.button("🚀 Translate Text"):
        if text.strip():
            translated = translate(text, languages[target_lang])
            st.success(f"**Translated to {target_lang}:**")
            st.write(translated)
        else:
            st.warning("⚠️ Please enter some text.")

# ---------------------------------------------------
# PDF MODE
# ---------------------------------------------------
elif mode == "📄 PDF":
    uploaded_pdf = st.file_uploader("📤 Upload a PDF file", type=["pdf"])
    if uploaded_pdf:
        reader = PdfReader(uploaded_pdf)
        text = ""
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text() + "\n"

        if text:
            st.text_area("📄 Extracted Text", text[:1500] + "..." if len(text) > 1500 else text, height=200)
            if st.button("🌐 Translate PDF"):
                translated = translate(text, languages[target_lang])
                st.text_area(f"✅ Translated to {target_lang}", translated, height=200)
        else:
            st.error("❌ No readable text found in PDF (might be scanned).")

# ---------------------------------------------------
# CAMERA MODE
# ---------------------------------------------------
elif mode == "📷 Live Camera Text":
    st.info("🎥 Turn on your webcam to capture and translate live text in real-time.")
    run_camera = st.checkbox("Start Camera")

    if run_camera:
        # Initialize webcam
        cap = cv2.VideoCapture(0)
        stframe = st.empty()
        extracted_text = ""

        while run_camera:
            ret, frame = cap.read()
            if not ret:
                st.error("Failed to access webcam.")
                break

            # Convert frame to RGB (for display)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            stframe.image(rgb, channels="RGB")

            # Extract text from current frame using pytesseract
            extracted_text = pytesseract.image_to_string(rgb)
            
            if extracted_text.strip():
                st.write("📜 **Detected Text:**", extracted_text[:200] + "..." if len(extracted_text) > 200 else extracted_text)
                translated = translate(extracted_text, languages[target_lang])
                st.success(f"🌐 **Translated to {target_lang}:**")
                st.write(translated)

            # Stop condition: use Streamlit checkbox
            run_camera = st.checkbox("Stop Camera", value=False)

        cap.release()
        st.success("✅ Camera stopped.")

# ---------------------------------------------------
# Footer
# ---------------------------------------------------
st.markdown("---")
st.caption("💡 Built with ❤️ by Nitin Singh using Streamlit + OpenCV + PyTesseract + mtranslate.")


