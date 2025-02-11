#!/usr/bin/env python3
import argparse
import datetime

def main():
    # Set up the command-line argument parser with shorthand switches.
    parser = argparse.ArgumentParser(
        description="Convert a text file of chess variations (one per line) into a PGN file."
    )
    parser.add_argument(
        "-i", "--input", required=True,
        help="Path to the input text file containing chess variations (one per line)."
    )
    parser.add_argument(
        "-o", "--output", required=True,
        help="Path to the output PGN file to write the converted games."
    )
    args = parser.parse_args()

    # Get today's date in PGN date format (YYYY.MM.DD)
    today = datetime.datetime.now().strftime("%Y.%m.%d")

    # Read all lines from the input file
    try:
        with open(args.input, 'r', encoding='utf-8') as fin:
            lines = fin.readlines()
    except FileNotFoundError:
        print(f"Error: The file '{args.input}' does not exist.")
        return

    # Open the output file for writing the PGN games
    with open(args.output, 'w', encoding='utf-8') as fout:
        for idx, line in enumerate(lines, start=1):
            # Remove any leading/trailing whitespace
            line = line.strip()
            if not line:
                continue  # Skip empty lines

            # Remove the "Line N:" prefix if present
            moves = line
            if moves.lower().startswith("line"):
                colon_index = moves.find(":")
                if colon_index != -1:
                    moves = moves[colon_index+1:].strip()

            # If the move text does not end with a game termination marker, append an asterisk.
            valid_results = ("1-0", "0-1", "1/2-1/2", "*")
            if not any(moves.endswith(result) for result in valid_results):
                moves = moves + " *"

            # Write PGN headers and the moves for this game block.
            fout.write(f'[Event "Line {idx}"]\n')
            fout.write(f'[Site "Local"]\n')
            fout.write(f'[Date "{today}"]\n')
            fout.write(f'[Round "-"]\n')
            fout.write(f'[White "White"]\n')
            fout.write(f'[Black "Black"]\n')
            fout.write('\n')
            fout.write(moves + "\n")
            fout.write('\n')

if __name__ == "__main__":
    main()
