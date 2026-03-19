from langchain_groq import ChatGroq
from dotenv import load_dotenv
 
load_dotenv()

chatBot = ChatGroq(model="llama-3.1-8b-instant", temperature = 0, max_completion_tokens=10) # temp controls the randomness of the models output ranges bw 0 to 2

result = chatBot.invoke("write a poem for cricket in 3 lines")

print("assistant > " + result.content)