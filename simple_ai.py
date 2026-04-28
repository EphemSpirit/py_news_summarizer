from dotenv import load_dotenv
import os
from langchain.chat_models import init_chat_model

load_dotenv()

model = init_chat_model(
    model="gemini-3-flash-preview",
    model_provider="google-genai",
    api_key=os.getenv("GEMINI_API_KEY")
)

response = model.invoke("How are you?")
response_str = response.content[0]["text"]
