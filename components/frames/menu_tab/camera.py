from tkinter import (Button, Label, Entry, LabelFrame, StringVar, messagebox, Canvas,
                     Listbox, OptionMenu, scrolledtext, ttk)
from tkinter import Tk, END, LEFT, RIGHT, TOP, BOTTOM, CENTER, BOTH
from tkinter import RAISED, GROOVE, SUNKEN, RIDGE, LAST, DISABLED, NORMAL
from tkinter.ttk import Style, Notebook, Combobox, Frame
from components.frames.config import BGWHITE, WHITE, BGDARKGREY, BACKTRACKING, DANCINGLINK
from lib.global_variable import set_variable, get_variable
from cv2 import cv2
import PIL
from PIL import Image,ImageTk

class CameraFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, style=BGWHITE, borderwidth=0)
        self._parent = parent
        self.__initUI()

    def __initUI(self):
        self.pack(side=LEFT, fill="both", expand=True)

        self.wrapMenu = Frame(self, height="80", style=BGWHITE)
        self.wrapMenu.pack(fill=BOTH, pady=15)

        self.wrapCamera = Frame(self, height="80", style=BGWHITE)
        self.wrapCamera.pack(fill=BOTH, pady=15)

        #top menu
        self.topMenuFrame = Frame(self.wrapMenu, style=BGWHITE)
        self.topMenuFrame.pack()

        Label(self.topMenuFrame, text="Camera", bg=WHITE).grid(
            column=0, row=0, padx=10)
        self.camera_value = StringVar()
        self.cameraChoosen = Combobox(
        self.topMenuFrame, state="readonly", textvariable=self.camera_value, font="Arial 12")
        self.cameraChoosen["values"] = tuple(map(str, self.return_camera_indexes()))
        self.cameraChoosen.current(0)
        self.cameraChoosen.grid(column=1, row=0, pady=2)

        Label(self.topMenuFrame, text="Thuật toán",
              bg=WHITE).grid(column=2, row=0, padx=10)
        self.alg_value = StringVar()
        self.algChoosen = Combobox(
            self.topMenuFrame, state="readonly", textvariable=self.alg_value, font="Arial 12")
        self.algChoosen["values"] = (BACKTRACKING, DANCINGLINK)
        self.algChoosen.current(0)
        self.algChoosen.grid(column=3, row=0, pady=2)

        self.btnSave = Button(self.topMenuFrame,state=DISABLED, relief=RIDGE, borderwidth=1, text="Lưu")
        self.btnRun = Button(self.topMenuFrame, text="Bắt đầu", command = self.start_run_camera)
        self.btnSave.grid(column=4, row=0, padx=5)
        self.btnRun.grid(column=5, row=0, padx=5)

        #show camera
        self.showCameraFrame = Frame(self.wrapCamera, relief=GROOVE, borderwidth=5, height=430, style=BGDARKGREY)
        self.showCameraFrame.pack(fill=BOTH, padx=10)
        self.lbCamera = Label(self.showCameraFrame)
        self.lbCamera.pack(fill=BOTH)

    def return_camera_indexes(self):
        index = 1
        arr = []
        i = 10
        while i > 0:
            cap = cv2.VideoCapture(index,cv2.CAP_DSHOW)
            if cap.read()[0]:
                arr.append('camera ' + (str(index)))
                cap.release()
            index += 1
            i -= 1
        cv2.destroyAllWindows()
        return arr

    def start_run_camera(self):
        width, height = 500, 300
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        def show_frame():
            _, frame = cap.read()
            frame = cv2.flip(frame, 1)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = PIL.Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            self.lbCamera.imgtk = imgtk
            self.lbCamera.configure(image=imgtk)
            self.lbCamera.after(10, show_frame)

        show_frame()