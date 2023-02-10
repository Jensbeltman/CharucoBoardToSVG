import argparse
import json
import pathlib

from CharucoBoard import Charuco2Svg
from arucoUtililties import toDict


def prepare_argument_parser():
    parser = argparse.ArgumentParser(
        description="Generates a set of charucoboard svg files and accompanying JSON files with the parameters")
    parser.add_argument('squaresX', type=int, help="The number of columns in the board")
    parser.add_argument('squaresY', type=int, help="The number of rows in the board")
    parser.add_argument('squareLength', type=float,
                        help="The side length of the chessboard square in meters")
    parser.add_argument('markerLength', type=float,
                        help="The side length of the marker square in meters (must be less than the squareLength)")
    parser.add_argument('dictionary', type=str, help="dictionary parameter used for OpenCv charuco board initialization")
    parser.add_argument("output_directory",  help="Path to the output directory")
    parser.add_argument("--number_boards", type=int, default=1, help="The number of boards to generate")
    return parser


def main(args):
    if args.markerLength >= args.squareLength:
        raise ValueError(f"A marker with side length {args.markerLength} will not fit in a "
                         f"square that has a side length of {args.squareLength} ")

    output_directory = pathlib.Path(args.output_directory)
    if not output_directory.exists():
        raise FileNotFoundError(f"The specified output directory {str(output_directory)} doesn't exist")

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
        Charuco2Svg(**params, svg_path=output_svg_file).generate_svg()
        print(f"Saved charuco board as {output_svg_file}")


if __name__ == "__main__":
    program_arguments = prepare_argument_parser().parse_args()
    main(program_arguments)
