from dotenv import load_dotenv
from email.message import EmailMessage
import requests
import os
import smtplib
from langchain.chat_models import init_chat_model


load_dotenv()

REQUEST_URL = (
    "https://newsapi.org/v2/top-headlines?"
    "category=business&"
    "language=en&"
    "pageSize=8&"
    "sortBy=publishedAt&apiKey=" + os.getenv("NEWS_API_KEY")
)

def get_news_content():
    res = requests.get(
        REQUEST_URL,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    content = res.json()
    articles = content["articles"]

    # AI summary
    model = init_chat_model(
        model="gemini-3-flash-preview",
        model_provider="google-genai",
        api_key=os.getenv("GEMINI_API_KEY")
    )

    prompt = f"""
    You're a news summarizer.
    Write a short paragraph analyzing news articles.
    Write another short paragraph telling me how they affect the stock market.
    Here are the news articles:
    {articles}
    """

    response = model.invoke(prompt)
    return response.content[0]["text"]

def send_news_email(content):
    msg = EmailMessage()
    msg["Subject"] = "Daily News Summary"
    msg["From"] = os.getenv("GMAIL_ADDRESS")
    msg["To"] = os.getenv("GMAIL_ADDRESS")

    msg.set_content(content)

    with smtplib.SMTP(os.getenv("SMTP_HOST"), port=587) as connection:
        connection.starttls()
        connection.login(user=os.getenv("GMAIL_ADDRESS"), password=os.getenv("GMAIL_APP_PASSWORD"))
        connection.send_message(msg)


if __name__ == "__main__":
    news_content = get_news_content()
    send_news_email(news_content)