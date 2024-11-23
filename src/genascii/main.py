#!/usr/bin/env python3

import argparse
import sys

from .core import img2img, img2txt, video2video


def make_arg_parser(argv: list[str]):
    parser = argparse.ArgumentParser(prog="genascii")
    parser.add_argument(
        "--version",
        default=False,
        action="store_true",
    )
    subparsers: argparse._SubParsersAction = parser.add_subparsers(title="commands", dest="command")
    make_txt_parser(subparsers)
    make_img_parser(subparsers)
    make_video_parser(subparsers)
    opt = parser.parse_args(argv[1:])
    if (func := getattr(opt, "func", None)) is None:
        parser.print_help()
    else:
        func(opt)


def make_txt_parser(subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
    txt_parser = subparsers.add_parser("img2txt", help="Image to ASCII text")
    txt_parser.add_argument(
        "--input", type=str, default="data/input.jpg", help="Path to input image, by default data/input.jpg"
    )
    txt_parser.add_argument(
        "--output",
        type=str,
        default="data/output.txt",
        help="Path to output text file, by default data/output.txt",
    )
    txt_parser.add_argument(
        "--mode",
        type=str,
        default="complex",
        choices=["simple", "complex"],
        help="10 or 70 different characters, 70 by default",
    )
    txt_parser.add_argument(
        "--num_cols", type=int, default=150, help="number of character for output's width, 150 by default"
    )

    txt_parser.set_defaults(func=img2txt)
    return txt_parser


def make_img_parser(subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
    img_parser = subparsers.add_parser("img2img", help="Image to ASCII image")
    img_parser.add_argument(
        "--input", type=str, default="data/input.jpg", help="Path to input image, by default data/input.jpg"
    )
    img_parser.add_argument(
        "--output",
        type=str,
        default="data/output.jpg",
        help="Path to output text file, by default data/output.jpg",
    )
    img_parser.add_argument("--language", type=str, default="english")
    img_parser.add_argument("--mode", type=str, default="standard")
    img_parser.add_argument(
        "--background",
        type=str,
        default="black",
        choices=["black", "white"],
        help="background's color, by default black",
    )
    img_parser.add_argument(
        "--num_cols", type=int, default=300, help="number of character for output's width, by default 300"
    )
    img_parser.add_argument("--color", default=False, action="store_true")
    img_parser.set_defaults(func=img2img)
    return img_parser


def make_video_parser(subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
    video_parser = subparsers.add_parser("video2video", help="Video to ASCII video")
    video_parser.add_argument("--input", type=str, default="data/input.mp4", help="Path to input video")
    video_parser.add_argument("--output", type=str, default="data/output.mp4", help="Path to output video")
    video_parser.add_argument(
        "--mode",
        type=str,
        default="simple",
        choices=["simple", "complex"],
        help="10 or 70 different characters",
    )
    video_parser.add_argument(
        "--background", type=str, default="white", choices=["black", "white"], help="background's color"
    )
    video_parser.add_argument(
        "--num_cols", type=int, default=100, help="number of character for output's width"
    )
    video_parser.add_argument("--scale", type=int, default=1, help="upsize output")
    video_parser.add_argument("--fps", type=int, default=0, help="frame per second")
    video_parser.add_argument("--overlay_ratio", type=float, default=0.2, help="Overlay width ratio")
    video_parser.add_argument("--color", default=False, action="store_true")

    video_parser.set_defaults(func=video2video)
    return video_parser


def main():
    make_arg_parser(sys.argv)
