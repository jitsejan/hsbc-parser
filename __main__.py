from hsbcpdfreader import HSBCPdfReader

import argparse
import os
import pandas as pd

def _get_args():
    """ Get the arguments """
    parser = argparse.ArgumentParser(
        description="HSBC statement parser"
    )
    parser.add_argument(
        "--directory",
        nargs="?",
        help="Directory with statement PDFs",
        required=False,
    )
    parser.add_argument(
        "--statement",
        nargs="?",
        help="Statement PDF",
        required=False,
    )
    return parser.parse_args()


def main():
    args = _get_args()
    if args.statement and os.path.isfile(args.statement):
        hpr = HSBCPdfReader(args.statement)
        df = hpr.get_dataframe()
        print(df)
        print(df['amount'].sum())
        df.to_csv('tmp.csv', index=False)

    elif os.path.isdir(args.directory):
        from pathlib import Path
        df_list = []
        for f in Path(args.directory).rglob('*.pdf'):
            hpr = HSBCPdfReader(f)
            df = hpr.get_dataframe()
            print(f"Parsing {f}")
            df_list.append(df)
        final_df = pd.concat(df_list)
        final_df.to_csv('final.csv', index=False)
    else:
        print(f"")


if __name__ == "__main__":
    main()
