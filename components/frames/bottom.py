from tkinter import (Button, Label, Entry, LabelFrame, StringVar, messagebox,
                     Listbox,OptionMenu, scrolledtext,ttk)
from tkinter import Tk, END, LEFT, RIGHT, TOP, BOTTOM,CENTER, BOTH, RAISED, GROOVE,NW
from tkinter.ttk import Style, Combobox, Frame
from components.frames.config import BGGREY

class BottomFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, height="30", relief=GROOVE, borderwidth=1)
        self.parent = parent
        self.__initUI()

    def __initUI(self):
        self.pack(side=BOTTOM,fill="x")
        Label(self,text="ĐHCN Hà Nội - K13").pack(side=RIGHT,padx=5)