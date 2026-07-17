import argparse
import sys
from .core import Str2Col, _FMT_MAP

ANSI_RESET = "\033[0m"


def main():
    parser = argparse.ArgumentParser(description="Map any value to a color")
    parser.add_argument("value", nargs="?", help="Value to convert (or pipe via stdin)")
    parser.add_argument("--format", "-f", default="hex", choices=list(_FMT_MAP), dest="fmt")
    parser.add_argument("--seed", default=None)
    parser.add_argument("--hue-range", nargs=2, type=float, metavar=("MIN", "MAX"), default=[0, 360])
    parser.add_argument("--sat-range", nargs=2, type=float, metavar=("MIN", "MAX"), default=[0.4, 0.9])
    parser.add_argument("--light-range", nargs=2, type=float, metavar=("MIN", "MAX"), default=[0.35, 0.65])
    parser.add_argument("--text", default=None, help="Print TEXT colored with the result (uses ansi_fg)")
    args = parser.parse_args()

    value = args.value
    if value is None:
        if sys.stdin.isatty():
            parser.error("Provide a value as argument or via stdin")
        value = sys.stdin.read().strip()
        if not value:
            parser.error("Provide a value as argument or via stdin")

    conv = Str2Col(
        seed=args.seed,
        hue_range=tuple(args.hue_range),
        sat_range=tuple(args.sat_range),
        light_range=tuple(args.light_range),
    )

    if args.text:
        print(f"{conv.to_ansi_fg(value)}{args.text}{ANSI_RESET}")
    else:
        print(getattr(conv, _FMT_MAP[args.fmt])(value))


if __name__ == "__main__":
    main()
