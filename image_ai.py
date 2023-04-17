import ai
import json
import base64
import os
from PIL import Image
import io

def aiImageMaker(userText, imgDir, pngFileName):
    print("aiImageMaker")
    try:
        mykey = os.getenv("OPENAI_API_KEY")
        bot = ai.Bot(apikey=mykey)

        reply = bot.createImages(
            userText=userText,
            numImages=1,
            imgSize=1024
        )

        if reply:
            with open('imagedata.json', 'w') as i:
                json.dump(reply, i, indent=4)

            imgDataList = reply["data"]
            countImages = len(imgDataList)
            print(f"NUm images: {countImages}")
            b64image = imgDataList[0]["b64_json"]
            with open('b64code.txt','w') as f:
                f.write(b64image)

            imgbytes = base64.b64decode(b64image)
            buf = io.BytesIO(imgbytes)

            img = Image.open(buf)
            imgFilePath = os.path.join(imgDir, pngFileName)
            img.save(imgFilePath)

    except BaseException as e:
        print(f"Error: {e}")
        return False
    return True


def runImageBot():
    print("Welcome to Image AI Bot\n")
    y='y'
    imgpath = "C:\\pix"
    count=0

    while y=='y':
        y=input("Do you want AI to make an image (y=yes, else no)?")
        if y.strip() != 'y':
            break

        x = input("Enter text to describe your image> ")

        imgName=f"ai_img{count}.png"

        ok = aiImageMaker(
            userText=x.strip(),
            imgDir=imgpath,
            pngFileName=imgName
        )

        out = "Image saved!" if ok else "Request failed!"

    print("Have a nice day!")

runImageBot()