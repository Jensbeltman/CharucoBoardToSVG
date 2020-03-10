import numpy as np
import cv2
import arucoUtililties as au
import svgwrite
from svgwrite import cm, mm


class charuco2svg(object):
    def __init__(self,SQUARE_X, SQUARE_Y, SQUARE_LENGTH, MARKER_LENGTH, DICT_STRING, SVG_PATH='' ):
        #Variable Parsing
        self.SQUARE_X = SQUARE_X
        self.SQUARE_Y = SQUARE_Y
        self.SQUARE_LENGTH = SQUARE_LENGTH
        self.MARKER_LENGTH = MARKER_LENGTH
        self.DICT_STRING = DICT_STRING
        self_PATH=SVG_PATH
        #OpenCV objects
        self.charucoBoard = cv2.aruco.CharucoBoard_create(
            SQUARE_Y, SQUARE_X, SQUARE_LENGTH, MARKER_LENGTH, au.toDict(DICT_STRING))
        self.DICT = au.toDict(DICT_STRING)
        #SVG related objects and variables 
        self.px_m = MARKER_LENGTH/au.markerWidth(DICT_STRING)
        self. markerOffset = ((SQUARE_LENGTH-MARKER_LENGTH)/2.0)
        self.drawing = svgwrite.Drawing(SVG_PATH, size=(SQUARE_X*SQUARE_LENGTH*100*cm, SQUARE_Y*SQUARE_LENGTH*100*cm), profile='full')


    def drawMarker(self,markerImage,point): 
        self.drawing.add(self.drawing.rect(insert=(point[0]*100*cm, point[1]*100*cm),
                size=(self.MARKER_LENGTH*100*cm, self.MARKER_LENGTH*100*cm), fill='black'))
        for y in range(markerImage.shape[0]):
            for x in range(markerImage.shape[1]):
                if markerImage[y][x] == 255:
                    self.drawing.add(self.drawing.rect(insert=((point[0]+x*self.px_m)*100*cm,(point[1]+ y*self.px_m)*100*cm), 
                                                        size=(self.px_m*100*cm, self.px_m*100*cm), fill='white'))

    def generateSVG(self):
        oddRows=self.SQUARE_Y%2
        markerPositions = [[oddRows==(i+j)%2 for i in range(self.SQUARE_X)]for j in range(self.SQUARE_Y)]
        print(self.charucoBoard.ids.flatten())
        markers = au.getMarkers(self.charucoBoard.ids.flatten(),self.DICT,au.markerWidth(self.DICT_STRING))


        
        for x in range(self.SQUARE_X):
            for y in range(self.SQUARE_Y):
                if markerPositions[y][x]:
                    self.drawMarker(markers[int((y+x)/2)], (x*self.SQUARE_LENGTH+self.markerOffset, y*self.SQUARE_LENGTH+self.markerOffset))
                    
                else:
                    self.drawing.add(self.drawing.rect(insert=(x*self.SQUARE_LENGTH*100*cm, y*self.SQUARE_LENGTH*100*cm),
                                    size=(self.SQUARE_LENGTH*100*cm, self.SQUARE_LENGTH*100*cm), fill='black'))
                    
        self.drawing.save()


if __name__ == "__main__":
    print("Types in the following variables seperated by spaces and or commas:")
    print("\tNumber of rows")
    print("\tNumber of columns")
    print("\tRow/columns size in meters")
    print("\tMarkers size in in meters")
    print("\tName of aruco dictionary (eg. DICT_4X4_50)")
    print("\tOutput file path")

    in_str=input().split(' ')
    if len(in_str)<4:
        charuco2svg(12,20,0.0125,0.01,"DICT_4X4_250","./charuco.svg").generateSVG()
    else:
        charuco2svg(int(in_str[0]),int(in_str[1]),float(in_str[2]),float(in_str[3]),in_str[4],in_str[5]).generateSVG()


    # markerImgEE = charuco2svg(4,4,0.025,0.02,"DICT_4X4_50","./EE.svg")
    # markerImgOO = charuco2svg(5,5,0.025,0.02,"DICT_4X4_50","./OO.svg")
    # markerImgEO = charuco2svg(4,5,0.025,0.02,"DICT_4X4_50","./EO.svg")
    # markerImgOE = charuco2svg(5,4,0.025,0.02,"DICT_4X4_50","./OE.svg")

    # markerImgEE.generateSVG()
    # markerImgOO.generateSVG()
    # markerImgEO.generateSVG()
    # markerImgOE.generateSVG()


