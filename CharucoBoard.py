import numpy as np
import cv2
import arucoUtililties as au
import svgwrite
from svgwrite import cm, mm
import json
import argparse

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
        markers = au.getMarkers(self.charucoBoard.ids.flatten(),self.DICT,au.markerWidth(self.DICT_STRING))


        markerIdx = 0
        for x in range(self.SQUARE_X):
            for y in range(self.SQUARE_Y):
                if markerPositions[y][x]:
                    self.drawMarker(markers[markerIdx], (x*self.SQUARE_LENGTH+self.markerOffset, y*self.SQUARE_LENGTH+self.markerOffset))
                    markerIdx+=1
                else:
                    self.drawing.add(self.drawing.rect(insert=(x*self.SQUARE_LENGTH*100*cm, y*self.SQUARE_LENGTH*100*cm),
                                    size=(self.SQUARE_LENGTH*100*cm, self.SQUARE_LENGTH*100*cm), fill='black'))
                    
        self.drawing.save()



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generates JSON with charucoBoard parameters")
    parser.add_argument('squaresX',help="squaresX parameter used for OpenCv charuco board initialization")
    parser.add_argument('squaresY',help="squaresY parameter used for OpenCv charuco board initialization")
    parser.add_argument('squareLength',help="squareLength parameter used for OpenCv charuco board initialization")
    parser.add_argument('markerLength',help="markerLength parameter used for OpenCv charuco board initialization")
    parser.add_argument('dictionary',help="dictionary parameter used for OpenCv charuco board initialization")
    parser.add_argument("--out_file",nargs="?",default='./charucoBoard.svg',help="output file")
    parser.add_argument("--charucoBoardJSON",nargs="?",default='./charucoBoard.json',help="output file")

    args = parser.parse_args()

    
    params = {'squaresX':args.squaresX,'squaresY':args.squaresY,'squareLength':args.squareLength,'markerLength':args.markerLength,'dictionary':args.dictionary}

    
    with open(args.charucoBoardJSON, 'w') as outfile:
        json.dump(params, outfile,indent=4)
    print("Wrote charuco board params to {}".format(args.charucoBoardJSON))
   
    charuco2svg(int(args.squaresX),int(args.squaresY),float(args.squareLength),float(args.markerLength),args.dictionary,args.out_file).generateSVG()
    print("Saved charuco board as {}".format(args.out_file))




