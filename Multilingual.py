import streamlit as st
import easyocr
from PIL import Image
import numpy as np
import os
import time
from mtranslate import translate
from transformers import pipeline
from langdetect import detect
import pyttsx3
import speech_recognition as sr

# -------------------- PAGE SETUP --------------------
st.set_page_config(page_title="🌍 Real-Life Multilingual Translator", page_icon="🌎", layout="centered")
st.title("🌍 AI-Powered OCR + Translator + Voice App")
st.write("📸 Extract, 🎙️ speak, or ✍️ type — and translate instantly with smart language detection!")

# -------------------- LANGUAGE SETUP --------------------
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

target_lang = st.selectbox("🌐 Choose Target Language", list(languages.keys()), index=10)
engine = st.radio("⚙️ Choose Translation Engine", ["mtranslate (Fast)", "Hugging Face (Accurate, Slow)"])

# -------------------- OCR SETUP --------------------
MODEL_DIR = os.path.join(os.getcwd(), "models")
os.makedirs(MODEL_DIR, exist_ok=True)
reader = easyocr.Reader(['en', 'hi'], model_storage_directory=MODEL_DIR, gpu=False)

# -------------------- TRANSLATION MEMORY --------------------
translation_memory = {}

# -------------------- UTILITIES --------------------
def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"

def text_to_speech(text, lang="en"):
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty("rate", 160)
    engine.setProperty("voice", voices[0].id)
    engine.say(text)
    engine.runAndWait()

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Speak now...")
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
    try:
        st.info("🧠 Recognizing...")
        return recognizer.recognize_google(audio)
    except Exception as e:
        st.error(f"❌ Speech Recognition Error: {e}")
        return ""

def translate_text(text, target_lang):
    """Translate text with memory + model fallback."""
    if text.strip() in translation_memory:
        return translation_memory[text.strip()] + " (⚡ from memory)"

    detected_lang = detect_language(text)
    st.write(f"🕵️ Detected Language: **{detected_lang.upper()}**")

    try:
        if engine == "mtranslate (Fast)":
            translated = translate(text, languages[target_lang])
        else:
            if target_lang == "Hindi":
                translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-hi")
            elif target_lang == "English":
                translator = pipeline("translation", model="Helsinki-NLP/opus-mt-hi-en")
            else:
                translated = translate(text, languages[target_lang])
                translation_memory[text.strip()] = translated
                return translated
            translated = translator(text)[0]['translation_text']

        translation_memory[text.strip()] = translated
        return translated
    except Exception as e:
        return f"❌ Error during translation: {str(e)}"

# -------------------- MAIN UI --------------------
mode = st.radio("🎯 Choose Input Mode", ["🖼️ Upload Image", "🎙️ Speak", "✍️ Type or Paste Text"])

if mode == "🖼️ Upload Image":
    img_file = st.file_uploader("📤 Upload an Image", type=["png", "jpg", "jpeg"])
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
            if st.button("🔊 Listen to Translation"):
                text_to_speech(translated_text, languages[target_lang])

elif mode == "🎙️ Speak":
    if st.button("🎤 Start Recording"):
        spoken_text = speech_to_text()
        st.write("🗣️ You said:", spoken_text)
        if spoken_text:
            translated_text = translate_text(spoken_text, target_lang)
            st.subheader(f"🌐 Translated to {target_lang}:")
            st.write(translated_text)
            if st.button("🔊 Listen to Translation"):
                text_to_speech(translated_text, languages[target_lang])

elif mode == "✍️ Type or Paste Text":
    user_text = st.text_area("🧾 Enter your text below:")
    if st.button("Translate Text"):
        translated_text = translate_text(user_text, target_lang)
        st.subheader(f"🌐 Translated to {target_lang}:")
        st.write(translated_text)
        if st.button("🔊 Listen to Translation"):
            text_to_speech(translated_text, languages[target_lang])





