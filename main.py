# Main Program ICOS

#VENV
#Create
    #python -m venv ICOSenv
#Activate
    #ICOSenv\Scripts\activate
#upgrade
    #pip install --upgrade pip

#Import packages
from tkinter import *
import math
#from PIL import Image, ImageTk

#Import custom libraries
from libraries.libraryDebugger import *
from libraries.libraryFiles import *
from libraries.libraryCalculations import *

#Control Variables
global mainPath
mainPath = getPath()
categoriesPath = mainPath+"\Categories"
categories = getFolders(categoriesPath)
categories.sort()
conceptsPath = categoriesPath+"\\"+categories[0]
concepts = getImages(conceptsPath)

#Configurations
configMain = readJSON(mainPath,"config.json")
    #rows, columns, gap, bgColor, txtColor, bgtxtColor, imgColor
configSentence = readJSON(mainPath,"configSentences.json")
    #width, height, concepts, gap, bgColor, txtColor, bgtxtColor, imgColor
#configCategories = getJSONs(categoriesPath,categories)
    #rows, columns, gap, bgColor, txtColor, bgtxtColor, imgColor

#Actual States
global statesActual
statesActual = readJSON(mainPath,"actualStates.json")

#Print categories
"""
printList("Categories:",listNames(categories))
"""

#Print concepts
"""
for category in categories:
    conceptsPath = categoriesPath+category
    printList("Concepts of "+str(getName(category))+":",listNames(getImages(conceptsPath)))
"""

#Start
root=Tk()
root.title("ICOS (Interactive COncept Simplifier)")
root.attributes("-fullscreen", True)

gW = root.winfo_screenwidth()
gH = root.winfo_screenheight()

disp = IntVar()
disp.set(statesActual["actualIndex"])
sentenceDist = IntVar()
sentenceDist.set(redim(configSentence["height"],gH))

def close_window(_event):
    root.destroy()

def onWords(event):
    global statesActual
    global mainPath
    x = event.x
    y = event.y
    if statesActual["actualPage"] != "main" and isOnBack(y,sentenceDist.get()):
        disp.set(0)
        createConcepts("main")
    else:
        if positionX(y,sentenceDist.get(),root.winfo_screenheight())=="Up":
            if disp.get()>0:
                disp.set(disp.get()-1)
                createConcepts(statesActual["actualPage"])
        else:
            print(statesActual["actualIndex"])
            if statesActual["actualMax"]>=disp.get()+1:
                disp.set(disp.get()+1)
                createConcepts(statesActual["actualPage"])

def resetSentence():
    global statesActual
    statesActual["words"] = 0
    statesActual["ConceptDirections"] = []
    statesActual["ActualConcepts"] = []
    for i in range(statesActual["Concepts"]):
        statesActual["ConceptDirections"].append("\\")
        statesActual["ActualConcepts"].append("Invalid.png")
    writeJSON(mainPath,"actualStates.json",statesActual)
    loadSentence()

def loadSentence():
    global SentencesImg
    global SentenceConcepts
    global statesActual
    SentencesImg = []
    SentenceConcepts = []
    for i in range(statesActual["Concepts"]):
        SentencesImg.append(PhotoImage(file=mainPath+statesActual["ConceptDirections"][i]+statesActual["ActualConcepts"][i]))
        SentenceConcepts.append(Button(Sentence, text=getName(statesActual["ActualConcepts"][i]), image= SentencesImg[i], \
                            width=redim((configSentence["width"]-2*configSentence["gapW"])/nSentence,gW), \
                            height=redim((configSentence["height"]-2*configSentence["gapH"]),gH), compound=TOP, \
                            bd= -2, command=lambda n1=i:btnSentence(n1)))
        SentenceConcepts[i].place(x=redim(configSentence["gapW"],gW)+redim((configSentence["width"]-2*\
                                configSentence["gapW"])/nSentence,gW)*i,y=redim(configSentence["gapH"],gH))



def onSentence(event):
    x = event.x
    y = event.y
    resetSentence()
    #print("onSentence, x: "+str(x)+", y: "+str(y))

def btnSentence(id):
    print("entro")
    global statesActual
    if statesActual["words"]>0:
        print("Tambien")
        statesActual["words"] = statesActual["words"]-1
        statesActual["ConceptDirections"][statesActual["words"]] = "\\"
        statesActual["ActualConcepts"][statesActual["words"]] = "Invalid.png"
        writeJSON(mainPath,"actualStates.json",statesActual)
        loadSentence()
    
def btnConcept(page,id):
    global statesActual

    if page=="main":
        disp.set(0)
        createConcepts(id)
    else:
        if statesActual["words"]<statesActual["Concepts"]:
            statesActual["ConceptDirections"][statesActual["words"]] = "\\Categories\\"+page+"\\"
            statesActual["ActualConcepts"][statesActual["words"]] = id
            statesActual["words"] = statesActual["words"]+1
            writeJSON(mainPath,"actualStates.json",statesActual)
            loadSentence()

def createConcepts(page):
    if page=="main":
        creationData = readJSON(mainPath,"config.json")
    else:
        creationData = readJSON(categoriesPath,page+"\\config.json")

    global conceptImg
    global conceptBtn
    global concepttxtBtn
    global statesActual

    conceptImg = []
    conceptBtn = []
    concepttxtBtn = []
    for r in range(creationData["rows"]):
        for c in range(creationData["columns"]):
            i = r*creationData["columns"]+c
            ind = creationData["rows"]*creationData["columns"]*disp.get()+i
            if page=="main":
                concepts = categories
            else:
                conceptsPath = categoriesPath+"\\"+page
                concepts = getImages(conceptsPath)
            if len(concepts)>ind:
                if page=="main":
                    conceptsPath = categoriesPath+"\\"+categories[ind]
                    dat = getImages(conceptsPath)
                    conceptImg.append(PhotoImage(file=conceptsPath+"\\"+dat[0]))
                    concepttxtBtn.append(categories[ind])
                else:
                    conceptImg.append(PhotoImage(file=conceptsPath+"\\"+concepts[ind]))
                    concepttxtBtn.append(concepts[ind])
            else:
                conceptImg.append(PhotoImage(file=mainPath+"\Invalid.png"))
                concepttxtBtn.append("")
            conceptBtn.append(Button(Words, text=getName(concepttxtBtn[i]), image=conceptImg[i], \
                            width=redim((creationData["width"]-(1+creationData["columns"])*creationData["gapW"])/creationData["columns"],gW), \
                            height=redim((creationData["height"]-configSentence["height"]-(2+creationData["rows"])*creationData["gapH"])\
                            /creationData["rows"],gH), compound=TOP, bd= -2, command=lambda txt=concepttxtBtn[i]:btnConcept(page,txt)))
            conceptBtn[i].place(x=redim(creationData["gapW"]+(creationData["width"]-(1+creationData["columns"])*\
                            creationData["gapW"])*c/creationData["columns"]+creationData["gapW"]*(c),gW),y=redim(configSentence["height"]+\
                            creationData["gapH"]*(r+1)+(creationData["height"]-configSentence["height"]-(2+creationData["rows"])*\
                            creationData["gapH"])*r/creationData["rows"],gH))
    
    statesActual["actualIndex"] = disp.get()
    statesActual["actualPage"] = page
    statesActual["actualMax"] = math.ceil(len(concepts)/(creationData["rows"]*creationData["columns"]))-1
    writeJSON(mainPath,"actualStates.json",statesActual)


#Main frames
Words = Frame(root, bg=configMain["bgColor"], width=gW, height=gH)
Words.pack() #Start of the Principal Frame with the first Flange Color
Sentence = Frame(root, bg=configSentence["bgColor"], width=redim(configSentence["width"],gW),\
                 height=redim(configSentence["height"],gH))
Sentence.place(x=redim(1-float(configSentence["width"]),gW),y=0)#Start the part of the sentences

#Create Concepts
nSentence = int(configSentence["concepts"])
if nSentence != int(statesActual["Concepts"]):
    statesActual["Concepts"] = nSentence
    writeJSON(mainPath,"actualStates.json",statesActual)
    resetSentence()

global SentencesImg
global SentenceConcepts
SentencesImg = []
SentenceConcepts = []

loadSentence()


global conceptImg
global conceptBtn
global concepttxtBtn
conceptImg = []
conceptBtn = []
concepttxtBtn = []

disp.set(0)
createConcepts(statesActual["actualPage"])
#createConcepts("main")

root.bind('<Escape>', close_window)
Words.bind("<1>", onWords)
Sentence.bind("<1>", onSentence)

root.mainloop()

