"""
Orig Author: Viet Nguyen <nhviet1009@gmail.com>
Maintainer: brightsunshine0917 <https://github.com/brightsunshine0917>
"""

import argparse
from pathlib import Path

import cv2
from utils import gen_rowchars


def get_args():
    parser = argparse.ArgumentParser("Image to ASCII")
    parser.add_argument(
        "--input", type=str, default="data/input.jpg", help="Path to input image, by default data/input.jpg"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/output.txt",
        help="Path to output text file, by default data/output.txt",
    )
    parser.add_argument(
        "--mode",
        type=str,
        default="complex",
        choices=["simple", "complex"],
        help="10 or 70 different characters, 70 by default",
    )
    parser.add_argument(
        "--num_cols", type=int, default=150, help="number of character for output's width, 150 by default"
    )
    args = parser.parse_args()
    return args


def main(opt):
    if opt.mode == "simple":
        candidate_chars = "@%#*+=-:. "
    else:
        candidate_chars = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

    num_chars = len(candidate_chars)
    num_cols = opt.num_cols
    image = cv2.imread(opt.input)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    height, width = image.shape
    cell_width = width / opt.num_cols
    cell_height = 2 * cell_width
    num_rows = int(height / cell_height)

    if num_cols > width or num_rows > height:
        print("Too many columns or rows. Using default setting")
        cell_width = 6
        cell_height = 12
        num_cols = int(width / cell_width)
        num_rows = int(height / cell_height)

    output_path = Path(opt.output)
    output_path.parent.mkdir(exist_ok=True, parents=True)
    with open(output_path, "w") as f:
        for rowchars in gen_rowchars(
            image,
            candidate_chars,
            height=height,
            width=width,
            cell_width=cell_width,
            cell_height=cell_height,
            num_chars=num_chars,
            num_rows=num_rows,
            num_cols=num_cols,
        ):
            f.write("".join(rowchars))
            f.write("\n")
    print(f"Output has been saved to {output_path}")


if __name__ == "__main__":
    opt = get_args()
    main(opt)
