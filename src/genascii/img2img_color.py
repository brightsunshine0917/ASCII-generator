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
    parser.add_argument("--input", type=str, default="data/input.jpg", help="Path to input image")
    parser.add_argument("--output", type=str, default="data/output.jpg", help="Path to output text file")
    parser.add_argument("--language", type=str, default="english")
    parser.add_argument("--mode", type=str, default="standard")
    parser.add_argument(
        "--background", type=str, default="black", choices=["black", "white"], help="background's color"
    )
    parser.add_argument("--num_cols", type=int, default=300, help="number of character for output's width")
    parser.add_argument("--scale", type=int, default=2, help="upsize output")
    args = parser.parse_args()
    return args


def main(opt):
    bg_code = (255, 255, 255) if opt.background == "white" else (0, 0, 0)
    char_list, font, sample_character, scale = get_data(opt.language, opt.mode)
    num_chars = len(char_list)
    num_cols = opt.num_cols
    image = cv2.imread(opt.input, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    height, width, _ = image.shape
    cell_width = width / opt.num_cols
    cell_height = scale * cell_width
    num_rows = int(height / cell_height)
    if num_cols > width or num_rows > height:
        print("Too many columns or rows. Use default setting")
        cell_width = 6
        cell_height = 12
        num_cols = int(width / cell_width)
        num_rows = int(height / cell_height)
    char_width, char_height = font.getsize(sample_character)
    out_width = char_width * num_cols
    out_height = scale * char_height * num_rows
    out_image = Image.new("RGB", (out_width, out_height), bg_code)
    draw = ImageDraw.Draw(out_image)
    for rowno in range(num_rows):
        for colno in range(num_cols):
            partial_image = image[
                int(rowno * cell_height) : min(int((rowno + 1) * cell_height), height),
                int(colno * cell_width) : min(int((colno + 1) * cell_width), width),
                :,
            ]
            partial_avg_color = np.sum(np.sum(partial_image, axis=0), axis=0) / (cell_height * cell_width)
            partial_avg_color = tuple(partial_avg_color.astype(np.int32).tolist())
            char = char_list[min(int(np.mean(partial_image) * num_chars / 255), num_chars - 1)]
            draw.text((colno * char_width, rowno * char_height), char, fill=partial_avg_color, font=font)

    cropped_image = ImageOps.invert(out_image).getbbox() if opt.background == "white" else out_image.getbbox()
    out_image = out_image.crop(cropped_image)
    out_image.save(opt.output)


if __name__ == "__main__":
    opt = get_args()
    main(opt)
