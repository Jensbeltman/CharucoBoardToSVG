# CharucoBoardToSVG

There are two programs to generate Charucoboards.

## make_charucoboards

Generates a set of charucoboard SVG files and accompanying JSON files with the parameters, with PNG and PDF versions too.

    usage: make_charucoboards.py [-h] [--number_boards NUMBER_BOARDS] [--output_png {0,1}] \
        [--png_width PNG_WIDTH] [--png_height PNG_HEIGHT] [--output_pdf {0,1}] [--pdf_dpi PDF_DPI]
    squaresX squaresY squareLength markerLength dictionary output_directory
    
    Generates a set of charucoboard svg files and accompanying JSON files with the parameters
    
    positional arguments:
    squaresX              The number of columns in the board
    squaresY              The number of rows in the board
    squareLength          The side length of the chessboard square in meters
    markerLength          The side length of the marker square in meters (must be less than the squareLength)
    dictionary            dictionary parameter used for OpenCv charuco board initialization
    output_directory      Path to the output directory
    
    optional arguments:
    -h, --help                          show this help message and exit
    --number_boards NUMBER_BOARDS       The number of boards to generate (default 1)
    --output_png {0,1}                  Also output PNG files (default 1)
    --png_width PNG_WIDTH               Specify the width of the PNG image in pixels (default 2048)
    --png_height PNG_HEIGHT             Specify the height of the PNG image in pixels (default 2048)
    --output_pdf {0,1}                  Also output PDF files (default 1)
    --pdf_dpi PDF_DPI                   The resolution of the PDF image (default 600)


This program will call the CharucoBoardToSVG program to create a set of charucoboards.  Please see below for
the description of the parameters.

Boards with an even number of rows and columns are preferred since a corner will be at the center of the board.

Example
--

To generate a set of nine 6x6 boards using the DICT_4X4_250 dictionary:

```shell
python3 make_charucoboards.py 6 6 0.165 0.1 DICT_4X4_250 ./boards/6x6_DICT_4X4_250 --number_boards=9
```
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

Internally, the list is obtained from OpenCV, so if more formats are added in future, they will be automatically
supported (provided the naming isn't changed to much).

The board label is optional, and if not specified then one will be created from the dictionary name and the square and
marker sizes.

The start_id is the id of the top left marker on the board.

Example
--

To generate a 7x7 chessboard starting at marker id 24 (which is the first marker of the second board in a set of boards)
using the APRILTAG_36h11 dictionary:

```shell
python3 CharucoBoard.py 7 7 0.165 0.1 DICT_APRILTAG_36h11  --start_id=24 \
    --output_file="./boards/7x7_DICT_APRILTAG_36h11/board2.svg" \
    --charuco_board_json="./boards/7x7_DICT_APRILTAG_36h11/board2.json"
```

The output directories must exist.

Notes
--
- Needs OpenCV as well as the requirements given in the requirements.txt file

