from tkinter import *
from random import randint
from time import sleep
from tkinter.messagebox import showerror

NODE_RADIUS = 30
BACKGROUND_COLOR = "black"
NODE_COLOR = "white"
TEXT_COLOR = "black"
LINE_COLOR = "white"
FONT = "Arial 20 bold"

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
X_PADDING = 150
Y_PADDING = NODE_RADIUS * 3 + 10

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


def insertNode(root: Node, value, depth, canvas, rootPositionX, rootPositionY):
    if depth > MAX_DEPTH:
        showerror(title="ERROR", message="Max depth reached")
        return root

    insertedOval = createOvalWithText(canvas, rootPositionX, rootPositionY - 2 * NODE_RADIUS - 5,
                     NODE_RADIUS, NODE_COLOR,
                     value, TEXT_COLOR, FONT)

    sleep(ANIMATION_DELAY)

    canvas.itemconfig(insertedOval, fill="lightgrey")

    if root is None:
        root = Node(value)
        return root

    if value < root.value:
        leftChildPositionX, leftChildPositionY = calculateLeftChildPosition(rootPositionX, rootPositionY, depth + 1)
        root.leftChild = insertNode(root.leftChild, value, depth + 1, canvas, leftChildPositionX, leftChildPositionY)
    elif value > root.value:
        rightChildPositionX, rightChildPositionY = calculateRightChildPosition(rootPositionX, rootPositionY, depth + 1)
        root.rightChild = insertNode(root.rightChild, value, depth + 1, canvas, rightChildPositionX, rightChildPositionY)
    elif value == root.value:
        showerror(title="ERROR", message="Node already in tree")

    return root


def deleteNode(root: Node, value: int):
    pass


def drawTree(root: Node, canvas, rootPositionX, rootPositionY, depth):
    if root is None:
        return

    if root.leftChild is not None:
        leftChildPositionX, leftChildPositionY = calculateLeftChildPosition(rootPositionX, rootPositionY, depth + 1)
        canvas.create_line(rootPositionX, rootPositionY,
                           leftChildPositionX, leftChildPositionY, 
                           fill=LINE_COLOR, width=5)
        drawTree(root.leftChild, canvas, leftChildPositionX, leftChildPositionY, depth + 1)

    if root.rightChild is not None:
        rightChildPositionX, rightChildPositionY = calculateRightChildPosition(rootPositionX, rootPositionY, depth + 1)
        canvas.create_line(rootPositionX, rootPositionY,
                           rightChildPositionX, rightChildPositionY, 
                           fill=LINE_COLOR, width=5)
        drawTree(root.rightChild, canvas, rightChildPositionX, rightChildPositionY, depth + 1)

    createOvalWithText(canvas, rootPositionX, rootPositionY, 
                     NODE_RADIUS, NODE_COLOR, 
                     root.value, TEXT_COLOR, FONT)


def createOvalWithText(canvas, centerX, centerY, radius, color, text, textColor, font):
    oval = canvas.create_oval(centerX - radius, centerY - radius,
                       centerX + radius, centerY + radius,
                       fill=color, width=0)
    canvas.create_text(centerX, centerY,
                       text=text,
                       fill=textColor,
                       font=font)
    window.update()

    return oval


def onClickInsert(value):
    global rootNode
    try:
        value = int(value)
    except ValueError:
        showerror(title="ERROR", message="Invalid input")
        return

    if value > MAX_VALUE:
        showerror(title="ERROR", message="Input value exceeding max allowed")
        return
    if value < MIN_VALUE:
        showerror(title="ERROR", message="Input value under min allowed")
        return

    rootPositionX = WINDOW_WIDTH/2
    rootPositionY = Y_PADDING

    rootNode = insertNode(rootNode, value, 0, canvas, rootPositionX, rootPositionY)

    canvas.delete("all")

    drawTree(rootNode, canvas, rootPositionX, rootPositionY, 0)


window.geometry(str(WINDOW_WIDTH) + "x" + str(WINDOW_HEIGHT) + "+100-100")
window.resizable(False, False)
window.title("Binary Search Tree Visualizer")


canvas = Canvas(window, bg=BACKGROUND_COLOR)
canvas.pack(side=TOP, fill=BOTH, expand=2)

insertRandom = Button(window, text="Insert Random", font=("Arial 15 bold"), 
                      command=lambda:onClickInsert(randint(MIN_VALUE, MAX_VALUE)))
insertRandom.pack(side=LEFT, fill=X, expand=1)
window.bind('<Rightshift>',lambda event:onClickInsert(inputField.get()))

insertButton = Button(window, text="Insert", font=("Arial 15 bold"), command=lambda:onClickInsert(inputField.get()))
insertButton.pack(side=LEFT, fill=X, expand=1)
window.bind('<Return>',lambda event:onClickInsert(inputField.get()))

deleteButton = Button(window, text="Delete", font=("Arial 15 bold"))
deleteButton.pack(side=LEFT, fill=X, expand=1)

inputField = Entry(window, font=("Arial 15 bold"))
inputField.pack(side=LEFT, expand=0)

window.mainloop()




