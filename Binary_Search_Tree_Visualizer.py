from cgitb import enable
from tkinter import *
from random import randint
from time import sleep
from tkinter.messagebox import showerror, showinfo
from venv import create

NODE_RADIUS = 30
BACKGROUND_COLOR = "black"
NODE_COLOR = "white"
HIGHLIGHT_COLOR = "lightgray"
TEXT_COLOR = "black"
LINE_COLOR = "white"
FONT_SIZE = 20

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
X_PADDING = 150
Y_PADDING = NODE_RADIUS * 4 + 5

MAX_DEPTH = 4
MAX_VALUE = 100
MIN_VALUE = 0

ANIMATION_DELAY = 0.5

rootNode = None
window = Tk()

class Node:
    def __init__(self, value):
        self.value = value
        self.leftChild = None
        self.rightChild = None


def calculateLeftChildPosition(parentPositionX, parentPositionY, childDepth):
    leftChildPositionX = parentPositionX - ((WINDOW_WIDTH - X_PADDING) / pow(2, childDepth)) / 2
    leftChildPositionY = parentPositionY + NODE_RADIUS * 4
    return (leftChildPositionX, leftChildPositionY)


def calculateRightChildPosition(parentPositionX, parentPositionY, childDepth):
    rightChildPositionX = parentPositionX + ((WINDOW_WIDTH - X_PADDING) / pow(2, childDepth)) / 2
    rightChildPositionY = parentPositionY + NODE_RADIUS * 4
    return (rightChildPositionX, rightChildPositionY)


def insertNode(rootNode, value, rootPositionX, rootPositionY, nodeDepth, canvas, window):
    if nodeDepth > MAX_DEPTH:
        showinfo(title="Insert", message="Max depth reached")
        return rootNode

    if rootNode is None:
        rootNode = Node(value)
        return rootNode

    createOvalWithText(canvas, rootPositionX, rootPositionY - 3 * NODE_RADIUS,
                        NODE_RADIUS, NODE_COLOR,
                        value, TEXT_COLOR, FONT_SIZE)
    window.update()
    sleep(ANIMATION_DELAY)
    

    if value < rootNode.value:
        createRectangleWithText(canvas, rootPositionX, rootPositionY - 1.5 * NODE_RADIUS,
                                NODE_RADIUS / 1.5, NODE_RADIUS / 1.5, NODE_COLOR,
                                "<", TEXT_COLOR, FONT_SIZE)
        window.update()
        sleep(ANIMATION_DELAY)

        leftChildPositionX, leftChildPositionY = calculateLeftChildPosition(rootPositionX, rootPositionY, nodeDepth + 1)
        rootNode.leftChild = insertNode(rootNode.leftChild, value, 
                                        leftChildPositionX, leftChildPositionY, 
                                        nodeDepth + 1, 
                                        canvas, window)
    elif value > rootNode.value:
        createRectangleWithText(canvas, rootPositionX, rootPositionY - 1.5 * NODE_RADIUS,
                                NODE_RADIUS / 1.5, NODE_RADIUS / 1.5, NODE_COLOR,
                                ">", TEXT_COLOR, FONT_SIZE)
        window.update()
        sleep(ANIMATION_DELAY)
        
        rightChildPositionX, rightChildPositionY = calculateRightChildPosition(rootPositionX, rootPositionY, nodeDepth + 1)
        rootNode.rightChild = insertNode(rootNode.rightChild, value, 
                                         rightChildPositionX, rightChildPositionY,
                                         nodeDepth + 1, 
                                         canvas, window)
    elif value == rootNode.value:
        showinfo(title="Insert", message="Node already in tree")

    return rootNode


def drawTree(rootNode, rootPositionX, rootPositionY, nodeDepth, canvas, window):
    if rootNode is None:
        return

    if rootNode.leftChild is not None:
        leftChildPositionX, leftChildPositionY = calculateLeftChildPosition(rootPositionX, rootPositionY, nodeDepth + 1)
        canvas.create_line(rootPositionX, rootPositionY,
                           leftChildPositionX, leftChildPositionY, 
                           fill=LINE_COLOR, width=5)
        drawTree(rootNode.leftChild, 
                 leftChildPositionX, leftChildPositionY, 
                 nodeDepth + 1,
                 canvas, window)

    if rootNode.rightChild is not None:
        rightChildPositionX, rightChildPositionY = calculateRightChildPosition(rootPositionX, rootPositionY, nodeDepth + 1)
        canvas.create_line(rootPositionX, rootPositionY,
                           rightChildPositionX, rightChildPositionY, 
                           fill=LINE_COLOR, width=5)
        drawTree(rootNode.rightChild, 
                 rightChildPositionX, rightChildPositionY, 
                 nodeDepth + 1,
                 canvas, window)

    createOvalWithText(canvas, rootPositionX, rootPositionY, 
                     NODE_RADIUS, NODE_COLOR, 
                     rootNode.value, TEXT_COLOR, FONT_SIZE)
    window.update()


def createOvalWithText(canvas, centerX, centerY, radius, ovalColor, text, textColor, fontSize):
    oval = canvas.create_oval(centerX - radius, centerY - radius,
                       centerX + radius, centerY + radius,
                       fill=ovalColor, width=0)
    text = canvas.create_text(centerX, centerY,
                       text=text, fill=textColor, font=("Arial " + str(int(fontSize)) + " bold"))


def createRectangleWithText(canvas, centerX, centerY, width, height, rectangleColor, text, textColor, fontSize):
    canvas.create_rectangle(centerX - width / 2, centerY - height / 2,
                            centerX + width / 2, centerY + height / 2,
                            fill=rectangleColor, width=0)
    canvas.create_text(centerX, centerY,
                       text=text, fill=textColor, font=("Arial " + str(int(fontSize)) + " bold"))


def isInputValid(value) -> bool:
    try:
        value = int(value)
    except ValueError:
        showerror(title="ERROR", message="Invalid input")
        return False

    if value > MAX_VALUE:
        showerror(title="ERROR", message="Input value exceeding max allowed")
        return False
    if value < MIN_VALUE:
        showerror(title="ERROR", message="Input value under min allowed")
        return False
    return True


def onClickInsert(value):
    global rootNode

    if not isInputValid(value):
        return

    value = int(value)

    rootPositionX = WINDOW_WIDTH/2
    rootPositionY = Y_PADDING

    insertButton["state"] = DISABLED
    insertRandom["state"] = DISABLED
    deleteButton["state"] = DISABLED
    inputField["state"] = DISABLED

    rootNode = insertNode(rootNode, value, rootPositionX, rootPositionY, 0, canvas, window)

    drawTree(rootNode, rootPositionX, rootPositionY, 0, canvas, window)

    sleep(1)
    canvas.delete("all")
    drawTree(rootNode, rootPositionX, rootPositionY, 0, canvas, window)

    insertButton["state"] = NORMAL
    insertRandom["state"] = NORMAL
    deleteButton["state"] = NORMAL
    inputField["state"] = NORMAL


window.geometry(str(WINDOW_WIDTH) + "x" + str(WINDOW_HEIGHT) + "+100-100")
window.resizable(False, False)
window.title("Binary Search Tree Visualizer")


canvas = Canvas(window, bg=BACKGROUND_COLOR)
canvas.pack(side=TOP, fill=BOTH, expand=2)

insertRandom = Button(window, text="Insert Random", font=("Arial 15"), 
                      command=lambda:onClickInsert(randint(MIN_VALUE, MAX_VALUE))
)
insertRandom.pack(side=LEFT, fill=X, expand=1)

insertButton = Button(window, text="Insert", font=("Arial 15"), command=lambda:onClickInsert(inputField.get()))
insertButton.pack(side=LEFT, fill=X, expand=1)

deleteButton = Button(window, text="Delete", font=("Arial 15"))
deleteButton.pack(side=LEFT, fill=X, expand=1)

inputField = Entry(window, font=("Arial 15"))
inputField.pack(side=LEFT, expand=0)

window.mainloop()






