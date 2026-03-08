import os as os
import time
from groq import Groq
from datetime import datetime

# creating a log file
if not os.path.exists("chat_logs"):
    os.makedirs("chat_logs")
timeStamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
logFile = f"chat_logs/session_{timeStamp}.txt"


# helper function for adding user assistant messages to the file
def write_log(text):
    with open(logFile, "a", encoding="utf-8") as f:
        f.write(text + "\n")
write_log("===== NEW CHAT SESSION =====")

def logUser(userInput):
    write_log(f"USER : {userInput}")

def logAssistant(userInput):
    write_log(f"ASSISTANT : {userInput}")

# this is the api key it is exported in the terminal
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# let's write some lines that will help, to choose behavior
userChoosenBehavior = input("choose Ai Mode : " \
"friendly, strict, normal -> ")

# defining temp globally to add dyanamic tmep control
temperature = 0.7

def chooseMode(mode):
    if mode == "normal":
        return  """
            You are an expert AI assistant.
            - Give clear and structured answers.
            - Use simple language unless asked for advanced.
            - If the question is unclear, ask for clarification.
            - Stay focused on the topic.
            - Do not hallucinate unknown facts."""
    
    elif mode == "strict":
        return  """You are a strict, concise AI tutor. Only give short direct answers.""" 
    
    elif mode == "friendly": return "You are a helpful and a friendly AI assistant, that speaks to user like friends"
    
    else: return "you are a helpful ai assistant"

# this message goes in with the user message, again and again so the chatbot doesn't loose the context  
systemPrompt = chooseMode(userChoosenBehavior.lower().strip())
modelNames = ["llama-3.1-8b-instant"] 
messages=[
    {
        "role":"system",
        "content": systemPrompt          
    }        
]

print("-> The Chatbot is ready, type 'exit' to quit.\n")
print(f"-> Current Mode is : {userChoosenBehavior}\n")
print(f"-> Model : {modelNames[0]}\n")
# history function
def showHistory():
    print("Conversation History")
    print("-" * 40)
    for msg in messages:
        role = msg["role"]
        if role == "system":
            continue
        content = msg["content"]
        print(f"{role.upper()} : {content}")

#stats function
def showStats():
    print("Chat Stats")
    print("-" * 40)
    lenOfMess = len(messages)
    print(f"Messages in memory : {lenOfMess}")
    print(f"Temperature : {temperature}")
    print(f"Current Mode is : {userChoosenBehavior}")
    print(f"Model : {modelNames[0]}\n")

# a helper function to handle user commands
def handleUserCommands(userInput):
    userInput = userInput.lower().strip()
    global messages
    global temperature
    global systemPrompt
    # exit
    if userInput == "exit":
        print("Chat Ended")
        exit()
    
    # clear
    if userInput == "/clear":
        
        messages = [messages[0]]
        print("Conversation Cleared")
        return True
    # help command
    if userInput == "/help":
        print("""
            Available Commands
            ------------------

            /help           -> Show all available commands
            /mode <mode>    -> Change AI mode (friendly | normal | strict)
            /temp <value>   -> Set temperature (0.0 - 2.0)
            /clear          -> Clear conversation memory
            /history        -> Show conversation history
            /stats          -> Shows the Chat Stats
            /exit           -> Exit chatbot

            Example:
                /mode friendly
                /temp 0.8
            """)
        return True
    
    # change mode
    if userInput.startswith("/mode"):
        parts = userInput.split()
        validModes = ["friendly", "normal", "strict"]
        if len(parts) != 2:
            
            print("Valid Modes are: /mode friendly | strict | normal")
            return True
        
        newMode = parts[1]
        if newMode not in validModes:
            print(f"{newMode} is not a valid mode")
            return True
        
        
        systemPrompt = chooseMode(newMode)
        
        
        messages[0] = {
            "role": "system",
            "content" : systemPrompt
        }
        
        messages = [messages[0]]
        print(f"Mode swtiched to: {newMode}\n")
        return True
    
    #dynamic temperature control
    if userInput.startswith("/temp"):
        partOfTemp = userInput.split()
        if(len(partOfTemp) != 2):
            print("kindly enter the temp is this format -> /temp 0.2 | /temp 0.5 | /temp 1.1")
            return True
        
        try:
            newTemp = float(partOfTemp[1])
            if not 0 <= newTemp < 2.0:
                print("The temperature must be between 0 - 2.0")
                return True
            
            temperature = newTemp
            print(f"The temperature is set to: {temperature}")
        
        except ValueError:
            print("The temperature must be a number")
        
        return True
    
    # Conversation history 
    if userInput =="/history":
        showHistory()
        return True
    
    # show stats
    if userInput == "/stats":
        showStats()
        return True


# for the chat looping, so the program doesn't end after giving one answer
while True:
    userInput = input("You > ")
    
    if handleUserCommands(userInput):
        continue
    
    logUser(userInput)

    # this is added in the messages list
    messages.append( 
        {
            "role":"user",
            "content": userInput
        }
    )
    # the response is stored here
    response = client.chat.completions.create(
    model=modelNames[0],
    messages=messages,# as the messages is define globally
    temperature=temperature,
    stream=True
    )

    assistantReply = "" 
    print("Ai > ", end="", flush=True)
    for i in response: # as deltas are created, a loop must be run to print again and again
        deltaStr = ""
        delta = i.choices[0].delta
        if delta and delta.content: # deltas can be null too.
            deltaStr = delta.content
            assistantReply += deltaStr
            print(deltaStr, end="", flush=True)
            time.sleep(0.05)
    print("\n")
    logAssistant(assistantReply)
    write_log("-" * 40)
    
    messages.append(
        {
            "role": "assistant",
            "content": assistantReply
        }
    )

    # this is sliding window function, to prevent excedding model's max token limit
    if len(messages)>12:
        messages= [messages[0]] + messages[-10:]




    # trying to do streaming output
    # print("Ai: ", assistantReply)
    # newTotalTokens = newTotalTokens + response.usage.total_tokens
    # print("tokensThis Call", response.usage.total_tokens)
    # print("totalTime", response.usage.total_time)
    # print("cumalativeTokens: ", newTotalTokens)