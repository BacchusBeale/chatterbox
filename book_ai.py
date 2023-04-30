import ai
import image_ai
import os
import fpdf
from PyPDF2 import PdfReader, PdfWriter

def addIllustratedPage(bookPdfFile, text, pngImageFile, isNewBook):
    print("addIllustratedPage")
    book = fpdf.FPDF()
    book.add_page(orientation="L")
    book.set_font('Arial', 'B', 16)
    book.cell(
        w=0,
        h=0,
        txt=text
    )

    book.ln(h=2)
    book.image(name=pngImageFile)

    pdfPage = book.output()

    existingPages = None
    numPages = 0
    
    if not isNewBook:
        reader = PdfReader(bookPdfFile)
        numPages = reader.getNumPages()
        print(f"num pages: {numPages}")
        existingPages = reader.pages

    writer = PdfWriter(bookPdfFile)
    for page in existingPages:
        writer.add_page(page)

    writer.add_page(pdfPage)
    writer.write(pdfPage)

def saveLog(text, logFile="book.log", overwrite=False):
    mode='a'
    if overwrite:
        mode='w'
        
    with open(logFile, mode=mode) as log:
        log.write(text+"\n")

def bookmaker():
    bookDir="./book"
    print("Welcome, to Book Maker!\n=========\n")
    y = input("Start writing a new book (y/n)? ")
    if y!='y':
        print("Have a nice day!")
        exit(0)

    log="./book/demo.log"

    fileName = input("Enter file name: ")
    fileName += ".pdf"
    saveLog(fileName, logFile=log, overwrite=True)
    bookTitle = input("Enter the book title: ")
    saveLog(bookTitle, logFile=log, overwrite=False)
    bookDescription = input("Type a description: ")
    saveLog(bookDescription, logFile=log, overwrite=False)
    yourCharacter = input("Type your character name: ")
    saveLog(yourCharacter, logFile=log, overwrite=False)
    botsCharacter = input("Type bot's chararcter name: ")
    saveLog(botsCharacter, logFile=log, overwrite=False)
    serverInstruction = f"Assistant please, write dialogue for {botsCharacter}, given the current story."
    saveLog(serverInstruction, logFile=log, overwrite=False)
    illustratorInstruction = "Draw an Illustration for this page. "
    saveLog(illustratorInstruction, logFile=log, overwrite=False)
    bookPath = os.path.join(bookDir, fileName)
    print(f"Creating {bookPath}")
    pageNum=0

    pngImageName = f"illustration{pageNum}.png"
    saveLog(pngImageName, logFile=log, overwrite=False)
    print(f"Make image: {pngImageName}")
    # make book cover
    image_ai.aiImageMaker(
        userText=f"{bookTitle}. {bookDescription}",
        imgDir=bookDir,
        pngFileName=pngImageName,
        imgSize=256,
        imgCount=1
    )

    addIllustratedPage(
        bookPdfFile=bookPath,
        text=bookTitle,
        pngImageFile=pngImageName,
        isNewBook=True
    )

    # mykey = os.getenv("OPENAI_API_KEY")
    # bot = ai.Bot(apikey=mykey)

    # userText=[]
    # botText=[]
    # y = 'y'
    # while y=='y':
    #     y=input("Add another page (y/n)? ")
    #     if y!='y':
    #         print("Book complete!")
    #         exit(0)

        


bookmaker()

