# CharucoBoardToSVG

There are two programs to generate Charucoboards.  There is also a program to create a single board with a grid of markers.

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
    --pdf_bleed PDF_BLEED               Size of bleed zone in mm, for PDF output only (default 6.35 mm)
    --pdf_margin PDF_MARGIN             Size of margin zone in mm, for PDF output only (default 10 mm)


This program will call the CharucoBoardToSVG program to create a set of charucoboards.  Please see below for
the description of the parameters.

Boards with an even number of rows and columns are preferred since then there will be a corner point at the center of the board.

Example
--

To generate a set of nine 6x6 boards using the DICT_4X4_250 dictionary:

```shell
python3 make_charucoboards.py 6 6 0.165 0.1 DICT_4X4_250 ./boards/6x6_DICT_4X4_250 --number_boards=9
```
The generated files are included in this repository.  

The example 6x6 and 8x8 boards are 36 inches square.  The example 8x6 board is 24 inches by 18 inches.

The PDF files are slightly different from the other two image formats, since crop marks are added around the boards.
The crop marks are at the interface between the bleed and margin zones; the material outside the crop marks is
the bleed zone and this is what is discarded by the crop.  The margin provides an area that may
be used to hold the board (in a frame, for example).


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
supported (provided the naming isn't changed too much).

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

## aruco_makers

This program will create a grid of Aruco markers, in the same way as the make_charucoboards program, but with no black 
squares.  
The same command line arguments are used (except without the --number_boards option).
This program will also create the same four types of files (.json, .png, .svg and .pdf).
