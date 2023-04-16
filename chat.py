import ai
import os

# https://platform.openai.com/docs/models/model-endpoint-compatibility

def runChatCompletion():
    mykey = os.getenv("OPENAI_API_KEY")
    bot = ai.Bot(apikey=mykey)
    modelGpt4 = ai.CHAT_MODEL_GPT35_TURBO

    temp=1
    numTokens=2048
    numCompletions=1

    talkToBot = True
    x = input("Enter text for completion \nTalk to bot (y/n)?")
    menu = [
        "1. Please assistant, answer the user's question.",
        "2. Please assistant, write a poem about...",
        "3. Hello assistant, please solve this...",
        '4. Other (you enter assistant prompt)',
        "Else exit!"
    ]

    valid=['1','2', '3', '4']
    talkToBot = (x.strip()=='y')
    chatHistory=''
    while talkToBot:
        msgList = []

        msgsys = ai.ChatMessage()

        option = input("\n".join(menu))
        if option.strip() in valid:
            index = int(option)-1
            if index>=0 and index<=3:
                msgsys.content = menu[index]
            else:
                sysText = input("Enter system instructions")
                msgsys.content = sysText

            msgsys.role = ai.ChatMessage.SYSTEM_ROLE
            msgList.append(msgsys.toDict())
        else:
            break

        print('\n')
        userInput = input("user query>")
        
        msg = ai.ChatMessage()
        msg.content = userInput
        chatHistory += msg.content+'\n'
        msg.role = ai.ChatMessage.USER_ROLE
        msgList.append(msg.toDict())
        
        with open('chathistory.txt', 'a') as h:
            h.write(f"User: {userInput}\n")

        botReply = bot.doChatCompletion(
            messages=msgList,
            modelName=modelGpt4,
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
                botMsg = ai.ChatMessage()
                botMsg.role=m["role"]
                botMsg.content=m["content"]
                out = f"{botMsg.role}: {botMsg.content}"
                print(out+"\n")
                with open('chathistory.txt', 'a') as h:
                    h.write(f"{out}\n")
            

    print("\n\nGoodbye, have a nice day!\n")

runChatCompletion()
