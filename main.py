# This database doesn't hold any confidential data and because of this I haven't yet bothered to harden it
# to attacks. If I ever do, it will be to demonstrate knowledge rather than to try and protect anything.
import tkinter as tk
import tkinter.font as tkFont
import requests
from PIL import ImageTk, Image
from io import BytesIO
import sqlite3
import re


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
    Warn.config(text='')    # reset Warning text
    # get input values
    inputTitleID = TitleID_Field.get()
    inputName = Name_Field.get()
    inputImage = Image_Field.get()
    inputTitleID = inputTitleID.upper()
    data = ((inputTitleID, inputName, inputImage))

    if not validateEntry(inputTitleID):
        showAlert('TitleID is not valid!')
    else:
    # TitleID needs to be validated as unique, if not, then modify existing row
        con = sqlite3.connect('zraGameDB.db')   # connect to DB
        cur = con.cursor()
        tblName = "PS3"
        result = cur.execute(f"SELECT titleID FROM {tblName} WHERE titleID == '{inputTitleID}'")
        result = result.fetchall()  # if a result is found, the titleID already exists and the entry should be UPDATED
        if len(result) == 1:    # UPDATE
            cur.execute(f"UPDATE {tblName} SET titleID='{data[0]}', name='{data[1]}', image='{data[2]}' WHERE titleID='{data[0]}'")
            con.commit()
        elif len(result) == 0:  # INSERT
            cur.execute(f"INSERT INTO {tblName} VALUES(?, ?, ?)", data)
            con.commit()

def clearEntries():         # clear user input and warning
    TitleID_Field.delete(0, tk.END)
    Name_Field.delete(0, tk.END)
    Image_Field.delete(0, tk.END)
    Warn.config(text='')
    DeleteButton.place_forget()
    # destroy image
    try:
        window.nametowidget('displayedImage').destroy()
    except KeyError:    # there is no image to destroy
        pass


def getRow():
    value = TitleID_Field.get()     # get value of Field
    value = value.upper()   # titleIDs are all uppercase
    # print('User entered "{val}"'.format(val=value))
    if not validateEntry(value):
        showAlert('TitleID is invalid!')
    else:
        con = sqlite3.connect('zraGameDB.db')   # connect to DB
        cur = con.cursor()
        tblName = "PS3"     # !will have to be changed if ever get around to implementing multiple tables!
        result = cur.execute(f'SELECT * FROM {tblName} WHERE titleID == "{value}"')     # execute sql
        result = result.fetchall()
        if len(result) > 1:  # if more than one row is selected something is very wrong with database as titleID should be unique
            exit('Database integrity error, more than one titleID found')
        elif len(result) == 0:  # no row was selected, entry does not exist
            alert = f"No entry found for '{value}'!"
            clearEntries()
            showAlert(alert)
        else:   # display found row in UI
            # delete all current text in fields
            clearEntries()
            # set values from DB
            TitleID_Field.insert(0, result[0][0])
            Name_Field.insert(0, result[0][1])
            Image_Field.insert(0, result[0][2])
            # display image
            img = result[0][2]
            img = img.strip('\n')   # newline character breaks Pillow(?)
            # enable button to delete row
            DeleteButton.place(x=100, y=300, width=100)
            showImg(img)


def validateEntry(val):    # validate user input is a valid titleID
    # from beginning of string match 4 letters followed by 5 numbers followed by the end of the string
    res = re.match('^([A-Z]{4}[0-9]{5})$', val)
    if res:
        return True
    else:
        return False


def showAlert(val):
    Warn.config(text=val)



workaround = []
def showImg(url):
    if url != "":   # Do not attempt to show an image if none has been supplied
        img_url = url
        try:
            response = requests.get(img_url)
            img_data = response.content
            img = Image.open(BytesIO(img_data))
            img = img.resize((250, 250))
            img = ImageTk.PhotoImage(img)
            workaround.append(img)  # without this garbage collection claims the reference and it doesn't work, stupid.
            panel = tk.Label(window, image=img, name="displayedImage")  # set a name so can be found in other functions
            panel.place(x=350, y=20)
        except Exception as e:
            Warn.config(text=e)


def deleteRow():
    inputTitleID = TitleID_Field.get()

    con = sqlite3.connect('zraGameDB.db')  # connect to DB
    cur = con.cursor()
    tblName = "PS3"  # !will have to be changed if ever get around to implementing multiple tables!
    try:
        cur.execute(f'DELETE FROM {tblName} WHERE titleID="{inputTitleID}"')
        con.commit()
        clearEntries()  # needs to be called here otherwise Warn will be cleared as well
    except Exception as e:
        Warn.config(text=e)




cl = Colors()  # create instance of Colors()

window = tk.Tk()
width = 650     # width of window
height = 400    # height of window
windowSize = '{w}x{h}'.format(w=width, h=height)    # format needed for tk.geometry()
window.geometry(windowSize)     # apply sizing. !Does not care about users resolution!
font = tkFont.Font(family='Helvetica', size=12)     # font used
window.title('Build 0.8')   # text shown in title-bar
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

DeleteButton = Button(window, text="Delete", command=deleteRow)


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

Warn = Label(window)
Warn.place(x=10, y=250)


window.mainloop()
