"""
@author: Viet Nguyen <nhviet1009@gmail.com>
"""

import argparse
from pathlib import Path

import cv2
import numpy as np


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
        CHAR_LIST = "@%#*+=-:. "
    else:
        CHAR_LIST = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
    num_chars = len(CHAR_LIST)
    num_cols = opt.num_cols
    image = cv2.imread(opt.input)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    height, width = image.shape
    cell_width = width / opt.num_cols
    cell_height = 2 * cell_width
    num_rows = int(height / cell_height)
    if num_cols > width or num_rows > height:
        print("Too many columns or rows. Use default setting")
        cell_width = 6
        cell_height = 12
        num_cols = int(width / cell_width)
        num_rows = int(height / cell_height)

    output_path = Path(opt.output)
    output_path.parent.mkdir(exist_ok=True, parents=True)
    with open(output_path, "w") as f:
        for i in range(num_rows):
            for j in range(num_cols):
                f.write(
                    CHAR_LIST[
                        min(
                            int(
                                np.mean(
                                    image[
                                        int(i * cell_height) : min(int((i + 1) * cell_height), height),
                                        int(j * cell_width) : min(int((j + 1) * cell_width), width),
                                    ]
                                )
                                * num_chars
                                / 255
                            ),
                            num_chars - 1,
                        )
                    ]
                )
            f.write("\n")
    print(f"Output has been saved to {output_path}")


if __name__ == "__main__":
    opt = get_args()
    main(opt)
