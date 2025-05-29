import streamlit as st
from PIL import Image
import pytesseract
import numpy as np
import cv2
import io

st.set_page_config(page_title="Utility Bill Verification", layout="centered")
st.title("🔍 Utility Bill Verifier")
st.markdown("Upload a scanned or photographed utility bill to check if it's **Real or Fake**.")

uploaded_file = st.file_uploader("📄 Upload Utility Bill Image", type=["png", "jpg", "jpeg"])

def extract_text(image):
    return pytesseract.image_to_string(image)

def detect_forgery(image_pil, extracted_text):
    image_cv = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)
    edges = cv2.Canny(image_cv, 100, 200)
    edge_density = np.sum(edges > 0) / edges.size

    if edge_density < 0.01:
        return True, "Low edge density — may indicate excessive editing or fake scan."

    required_keywords = ["electricity", "account", "meter", "bill", "customer"]
    found_keywords = [kw for kw in required_keywords if kw in extracted_text.lower()]

    if len(found_keywords) < 2:
        return True, f"Missing key utility terms — found: {', '.join(found_keywords) or 'none'}"

    return False, "Document appears legitimate."

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Utility Bill", use_column_width=True)

    with st.spinner("🔍 Analyzing the document..."):
        text = extract_text(image)
        is_fake, reason = detect_forgery(image, text)

    st.subheader("📄 Extracted Text")
    st.text(text)

    st.subheader("✅ Verification Result")
    if is_fake:
        st.error("❌ FAKE DOCUMENT DETECTED")
    else:
        st.success("✅ DOCUMENT APPEARS REAL")

    st.markdown(f"**Reason:** {reason}")
