from hsbcpdfreader import HSBCPdfReader

import argparse
import os

def _get_args():
    """ Get the arguments """
    parser = argparse.ArgumentParser(
        description="HSBC statement parser"
    )
    parser.add_argument(
        "--statement",
        nargs="?",
        help="Statement PDF",
        required=True,
    )
    return parser.parse_args()


def main():
    args = _get_args()
    if os.path.isfile(args.statement):
        hpr = HSBCPdfReader(args.statement)
        df = hpr.get_dataframe()
        print(df)
    else:
        print(f"Error for {args.statement}")


if __name__ == "__main__":
    main()
