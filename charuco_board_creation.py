from charucoSVGUtil import str2arucoDict
from charuco2svg import charuco2svg
import numpy as np
import cv2
from cv2 import aruco
import glob
import yaml

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("charuco_board_yaml", nargs="?", type=str,default='new_charuco_board.yaml', help="charuco board yaml file location")
parser.add_argument("svg_location", nargs="?", type=str,default='./new_charuco_board.svg', help="svg location")
parser.add_argument("-v", "--verbose", default=False,action='store_true', help="Might show extra info ")
parser.add_argument("-b", "--boardparams", nargs=5, default=[4, 4, 0.05, 0.03, "DICT_6X6_250"],help="type in charuco board parameters directly the format should be \n [rowCount, colCount, squareSize, markerSize, dictionaryName]")
parser.add_argument("-y", "--yaml", default=False, action='store_true',help="indicates that parameters should be loaded from the given/default yaml file. If this is not set the board parameters will be the set/default value of -b")
args = parser.parse_args()

# ChAruco board parameters
bp = {}
dict_string=''
if args.yaml:
    with open(args.charuco_board_yaml, "r") as f:
        yaml_board_params = list(yaml.load_all(f))[0]
    SQUARE_X = yaml_board_params['SQUARE_X']
    SQUARE_Y = yaml_board_params['SQUARE_Y']
    SQUARE_LENGTH = yaml_board_params['SQUARE_LENGTH']
    MARKER_LENGTH = yaml_board_params['MARKER_LENGTH']
    DICTIONARY = str2arucoDict(yaml_board_params['DICTIONARY'])
    dict_string=yaml_board_params['DICTIONARY']
else:
    SQUARE_X = int(args.boardparams[0])
    SQUARE_Y = int(args.boardparams[1])
    SQUARE_LENGTH = float(args.boardparams[2])
    MARKER_LENGTH = float(args.boardparams[3])
    DICTIONARY = str2arucoDict(args.boardparams[4])
    dict_string=args.boardparams[4]

# Creating and drawing charuco board 
charuco2svg(SQUARE_X,SQUARE_Y,SQUARE_LENGTH,MARKER_LENGTH,DICTIONARY,args.svg_location,dict_string)

if args.verbose:
    print("Charuco board image created with size: "+str(CHARUCO_BOARD.getChessboardSize()))

yaml_out = {"DICTIONARY": dict_string, "SQUARE_X": SQUARE_X ,"SQUARE_Y":SQUARE_Y ,"SQUARE_LENGTH":SQUARE_LENGTH , "MARKER_LENGTH":MARKER_LENGTH}

if not args.yaml :
    with open(args.charuco_board_yaml, "w") as f:
        yaml.dump(yaml_out, f)
    print("yaml file created: ")
    print(args.charuco_board_yaml)

