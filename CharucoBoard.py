import pathlib

import cv2
import arucoUtililties as au
import svgwrite
from svgwrite import cm
import json
import argparse


class Charuco2Svg(object):
    def __init__(self, squaresX, squaresY, squareLength, markerLength, dict_string, start_id=0,
                 board_label="", svg_path=''):
        # Variable Parsing
        self.squares_x = squaresX
        self.squares_y = squaresY
        self.square_length = squareLength
        self.marker_length = markerLength
        self.dict_string = dict_string
        self.dictionary = au.toDict(self.dict_string)
        self.start_id = start_id
        self.board_label = board_label

        # OpenCV objects
        self.charucoBoard = cv2.aruco.CharucoBoard_create(self.squares_x, self.squares_y, self.square_length,
                                                          self.marker_length, self.dictionary)
        number_markers = self.dictionary.bytesList.shape[0]
        if self.start_id + (self.squares_x * self.squares_y)//2  > number_markers:
            raise ValueError(f"The number of markers {number_markers} in the dictionary {self.dict_string} isn't"
                             f"enough when the start id is {self.start_id}")

        # SVG related objects and variables
        self.marker_width = au.markerWidth(self.dict_string)
        self.px_m = self.marker_length / self.marker_width
        self.markerOffset = ((self.square_length - self.marker_length) / 2.0)
        self.drawing = svgwrite.Drawing(svg_path,
                                        size=(self.squares_x * self.square_length * 100 * cm,
                                              self.squares_y * self.square_length * 100 * cm),
                                        profile='full')

    def draw_marker(self, marker_image, point):
        self.drawing.add(self.drawing.rect(insert=(point[0] * 100 * cm, point[1] * 100 * cm),
                                           size=(self.marker_length * 100 * cm, self.marker_length * 100 * cm),
                                           fill='black', shape_rendering="crispEdges"))
        for y in range(marker_image.shape[0]):
            for x in range(marker_image.shape[1]):
                if marker_image[y][x] == 255:
                    self.drawing.add(self.drawing.rect(
                        insert=((point[0] + x * self.px_m) * 100 * cm, (point[1] + y * self.px_m) * 100 * cm),
                        size=(self.px_m * 100 * cm, self.px_m * 100 * cm), fill='white', shape_rendering="crispEdges"))

    def generate_svg(self):
        oddRows = self.squares_y % 2
        markerPositions = [[oddRows == (i + j) % 2 for i in range(self.squares_x)] for j in range(self.squares_y)]
        markers = au.getMarkers(self.charucoBoard.ids.flatten(), self.dictionary, self.marker_width, self.start_id)
        marker_ids = [f"{marker_index + self.start_id}" for marker_index in range(len(markers))]

        markerIdx = 0
        for y in range(self.squares_y):
            for x in range(self.squares_x):
                if markerPositions[y][x]:
                    self.drawing.add(
                        self.drawing.rect(insert=(x * self.square_length * 100 * cm, y * self.square_length * 100 * cm),
                                          size=(self.square_length * 100 * cm, self.square_length * 100 * cm),
                                          fill='white', shape_rendering="crispEdges"))
                    self.draw_marker(markers[markerIdx], (
                        x * self.square_length + self.markerOffset, y * self.square_length + self.markerOffset))

                    # Label the marker with its id in the top left corner
                    offset_x = x + 0.05
                    offset_y = y + 0.075
                    self.drawing.add(self.drawing.text(marker_ids[markerIdx],
                                                       insert=(offset_x * self.square_length * 100 * cm,
                                                               offset_y * self.square_length * 100 * cm),
                                                       fill='black', font_size=self.square_length * 5 * cm,
                                                       font_family="Arial, Helvetica, sans-serif",
                                                       shape_rendering="crispEdges"))
                    markerIdx += 1
                else:
                    self.drawing.add(
                        self.drawing.rect(insert=(x * self.square_length * 100 * cm, y * self.square_length * 100 * cm),
                                          size=(self.square_length * 100 * cm, self.square_length * 100 * cm),
                                          fill='black', shape_rendering="crispEdges"))

        # Label the board in top left black square
        offset_x = 0.1 if ((self.squares_x % 2) == 1) else 1.1      # in square_length units
        offset_y = 0.1
        self.drawing.add(self.drawing.text(self.board_label,
                                           insert=(offset_x * self.square_length * 100 * cm,
                                                   offset_y * self.square_length * 100 * cm),
                                           fill='white', font_size=self.square_length * 5 * cm,
                                           font_family="Arial, Helvetica, sans-serif",
                                           shape_rendering="crispEdges"))
        self.drawing.save()


def prepare_argument_parser():
    parser = argparse.ArgumentParser(
        description="Generates a charucoBoard svg file and also a JSON file with the parameters")
    parser.add_argument('squaresX', type=int, help="squaresX parameter used for OpenCv charuco board initialization")
    parser.add_argument('squaresY', type=int, help="squaresY parameter used for OpenCv charuco board initialization")
    parser.add_argument('squareLength', type=float,
                        help="squareLength parameter used for OpenCv charuco board initialization")
    parser.add_argument('markerLength', type=float,
                        help="markerLength parameter used for OpenCv charuco board initialization")
    parser.add_argument('dictionary', type=str, help="dictionary parameter used for OpenCv charuco board initialization")
    parser.add_argument("--start_id", type=int, default=0, help="The id of the first marker on the board")
    parser.add_argument("--board_label", type=str, default="",
                        help="A label for the board; the default will be:"
                             " dictionary name, squareLength, markerLength")
    parser.add_argument("--output_file", nargs="?", default='./charucoBoard.svg', help="output svg file")
    parser.add_argument("--charuco_board_json", nargs="?", default='./charucoBoard.json',
                        help="output charuco board JSON file")
    return parser


def main(args):
    # pre-flight the output locations
    output_files = [getattr(args, n, "") for n in ['output_file', 'charuco_board_json']]
    for output_file in output_files:
        if not output_file:
            continue
        directory = pathlib.Path(output_file).parent
        if not directory.exists():
            raise FileNotFoundError(f"The specified output directory {directory} doesn't exist")

    board_label = args.board_label
    if not board_label:
        board_label = f"{args.dictionary[len('DICT_'):]}, {args.squareLength}, {args.markerLength}"

    params = {'squaresX': args.squaresX, 'squaresY': args.squaresY, 'squareLength': args.squareLength,
              'markerLength': args.markerLength, 'dict_string': args.dictionary, 'start_id': args.start_id,
              'board_label': board_label}

    with open(args.charuco_board_json, 'w') as outfile:
        json.dump(params, outfile, indent=4)
    print("Wrote charuco board params to {}".format(args.charuco_board_json))

    Charuco2Svg(**params, svg_path=args.output_file).generate_svg()
    print("Saved charuco board as {}".format(args.output_file))


if __name__ == "__main__":
    program_arguments = prepare_argument_parser().parse_args()
    main(program_arguments)
