import ai
import json
import base64
import os
from PIL import Image
import io
import uuid

def aiImageMaker(userText, imgDir, pngFileName, imgCount=1):
    print("aiImageMaker")
    try:
        mykey = os.getenv("OPENAI_API_KEY")
        bot = ai.Bot(apikey=mykey)

        reply = bot.createImages(
            userText=userText,
            numImages=imgCount,
            imgSize=1024
        )

        prefix = "ai"
        
        if reply:
            with open('imagedata.json', 'w') as i:
                json.dump(reply, i, indent=4)

            imgDataList = reply["data"]
            countImages = len(imgDataList)
            print(f"NUm images: {countImages}")

            for i in range(countImages):
                b64image = imgDataList[i]["b64_json"]
                with open('b64code.txt','w') as f:
                    f.write(b64image)

                uid = str(uuid.uuid1())
                imgName = f"{prefix}_{uid}_{pngFileName}"
                imgbytes = base64.b64decode(b64image)
                buf = io.BytesIO(imgbytes)

                img = Image.open(buf)
                imgFilePath = os.path.join(imgDir, imgName)
                img.save(imgFilePath)


    except BaseException as e:
        print(f"Error: {e}")
        return False
    return True


def runImageBot():
    print("Welcome to Image AI Bot\n")
    print("====================\n")
    y='y'
    imgpath = "C:\\pix"
    count=0

    while y=='y':
        y=input("Do you want AI to make an image (y=yes, else no)? ")
        if y.strip() != 'y':
            break
        
        print("\n")
        x = input("Enter text to describe your image> ")
        with open('chathistory.txt', 'a') as h:
            h.write(f"User: {x}\n")

        n = input("How many images? ")
        numImgs = int(n)

        imgName=f"img{count}.png"

        ok = aiImageMaker(
            userText=x.strip(),
            imgDir=imgpath,
            pngFileName=imgName,
            imgCount=numImgs
        )

        out = "Image saved!" if ok else "Request failed!"
        print(out+"\n")

        count += 1

        print("====================\n")

    print("Have a nice day!")

runImageBot()