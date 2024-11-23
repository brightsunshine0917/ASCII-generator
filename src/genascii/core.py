#!/usr/bin/env python3

import argparse
import json
from pathlib import Path

from .consts import ALPHABETS_PATH
from .utils import gen_colored_char, gen_rowchars, get_data, get_size

with open(ALPHABETS_PATH, "rb") as f:
    LANG_CHARINFO = json.load(f)


def img2txt(opt: argparse.Namespace):
    import cv2

    candidate_chars = LANG_CHARINFO["general"]["modes"][opt.mode]

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


def img2img(opt: argparse.Namespace):
    import cv2
    from PIL import Image, ImageDraw, ImageOps

    if opt.color:
        bg_code = (255, 255, 255) if opt.background == "white" else (0, 0, 0)
    else:
        bg_code = 255 if opt.background == "white" else 0

    candidate_chars, font, sample_character, scale = get_data(opt.language, opt.mode, LANG_CHARINFO)
    num_chars = len(candidate_chars)
    num_cols = opt.num_cols
    image = cv2.imread(opt.input, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    height, width = image.shape
    char_width, char_height = get_size(font, sample_character)
    cell_width = width / opt.num_cols
    cell_height = (char_height / char_width) * cell_width
    num_rows = int(height / cell_height)

    if num_cols > width or num_rows > height:
        print("Too many columns or rows. Using default setting")
        cell_width = 6
        cell_height = (char_height / char_width) * cell_width
        num_cols = int(width / cell_width)
        num_rows = int(height / cell_height)

    out_width = char_width * num_cols
    out_height = scale * char_height * num_rows
    out_image = Image.new("L", (out_width, out_height), bg_code)
    draw = ImageDraw.Draw(out_image)

    if opt.color:
        for char, rowno, colno, color in gen_colored_char(
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
            draw.text((colno * char_width, rowno * char_height), char, fill=color, font=font)
    else:
        for rowno, rowchars in enumerate(
            gen_rowchars(
                image,
                candidate_chars,
                height=height,
                width=width,
                cell_width=cell_width,
                cell_height=cell_height,
                num_chars=num_chars,
                num_rows=num_rows,
                num_cols=num_cols,
            )
        ):
            draw.text((0, rowno * char_height), "".join(rowchars), fill=255 - bg_code, font=font)

    cropped_image = ImageOps.invert(out_image).getbbox() if opt.background == "white" else out_image.getbbox()
    out_image = out_image.crop(cropped_image)
    out_image.save(opt.output)


def video2video(opt: argparse.Namespace):
    import cv2
    import numpy as np
    from PIL import Image, ImageDraw, ImageFont, ImageOps

    candidate_chars = LANG_CHARINFO["general"]["modes"][opt.mode]

    if opt.color:
        bg_code = (255, 255, 255) if opt.background == "white" else (0, 0, 0)
        mode = "RGB"
    else:
        bg_code = 255 if opt.background == "white" else 0
        mode = "L"

    font = ImageFont.truetype("fonts/DejaVuSansMono-Bold.ttf", size=int(10 * opt.scale))
    cap = cv2.VideoCapture(opt.input)
    fps = int(cap.get(cv2.CAP_PROP_FPS)) if opt.fps == 0 else opt.fps
    num_chars = len(candidate_chars)
    num_cols = opt.num_cols
    while cap.isOpened():
        flag, frame = cap.read()
        if flag:
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        else:
            break
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
        char_width, char_height = get_size(font, "A")
        out_width = char_width * num_cols
        out_height = 2 * char_height * num_rows

        out_image = Image.new(mode, (out_width, out_height), bg_code)

        draw = ImageDraw.Draw(out_image)

        if opt.color:
            for char, rowno, colno, color in gen_colored_char(
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
                draw.text((colno * char_width, rowno * char_height), char, fill=color, font=font)
        else:
            for rowno, rowchars in enumerate(
                gen_rowchars(
                    image,
                    candidate_chars,
                    height=height,
                    width=width,
                    cell_width=cell_width,
                    cell_height=cell_height,
                    num_chars=num_chars,
                    num_rows=num_rows,
                    num_cols=num_cols,
                )
            ):
                draw.text((0, rowno * char_height), "".join(rowchars), fill=255 - bg_code, font=font)

        if opt.background == "white":
            cropped_image = ImageOps.invert(out_image).getbbox()
        else:
            cropped_image = out_image.getbbox()
        out_image = out_image.crop(cropped_image)
        out_image = cv2.cvtColor(np.array(out_image), cv2.COLOR_GRAY2BGR)
        out_image = np.array(out_image)
        try:
            out
        except:
            out = cv2.VideoWriter(
                opt.output, cv2.VideoWriter_fourcc(*"XVID"), fps, ((out_image.shape[1], out_image.shape[0]))
            )

        if opt.overlay_ratio:
            height, width, _ = out_image.shape
            overlay = cv2.resize(frame, (int(width * opt.overlay_ratio), int(height * opt.overlay_ratio)))
            out_image[
                height - int(height * opt.overlay_ratio) :, width - int(width * opt.overlay_ratio) :, :
            ] = overlay
        out.write(out_image)
    cap.release()
    out.release()
