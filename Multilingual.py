import streamlit as st
import easyocr
from PIL import Image
import numpy as np
import os
import time
from mtranslate import translate
from transformers import pipeline

# -------------------- Page Setup --------------------
st.set_page_config(page_title="📷 OCR + Translator", page_icon="🌍", layout="centered")
st.title("📷 OCR + Translation App")
st.write("Extract or enter text, then translate it instantly using mtranslate or Hugging Face models!")

# -------------------- Language Setup --------------------
languages = {
    "Afrikaans": "af", "Albanian": "sq", "Amharic": "am", "Arabic": "ar", "Armenian": "hy",
    "Azerbaijani": "az", "Basque": "eu", "Belarusian": "be", "Bengali": "bn", "Bosnian": "bs",
    "Bulgarian": "bg", "Catalan": "ca", "Chinese (Simplified)": "zh-CN",
    "Chinese (Traditional)": "zh-TW", "Croatian": "hr", "Czech": "cs", "Danish": "da",
    "Dutch": "nl", "English": "en", "French": "fr", "German": "de", "Greek": "el",
    "Gujarati": "gu", "Hindi": "hi", "Italian": "it", "Japanese": "ja", "Kannada": "kn",
    "Korean": "ko", "Malayalam": "ml", "Marathi": "mr", "Nepali": "ne", "Polish": "pl",
    "Portuguese": "pt", "Punjabi": "pa", "Russian": "ru", "Spanish": "es", "Swahili": "sw",
    "Tamil": "ta", "Telugu": "te", "Thai": "th", "Turkish": "tr", "Urdu": "ur", "Vietnamese": "vi"
}
target_lang = st.selectbox("🌐 Choose Target Language", list(languages.keys()), index=1)

# Choose translation engine
engine = st.radio("⚙️ Choose Translation Engine", ["mtranslate (Fast)", "Hugging Face (Accurate, Slow)"])

# -------------------- Mode Selection --------------------
mode = st.radio("🎯 Choose Input Mode", ["🖼️ Upload Image", "✍️ Type or Paste Text"])

# -------------------- EasyOCR Setup --------------------
MODEL_DIR = os.path.join(os.getcwd(), "models")
os.makedirs(MODEL_DIR, exist_ok=True)
reader = easyocr.Reader(['en', 'hi'], model_storage_directory=MODEL_DIR, gpu=False)

# -------------------- Translation Function --------------------
def translate_text(text, target_lang):
    """Translate text using chosen engine."""
    if not text.strip():
        return "⚠️ No text provided!"
    if engine == "mtranslate (Fast)":
        return translate(text, languages[target_lang])
    else:
        if target_lang == "Hindi":
            translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-hi")
        elif target_lang == "English":
            translator = pipeline("translation", model="Helsinki-NLP/opus-mt-hi-en")
        else:
            return translate(text, languages[target_lang])
        translated = translator(text)
        return translated[0]['translation_text']

# -------------------- MAIN LOGIC --------------------
if mode == "🖼️ Upload Image":
    img_file = st.file_uploader("📤 Upload an image", type=["png", "jpg", "jpeg"])
    if img_file:
        image = Image.open(img_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)
        with st.spinner("🔍 Extracting text..."):
            result = reader.readtext(np.array(image))
            extracted_text = " ".join([res[1] for res in result])
        st.subheader("📝 Extracted Text:")
        st.write(extracted_text if extracted_text.strip() else "⚠️ No text detected.")
        if st.button("Translate Text"):
            translated_text = translate_text(extracted_text, target_lang)
            st.subheader(f"🌐 Translated to {target_lang}:")
            st.write(translated_text)

elif mode == "✍️ Type or Paste Text":
    user_text = st.text_area("🧾 Enter your text below:")
    if st.button("Translate Text"):
        translated_text = translate_text(user_text, target_lang)
        st.subheader(f"🌐 Translated to {target_lang}:")
        st.write(translated_text)

            st.subheader(f"🌐 Translated to {target_lang}:")
            st.write(translated_text)



