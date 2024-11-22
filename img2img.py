"""
@author: Viet Nguyen <nhviet1009@gmail.com>
@author: brightsunshine0917 <https://github.com/brightsunshine0917>
"""

import argparse

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageOps

from utils import get_data


def get_args():
    parser = argparse.ArgumentParser("Image to ASCII")
    parser.add_argument(
        "--input", type=str, default="data/input.jpg", help="Path to input image, by default data/input.jpg"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/output.jpg",
        help="Path to output text file, by default data/output.jpg",
    )
    parser.add_argument("--language", type=str, default="english")
    parser.add_argument("--mode", type=str, default="standard")
    parser.add_argument(
        "--background",
        type=str,
        default="black",
        choices=["black", "white"],
        help="background's color, by default black",
    )
    parser.add_argument(
        "--num_cols", type=int, default=300, help="number of character for output's width, by default 300"
    )
    args = parser.parse_args()
    return args


def main(opt):
    bg_code = 255 if opt.background == "white" else 0
    candidate_chars, font, sample_character, scale = get_data(opt.language, opt.mode)
    num_chars = len(candidate_chars)
    num_cols = opt.num_cols

    image = cv2.imread(opt.input)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    height, width = image.shape
    cell_width = width / opt.num_cols
    cell_height = scale * cell_width
    num_rows = int(height / cell_height)

    if num_cols > width or num_rows > height:
        print("Too many columns or rows. Using default setting")
        cell_width = 6
        cell_height = 12
        num_cols = int(width / cell_width)
        num_rows = int(height / cell_height)

    char_width, char_height = font.getsize(sample_character)
    out_width = char_width * num_cols
    out_height = scale * char_height * num_rows
    out_image = Image.new("L", (out_width, out_height), bg_code)
    draw = ImageDraw.Draw(out_image)

    for rowno in range(num_rows):
        chosen_chars = []
        for colno in range(num_cols):
            block = image[
                int(rowno * cell_height) : min(int((rowno + 1) * cell_height), height),
                int(colno * cell_width) : min(int((colno + 1) * cell_width), width),
            ]
            avg_brightness = np.mean(block) / 255 * num_chars
            chosen_chars.append(candidate_chars[min(int(avg_brightness), num_chars - 1)])
        chosen_chars.append("\n")

        draw.text((0, rowno * char_height), "".join(chosen_chars), fill=255 - bg_code, font=font)

    cropped_image = ImageOps.invert(out_image).getbbox() if opt.background == "white" else out_image.getbbox()
    out_image = out_image.crop(cropped_image)
    out_image.save(opt.output)


if __name__ == "__main__":
    opt = get_args()
    main(opt)
