import streamlit as st
import pytesseract
from PIL import Image
import numpy as np
import time
from mtranslate import translate
from transformers import pipeline

# -------------------- Page Setup --------------------
st.set_page_config(page_title="📷 OCR + Translator", page_icon="🌍", layout="centered")

st.title("📷 OCR + Translation App")
st.write("Extract or enter text, then translate it instantly using mtranslate or Hugging Face models!")

# -------------------- Language Setup --------------------
languages = {
    "English": "en", "Hindi": "hi", "French": "fr", "German": "de", "Spanish": "es",
    "Japanese": "ja", "Chinese (Simplified)": "zh-CN", "Arabic": "ar", "Russian": "ru"
}
target_lang = st.selectbox("🌐 Choose Target Language", list(languages.keys()), index=1)

# Choose translation engine
engine = st.radio("⚙️ Choose Translation Engine", ["mtranslate (Fast)", "Hugging Face (Accurate, Slow)"])

# -------------------- Mode Selection --------------------
mode = st.radio("🎯 Choose Input Mode", ["📸 Camera", "🖼️ Upload Image", "✍️ Type or Paste Text"])

# Refresh time for camera mode
refresh_time = st.slider("⏱️ Refresh every (seconds)", 2, 10, 4, help="Used only for camera mode.")

start = st.toggle("▶️ Start Translation")

# -------------------- Core Function --------------------
def translate_text(text, target_lang):
    """Translate text using chosen engine."""
    if not text.strip():
        return "⚠️ No text provided!"
    if engine == "mtranslate (Fast)":
        return translate(text, languages[target_lang])
    else:
        # Auto detect direction for Hindi ↔ English only
        if target_lang == "Hindi":
            translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-hi")
        elif target_lang == "English":
            translator = pipeline("translation", model="Helsinki-NLP/opus-mt-hi-en")
        else:
            # Default fallback for other languages using mtranslate
            return translate(text, languages[target_lang])
        translated = translator(text)
        return translated[0]['translation_text']

# -------------------- MAIN LOGIC --------------------
if start:
    placeholder_text = st.empty()
    placeholder_trans = st.empty()

    if mode == "📸 Camera":
        st.info("Camera is active. Keep text visible for detection.")
        while True:
            img_file = st.camera_input("📷 Show text to the camera", key=time.time())
            if img_file is not None:
                image = Image.open(img_file)
                text = pytesseract.image_to_string(np.array(image))

                if text.strip():
                    placeholder_text.subheader("📝 Detected Text:")
                    placeholder_text.write(text[:400] + "..." if len(text) > 400 else text)

                    translated_text = translate_text(text, target_lang)
                    placeholder_trans.subheader(f"🌐 Translated to {target_lang}:")
                    placeholder_trans.write(translated_text)
                else:
                    placeholder_text.warning("⚠️ No readable text detected.")
            else:
                placeholder_text.info("Waiting for image capture...")

            time.sleep(refresh_time)
            st.rerun()

    elif mode == "🖼️ Upload Image":
        img_file = st.file_uploader("📤 Upload an image", type=["png", "jpg", "jpeg"])
        if img_file:
            image = Image.open(img_file)
            text = pytesseract.image_to_string(np.array(image))
            st.subheader("📝 Extracted Text:")
            st.write(text if text.strip() else "⚠️ No text detected.")
            if st.button("Translate Text"):
                translated_text = translate_text(text, target_lang)
                st.subheader(f"🌐 Translated to {target_lang}:")
                st.write(translated_text)

    elif mode == "✍️ Type or Paste Text":
        user_text = st.text_area("🧾 Enter your text below:")
        if st.button("Translate Text"):
            translated_text = translate_text(user_text, target_lang)
            st.subheader(f"🌐 Translated to {target_lang}:")
            st.write(translated_text)


