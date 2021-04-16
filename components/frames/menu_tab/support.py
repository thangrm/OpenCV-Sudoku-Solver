from tkinter import (Button, Label, Entry, LabelFrame, StringVar, messagebox, Canvas,
                     Listbox,OptionMenu, scrolledtext,ttk)
from tkinter import Tk, END, LEFT, RIGHT, TOP, BOTTOM,CENTER, BOTH, RAISED, GROOVE,LAST
from tkinter.ttk import Style, Notebook, Combobox, Frame
from components.frames.config import BGWHITE, WHITE, BGDARKGREY
from lib.global_variable import set_variable,get_variable

class SupportFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent,style=BGWHITE, borderwidth=0)
        self._parent = parent
        self.__initUI()

    def __initUI(self):
        self.pack(side=LEFT, fill="both", expand=True)
        
        self.wrapLeft = Frame(self, width=250, style=BGWHITE)
        self.wrapLeft.pack(side=LEFT, fill="y", pady=10, padx=10)

        self.wrapRight = Frame(self, style=BGWHITE)
        self.wrapRight.pack(side=LEFT, fill=BOTH, pady=60, padx=10)

        #Logo in left side
        self.logoFrame = Frame(self.wrapLeft, width=150, height=150, relief=GROOVE, borderwidth=5 ,style=BGDARKGREY)
        self.logoFrame.pack(padx=60, pady=50)


        #infor in right side
        txtInfor = "Phiên bản: v0.0.1\n\nNhóm phát triển: Nhóm 2 - K13 - Đại học Công Nghiệp Hà Nội\n\n\n\n\nLiên hệ: email@example.com"

        Label(self.wrapRight, text="Giải sudoku theo thời gian thực", font="Arial 18 bold", bg=WHITE).pack(pady=5)
        Label(self.wrapRight, text= txtInfor, font="Arial 12", bg=WHITE, justify=LEFT).pack()





        
    