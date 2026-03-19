from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv

load_dotenv()

# using endpoint we have to call/access the model from the HF library
llm = HuggingFaceEndpoint(
    repo_id= "MiniMaxAI/MiniMax-M2.5",
    task="text-generation"
)

model = ChatHuggingFace(llm = llm)

result = model.invoke("what is capital of india")

print(result.content)