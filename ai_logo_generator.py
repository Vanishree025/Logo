import streamlit as st
import requests
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="Free AI Logo Generator", page_icon="🤖")

st.title("🤖 Free AI Logo Generator")
st.write("Generate custom logos using AI with no downloads or GPU!")

prompt = st.text_input("Enter a description for your logo", placeholder="e.g. minimal robot head with neural pattern")
color = st.text_input("Optional color palette (e.g. blue, white, black)")

api_key = "7mBg8Nk94JqhLNYu9FKcS5U49XdNnlo5Cb3U1pDCIwYM94NPWPobH44FrGhW"  # Replace with your actual API key

if st.button("Generate Logo") and prompt:
    with st.spinner("Generating logo..."):
        full_prompt = f"{prompt}, logo, minimal, modern, vector-style"
        if color:
            full_prompt += f", colors: {color}"
        payload = {
            "key": api_key,
            "prompt": full_prompt,
            "negative_prompt": "text, watermark, blurry, extra lines",
            "width": "512",
            "height": "512",
            "samples": "1",
            "num_inference_steps": "25",
            "guidance_scale": 7.5
        }
        try:
            res = requests.post("https://modelslab.com/api/v6/realtime/text2img", json=payload)
            res.raise_for_status()
            data = res.json()
            if "output" in data:
                img_url = data["output"][0]
                img_data = requests.get(img_url).content
                image = Image.open(BytesIO(img_data))
                st.image(image, caption="Your AI-Generated Logo", use_container_width=True)
                st.download_button("Download Logo", img_data, "ai_logo.png", "image/png")
            else:
                st.error("Something went wrong. Please try again.")
        except Exception as e:
            st.error(f"API error: {e}")
