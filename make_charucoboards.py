"""
Copyright 2023 Felix & Paul Studios Inc.  MIT license

This program calls an instance of the class Charuco2Svg to create a set of charucoboards in various formats and
write JSON files with the board parameters.

usage: make_charucoboards.py [-h] [--number_boards NUMBER_BOARDS] [--output_png {0,1}] \
        [--png_width PNG_WIDTH] [--png_height PNG_HEIGHT] [--output_pdf {0,1}] [--pdf_dpi PDF_DPI]
    squaresX squaresY squareLength markerLength dictionary output_directory

"""

import argparse
import json
import pathlib

from CharucoBoard import Charuco2Svg, supported_dictionaries
from arucoUtililties import toDict

# For conversion of the SVG to PNG and PDF
import cairosvg


def prepare_argument_parser():
    parser = argparse.ArgumentParser(
        description="Generates a set of charucoboard svg files and accompanying JSON files with the parameters")
    parser.add_argument('squaresX', type=int, help="The number of columns in the board")
    parser.add_argument('squaresY', type=int, help="The number of rows in the board")
    parser.add_argument('squareLength', type=float, default=0.,
                        help="The side length of the chessboard square in meters")
    parser.add_argument('markerLength', type=float, default=0.,
                        help="The side length of the marker square in meters (must be less than the squareLength)")
    parser.add_argument('dictionary', type=str,
                        help="dictionary parameter used for OpenCv charuco board initialization; "
                             f"must be one of  {', '.join(supported_dictionaries)}")
    parser.add_argument("output_directory",  help="Path to the output directory")
    parser.add_argument("--number_boards", type=int, default=1, help="The number of boards to generate")
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

    dictionary = toDict(args.dictionary)
    number_markers_in_dictionary = dictionary.bytesList.shape[0]
    markers_per_board = (args.squaresX * args.squaresY) // 2
    number_markers_needed = args.number_boards * markers_per_board

    if number_markers_needed > number_markers_in_dictionary:
        raise ValueError(f"The number of markers {number_markers_in_dictionary} in the dictionary {args.dictionary} "
                         f"isn't enough for {args.number_boards} boards:  {number_markers_needed} markers needed")

    board_label = f"{args.dictionary[len('DICT_'):]}, {args.squareLength}, {args.markerLength}"

    for board_number in range(args.number_boards):
        start_id = markers_per_board * board_number
        params = {'squaresX': args.squaresX, 'squaresY': args.squaresY, 'squareLength': args.squareLength,
                  'markerLength': args.markerLength, 'dict_string': args.dictionary, 'start_id': start_id,
                  'board_label': board_label}

        output_json_file = output_directory / f"board_{board_number}.json"
        with open(output_json_file, 'w') as outfile:
            json.dump(params, outfile, indent=4)
        print(f"Wrote charuco board params to {output_json_file}")

        output_svg_file = output_directory / f"board_{board_number}.svg"
        svg_data = Charuco2Svg(svg_path=output_svg_file, **params).generate_svg()
        print(f"Saved charuco board as {output_svg_file}")

        if args.output_png:
            output_png_file = output_directory / f"board_{board_number}.png"
            cairosvg.svg2png(svg_data.tostring(), output_width=args.png_width, output_height=args.png_height,
                             write_to=str(output_png_file))
            print(f"Saved png version as {output_png_file}")

        if args.output_pdf:
            board = Charuco2Svg(svg_path=output_svg_file, **params,
                                border_dimensions=[args.pdf_bleed * m_per_mm, args.pdf_margin * m_per_mm])
            svg_data = board.generate_svg()
            output_width = round(args.squareLength * (args.squaresX + 2 * board.border_size) * pixels_per_m)
            output_height = round(args.squareLength * (args.squaresY + 2 * board.border_size) * pixels_per_m)
            output_pdf_file = output_directory / f"board_{board_number}.pdf"
            cairosvg.svg2pdf(svg_data.tostring(), dpi=args.pdf_dpi, write_to=str(output_pdf_file),
                             output_width=int(output_width), output_height=int(output_height),
                             background_color="white")
            print(f"Saved pdf version as {output_pdf_file}")


if __name__ == "__main__":
    program_arguments = prepare_argument_parser().parse_args()
    main(program_arguments)
