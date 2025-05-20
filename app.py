import streamlit as st
import pytesseract
import cv2
import tempfile
import os
from googletrans import Translator
from PIL import Image

translator = Translator()

st.title("OCR and Translation App")

uploaded_file = st.file_uploader("Upload Image or Video", type=["jpg", "png", "mp4"])
target_lang = st.text_input("Target Language Code (e.g., 'hi' for Hindi)", value='hi')

def extract_text_from_image(img_path):
    image = cv2.imread(img_path)
    return pytesseract.image_to_string(image, lang='eng')

def extract_text_from_video(video_path):
    cap = cv2.VideoCapture(video_path)
    text = ""
    frame_count = 0
    while cap.isOpened() and frame_count < 5:
        ret, frame = cap.read()
        if not ret:
            break
        text += pytesseract.image_to_string(frame, lang='eng') + "\n"
        frame_count += 1
    cap.release()
    return text

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    if uploaded_file.type.startswith('image'):
        text = extract_text_from_image(tmp_path)
    elif uploaded_file.type.startswith('video'):
        text = extract_text_from_video(tmp_path)
    else:
        st.error("Unsupported file type")
        text = ""

    if text:
        words = [w for w in text.split() if w.isalpha()]
        english_text = " ".join(words)
        translated = translator.translate(english_text, dest=target_lang)
        st.subheader("Extracted English Text")
        st.write(english_text)
        st.subheader("Translated Text")
        st.write(translated.text)
    os.remove(tmp_path)