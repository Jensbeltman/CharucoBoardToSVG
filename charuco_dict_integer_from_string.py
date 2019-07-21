import cv2

def str2arucoDict(str):
    return {
    'DICT_4X4_50': cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50),
    'DICT_4X4_100': cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_100),
    'DICT_4X4_250': cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_250),
    'DICT_4X4_1000': cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_1000),
    'DICT_5X5_50': cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_50),
    'DICT_5X5_100': cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_100),
    'DICT_5X5_250': cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_250),
    'DICT_5X5_1000': cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_1000),
    'DICT_6X6_50': cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_50),
    'DICT_6X6_100': cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_100),
    'DICT_6X6_250': cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250),
    'DICT_6X6_1000': cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_1000),
    'DICT_7X7_50': cv2.aruco.Dictionary_get(cv2.aruco.DICT_7X7_50),
    'DICT_7X7_100': cv2.aruco.Dictionary_get(cv2.aruco.DICT_7X7_100),
    'DICT_7X7_250': cv2.aruco.Dictionary_get(cv2.aruco.DICT_7X7_250),
    'DICT_7X7_1000': cv2.aruco.Dictionary_get(cv2.aruco.DICT_7X7_1000)
    }[str]

    
    
   

