import openai
import os
import json

CHAT_MODEL_GPT4 = 'gpt-4' # does not exist
CHAT_MODEL_GPT35_TURBO = 'gpt-3.5-turbo'
EDIT_MODEL_DAVINCI = 'text-davinci-edit-001'
AUDIO_MODEL_WHISPER = 'whisper-1'

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

class Bot():
    SYSTEM_ROLE="system"
    ASSISTANT_ROLE="assistant"
    USER_ROLE="user"
    def __init__(self, apikey) -> None:
        self.apikey=apikey
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
    
    def createImages(self,
                      userText,
                      numImages=1,
                      imgSize=1024):
        response={}
        try:

            openai.api_key = self.apikey
            response = openai.Image.create(
                prompt=userText,
                n=numImages,
                size=f"{imgSize}x{imgSize}",
                response_format="b64_json"
            )
            
        except BaseException as e:
            self.lastError=f"Bot error: {e}"
            print(self.lastError)
            self.success=False
        return response
    
    def editAnImage(self,
                    originalImage,
                    userText,
                    numImages=1,
                    imgSize=1024):
        response={}
        try:

            openai.api_key = self.apikey
            response = openai.Image.create(
                image=open(originalImage, 'rb'),
                prompt=userText,
                n=numImages,
                size=f"{imgSize}x{imgSize}",
                response_format="b64_json"
            )
            
        except BaseException as e:
            self.lastError=f"Bot error: {e}"
            print(self.lastError)
            self.success=False
        return response