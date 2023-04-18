import ai
import json
import base64
import os
from PIL import Image
import io
import uuid

def doUserImageEdit(userText, imgDir, pngFileIn, pngFileOut, 
                    imgSize=1024, imgCount=1):
    print("doUserImageEdit")
    try:
        mykey = os.getenv("OPENAI_API_KEY")
        bot = ai.Bot(apikey=mykey)

        reply = bot.editAnImage(
            originalImage=pngFileIn,
            userText=userText,
            numImages=imgCount,
            imgSize=imgSize
        )

        prefix = "ai_edit_"
        
        if reply:
            with open('imageedit.json', 'w') as i:
                json.dump(reply, i, indent=4)

            imgDataList = reply["data"]
            countImages = len(imgDataList)
            print(f"NUm images: {countImages}")

            for i in range(countImages):
                b64image = imgDataList[i]["b64_json"]
                with open('b64code.txt','w') as f:
                    f.write(b64image)

                uid = str(uuid.uuid1())
                imgName = f"{prefix}_{uid}_{pngFileOut}"
                imgbytes = base64.b64decode(b64image)
                buf = io.BytesIO(imgbytes)

                img = Image.open(buf)
                imgFilePath = os.path.join(imgDir, imgName)
                img.save(imgFilePath)


    except BaseException as e:
        print(f"Error: {e}")
        return False
    return True

def runEditBot():
    print("runEditBot")
    imgpath = "C:\\pix"
    pngFile = 'road.PNG'
    pngpath = os.path.join(imgpath, pngFile)

    img = Image.open(pngpath)
    w=img.width
    h=img.height

    srcImagePath = pngpath
    if w!=h:
        sz = max([w,h])
        squareImage = img.resize((sz,sz))
        newImgPath = os.path.join(imgpath, 'squareImage.png')
        squareImage.save(newImgPath)
        srcImagePath = newImgPath


    instructions = 'draw a red sports car on the road'
    res = doUserImageEdit(
        userText=instructions,
        imgDir=imgpath,
        pngFileIn=srcImagePath,
        pngFileOut='result.png',
        imgSize=1024,
        imgCount=1
    )

    print(f"Edit Image OK? {res}")

runEditBot()
