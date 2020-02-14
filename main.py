"""
Christopher Mendez & Rupika Dikkala
Programming Assignment 3
Sudoku
CS 531 - AI
February 17, 2020
***********************************
"""

import sudoku as s


def main():
    # initializing board
    s.create_board()
    s.calculate_poss(s.board_objects)
    print("\nPRINTING FRESH BOARD")
    # print_board()

    print("\nnaked single FUNCTION")
    s.naked_singles(s.board_objects)
    s.print_board()





if __name__ == "__main__":
    main()

