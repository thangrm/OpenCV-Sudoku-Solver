from tkinter import Tk,Canvas,LAST,Frame,Button,LEFT,RIGHT, NO, NONE, GROOVE
from components.frames import bottom,style,tab
from lib.global_variable import set_variable,get_variable

class MainPage():
    def __init__(self):
        self._window = Tk()
        self._window.title("Giải sudoku theo thời gian thực")
        self._window.geometry("800x650")
        
        self.main_window(self._window)

        self._window.mainloop()

    def main_window(self,window):
        style.CreateStyle(self._window) 
        tab.TabFrame(self._window)   
        bottom.BottomFrame(self._window)