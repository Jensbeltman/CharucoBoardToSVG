import numpy as np 
import cv2


def toDict(dict_string):
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
    }[dict_string]


def markerWidth(dict_string, include_boarder = True):
    for i in range(1, 10):
        if dict_string.find('X'+str(i)) is not -1:
            if include_boarder:
                return i+2 #+2 beacause of the black border on each marker
            else :
                return i

def getMarkers(ids,DICT,pxpm):
    markerImg = [cv2.aruco.drawMarker(DICT, id, pxpm) for id in ids]
    return markerImg

