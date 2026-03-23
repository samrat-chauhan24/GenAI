from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

model = ChatGroq(model="llama-3.1-8b-instant")

# we're trying to make the messages dyanamic
# chat prompt template is not exactly similar to the prompt template
# if we want to use dynamic messages the classes will not work, so we use other syntax
chat_template = ChatPromptTemplate([
    ('system', "you are a {domain} expert with 20 years for expierence"),
    ('human', "explain this {topic} in simple terms")
    # SystemMessage(content="you are a {domain} expert with 20 years for expierence"),
    # HumanMessage(content="explain this {topic} in simple terms")
])

prompt = chat_template.invoke({'domain':'cricket', 'topic':'NO Ball'})

print(prompt)
 
# generally prompt templates are used for single turn messages
# and chat prompt templates are used for multi turn convo messages