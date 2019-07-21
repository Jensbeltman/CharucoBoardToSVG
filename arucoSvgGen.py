import numpy as np
import cv2
from cv2 import aruco
import svgwrite

from svgwrite import cm, mm


def arucoSvgGen(dict, id, offset):
    return


    

CHARUCO_BOARD = aruco.CharucoBoard_create(4, 4, 0.05, 0.03, aruco.Dictionary_get(aruco.DICT_5X5_100))

print(CHARUCO_BOARD.ids[0])