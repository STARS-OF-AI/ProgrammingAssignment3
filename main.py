"""
Christopher Mendez, Rupika Dikkala & Rajesh
Programming Assignment 3
Sudoku
CS 531 - AI
February 17, 2020
***********************************
"""

import sudoku as s
from pandas import DataFrame

boards = []

def get_score(solved, starting):
    s1 = s.convert_to_numbers(solved)
    score = 0
    unsolve = 0
    num_start = 0
    for i in range(9):
        for j in range(9):
            if s1[i][j] == 0:
                unsolve += 1     
            elif s1[i][j] == starting[i][j]:
                num_start +=1
            else:
                score += 1
    percent_correct = (score+num_start)/81
    print('Score: ', percent_correct)
    return percent_correct, score, num_start

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
    scores = []
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
            print('Final Scores: ', scores) 
            s2 = DataFrame(scores)
            print(s2)
            s2.to_csv('scores.csv')
            return
        print('Attempting to solve:', boards[i][0], b_instance)
        s.create_board(b_instance)
        s.calculate_poss(s.board_objects)
        #s.print_board()
        
        iter_depth = s.backtrack(s.board_objects, 0)
        s.print_board()
        score_tup = get_score(s.board_objects, b_instance)
        curr_score = (boards[i][0], score_tup[0], score_tup[1], score_tup[2], iter_depth)
        b_instance = []
        scores.append(curr_score)    
    
    
                                      
        

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

