import requests
import openai
import os
import json

class ChatMessage():
    SYSTEM_ROLE="system"
    ASSISTANT_ROLE="assistant"
    USER_ROLE="user"
    def __init__(self) -> None:
        self.role=""
        self.content=""
    
    def toDict(self):
        msg = {
            "role":self.role,
            "content":self.content
        }
        return msg

class ChatBot():
    def __init__(self) -> None:
        self.apikey = os.getenv('OPENAI_API_KEY')
        self.success=False
        self.lastError=''

    def clearError(self):
        self.success=True
        self.lastError=''
        
    def doChatCompletion(self,
                         messages=[],
                         modelName="gpt-4",
                         temperature=1.0,
                         maxTokens=2048,
                         numCompletions=1):
        print("doChatCompletion")
        self.clearError()
        response={}
        try:

            openai.api_key = self.apikey
            response = openai.ChatCompletion.create(
                model=modelName,
                messages=messages,
                temperature=temperature,
                max_tokens=maxTokens,
                n=numCompletions
            )
            
        except BaseException as e:
            self.lastError=f"Bot error: {e}"
            print(self.lastError)
            self.success=False
        return response
        

    def getModelList(self):
        print("getModelList")
        self.clearError()
        modelList=[]
        try:
            openai.api_key = self.apikey
            modelList = openai.Model.list()
        except BaseException as e:
            self.lastError=f"Bot error: {e}"
            print(self.lastError)
            self.success=False
        return modelList

def getChatModels():
    bot = ChatBot()
    reply = bot.getModelList()
    modelData = {
        "models": reply["data"]
    }
    numModels = len(reply)
    print(f"Num models: {numModels}")
    json.dumps(modelData, indent=4)
    with open('models.json', 'w') as f:
        
        json.dump(modelData, f, indent=4)


# getChatModels()

# https://platform.openai.com/docs/models/model-endpoint-compatibility

def runChatCompletion():
    bot = ChatBot()
    modelGpt4 = "gpt-4"

    modelGpt3 = 'gpt-3.5-turbo-0301'
    #completionId="text-davinci-edit-003"
    
    temp=1
    numTokens=2048
    numCompletions=1

    talkToBot = True
    x = input("Enter text for completion \nEnter q to quit\n\nTalk to bot (y/n)?")
    talkToBot = (x.strip()=='y')
    chatHistory=''
    while talkToBot:
        print('\n')
        userInput = input("user input>")
        if userInput.strip()=="q":
            break

        msgList = []
        msgsys = ChatMessage()
        msgsys.content = "Please assistant, answer the user's question."
        msgsys.role = ChatMessage.SYSTEM_ROLE
        msgList.append(msgsys.toDict())

        msg = ChatMessage()
        msg.content = userInput
        chatHistory += msg.content+'\n'
        msg.role = ChatMessage.USER_ROLE
        msgList.append(msg.toDict())
        
        with open('chathistory.txt', 'a') as h:
            h.write(f"User: {userInput}\n")

        botReply = bot.doChatCompletion(
            messages=msgList,
            modelName=modelGpt3,
            temperature=temp,
            maxTokens=numTokens,
            numCompletions=numCompletions
        )

        if botReply:
            print(f"bot:")
            answers = botReply["choices"]
            numAnswers=len(answers)
            print(f"Num answers: {numAnswers}")
            for a in answers:
                m=a["message"]
                botMsg = ChatMessage()
                botMsg.role=m["role"]
                botMsg.content=m["content"]
                out = f"{botMsg.role}: {botMsg.content}"
                print(out+"\n")
                with open('chathistory.txt', 'a') as h:
                    h.write(f"{out}\n")
            

    print("\n\nGoodbye, have a nice day!\n")

runChatCompletion()
