from openai import OpenAI
from calculate_calori.prompts import sys_prompts
from calculate_calori.schemas import parse_sonuc
import base64
import mimetypes
import os
import dotenv
dotenv.load_dotenv()

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY", ""),
)


input_text = "Bu fotoğraftaki yemeğin kalorisini hesapla."

def generate_image(image_path, description=""):
    if not image_path:
        return "Lütfen bir yemek fotoğrafı yükleyin."

    mime = mimetypes.guess_type(image_path)[0] or "image/jpeg"
    with open(image_path, "rb") as f:
        data_url = f"data:{mime};base64,{base64.b64encode(f.read()).decode()}"

    if not os.getenv("GROQ_API_KEY"):
        return "API hatası: .env dosyasında GROQ_API_KEY bulunamadı."

    try:
        response = client.responses.create(
            model="qwen/qwen3.8-27b",
            instructions=sys_prompts,
            input=[
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": description or input_text},
                        {"type": "input_image", "image_url": data_url},
                    ],
                }
            ],
        )
    except Exception as e:
        return f"API hatası: {e}"

    if response.status == "failed":
        return f"API hatası: {response.error.message if response.error else 'bilinmeyen hata'}"
    text = response.output_text
    if not text:
        return "Model boş yanıt döndürdü."
    sonuc = parse_sonuc(text)
    return sonuc.to_markdown() if sonuc else text