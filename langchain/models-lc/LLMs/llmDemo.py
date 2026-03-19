# this is the llm integration, and it is not trendy now a days
from langchain_groq import ChatGroq # can simply install any other library , as there no support for old models basic llm class is not here
from dotenv import load_dotenv # loads environment variables from .env file into system env

load_dotenv()

llm = ChatGroq(model="llama-3.1-8b-instant") # created object and stored in llm variable

result = llm.invoke("what is the capital of india") # used to interact with the model, it sends as well as receives

print("assistant > " + result.content)