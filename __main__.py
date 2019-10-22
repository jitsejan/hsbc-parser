from hsbcpdfreader import HSBCPdfReader
from hsbccreditcardpdfreader import HSBCCreditCardPdfReader

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
        help="Data source",
        required=True,
    )
    return parser.parse_args()


def main():
    args = _get_args()
    if os.path.isfile(args.statement):
        hpr = HSBCCreditCardPdfReader(args.statement)
        df = hpr.get_dataframe()  
        print(df)
    

if __name__ == "__main__":
    main()
