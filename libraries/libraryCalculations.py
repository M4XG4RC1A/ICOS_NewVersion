def redim(percentage,original):
    return float(percentage)*original

def isOnBack(datY,heightBack):
    return True if datY<heightBack else False

def positionX(dat,sentence,height):
    return "Up" if dat<sentence+(height-sentence)/2 else "Down"

def positionY(dat,width):
    return "Left" if dat<width/2 else "Right"