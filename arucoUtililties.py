import numpy as np
import re
import cv2

april_tag_size_matcher = re.compile(r"DICT_APRILTAG_([0-9]{2})")
aruco_tag_size_matcher = re.compile(r"DICT_([0-9]{1})X")

# Marker dictionaries
dictionaries = ['DICT_4X4_50', 'DICT_4X4_100', 'DICT_4X4_250', 'DICT_4X4_1000', 'DICT_5X5_50', 'DICT_5X5_100',
                'DICT_5X5_250', 'DICT_5X5_1000', 'DICT_6X6_50', 'DICT_6X6_100', 'DICT_6X6_250', 'DICT_6X6_1000',
                'DICT_7X7_50', 'DICT_7X7_100', 'DICT_7X7_250', 'DICT_7X7_1000', 'DICT_APRILTAG_16h5',
                'DICT_APRILTAG_25h9', 'DICT_APRILTAG_36h10', 'DICT_APRILTAG_36h11']


def toDict(dict_string):
    return cv2.aruco.getPredefinedDictionary(getattr(cv2.aruco, dict_string))


def markerWidth(dict_string, include_border=True):
    # When include_border, +2 because of the black border on each marker
    # This value assumes that the border_bits parameter for cv.aruco.drawMarker() is = 1 (the default)
    if "APRIL" in dict_string:
        match = april_tag_size_matcher.match(dict_string)
        if match:
            return int(np.sqrt(float(match.group(1)))) + (2 if include_border else 0)
    else:
        match = aruco_tag_size_matcher.match(dict_string)
        if match:
            return int(match.group(1)) + (2 if include_border else 0)

    raise ValueError(f"{dict_string} was not supported as a tag dictionary type")


def getMarkers(ids, DICT, pxpm, start_id=0):
    markerImg = [cv2.aruco.drawMarker(DICT, id+start_id, pxpm) for id in ids.astype(int)]
    return markerImg
