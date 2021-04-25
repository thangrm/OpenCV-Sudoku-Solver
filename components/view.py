from tkinter import Tk,Canvas,LAST,Frame,Button,LEFT,RIGHT, NO, NONE, GROOVE
from components.frames import bottom,style,tab
from lib.global_variable import set_variable,get_variable
from lib.model import Model
import os

class MainPage():
    def __init__(self):
        self._window = Tk()
        self._window.title("Giải sudoku theo thời gian thực")
        self._window.geometry("800x650")
        
        self.config_global_variable()
        self.main_window(self._window)

        self._window.mainloop()

    def main_window(self,window):
        style.CreateStyle(self._window) 
        tab.TabFrame(self._window)   
        bottom.BottomFrame(self._window)

    def config_global_variable(self):
        path = os.path.dirname(os.path.abspath(__file__))
        path = os.path.abspath(os.path.join(path, os.pardir))
        path = os.path.join(path,'lib')
        path = os.path.join(path,'digitalModelWithoutZero.h5')
        
        model = Model()
        model.load_model_from_file(path)

        set_variable("model",model)

