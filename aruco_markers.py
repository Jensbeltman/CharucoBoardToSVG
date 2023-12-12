import pathlib
import typing

import cv2
import arucoUtililties as au
import svgwrite
from svgwrite import cm
import json
import argparse

# For conversion of the SVG to PNG and PDF
import cairosvg

supported_dictionaries = [s for s in dir(cv2.aruco) if s.startswith('DICT_')]


class ArucoGrid2Svg(object):
    def __init__(self, squaresX, squaresY, squareLength, markerLength, dict_string, start_id=0, board_label="",
                 svg_path='', border_dimensions: [None, typing.Tuple[float, float]] = None):
        """
        Create an SVG drawing for an array of Aruco markers (which may have another marker design than Aruco)
        This is different from a Charucoboard since there are no black squares
        :param squaresX:        The number of columns of squares
        :param squaresY:        The number of rows of squares
        :param squareLength:    The side length of a square in meters
        :param markerLength:    The side length of a marker in meters (must be less than squareLength)
        :param dict_string:     The name of the marker dictionary
        :param start_id:        The starting id in the marker dicctionary
        :param board_label:     A text label for the board (inserted on top leftmost black square)
        :param svg_path:        The path to the SVG file
        :param border_dimensions:   None, or a tuple of dimensions (bleed size, margin size) in meters
        """
        # Variable Parsing
        self.squares_x = squaresX
        self.squares_y = squaresY
        self.square_length = squareLength
        self.marker_length = markerLength
        self.dict_string = dict_string
        self.dictionary = au.toDict(self.dict_string)
        self.start_id = start_id
        self.board_label = board_label

        # Allow for two zones around the board, the bleed and the margin.  The board material is trimmed at the
        # interface of these two zones.  See: https://en.wikipedia.org/wiki/Bleed_(printing)
        if border_dimensions is not None:
            self.bleed = border_dimensions[0] / self.square_length
            self.margin = border_dimensions[1] / self.square_length
            self.border_size = (self.bleed + self.margin)       # in squareLength units
            self.crop_line_length = 0.25  # in squareLength units
        else:
            self.border_size = 0.

        self.text_scale = 0.1   # in squareLength units
        self.unit = cm
        self.unit_multiplier = 100

        # OpenCV objects
        self.board = cv2.aruco.GridBoard_create(self.squares_x, self.squares_y, self.marker_length,
                                                self.square_length,
                                                self.dictionary, self.start_id)
        number_markers = self.dictionary.bytesList.shape[0]
        if self.start_id + (self.squares_x * self.squares_y)//2  > number_markers:
            raise ValueError(f"The number of markers {number_markers} in the dictionary {self.dict_string} isn't"
                             f"enough when the start id is {self.start_id}")

        # SVG related objects and variables
        self.marker_width = au.markerWidth(self.dict_string)
        self.px_m = self.marker_length / self.marker_width
        self.markerOffset = ((self.square_length - self.marker_length) / 2.0)
        self.drawing = svgwrite.Drawing(svg_path,
                                        size=(self.unit_str((self.squares_x + 2 * self.border_size) *
                                                            self.square_length),
                                              self.unit_str((self.squares_y + 2 * self.border_size) *
                                                            self.square_length)),
                                        profile='full')

    def unit_str(self, x):
        return x * self.unit_multiplier * self.unit

    def draw_marker(self, marker_image, point):
        self.drawing.add(self.drawing.rect(insert=(self.unit_str(point[0]), self.unit_str(point[1])),
                                           size=(self.unit_str(self.marker_length),
                                                 self.unit_str(self.marker_length)),
                                           fill='black', shape_rendering="crispEdges"))
        # Some PDF renderers produce a line between the whites squares.  To circumvent this, enlarge the rectangle
        # by the maximum amount in the vertical and then horizontal directions, leading to overlapping rectangles
        for x in range(marker_image.shape[1]):
            for y in range(marker_image.shape[0]):
                start_y = y
                if marker_image[y][x] == 255:
                    while y <= marker_image.shape[0]:
                        if marker_image[y+1][x] == 255:
                            y += 1
                        else:
                            break
                    self.drawing.add(self.drawing.rect(
                        insert=(self.unit_str(point[0] + x * self.px_m), self.unit_str(point[1] + start_y * self.px_m)),
                        size=(self.unit_str(self.px_m), self.unit_str((y - start_y + 1) * self.px_m)), fill='white',
                        shape_rendering="crispEdges"))

        for y in range(marker_image.shape[0]):
            for x in range(marker_image.shape[1]):
                start_x = x
                if marker_image[y][x] == 255:
                    while x <= marker_image.shape[1]:
                        if marker_image[y][x+1] == 255:
                            x += 1
                        else:
                            break
                    self.drawing.add(self.drawing.rect(
                        insert=(self.unit_str(point[0] + start_x * self.px_m), self.unit_str(point[1] + y * self.px_m)),
                        size=(self.unit_str((x - start_x + 1) * self.px_m), self.unit_str(self.px_m)), fill='white',
                        shape_rendering="crispEdges"))

    def generate_svg(self):
        markers = au.getMarkers(self.board.ids.flatten(), self.dictionary, self.marker_width)
        marker_ids = [f"{marker_index + self.start_id}" for marker_index in range(len(markers))]

        # Draw the squares
        markerIdx = 0
        for y in range(self.squares_y):
            for x in range(self.squares_x):
                self.drawing.add(
                    self.drawing.rect(insert=(self.unit_str((x + self.border_size) * self.square_length),
                                              self.unit_str((y + self.border_size) * self.square_length)),
                                      size=(self.unit_str(self.square_length), self.unit_str(self.square_length)),
                                      fill='white', shape_rendering="crispEdges"))
                self.draw_marker(markers[markerIdx], (
                    (x + self.border_size) * self.square_length + self.markerOffset,
                    (y + self.border_size) * self.square_length + self.markerOffset))

                # Label the marker with its id in the top left corner
                offset_x = x + self.border_size + 0.5     # Add 0.5 to center the id in the square horizontally
                offset_y = y + self.border_size + self.text_scale
                self.drawing.add(self.drawing.text(marker_ids[markerIdx],
                                                   insert=(self.unit_str(offset_x * self.square_length),
                                                           self.unit_str(offset_y * self.square_length)),
                                                   fill='black', text_anchor="middle",
                                                   font_size=self.unit_str(self.square_length * self.text_scale),
                                                   font_family="Arial, Helvetica, sans-serif",
                                                   shape_rendering="crispEdges"))
                markerIdx += 1

        if self.border_size > 0:
            # Add lines for crop marks at the corners
            lines = [(self.bleed, self.bleed, 1, 0), (self.bleed, self.bleed, 0, 1),
                     (self.squares_x + self.border_size + self.margin, self.bleed, -1, 0),
                     (self.squares_x + self.border_size + self.margin, self.bleed, 0, 1),
                     (self.bleed, self.squares_y + self.border_size + self.margin, 1, 0),
                     (self.bleed, self.squares_y + self.border_size + self.margin, 0, -1),
                     (self.squares_x + self.border_size + self.margin,
                     self.squares_y + self.border_size + self.margin, -1, 0),
                     (self.squares_x + self.border_size + self.margin,
                      self.squares_y + self.border_size + self.margin, 0, -1)]
            for (x, y, dir_x, dir_y) in lines:
                self.drawing.add(self.drawing.line(
                    start=(self.unit_str((x - dir_x * self.bleed) * self.square_length),
                           self.unit_str((y - dir_y * self.bleed) * self.square_length)),
                    end=(self.unit_str((x + dir_x * self.crop_line_length) * self.square_length),
                         self.unit_str((y + dir_y * self.crop_line_length) * self.square_length)),
                    shape_rendering="crispEdges", stroke="black", stroke_width=1, fill="none"))

        self.drawing.save()
        return self.drawing


def prepare_argument_parser():
    parser = argparse.ArgumentParser(
        description="Generates an Aruco grid board svg file and also a JSON file with the parameters")
    parser.add_argument('squaresX', type=int, help="The number of columns in the board")
    parser.add_argument('squaresY', type=int, help="The number of rows in the board")
    parser.add_argument('squareLength', type=float, default=0.,
                        help="The side length of the chessboard square in meters")
    parser.add_argument('markerLength', type=float, default=0.,
                        help="The side length of the marker square in meters (must be less than the squareLength)")
    parser.add_argument('dictionary', type=str,
                        help="dictionary parameter used for OpenCv Aruco grid board initialization; must be one of "
                             f"{', '.join(supported_dictionaries)}")
    parser.add_argument("output_directory",  help="Path to the output directory")
    parser.add_argument("--start_id", type=int, default=0, help="The id of the first marker on the board")
    parser.add_argument("--board_label", type=str, default="",
                        help="A label for the board; the default will be:"
                             " dictionary name, squareLength, markerLength")
    parser.add_argument("--output_file", nargs="?", default='./board.svg', help="output svg file")
    parser.add_argument("--board_json", nargs="?", default='./board.json',
                        help="output board JSON file")
    parser.add_argument("--output_png", type=int, choices=(0, 1), default=1, help="Also output PNG files")
    parser.add_argument("--png_width", type=int, default=2048, help="Specify the width of the PNG image in pixels")
    parser.add_argument("--png_height", type=int, default=2048, help="Specify the height of the PNG image in pixels")
    parser.add_argument("--output_pdf", type=int, choices=(0, 1), default=1, help="Also output PDF files")
    parser.add_argument("--pdf_dpi", type=int, default=600, help="The resolution of the PDF image")
    parser.add_argument("--pdf_bleed", type=float, default=6.35, help="Size of bleed zone in mm, for PDF output only")
    parser.add_argument("--pdf_margin", type=float, default=10., help="Size of margin zone in mm, for PDF output only")
    return parser


def main(args):
    inches_per_m = 1 / 0.0254
    pixels_per_m = args.pdf_dpi * inches_per_m
    m_per_mm = 1/1000.

    if args.markerLength >= args.squareLength:
        raise ValueError(f"A marker with side length {args.markerLength} will not fit in a "
                         f"square that has a side length of {args.squareLength} ")

    output_directory = pathlib.Path(args.output_directory)
    if not output_directory.exists():
        raise FileNotFoundError(f"The specified output directory {str(output_directory)} doesn't exist")

    # Marker dictionaries
    if args.dictionary not in supported_dictionaries:
        ValueError(f"The '{args.dictionary}' value for the dictionary is not supported. "
                   f"Please use -h to see the values")

    dictionary = au.toDict(args.dictionary)
    number_markers_in_dictionary = dictionary.bytesList.shape[0]
    markers_per_board = (args.squaresX * args.squaresY) // 2
    number_markers_needed = markers_per_board

    if number_markers_needed > number_markers_in_dictionary:
        raise ValueError(f"The number of markers {number_markers_in_dictionary} in the dictionary {args.dictionary} "
                         f"isn't enough for {args.number_boards} boards:  {number_markers_needed} markers needed")

    board_label = f"{args.dictionary[len('DICT_'):]}, {args.squareLength}, {args.markerLength}"

    params = {'squaresX': args.squaresX, 'squaresY': args.squaresY, 'squareLength': args.squareLength,
              'markerLength': args.markerLength, 'dict_string': args.dictionary, 'start_id': args.start_id,
              'board_label': board_label}

    output_json_file = output_directory / f"board.json"
    with open(output_json_file, 'w') as outfile:
        json.dump(params, outfile, indent=4)
    print(f"Wrote board params to {output_json_file}")

    output_svg_file = output_directory / f"board.svg"
    svg_data = ArucoGrid2Svg(svg_path=str(output_svg_file), **params).generate_svg()
    print(f"Saved board as {output_svg_file}")

    if args.output_png:
        output_png_file = output_directory / f"board.png"
        cairosvg.svg2png(svg_data.tostring(), output_width=args.png_width, output_height=args.png_height,
                         write_to=str(output_png_file))
        print(f"Saved png version as {output_png_file}")

    if args.output_pdf:
        board = ArucoGrid2Svg(svg_path=str(output_svg_file), **params,
                              border_dimensions=[args.pdf_bleed * m_per_mm, args.pdf_margin * m_per_mm])
        svg_data = board.generate_svg()
        output_width = round(args.squareLength * (args.squaresX + 2 * board.border_size) * pixels_per_m)
        output_height = round(args.squareLength * (args.squaresY + 2 * board.border_size) * pixels_per_m)
        output_pdf_file = output_directory / f"board.pdf"
        cairosvg.svg2pdf(svg_data.tostring(), dpi=args.pdf_dpi, write_to=str(output_pdf_file),
                         output_width=int(output_width), output_height=int(output_height),
                         background_color="white")
        print(f"Saved pdf version as {output_pdf_file}")


if __name__ == "__main__":
    program_arguments = prepare_argument_parser().parse_args()
    main(program_arguments)
