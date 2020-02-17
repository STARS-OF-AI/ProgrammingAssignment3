"""
Christopher Mendez & Rupika Dikkala
Programming Assignment 3
Sudoku
CS 531 - AI
February 17, 2020
***********************************
"""

import sudoku as s

board = [
[2,4,0, 3,0,0, 0,0,0],
[0,0,0, 5,2,0, 4,0,7],
[0,0,0, 0,4,6, 0,0,8],
[6,1,0, 7,0,0, 0,8,4],
[0,0,9, 0,6,0, 5,0,0],
[7,3,0, 0,0,5, 0,6,1],
[1,0,0, 4,7,0, 0,0,0],
[3,0,2, 0,5,1, 0,0,0],
[0,0,0, 0,0,2, 0,1,9]]

boards = []

def main():
    f = open('sudoku-problems.txt', 'r')

    data = f.read()
    x = len(data)
    input_data = data[0:x].split("\n")

    #print(input_data)
    temp_board = []
    for i in input_data:
        if len(i) == 0:
            #print('end of board')
            boards.append(temp_board)
            temp_board = []
        else:
            temp_board.append(i)
    print(boards[0][1])
    b_instance = []
    b_row = []
    for i in range (len(boards)):
        for j in range(1, len(boards[i])):
            for k in range (len(boards[i][j])):
                #print('ijk', i, j, k)
                try:
                    b_row.append(int(boards[i][j][k]))
                except:
                    continue
            b_instance.append(b_row)
            b_row = []
            
        #print('i', i, boards[i])
        if len(boards[i]) == 0:
            return
        print('Attempting to solve:', boards[i][0])
        s.create_board(b_instance)
        s.calculate_poss(s.board_objects)
        s.print_board()
        s.backtrack(s.board_objects, 0)
        #s.print_board()
        b_instance = []
        
       
                                      
        

    # initializing board
    #s.create_board(board)
    #s.calculate_poss(s.board_objects)
    #print("\nPRINTING FRESH BOARD")
    #s.print_board()
    #s.backtrack(s.board_objects, 0)

    # print("\nnaked single FUNCTION")
    # s.naked_singles(s.board_objects)
    # s.print_board()

    # print("\nNAKED DOUBLES FUNCTION NOW")
    # s.naked_doubles(s.board_objects)
    # s.print_board()

    #print("\nNAKED TRIPLE FUNCTION NOW")
    #s.naked_triple(s.board_objects)
    #s.print_board()


if __name__ == "__main__":
    main()

