from tkinter import (Button, Label, Entry, LabelFrame, StringVar, messagebox, Canvas,
                     Listbox,OptionMenu, scrolledtext,ttk)
from tkinter import Tk, END, LEFT, RIGHT, TOP, BOTTOM,CENTER, BOTH, RAISED, GROOVE,LAST
from tkinter.ttk import Style, Notebook, Combobox, Frame
from tkinter.filedialog import askopenfilename
from components.frames.config import BGWHITE, WHITE, BGDARKGREY
from lib.global_variable import set_variable,get_variable

class PictureFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent,style=BGWHITE, borderwidth=0)
        self._parent = parent
        self.__initUI()

    def __initUI(self):
        self.pack(side=LEFT, fill="both", expand=True)

        self.wrapMenu = Frame(self, height="80", style=BGWHITE)
        self.wrapMenu.pack(fill=BOTH, pady=15)

        self.wrapPicture = Frame(self, height=460, relief=GROOVE, borderwidth=5, style=BGWHITE)
        self.wrapPicture.pack(fill=BOTH, padx=10, pady=15, expand=True)

        #top menu
        self.topMenuFrame = Frame(self.wrapMenu, style=BGWHITE)
        self.topMenuFrame.pack()

        Label(self.topMenuFrame, text="Thuật toán",
              bg=WHITE).grid(column=2, row=0, padx=10)
        self.alg_value = StringVar()
        self.algChoosen = Combobox(
            self.topMenuFrame, state="readonly", textvariable=self.alg_value, font="Arial 12")
        self.algChoosen["values"] = ("Backtracking", "Dancing link")
        self.algChoosen.current(0)
        self.algChoosen.grid(column=3, row=0, pady=2)

        #show Picture
        self.showPictureFrame = Frame(self.wrapPicture, style=BGWHITE)
        self.showPictureFrame.pack(fill=None, padx=10, expand=True)
        self.btnChooseFile = Button(self.showPictureFrame, width=60, text="Chọn ảnh để xử lý")
        self.btnChooseFile.pack(fill=None, expand=True, ipady=5)
        Label(self.showPictureFrame, text="Hoặc kéo thả ảnh vào", bg=WHITE).pack(fill=None, expand=True)
    
    