"""
Christopher Mendez & Rupika Dikkala
Programming Assignment 3
Sudoku
CS 531 - AI
February 17, 2020
***********************************
"""

import cell as c

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
            if board[i][y] != 0:
                if board[i][y].value in board[x][y].list:
                    board[x][y].list.remove(board[i][y].value)

        #iterate through box
        boxX = x - (x%3)
        boxY = y - (y%3)
        #print('box', boxX, boxY)
        for j in range(boxX, boxX+3):
            for k in range(boxY, boxY+3):
                if board[j][k] != 0:
                    if board[j][k].value in board[x][y].list :
                        board[x][y].list.remove(board[j][k].value)


# append cells into sudoku board
# put these for loops into a function
for i in range (9):
    board_objects_row = []
    for j in range (9) :
        board_objects_row.append(c.cell(board[i][j], i , j))

    board_objects.append(board_objects_row)

# calculate the poss list for each cell
for i in range (9):
    for j in range (9) :
        possibilities(board_objects, i,j )

# print the board
for i in range (9):
    for j in range (9) :
        print (board_objects[i][j].list)
    print("end of row", i+1)


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


# # function to calculate naked single
# def naked_singles(board):
#     for row in range(9):
#         for i in range(9):
#             try:
#                 if isinstance(pvals[row][i], list) and len(pvals[row][i]) == 1:
#                     board[row][i] = pvals[row][i][0]
#                 p_vals = calculate_possible_vals(board)
#             except:
#                 print("can't DO THAT")
#                 temp = deepcopy(board)
#                 temp[row][i] = pvals[row][i][0]
#                 continue
# #             try on temp board??









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







