from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

model = ChatGroq(model="llama-3.1-8b-instant")

# human message -> user message
# ai message -> replty from model to the user is known as ai message
# system message -> it is basically an intstructon to control the model behavior

# these are static messages

messages = [
    SystemMessage(content="you are an helpful assistant")
]

while True:
    user_input = input("You > ")
    if user_input.lower().strip() == "/exit":
        
        break
    
    messages.append(HumanMessage(content=user_input))
    
    result = model.invoke(messages)
    assistant_reply = result.content
    print("assistant > ", assistant_reply)
    
    messages.append(AIMessage(content=assistant_reply))

    if len(messages) > 15:
        messages = [messages[0]] + messages[-10:]
print("-" * 80)
for msg in messages:
    print(f"{msg.type}: {msg.content}")

