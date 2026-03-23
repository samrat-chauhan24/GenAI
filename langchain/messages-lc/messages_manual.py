from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

model = ChatGroq(model="llama-3.1-8b-instant")

# here i wrote the functionality for the chat history but langchain identified this problem and gave us diffenrent types of classes for messages
chat_history = [
    {
        "role" : "system",
        "content": "you are a helper personal assistant you have to answer every question user asks"
    }
]

while True:
    user_input = input("You > ")
    if user_input == "/exit":
        break
    
    chat_history.append(
        {
        "role": "user",
        "content": user_input
        }
    )
    
    result = model.invoke(chat_history)
    print("assistant > ", result.content)

    chat_history.append(
        {
        "role": "assistant",
        "content": result.content
        }
    )

if len(chat_history) > 15:
    chat_history = [chat_history[0]] + chat_history[-10:]