import numpy as np
import math
import os
import math
from cv2 import cv2
from scipy import ndimage
from lib.model import Model

# Tính toán cách lấy nét trung tâm của ảnh
def get_best_shift(img):
    cy, cx = ndimage.measurements.center_of_mass(img)
    rows, cols = img.shape
    shiftx = np.round(cols/2.0-cx).astype(int)
    shifty = np.round(rows/2.0-cy).astype(int)
    return shiftx, shifty

# Thay đổi hình ảnh bằng giá trị của hafmg get_best_shift
def shift(img,sx,sy):
    rows,cols = img.shape
    M = np.float32([[1,0,sx],[0,1,sy]])
    shifted = cv2.warpAffine(img,M,(cols,rows))
    return shifted

# chuẩn bị và đưa hình ảnh về dạng chuẩn của model để sẵn sàng nhận diện
def prepare(img_array):
    new_array = img_array.reshape(-1, 28, 28, 1)
    new_array = new_array.astype('float32')
    new_array /= 255
    return new_array

def showImg(image):
    cv2.imshow('Image',image)
    cv2.waitKey(0)

# đầu vào là một ảnh chỉ chứa bảng sudoku
def split_sudoku_board_to_array(warp): 
    warp = cv2.cvtColor(warp,cv2.COLOR_BGR2GRAY)
    warp = cv2.GaussianBlur(warp, (5,5), 0)
    warp = cv2.adaptiveThreshold(warp, 255, 1, 1, 11, 2)
    warp = cv2.bitwise_not(warp)
    _, warp = cv2.threshold(warp, 150, 255, cv2.THRESH_BINARY)

    # Tạo mảng để lưu trữ bảng sudoku
    SIZE = 9
    grid = []
    for i in range(SIZE):
        row = []
        for j in range(SIZE):
            row.append(0)
        grid.append(row)

    height = warp.shape[0] // 9
    width = warp.shape[1] // 9

    # Offset để có thể loại bỏ đường viền sudoku ra khỏi ảnh
    offset_width = width // 10
    offset_height = height // 10

    # lấy model đã train để nhận diện số
    model = Model()
    path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(path,'digitalModel.h5')
    model.load_model_from_file(path)

    # chia bảng sudoku theo hình vuông 9x9
    for i in range(SIZE):
        for j in range(SIZE):

            # cắt ảnh với offset để loại bỏ đường viền của khung sudoku
            crop_image = warp[height*i+offset_height:height*(i+1)-offset_height, width*j+offset_width:width*(j+1)-offset_width]        
            #showImg(crop_image)

            ratio = 0.6
            # Để đảm bảo hơn ta lọc qua 4 cạnh của ảnh
            # ratio = 0.6 => là nếu 60% ở viền là màu đen thì xóa dòng đó đi

            # Top
            while np.sum(crop_image[0]) <= (1-ratio) * crop_image.shape[1] * 255:
                crop_image = crop_image[1:]
            # Bottom
            while np.sum(crop_image[:,-1]) <= (1-ratio) * crop_image.shape[1] * 255:
                crop_image = np.delete(crop_image, -1, 1)
            # Left
            while np.sum(crop_image[:,0]) <= (1-ratio) * crop_image.shape[0] * 255:
                crop_image = np.delete(crop_image, 0, 1)
            # Right
            while np.sum(crop_image[-1]) <= (1-ratio) * crop_image.shape[0] * 255:
                crop_image = crop_image[:-1]    
        
            # chuyển ảnh về 28x28
            digit_pic_size = 28
            crop_image = cv2.resize(crop_image, (digit_pic_size,digit_pic_size))

            # Kiểm tra xem ô có chứa số không

            # Ô nào có quá ít pixel đen thì coi đó là ô trắng
            if crop_image.sum() >= digit_pic_size**2*255 - digit_pic_size * 1 * 255:
                grid[i][j] == 0
                continue    

            # Để đảm bảo hơn, kiểm tra trung tâm ảnh chứa một vùng trắng lớn không
            # Nếu đúng thì đó không phải ô chứa số
            center_width = crop_image.shape[1] // 2
            center_height = crop_image.shape[0] // 2
            x_start = center_height // 2
            x_end = center_height // 2 + center_height
            y_start = center_width // 2
            y_end = center_width // 2 + center_width
            center_region = crop_image[x_start:x_end, y_start:y_end]
            
            if center_region.sum() >= center_width * center_height * 255 - 255:
                grid[i][j] = 0
                continue
            
            # Giờ chỉ còn những ô chứa số cần được xử lý

            # Thêm ngưỡng nhị phân để ảnh rõ ràng hơn
            _, crop_image = cv2.threshold(crop_image, 200, 255, cv2.THRESH_BINARY) 
            crop_image = crop_image.astype(np.uint8)

            # Căn giữa ảnh theo khối lượng tâm
            crop_image = cv2.bitwise_not(crop_image)
            shift_x, shift_y = get_best_shift(crop_image)
            shifted = shift(crop_image,shift_x,shift_y)
            crop_image = shifted

            # Đưa ảnh về dạng chuẩn để nhận dạng
            crop_image = prepare(crop_image)

            # Nhận dạng số và lưu vào ma trận
            prediction = model.predict_digital(crop_image) # model is trained by digitRecognition.py
            grid[i][j] = prediction

            #print("[" + str(i) + ":" + str(j) + "] = " + str(np.argmax(prediction[0])))
            #showImg(crop_image)
            
    return grid
