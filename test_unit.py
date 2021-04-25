# This is the entry point. Run this file!
# You don't need to run digitRecognition.py to train the Convolutional Neural Network (CNN).
# I have trained the CNN on my computer and saved the architecture in digitRecognition.h5

from cv2 import cv2
import numpy as np
import tensorflow as tf
import os
import keras
import time
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
from keras.models import model_from_json
from lib.model import Model
from lib.findsudokuboard import find_sudoku_board
from lib.splitsudokuboard import split_sudoku_board_to_array
#from components.frame.config import Backtracking

# physical_devices = tf.config.list_physical_devices("GPU")
# tf.config.experimental.set_memory_growth(physical_devices[0], True)

def showImage(img, name, width, height):
    new_image = np.copy(img)
    new_image = cv2.resize(new_image, (width, height))
    cv2.imshow(name, new_image)

model = Model()
path = r"C:\Users\Moon\Downloads\Code\OpenCV-Sudoku-Solver\lib\digitalModel.h5"
model.load_model_from_file(path)
# batch_size = 128
# num_classes = 9
# epochs = 35
# input_shape = (28, 28, 1)

# path = os.path.dirname(os.path.abspath(__file__))
# path = os.path.join(path,'lib')
# path = os.path.join(path,'digitRecognition.h5')

# model = Sequential()
# model.add(Conv2D(32, kernel_size=(3, 3),
#                  activation='relu',
#                  input_shape=input_shape))
# model.add(Conv2D(64, (3, 3), activation='relu'))
# model.add(MaxPooling2D(pool_size=(2, 2)))
# model.add(Dropout(0.25))
# model.add(Flatten())
# model.add(Dense(128, activation='relu'))
# model.add(Dropout(0.5))
# model.add(Dense(num_classes, activation='softmax'))

# model.compile(loss=keras.losses.categorical_crossentropy,
#               optimizer=keras.optimizers.Adadelta(),
#               metrics=['accuracy'])

# model.load_weights(path)
# Let's turn on webcam

# Load and set up Camera
#cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# cap.set(3, 1280)    # HD Camera
# cap.set(4, 720)

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
old_sudoku = None
while(True):
    ret, frame = cap.read() # Read the frame
    if ret == True:
        sudokuBoardImg, isSudoku = find_sudoku_board(frame)
        
        # Nếu không có bảng sudoku trả lại ảnh gốc
        if isSudoku:
            print("Hello")
            # Lấy mảng chứa đề sudoku (mảng 9x9)
            sudoku =  split_sudoku_board_to_array(sudokuBoardImg, model, Backtracking)
            showImage(sudoku, "Real Time Sudoku Solver", 1066, 600) # Print the 'solved' image
            cv2.waitKey(0)
            break
        else:
            showImage(frame, "Real Time Sudoku Solver", 1066, 600)
        if cv2.waitKey(1) & 0xFF == ord('q'):   # Hit q if you want to stop the camera
            break
    else:
       break
cap.release()
#out.release()
cv2.destroyAllWindows()

# path = r'C:\Users\Moon\Downloads\Code\test\9.png'
# img = cv2.imread(path)

# sudokuBoardImg, isSudoku = find_sudoku_board(img)
        
# # Nếu không có bảng sudoku trả lại ảnh gốc
# if isSudoku:
#     print("Hello")
#     # Lấy mảng chứa đề sudoku (mảng 9x9)qqqqq
#     sudoku =  split_sudoku_board_to_array(sudokuBoardImg, model)
#     showImage(sudoku, "Real Time Sudoku Solver", 1066, 600) # Print the 'solved' image
# else:
#     showImage(img, "Real Time Sudoku Solver", 1066, 600)
    
# cv2.waitKey(0)