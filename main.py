import tkinter as tk
import tkinter.font as tkFont
import requests
from PIL import ImageTk, Image
from io import BytesIO


class Colors:
    def __init__(self):
        self.gray = '#36393E'
        self.white = '#ffffff'
        self.dark_gray = '#2C2F33'


class Button(tk.Button):
    def __init__(self, master, **kw):
        tk.Button.__init__(self, master=master, **kw)
        self['font'] = font
        self['bg'] = cl.gray        # background colour
        self['fg'] = cl.white       # text colour
        self['relief'] = 'ridge'    # the outline
        self['cursor'] = 'hand2'    # not to be confused with 'hand' (doesn't exist), or 'hand1'
        self['activebackground'] = cl.dark_gray     # when clicked bg colour
        self['activeforeground'] = cl.white         # when clicked fg colour


class Field(tk.Entry):
    def __init__(self, master, **kw):
        tk.Entry.__init__(self, master=master, **kw)
        self['font'] = font
        self['fg'] = cl.white       # text colour
        self['bg'] = cl.dark_gray   # element colour


class Label(tk.Label):
    def __init__(self, master, **kw):
        tk.Label.__init__(self, master=master, **kw)
        self['font'] = font
        self['fg'] = cl.white
        self['bg'] = cl.gray


def applyEntries():     # decide whether to append a new row or modify existing based on given titleID
    print('applyEntries')


def clearEntries():         # clear user input
    TitleID_Field.delete(0, tk.END)
    Name_Field.delete(0, tk.END)
    Image_Field.delete(0, tk.END)
    # need to destroy image as well


def getRow():
    # should get value of TitleID_Field, then clear all Fields, then search for input value in database,
    # if found, populate all Fields with respective info, if not found, alert user in some way
    value = TitleID_Field.get()
    print('User entered "{val}"'.format(val=value))
    if value == "":
        pass
    else:
        pass
        # DOTHIS


def validateEntry():    # validate user input is a valid titleID
    # titleIDs are 'ABCD12345' form, capitalised, without any punctuation.
    pass


cl = Colors()  # create instance of Colors()

window = tk.Tk()
width = 650     # width of window
height = 400    # height of window
windowSize = '{w}x{h}'.format(w=width, h=height)    # format needed for tk.geometry()
window.geometry(windowSize)     # apply sizing
font = tkFont.Font(family='Helvetica', size=12)     # font used
window.title('Build 0.3')   # text shown in title-bar
window.iconbitmap('froge.ico')  # set icon to be used in title-bar
window.configure(bg=cl.gray)  # set background colour of window
window.resizable(width=False, height=False)     # disable resizing as widgets are not scalable anyway

# Create and place buttons
ApplyButton = Button(window, text='Apply', command=applyEntries)
ApplyButton.place(x=355, y=300, width=100)

DiscardButton = Button(window, text='Discard', command=clearEntries)
DiscardButton.place(x=500, y=300, width=100)

GetButton = Button(window, text="Get row", command=getRow)
GetButton.place(x=200, y=35, width=100)

# Create and place entries and labels
TitleID_Label = Label(window, text="TitleID:")
TitleID_Label.place(x=10, y=10)
TitleID_Field = Field(window)
TitleID_Field.place(x=10, y=40)

Name_Label = Label(window, text="Name:")
Name_Label.place(x=10, y=80)
Name_Field = Field(window)
Name_Field.place(x=10, y=110)

Image_Label = Label(window, text="Image:")
Image_Label.place(x=10, y=150)
Image_Field = Field(window)
Image_Field.place(x=10, y=180)



workaround = []
def showImg():
    img_url = 'https://i.imgur.com/Voz3cKk.jpg'
    response = requests.get(img_url)
    img_data = response.content
    img = Image.open(BytesIO(img_data))
    img = img.resize((250, 250))
    img = ImageTk.PhotoImage(img)
    workaround.append(img)  # without this garbage collection claims the reference and it doesn't work, stupid.
    panel = tk.Label(window, image=img)
    # panel.pack(side="bottom", fill="both", expand="yes")
    panel.place(x=350, y=20)


# showImg()
window.mainloop()
