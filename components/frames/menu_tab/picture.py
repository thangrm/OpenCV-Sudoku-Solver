from tkinter import (Button, Label, Entry, LabelFrame, StringVar, messagebox, Canvas,
                     Listbox,OptionMenu, scrolledtext,ttk)
from tkinter import Tk, END, LEFT, RIGHT, TOP, BOTTOM,CENTER, BOTH, RAISED, GROOVE,LAST
from tkinter.ttk import Style, Notebook, Combobox, Frame
from tkinter.filedialog import askopenfilename
from components.frames.config import BGWHITE, WHITE, BGDARKGREY, BeFS, BACKTRACKING
from lib.global_variable import set_variable,get_variable
from lib.findsudokuboard import find_sudoku_board
from lib.splitsudokuboard import split_sudoku_board_to_array

from cv2 import cv2
import os
import PIL
from PIL import Image,ImageTk
class PictureFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent,style=BGWHITE, borderwidth=0)
        self._parent = parent
        self.model = get_variable("model")
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
        self.algChoosen["values"] = (BACKTRACKING, BeFS)
        self.algChoosen.current(0)
        self.algChoosen.grid(column=3, row=0, pady=2)

        #show Picture
        self.showPictureFrame = Frame(self.wrapPicture, style=BGWHITE)
        self.showPictureFrame.pack(fill=None, padx=10, expand=True)
        
        self.lbCamera = Label(self.showPictureFrame, bg=WHITE)
        self.lbCamera.pack(fill=None, expand=True)
        
        self.btnChooseFile = Button(self.showPictureFrame, width=60, text="Chọn ảnh để xử lý", command=self.btn_choose_file_click)
        self.btnChooseFile.pack(fill=None, expand=True, ipady=5)
        
        Label(self.showPictureFrame, text="Hoặc kéo thả ảnh vào", bg=WHITE).pack(fill=None, expand=True, ipady=5)

    
    def btn_choose_file_click(self):
        file_path = askopenfilename()
        #print(file_path)
        img = cv2.imread(file_path)

        if img is None:
            return
        
        #cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
        result = self.recognize_and_solve_sudoku(img)
        resized = self.resize_image(result)
        img = PIL.Image.fromarray(resized)
        imgtk = ImageTk.PhotoImage(image=img)
        self.lbCamera.imgtk = imgtk
        self.lbCamera.configure(image=imgtk)

    def recognize_and_solve_sudoku(self,image):
        # Tìm bảng sudoku
        sudokuBoardImg, isSudoku = find_sudoku_board(image)
        
        # Nếu không có bảng sudoku trả lại ảnh gốc
        if not isSudoku:
            return image

        # Lấy mảng chứa đề sudoku (mảng 9x9)
        result, _ =  split_sudoku_board_to_array(sudokuBoardImg,self.model, self.alg_value.get())
        return result
    
    def resize_image(self, image):
        height = 420
        width = 715
        
        h = image.shape[0]
        w = image.shape[1]

        if h > height:
            w = w * height // h
            h = height

        if w > width:
            h = h * width // w
            w = width

        dim = (w, h)
        resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
        return resized
        
