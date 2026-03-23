from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# message placeholder is used to load/inject dynamic chat history into the prompt

# it is required for chat apps, otheriwise there is no use of dyanmic messages and prompts in simple api call chatbots (this is my thinking)

# chat template
chat_template = ChatPromptTemplate([
    ('system', "you're a helpful customer support agent"),
    # here in between the placeholder will be created
    MessagesPlaceholder(variable_name='chat_history'),
    ('human', "{query}")
])

# now we'll load the chat history from the database and for practices from a text file
chat_history = []
with open('messages-lc/chat_history.txt') as f:
    chat_history.extend(f.readlines())

# create the prompt
# therefore my todays query will have all the history from before.
prompt = chat_template.invoke({'chat_history':chat_history, 'query': "what is the update of my refund"})

print(prompt)