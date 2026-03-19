from langchain_huggingface import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

# text can be replcaed with the documents and the embed_query can be changed to embed_documents for multi line conversion
text = "delhi is the capital of India"

vector = embedding.embed_query(text)

print(str(vector))