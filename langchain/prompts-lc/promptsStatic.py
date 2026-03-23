# today we'll learn text based prompts
# this is the eg of static prompts
# as we know, models are very sensitive to prompts, therefore in static prompts the whole power is with the user which is not good for the app/chatbot

from langchain_groq import ChatGroq
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

st.header("ChatBot")
user_input = st.text_input("Enter Your Prompt")


chatBot = ChatGroq(model="llama-3.1-8b-instant")

if st.button("send"):
    result = chatBot.invoke(user_input)
    st.write(result.content)


