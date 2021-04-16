from tkinter import GROOVE,LEFT,TOP
from tkinter.ttk import Frame,Notebook
from components.frames.menu_tab import camera, picture, support
from components.frames.config import BGWHITE, WHITE
from lib.global_variable import set_variable

class TabFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent,style=BGWHITE,relief=GROOVE, borderwidth=1)
        self._parent = parent
        self.__initUI()
    
    def __initUI(self):
        self.pack(side=TOP, fill="both", expand=True)
        tabControl = Notebook(self)
        tabControl.pack(side=LEFT, fill="both", expand=True)
        tab1 = camera.CameraFrame(self._parent)
        tab2 = picture.PictureFrame(self._parent)
        tab3 = support.SupportFrame(self._parent)
        tabControl.add(tab1,text="Camera")
        tabControl.add(tab2,text="Ảnh")
        tabControl.add(tab3,text="Hỗ trợ")

        set_variable("matrix",tab2)
        set_variable("tabControl",tabControl)