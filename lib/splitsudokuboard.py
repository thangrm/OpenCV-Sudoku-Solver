import numpy as np
import math
import os
import copy
import math
from cv2 import cv2
from scipy import ndimage
from lib.model import Model
from lib.algorithm import solve_sudoku_BeFS, isNonZero, boardBackTracking
from components.frames.config import BACKTRACKING, BeFS

import time

# Tính toán cách lấy nét trung tâm của ảnh
def get_best_shift(img):
    cy, cx = ndimage.measurements.center_of_mass(img)
    rows, cols = img.shape
    shiftx = np.round(cols/2.0-cx).astype(int)
    shifty = np.round(rows/2.0-cy).astype(int)
    return shiftx, shifty

# Thay đổi hình ảnh bằng giá trị của hàm get_best_shift
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
def split_sudoku_board_to_array(warp, model, alg): 
    showImg(warp)
    orginal_warp = np.copy(warp)
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
    offset_width = width // 8
    offset_height = height // 8

    # chia bảng sudoku theo hình vuông 9x9
    for i in range(SIZE):
        for j in range(SIZE):

            # cắt ảnh với offset để loại bỏ đường viền của khung sudoku
            crop_image = warp[height*i+int(offset_height*1.5):height*(i+1)-offset_height, width*j+int(offset_height*1.5):width*(j+1)-offset_width]        
            #showImg(cv2.bitwise_not(crop_image))

            ratio = 0.5
            # Để đảm bảo hơn ta lọc qua 4 cạnh của ảnh
            # ratio = 0.5 => là nếu 50% ở viền là màu đen thì xóa dòng đó đi

            # Top
            while np.sum(crop_image[0]) <= (1-ratio) * crop_image.shape[1] * 255 or np.sum(crop_image[1]) <= (1-ratio) * crop_image.shape[1] * 255 or np.sum(crop_image[2]) <= (1-ratio) * crop_image.shape[1] * 255:
                crop_image = crop_image[1:]
            # Bottom
            while np.sum(crop_image[:,-1]) <= (1-ratio) * crop_image.shape[1] * 255 or np.sum(crop_image[:,-2]) <= (1-ratio) * crop_image.shape[1] * 255 or np.sum(crop_image[:,-3]) <= (1-ratio) * crop_image.shape[1] * 255:
                crop_image = np.delete(crop_image, -1, 1)
            # Left
            while np.sum(crop_image[:,0]) <= (1-ratio) * crop_image.shape[0] * 255 or np.sum(crop_image[:1]) <= (1-ratio) * crop_image.shape[0] * 255 or np.sum(crop_image[:,2]) <= (1-ratio) * crop_image.shape[0] * 255:
                crop_image = np.delete(crop_image, 0, 1)
            # Right
            while np.sum(crop_image[-1]) <= (1-ratio) * crop_image.shape[0] * 255 or np.sum(crop_image[-1]) <= (1-ratio) * crop_image.shape[0] * 255 or np.sum(crop_image[-1]) <= (1-ratio) * crop_image.shape[0] * 255:
                crop_image = crop_image[:-1]    
        
            # chuyển ảnh về 28x28
            digit_pic_size = 28
            crop_image = cv2.resize(crop_image, (digit_pic_size,digit_pic_size))

            # Kiểm tra xem ô có chứa số không

            # Ô nào có quá ít pixel đen thì coi đó là ô trắng
            print("full : " + str(crop_image.sum()  / (digit_pic_size**2*255)))
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

            if center_region.sum() >= (center_width * center_height * 255 * 0.8):
                grid[i][j] = 0
                continue                    
            print("center : " + str(center_region.sum() / (center_width * center_height * 255)))
            
            # Giờ chỉ còn những ô chứa số cần được xử lý

            # Thêm ngưỡng nhị phân để ảnh rõ ràng hơn
            _, crop_image = cv2.threshold(crop_image, 200, 255, cv2.THRESH_BINARY) 
            crop_image = crop_image.astype(np.uint8)

            # Căn giữa ảnh theo khối lượng tâm
            crop_image = cv2.bitwise_not(crop_image)
            shift_x, shift_y = get_best_shift(crop_image)
            shifted = shift(crop_image,shift_x,shift_y)
            crop_image = shifted
            
            #imgTemp = np.copy(crop_image)

            # Đưa ảnh về dạng chuẩn để nhận dạng
            crop_image = prepare(crop_image)

            # Nhận dạng số và lưu vào ma trận
            #prediction = model.predict_digital(crop_image) # model is trained by digitRecognition.py
            #listImg.append(crop_image)
            #prediction = model.predict_digital([crop_image])
            
            #t0 = time.time()
            prediction = model.predict_digital(crop_image)
            grid[i][j] = np.argmax(prediction[0])
            #t1 = time.time()
            #print(t1-t0)

            print("[" + str(i) + ":" + str(j) + "] = " + str(np.argmax(prediction[0])))
            # if(np.argmax(prediction[0]) == 3):
            #     showImg(imgTemp)
    
    """
    Giải sudoku và viết kết quả lên ảnh
    """
    user_grid = copy.deepcopy(grid)
    if alg == BeFS:
        print(BeFS)
        solve_sudoku_BeFS(grid)
    elif alg == BACKTRACKING:
        print(BACKTRACKING)
        grid, _ = boardBackTracking(grid)
    else:
        solve_sudoku_BeFS(grid)

    for line in grid:
        print(line)

    if(isNonZero(grid)): # If we got a solution
        orginal_warp = write_solution_on_image(orginal_warp, grid, user_grid)  
        return orginal_warp, True

    # Apply inverse perspective transform and paste the solutions on top of the orginal image
    # result_sudoku = cv2.warpPerspective(orginal_warp, perspective_transformed_matrix, (image.shape[1], image.shape[0])
    #                                     , flags=cv2.WARP_INVERSE_MAP)
    # result = np.where(result_sudoku.sum(axis=-1,keepdims=True)!=0, result_sudoku, image)

    return orginal_warp, False

 
def write_solution_on_image(image, grid, user_grid):
    # Write grid on image
    SIZE = 9
    width = image.shape[1] // 9
    height = image.shape[0] // 9
    for i in range(SIZE):
        for j in range(SIZE):
            if(user_grid[i][j] != 0):    # If user fill this cell
                continue                # Move on
            text = str(grid[i][j])
            off_set_x = width // 15
            off_set_y = height // 15
            font = cv2.FONT_HERSHEY_SIMPLEX
            (text_height, text_width), _ = cv2.getTextSize(text, font, fontScale=1, thickness=3)
            # marginX = math.floor(width / 7)
            # marginY = math.floor(height / 7)
        
            font_scale = 0.6 * min(width, height) / max(text_height, text_width)
            text_height *= font_scale
            text_width *= font_scale
            bottom_left_corner_x = width*j + math.floor((width - text_width) / 2) + off_set_x
            bottom_left_corner_y = height*(i+1) - math.floor((height - text_height) / 2) + off_set_y
            image = cv2.putText(image, text, (bottom_left_corner_x, bottom_left_corner_y), 
                                                  font, font_scale, (0,255,0), thickness=3, lineType=cv2.LINE_AA)
    return image