import urllib.request
import os

MODEL_URL = (
    "https://huggingface.co/TheBloke/DeepSeek-Coder-6.7B-Instruct-GGUF/"
    "resolve/main/deepseek-coder-6.7b-instruct.Q4_K_M.gguf"
)

MODEL_PATH = "models/deepseek-coder-6.7b-instruct.Q4_K_M.gguf"

os.makedirs("models", exist_ok=True)

print("⬇️ Downloading DeepSeek-Coder-6.7B GGUF model...")
urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
print("✅ Download complete. Model saved in models/")