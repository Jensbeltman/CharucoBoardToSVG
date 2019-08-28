import cv2
from cv2 import aruco_Board
import arucoUtililties as au


def markerMap(x,y):

    return 0



boardEE = cv2.aruco.CharucoBoard_create(4,4,5,4,au.toDict('DICT_4X4_50'))
boardOO = cv2.aruco.CharucoBoard_create(5,5,5,4,au.toDict('DICT_4X4_50'))
boardEO = cv2.aruco.CharucoBoard_create(4,5,5,4,au.toDict('DICT_4X4_50'))
boardOE = cv2.aruco.CharucoBoard_create(5,4,5,4,au.toDict('DICT_4X4_50'))

func(4,4)
img= boardEE.draw((100,100))
cv2.imshow("windows",img)
cv2.waitKey()
func(5,5)
img= boardOO.draw((100,100))
cv2.imshow("windows",img)
cv2.waitKey()
func(4,5)
img= boardEO.draw((100,100))
cv2.imshow("windows",img)
cv2.waitKey()
func(5,4)
img= boardOE.draw((100,100))
cv2.imshow("windows",img)
cv2.waitKey()

