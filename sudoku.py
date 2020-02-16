"""
Christopher Mendez & Rupika Dikkala
Programming Assignment 3
Sudoku
CS 531 - AI
February 17, 2020
***********************************
"""

import cell as c
from prettytable import PrettyTable
from collections import Counter
import numpy as np

# hardcoding the board for now (board feeder function goes here)
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

# array of board objects
board_objects = []


# calculate the list possibilities for each function
def possibilities(board, x, y):
    possList = []
    if board[x][y].value == 0:
        for i in range(9):
            if board[x][i].value != 0:
                #rowP.remove(board[x][i].value)
                if board[x][i].value in board[x][y].list :
                    board[x][y].list.remove(board[x][i].value)
            if board[i][y].value != 0:
                if board[i][y].value in board[x][y].list:
                    board[x][y].list.remove(board[i][y].value)

        #iterate through box
        boxX = x - (x%3)
        boxY = y - (y%3)
        #print('box', boxX, boxY)
        for j in range(boxX, boxX+3):
            for k in range(boxY, boxY+3):
                if board[j][k].value != 0:
                    if board[j][k].value in board[x][y].list :
                        board[x][y].list.remove(board[j][k].value)


# append cells into sudoku board
def create_board():
    for i in range (9):
        board_objects_row = []
        for j in range (9) :
            board_objects_row.append(c.cell(board[i][j], i, j))

        board_objects.append(board_objects_row)


# calculate the poss list for each cell
def calculate_poss(board_obj):
    for i in range (9):
        for j in range (9) :
            possibilities(board_obj, i,j )


# print the sudoku board using pretty table
def print_board():
    p = PrettyTable()
    table = []

    for i in range(9):
        row = []
        for j in range(9):
            if len(board_objects[i][j].list) == 0:
                row.append(board_objects[i][j].value)
            else:
                row.append(board_objects[i][j].list)
        table.append(row)

    for i in table:
        p.add_row(i)

    print(p.get_string(header=True, border=False))



################ BACKTRACKING FUNCTIONS ############

#print(board)
def board_complete(board):
    for x in range(9):
        for y in range(9):
            if board[x][y] != 0:
                return False
    return True

def select_var(board, n):
    if n == 1:
        for x in range(9):
            for y in range(9):
                if board[x][y] == 0:
                    return board[x][y]
    elif n == 2:
        return 0
        #run MRV to get var

def arc_consistent():
    # need to implement
    return True
    
def backtrack(board):
    if board_complete(board):
        return board
    var = select_var(board, 1)
    #make a move on selected var
    if arc_consistent():
        result = backtrack(board)
        if result:
            return result
        #mayb eneed to remove vals from assignment
    return False
 
''' currently pseudocode
def backtrack(board)
    # inference rule returns a move as a num, x and y then
    if(check_location(board,x,y,num)): 
              
            # make move 
            board[x][y]=num 
  
            if(backtrack(board): 
                return True
  
            board[x][y] = 0 #undo move
                 
    return False 
'''
################ INFERENCE FUNCTIONS ############


# function to calculate naked single
def naked_singles(board_obj):
    # find by row
    for x in range(9):
        for y in range(9):
            # if list size is 1
            if len(board_obj[x][y].list) == 1:
                # assign value to the one in list
                val = board_obj[x][y].list[0]
                board_obj[x][y].value = val

                # clear the list
                board_obj[x][y].list.clear()

                # remove all the singles across row, column, box
                calculate_poss(board_obj)
                print("\nrow single value found: ", val)

    # print("\n******PRINTING AFTER ROW BOARD**********")
    # print_board()

    # find by column
    for y in range(9):
        for x in range(9):
            if len(board_obj[x][y].list) == 1:
                val = board_obj[x][y].list[0]
                board_obj[x][y].value = val

                board_obj[x][y].list.clear()

                calculate_poss(board_obj)
                print("\ncol single value found: ", val)
                # print_board()

    print("\n*********PRINTING AFTER COL BOARD********")
    print_board()

    # find by box
    for x in range(9):
        # calculate box range
        box_x = x - (x % 3)
        for y in range(9):
            box_y = y - (y % 3)
            # traverse the box
            for j in range(box_x, box_x+3):
                for k in range(box_y, box_y+3):
                    if len(board_obj[j][k].list) == 1:
                        val = board_obj[j][k].list[0]
                        board_obj[j][k].value = val

                        board_obj[j][k].list.clear()

                        calculate_poss(board_obj)
                        print("\nbox single value found: ", val)
                        print_board()

    print("\n*********PRINTING BOX BOARD********")
    # print_board()


# function for naked doubles
def naked_doubles(board_obj):
    # find by row
    for x in range(9):
        # func to check if size=2 of each item list in the row
        # return the naked double
        double = get_double(board_obj[x])
        if len(double) == 0:
            continue
        else:
            # print("ROW VALUE: ",x+1)
            for y in range(9):
                # check if list of element = naked double
                if double == board_obj[x][y].list:
                    # print("ENTERING THE ROW CELL: {}, {} ".format(x+1, y+1))
                    # print("double: ", double)
                    # then run the possibilities to remove it from
                    # neighboring cells
                    calculate_poss(board_obj)

    # find by column
    for y in range(9):
        # func to check if size=2 of each item list in the row
        # return the naked double
        double = get_double(board_obj[y])
        if len(double) == 0:
            continue
        else:
            # print("ROW VALUE: ",x+1)
            for x in range(9):
                # check if list of element = naked double
                if double == board_obj[x][y].list:
                    # print("ENTERING THE COL CELL: {}, {} ".format(x+1, y+1))
                    # print("double: ", double)
                    # then run the possibilities to remove it from
                    # neighboring cells
                    calculate_poss(board_obj)

    # find by box
    # for x in range(9):
    #     # calculate box range
    #     box_x = x - (x % 3)
    #     for y in range(9):
    #         box_y = y - (y % 3)
    #
    #         # traverse the box to find
    #         # the naked doubles
    #         double_list = []
    #         for j in range(box_x, box_x+3):
    #             for k in range(box_y, box_y+3):
    #                 if len(board_obj[j][k].list) == 2:
    #                     double_list.append(board_obj[j][k].list)
    #                     print("list: ", board_obj[j][k].list)
    #                     # print("ENTERING THE CELL: {}, {} ".format(x+1, y+1))
    #
    #         # print(double_list)
    #
    #         # call duplicate function here and catch
    #         # the naked double
    #         duplicate = get_duplicate(double_list, 2)
    #
    #         if len(duplicate) == 0:
    #             continue
    #         else:
    #             # remove the naked double from each
    #             # cell in the box
    #             # print(double_list)
    #             # print("THIS IS DUPLICATE")
    #             # print(duplicate)
    #             for j in range(box_x, box_x+3):
    #                 for k in range(box_y, box_y+3):
    #                     if duplicate == board_obj[j][k].list:
    #                         # print("ENTERING THE BOX CELL: {}, {} ".format(j+1, k+1))
    #                         # print(duplicate)
    #                         # then run the possibilities to remove it from
    #                         # neighboring cells
    #                         calculate_poss(board_obj)


# set up naked triple -- PART 1, only checks for
# full triples
# def naked_triple(board_obj):
#     # find by row
#     for x in range(9):
#         # func to check if size=2 of each item list in the row
#         # return the naked triple
#         triple = get_triple(board_obj[x])
#         if len(triple) == 0:
#             continue
#         else:
#             # print("ROW VALUE: ",x+1)
#             for y in range(9):
#                 # check if list of element = naked triple
#                 if triple == board_obj[x][y].list:
#                     print("ENTERING THE ROW CELL: {}, {} ".format(x+1, y+1))
#                     print("triple: ", triple)
#                     # then run the possibilities to remove it from
#                     # neighboring cells
#                     calculate_poss(board_obj)
#
#     # find by column
#     # for y in range(9):
#     #     # func to check if size=2 of each item list in the row
#     #     # return the naked triple
#     #     triple = get_triple(board_obj[y])
#     #     if len(triple) == 0:
#     #         continue
#     #     else:
#     #         # print("ROW VALUE: ",x+1)
#     #         for x in range(9):
#     #             # check if list of element = naked triple
#     #             if triple == board_obj[x][y].list:
#     #                 # print("ENTERING THE COL CELL: {}, {} ".format(x+1, y+1))
#     #                 # print("triple: ", triple)
#     #                 # then run the possibilities to remove it from
#     #                 # neighboring cells
#     #                 calculate_poss(board_obj)
#
#     # ADD BOX FUNCTIONALITY


# function to get naked double row/column
def get_double(row):
    # catch the lists with 2 element and store
    double_list = []
    for i in row:
        if len(i.list) == 2:
            double_list.append(i.list)

    # get duplicate if exists
    # params: list, double/triple val
    return get_duplicate(double_list, 2)


# function to get naked triple row/column
def get_triple(row):
    # catch the lists with 2 element and store
    triple_list = []
    for i in row:
        if len(i.list) == 3:
            triple_list.append(i.list)

    # get duplicate if exists
    # params: list, double/triple val
    get_duplicate(triple_list, 3)

    # catch all len 2 and append
    # to double list
    double_list = []
    for i in row:
        if len(i.list) == 2:
            double_list.append(i.list)

    # if double list = 3


    length = len(double_list)
    triple = []
    combo = set()
    found = False

    #  get the combo triples
    for i in range(length):
        combo.update(double_list[i][0], double_list[i][1])
        # combo.update(i[0], i[1])
        for j in range(i+1, length):
            combo.update(double_list[j][0], double_list[j][1])
            if len(combo) > 3:
                combo.remove(double_list[j][0])
                combo.remove(double_list[j][1])
                continue
            elif len(combo) == 3:
                for k in range(j+1, length):
                    combo.update(double_list[k][0], double_list[k][1])
                    if len(combo) > 3:
                        combo.remove(double_list[k][0])
                        combo.remove(double_list[k][1])
                        continue
                    elif len(combo) == 3:
                        found = True
                        triple.extend([double_list[k], double_list[j], double_list[i]])
                        break
                if found:
                    break
        if found:
            break


# function to find the duplicate in the
# naked double/triple list
def get_duplicate(seq, val):

    # if there's more than 2 pairs in the list
    if len(seq) >= val:
        # convert to np array and check for duplicates
        np_list = np.asarray(seq)
        unique = len(np.unique(np_list)) != len(np_list)

        # if there are duplicates
        if not unique:
            # find the duplicate double/triple and return that
            matrix = map(tuple, seq)
            freq_list = Counter(matrix)

            # return the duplicate pair/trio
            for (row, freq) in freq_list.items():
                if freq == val:
                    return list(row)
        else:
            return []
    else:
        return []













########################### DEAD CODE ###########################
    
# def possibilities(board, x, y):
#     possList = []
#     if board[x][y] == 0:
#         rowP = [1,2,3,4,5,6,7,8,9]
#         colP = [1,2,3,4,5,6,7,8,9]
#         boxP = [1,2,3,4,5,6,7,8,9]
#         for i in range(9):
#             if board[x][i] != 0:
#                 rowP.remove(board[x][i])
#             if board[i][y] != 0:
#                 #print('removing', board[i][y], colP)
#                 #print('i', i)
#                 colP.remove(board[i][y])
#
#
#         #iterate through box
#         boxX = x - (x%3)
#         boxY = y - (y%3)
#         #print('box', boxX, boxY)
#         for j in range(2):
#             for k in range(2):
#                 if board[j][k] != 0:
#                     boxP.remove(board[j][k])
#
#         for z in range(9):
#             if z in rowP and z in colP and z in boxP:
#                 possList.append(z)
#         #print(possList, rowP, colP, boxP)
#         return possList
#     else:
#         return 0 #no available numbers
        
# def calculate_possible_vals(board):
#     possible_vals = [[[0 for k in range(9)] for j in range(9)] for i in range(9)]
#
#     for x in range(9):
#         for y in range(9):
#             possible_vals[x][y] = possibilities(board, x, y)
#             #print(possible_vals)
#     return possible_vals
#
# p_vals = calculate_possible_vals(board)
#
# print(p_vals)
#print(p_vals[1][1], len(p_vals[1][1]))
#backtrack(board)







