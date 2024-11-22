"""
@author: Viet Nguyen <nhviet1009@gmail.com>
@author: brightsunshine0917 <https://github.com/brightsunshine0917>
"""

import json

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps

from consts import ALPHABETS_PATH, FONT_FOLDER


def sort_chars(char_list, font, language):
    if language == "chinese":
        char_width, char_height = font.getsize("制")
    elif language == "korean":
        char_width, char_height = font.getsize("ㅊ")
    elif language == "japanese":
        char_width, char_height = font.getsize("あ")
    elif (
        language in ["english", "german", "french", "spanish", "italian", "portuguese", "polish"]
        or language == "russian"
    ):
        char_width, char_height = font.getsize("A")
    num_chars = min(len(char_list), 100)
    out_width = char_width * len(char_list)
    out_height = char_height
    out_image = Image.new("L", (out_width, out_height), 255)
    draw = ImageDraw.Draw(out_image)
    draw.text((0, 0), char_list, fill=0, font=font)
    cropped_image = ImageOps.invert(out_image).getbbox()
    out_image = out_image.crop(cropped_image)
    brightness = [np.mean(np.array(out_image)[:, 10 * i : 10 * (i + 1)]) for i in range(len(char_list))]
    char_list = list(char_list)
    zipped_lists = zip(brightness, char_list)
    zipped_lists = sorted(zipped_lists)
    result = ""
    counter = 0
    incremental_step = (zipped_lists[-1][0] - zipped_lists[0][0]) / num_chars
    current_value = zipped_lists[0][0]
    for value, char in zipped_lists:
        if value >= current_value:
            result += char
            counter += 1
            current_value += incremental_step
        if counter == num_chars:
            break
    if result[-1] != zipped_lists[-1][1]:
        result += zipped_lists[-1][1]
    return result


def get_data(language, mode):
    with open(ALPHABETS_PATH, "rb") as f:
        lang_charinfo = json.load(f)

    charinfo = lang_charinfo.get(language)
    if charinfo is None:
        raise ValueError(f"Invalid language: expected one of {', '.join(lang_charinfo)}, got {language}")
    font = ImageFont.truetype(FONT_FOLDER / charinfo["font-name"], size=charinfo["font-size"])
    sample_character = charinfo["sample_character"]
    scale = charinfo["scale"]

    if mode not in charinfo["modes"]:
        raise ValueError(
            f"Invalide mode: expected one of {', '.join(charinfo['modes'])} for {language}, got {mode}"
        )
    chars = charinfo["modes"][mode]

    if language != "general":
        chars = sort_chars(chars, font, language)

    return chars, font, sample_character, scale
