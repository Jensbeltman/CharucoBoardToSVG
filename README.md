# CharucoBoardToSVG

There are two programs to generate Charucoboards.

## make_charucoboards

Generates a set of charucoboard svg files and accompanying JSON files with the parameters

    usage: make_charucoboards.py
    squaresX            The number of columns in the board
    squaresY            The number of rows in the board
    squareLength        The side length of the chessboard square in meters
    markerLength        The side length of the marker square in meters (must be less than squareLength)
    dictionary          See the list below for the supported marker dictionary names
    output_directory    The directory where the boards and parameter files will be written
    [--number_boards NUMBER_BOARDS]  (default is 1)
    [-h]                Generates a help description

This program will call the CharucoBoardToSVG program to create a set of charucoboards.  Please see below for
the description of the parameters.

Example
--

To generate a set of nine 7x7 boards using the APRILTAG_36h11 dictionary:

    python3 make_charucoboards.py 7 7 0.165 0.1 DICT_APRILTAG_36h11 ./boards/7x7_DICT_APRILTAG_36h11 --number_boards=9

The generated files are included in this repository.


## CharucoBoardToSVG

Python script to generate SVG files of specified charuco boards using OpenCV and svgwrite

Run CharucoBoard.py to see the required and optional parameters:

    usage: CharucoBoard.py
    [-h]
    [--start_id START_ID]
    [--board_label BOARD_LABEL]
    [--output_file [OUTPUT_FILE]]
    [--charuco_board_json [CHARUCO_BOARD_JSON]]
    squaresX
    squaresY
    squareLength
    markerLength
    dictionary

The squaresX and squaresY parameter are the number of columns and rows of the chessboard.
The squareLength and markerLength parameters are the size of the square and marker in meters.

Supported marker dictionaries are:

- DICT_4X4_50
- DICT_4X4_100
- DICT_4X4_250
- DICT_4X4_1000
- DICT_5X5_50
- DICT_5X5_100
- DICT_5X5_250
- DICT_5X5_1000
- DICT_6X6_50
- DICT_6X6_100
- DICT_6X6_250
- DICT_6X6_1000
- DICT_7X7_50
- DICT_7X7_100
- DICT_7X7_250
- DICT_7X7_1000
- DICT_APRILTAG_16h5
- DICT_APRILTAG_25h9
- DICT_APRILTAG_36h10
- DICT_APRILTAG_36h11

The board label is optional, and if not specified then one will be created from the dictionary name and the square and
marker sizes.

The start_id is the id of the top left marker on the board.

Example
--

To generate a 7x7 chessboard starting at marker id 24 (which is the first marker of the second board in a set of boards)
using the APRILTAG_36h11 dictionary:

    python3 CharucoBoard.py 7 7 0.165 0.1 DICT_APRILTAG_36h11  --start_id=24 \
    --output_file="./boards/7x7_DICT_APRILTAG_36h11/board2.svg" \
    --charuco_board_json="./boards/7x7_DICT_APRILTAG_36h11/board2.json"

The output directories must exist.

Notes
--
- Needs OpenCV and svgwrite

