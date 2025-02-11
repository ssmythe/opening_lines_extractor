#!/usr/bin/env python3
import argparse
import chess
import chess.pgn

def format_moves_as_algebraic(move_list):
    """
    Given a list of moves with optional comments (e.g. ["d4 {good move}", "Nf6", "Nf3 {develops knight}", ...]),
    format them in standard algebraic notation with move numbers.
    For example, if move_list == ["d4 {good move}", "Nf6", "Nf3 {develops knight}"],
    the result is: "1.d4 {good move} Nf6 2.Nf3 {develops knight}"
    """
    result = []
    i = 0
    move_number = 1
    while i < len(move_list):
        # White move: prefix with move number and a dot.
        white_move = f"{move_number}.{move_list[i]}"
        result.append(white_move)
        i += 1
        # If there's a corresponding Black move, append it.
        if i < len(move_list):
            black_move = move_list[i]
            result.append(black_move)
            i += 1
        move_number += 1
    return " ".join(result)

def traverse(node, board, move_list, unique_lines, no_comments=False):
    """
    Recursively traverse the move tree starting at node.
      - board: current board state.
      - move_list: list of SAN moves (strings) made so far, including comments if available.
      - unique_lines: a set that stores unique branches (move sequences).
      - no_comments: if True, comments will be stripped from moves.
    """
    if node.move is not None:
        # Get the SAN notation for the move.
        san = board.san(node.move)
        # Only include comments if no_comments flag is False.
        if not no_comments and node.comment:
            comment = node.comment.strip()
        else:
            comment = ""
        if comment:
            move_str = f"{san} {{{comment}}}"
        else:
            move_str = san
        new_move_list = move_list + [move_str]
        new_board = board.copy(stack=False)
        new_board.push(node.move)
    else:
        # Root node: no move to record.
        new_move_list = move_list
        new_board = board

    # If this node is a leaf (no further variations), add the formatted move sequence.
    if not node.variations:
        line = format_moves_as_algebraic(new_move_list)
        unique_lines.add(line)
    else:
        # Continue traversing each variation.
        for variation in node.variations:
            traverse(variation, new_board.copy(stack=False), new_move_list, unique_lines, no_comments)

def main():
    # Set up argument parsing.
    parser = argparse.ArgumentParser(
        description="Process a PGN file and output unique move lines."
    )
    parser.add_argument("pgn_file", help="Path to the PGN file")
    parser.add_argument(
        "-n", "--no-comments",
        action="store_true",
        help="Strip out all comments from the moves"
    )
    args = parser.parse_args()

    unique_lines = set()
    pgn_path = args.pgn_file  # Use the provided PGN file path.
    
    with open(pgn_path) as pgn_file:
        while True:
            game = chess.pgn.read_game(pgn_file)
            if game is None:
                break
            board = game.board()
            traverse(game, board, [], unique_lines, args.no_comments)

    # Print each unique branch with a "Line N:" prefix.
    for i, line in enumerate(sorted(unique_lines), start=1):
        print(f"Line {i}: {line}")

if __name__ == "__main__":
    main()
