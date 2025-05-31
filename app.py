from dotenv import load_dotenv
import os
from openai import OpenAI
import gradio as gr
from pypdf import PdfReader
load_dotenv(override=True)

#Use Gemini or OpenAI API as per your preference
gemini = OpenAI(api_key=os.getenv("GOOGLE_API_KEY"), base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
model_name = "gemini-2.0-flash"

# openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url="https://api.openai.com/v1")


profile_path = "Your_LinkedIn_Profile.pdf"
with open(profile_path, "rb") as file:
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()

name = "Your Name"

system_prompt = f"You are acting as {name}. Your task is to answer questions related to {name}, his work, and his experience. " \
    f"Your responses should be based on the information provided in the PDF file. " \
    f"Your responsibility is to represent {name} for interactions on the website as faithfully as possible. \
You are given a summary of {name}'s background and LinkedIn profile which you can use to answer questions. \
Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
If you don't know the answer, say so."

system_prompt += text
system_prompt += "With this context, chat with the user and answer their questions, always staying in character. " \


def chat(message, history):
    formatted_history = []
    for user_msg, bot_reply in history:
        formatted_history.append({"role": "user", "content": user_msg})
        formatted_history.append({"role": "assistant", "content": bot_reply})

    messages = [{"role": "system", "content": system_prompt}] + formatted_history + [{"role": "user", "content": message}]
    
    response = gemini.chat.completions.create(
        model=model_name,
        messages=messages
    )
    
    return response.choices[0].message.content

gr.ChatInterface(
    fn=chat,
    title="Your Name's Chatbot",
    type="messages"
).launch()
