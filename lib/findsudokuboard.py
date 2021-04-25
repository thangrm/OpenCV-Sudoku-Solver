from cv2 import cv2
from scipy import ndimage
import numpy as np
import math
import os
import math

# tính góc giữa 2 vector
def angle_between(vector_1, vector_2):
    unit_vector_1 = vector_1 / np.linalg.norm(vector_1)
    unit_vector2 = vector_2 / np.linalg.norm(vector_2)
    dot_droduct = np.dot(unit_vector_1, unit_vector2)
    angle = np.arccos(dot_droduct) *  57.2958  # chuyển từ radian về độ
    return angle

# hàm kiểm tra xem 2 vector có tạo thành 1 góc 90 độ không
# epsilon là số sai số cho phép (đơn vị là độ)
def approx_90_degrees(vector_1, vector_2, epsilon):
    return abs(angle_between(vector_1, vector_2) - 90) < epsilon

# hàm kiểm tra xem độ dài của 4 cạnh có bằng nhau không
# epsilon là số sai số cho phép (đơn vị là %) 
def check_square_size(A, B, C, D, epsilon):
    AB = math.sqrt((B[0]-A[0])**2 + (B[1]-A[1])**2)
    BC = math.sqrt((C[0]-B[0])**2 + (C[1]-B[1])**2)
    CD = math.sqrt((D[0]-C[0])**2 + (D[1]-C[1])**2)
    DA = math.sqrt((A[0]-D[0])**2 + (A[1]-D[1])**2)

    shortest = min(AB, BC, CD, DA)
    longest = max(AB, BC, CD, DA)
    print(shortest/longest)
    return (epsilon/100) * longest < shortest

# hàm tìm các góc của đường viền
def get_corners_from_contours(contours, corner_amount=4, max_iter=200):

    coefficient = 1
    while max_iter > 0 and coefficient >= 0:
        max_iter = max_iter - 1

        epsilon = coefficient * cv2.arcLength(contours, True)

        poly_approx = cv2.approxPolyDP(contours, epsilon, True)
        hull = cv2.convexHull(poly_approx)
        if len(hull) == corner_amount:
            return hull
        else:
            if len(hull) > corner_amount:
                coefficient += .01
            else:
                coefficient -= .01
    return None

def showImg(image):
    cv2.imshow('Image',image)
    cv2.waitKey(0)

def find_sudoku_board(img): 

    # Chuyển qua ảnh đen trắng để tìm khung của sudoku dễ hơn
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #showImg(gray)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    #showImg(blur)
    thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)
    #showImg(thresh)

    # Tìm các đường viền, lọc ra đường viền lớn nhất là bảng sudoku
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for line in contours:
        area = cv2.contourArea(line)
        if area > 50000:
            #print("=======================================\n")
            #print(area)
            # Lấy ra 4 góc của đường viền
            corners = get_corners_from_contours(line, 4)
            if corners is None:         # Không phải là sudoku
                continue

            corners = corners.reshape(4,2)  
            #print(corners)
        
            #  Thứ tự ma trận của hình square tương ứng với các vị trí 
            #  0 1         
            #  3 2                          
            square = np.zeros((4, 2), dtype = "float32")
            tempCorners = np.copy(corners)
            
            # Tìm điểm trên cùng bên trái - tổng tọa độ nhỏ nhất

            sum = tempCorners[0][0]+tempCorners[0][1]
            index = 0
            for i in range(4):
                if(tempCorners[i][0]+tempCorners[i][1] < sum):
                    sum = tempCorners[i][0]+tempCorners[i][1]
                    index = i
            square[0] = tempCorners[index]
            tempCorners = np.delete(tempCorners, index, 0)

            # Tìm điểm dưới bên phải - tổng tọa độ lớn nhất
            sum = 0
            for i in range(3):
                if(tempCorners[i][0]+tempCorners[i][1] > sum):
                    sum = tempCorners[i][0]+tempCorners[i][1]
                    index = i
            square[2] = tempCorners[index]
            tempCorners = np.delete(tempCorners, index, 0)

            # Tìm 2 điểm còn lại
            if(tempCorners[0][0] > tempCorners[1][0]):
                square[1] = tempCorners[0]
                square[3] = tempCorners[1]
                
            else:
                square[1] = tempCorners[1]
                square[3] = tempCorners[0]
            
            #print(square)
            # Bảng sudoku có hình vuông nên sẽ lọc ra những đường viền là hình vuông
            # Để là hình vuông thì đầu tiên 4 góc phải xấp xỉ 90 độ
            # Ta quy ước 4 điểm của square  0 1  = A B
            #                               3 2    D C 
            A = square[0]
            B = square[1]
            C = square[2]
            D = square[3]
            #print(A,B,C,D)
            
            AB = B - A
            AD = D - A
            CB = B - C
            CD = D - C
            #print(AB,AD,CB,CD)
            if approx_90_degrees(AB,AD,20) and approx_90_degrees(CB,CD,20):
                #print("4 góc vuông")
                if check_square_size(A, B, C, D, 98):
                    print("4 cạnh bằng nhau => Là hình vuông")

                    # Tìm chiều rộng của bảng sudoku
                    width_A = math.sqrt((B[0]-A[0])**2 + (B[1]-A[1])**2)
                    width_B = math.sqrt((D[0]-C[0])**2 + (D[1]-C[1])**2)

                    # Tìm chiều cao của bảng sudoku
                    height_A = math.sqrt((C[0]-B[0])**2 + (C[1]-B[1])**2)
                    height_B = math.sqrt((A[0]-D[0])**2 + (A[1]-D[1])**2)

                    # Lấy độ dài lớn nhất
                    max_width = max(int(width_A), int(width_B))
                    max_height = max(int(height_A), int(height_B))

                    # Xây dựng điểm đích
                    # Chuyển ảnh về chế độ nhìn mắt chim (nhìn từ trên xuống)
                    dst = np.array([
                    [0, 0],
                    [max_width - 1, 0],
                    [max_width - 1, max_height - 1],
                    [0, max_height - 1]], dtype = "float32")

                    # Tính ma trận biến đổi ảnh để wrap lại ảnh
                    perspective_transformed_matrix = cv2.getPerspectiveTransform(square, dst)
                    warp = cv2.warpPerspective(img, perspective_transformed_matrix, (max_width, max_height))

                    return warp, True
    return None, False