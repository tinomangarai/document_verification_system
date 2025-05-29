import streamlit as st
from PIL import Image
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub

# Load a pre-trained EfficientNet model from TensorFlow Hub
model_url = "https://tfhub.dev/google/imagenet/efficientnet/b7/classification/5"
model = tf.keras.Sequential([
    hub.KerasLayer(model_url, input_shape=(224, 224, 3))
])

st.set_page_config(page_title="Document Fog Detection", layout="centered")
st.title("🔍 Document Fog Detection")
st.markdown("Upload an image to check if it's **Fogged or Clear**.")

uploaded_file = st.file_uploader("📄 Upload Document Image", type=["png", "jpg", "jpeg"])

def preprocess_image(image):
    image = image.resize((224, 224))  # Resize for EfficientNet input
    image_array = np.array(image) / 255.0  # Normalize the image
    return np.expand_dims(image_array, axis=0)  # Add batch dimension

def predict_fog(image):
    processed_image = preprocess_image(image)
    prediction = model.predict(processed_image)
    return prediction[0]  # Return the prediction probabilities

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Document", use_column_width=True)

    with st.spinner("🔍 Analyzing..."):
        prediction = predict_fog(image)
        label = "Fogged Document" if prediction[0] > 0.5 else "Clear Document"
        confidence = prediction[0] if prediction[0] > 0.5 else 1 - prediction[0]

    st.subheader("✅ Detection Result")
    st.success(f"**Result:** {label} (Confidence: {confidence:.2f})")
