import numpy as np
import cv2


a = np.array([5, 5, 5])
print(a)

img = cv2.imread('IMG_1111.jpg', cv2.IMREAD_COLOR)
cv2.imshow('window', img)

cv2.waitKey()



