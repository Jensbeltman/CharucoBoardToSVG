from charuco_dict_integer_from_string import str2arucoDict
import numpy as np
import cv2
from cv2 import aruco
import glob
import svgwrite
from svgwrite import cm, mm




def markerPixelWidth(s, include_boarder = True):
    for i in range(1, 10):
        if s.find('X'+str(i)) is not -1:
            if include_boarder:
                return i+2 #+2 beacause of the black border on each marker
            else :
                return i

def draw_aruco(dwg, bit_mask, p, pxs, pxsize):
    offsetx = p[0]+pxsize
    offsety = p[1]+pxsize
    dwg.add(dwg.rect(insert=(p[0]*100*cm, p[1]*100*cm),
                     size=(pxsize*pxs*100*cm, pxsize*pxs*100*cm), fill='black'))
    for y in range(bit_mask.shape[0]):
        for x in range(bit_mask.shape[1]):
            if bit_mask[y, x] == 1:
                dwg.add(dwg.rect(insert=((offsetx+x*pxsize)*100*cm, (offsety+y*pxsize)
                                         * 100*cm), size=(pxsize*100*cm, pxsize*100*cm), fill='white'))

# Creating and drawing charuco board


def charuco2svg(SQUARE_X, SQUARE_Y, SQUARE_LENGTH, MARKER_LENGTH, DICT, SVG_PATH, DICT_STRING):
    CHARUCO_BOARD = cv2.aruco.CharucoBoard_create(
        SQUARE_Y, SQUARE_X, SQUARE_LENGTH, MARKER_LENGTH, DICT)
    print(CHARUCO_BOARD.ids)

    pxpm = markerPixelWidth(DICT_STRING)
    board_markers = np.zeros((len(CHARUCO_BOARD.ids), pxpm-2, pxpm-2))#-2 to not waste memory on white boarder

    id_cnt = 0
    for ids in CHARUCO_BOARD.ids:
        marker_img = aruco.drawMarker(DICT, ids, pxpm)
        cv2.imshow('image', marker_img)
        cv2.waitKey()
        marker_img = marker_img[1:pxpm-1, 1:pxpm-1]
        bit_mask = np.zeros(marker_img.shape)
        bit_mask[marker_img > 0] = 1
        board_markers[id_cnt] = (bit_mask)
        id_cnt += 1

    dwg = svgwrite.Drawing(SVG_PATH, size=(
        SQUARE_X*SQUARE_LENGTH*100*cm, SQUARE_Y*SQUARE_LENGTH*100*cm), profile='full')

    marker_offset = (SQUARE_LENGTH-MARKER_LENGTH)/2
    px_size = float(MARKER_LENGTH/pxpm)

    even_rows = ((SQUARE_Y % 2) == 0)
    id_cnt = 0
    for y in range(SQUARE_Y):
        for x in range( ):
            if even_rows:
                if ((x % 2) != 0 and (y % 2) == 0) or ((x % 2) == 0 and (y % 2) != 0):
                    dwg.add(dwg.rect(insert=(x*SQUARE_LENGTH*100*cm, y*SQUARE_LENGTH*100*cm),
                                     size=(SQUARE_LENGTH*100*cm, SQUARE_LENGTH*100*cm), fill='black'))
                elif ((x % 2) == 0 and (y % 2) == 0) or ((x % 2) != 0 and (y % 2) != 0):
                    draw_aruco(dwg, board_markers[id_cnt], (
                        x*SQUARE_LENGTH+marker_offset, y*SQUARE_LENGTH+marker_offset), pxpm, px_size)
                    id_cnt += 1
            if not even_rows:
                if ((x % 2) == 0 and (y % 2) == 0) or ((x % 2) != 0 and (y % 2) != 0):
                    dwg.add(dwg.rect(insert=(x*SQUARE_LENGTH*100*cm, y*SQUARE_LENGTH*100*cm),
                                     size=(SQUARE_LENGTH*100*cm, SQUARE_LENGTH*100*cm), fill='black'))
                elif ((x % 2) == 0 and (y % 2) != 0) or ((x % 2) != 0 and (y % 2) == 0):
                    draw_aruco(dwg, board_markers[id_cnt], (
                        x*SQUARE_LENGTH+marker_offset, y*SQUARE_LENGTH+marker_offset), pxpm, px_size)
                    id_cnt += 1

    dwg.save()
