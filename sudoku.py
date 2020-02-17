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


# board = [
# [0,0,2, 5,0,7, 3,1,0,],
# [0,8,0, 0,0,0, 0,6,0,],
# [0,0,0, 0,0,3, 2,0,8,],
# [0,0,4, 3,0,2, 0,8,1,],
# [8,0,1, 0,9,0, 7,0,3,],
# [7,3,0, 8,0,4, 5,0,0,],
# [4,0,9, 2,0,0, 0,0,0,],
# [0,6,0, 0,0,0, 0,5,0,],
# [0,1,3, 9,0,6, 8,0,0,]]


# array of board objects
board_objects = []

def check_sudoku(grid):
    for row in range(9):
        for col in range(9):
            # check value is an int
            if grid[row][col] < 1 :
                return False
    # check the rows
    for row in grid:
        if sorted(list(set(row))) != sorted(row):
            return False
    # check the cols
    cols = []
    for col in range(len(grid)):
        for row in grid:
            cols += [row[col]]
        # set will get unique values, its converted to list so you can compare
        # it's sorted so the comparison is done correctly.
        if sorted(list(set(cols))) != sorted(cols):
            return False
        cols = []
    # if you get past all the false checks return True
    return True

def convert_to_numbers(board_objects):
	board = []
	for i in range(0, 9):
		board_row = []
		for j in range(0, 9):
			board_row.append(board_objects[i][j].value)
		board.append(board_row)
	return board


def hidden_singles(board_objects):

	for k in range (1,10):
		
		for i in range (9):
			row_possibility = []
			for j in range(9):
				if k in board_objects[i][j].list:
					row_possibility.append(j)
					if len(row_possibility) > 1:# and len(row_possibility) > 1:
						break
			if len(row_possibility) == 1 :
				board_objects[i][row_possibility[0]].value = k
				board_objects[i][row_possibility[0]].list = []
				calculate_poss(board_objects)

		
		#print_board()
		
		for j in range (9):
			column_possibility = []
			for i in range(9):
				if k in board_objects[i][j].list:
					column_possibility.append(i)

					if len(column_possibility) > 1:# and len(row_possibility) > 1:
						break


			if len(column_possibility) == 1 :
				board_objects[column_possibility[0]][j].value = k
				board_objects[column_possibility[0]][j].list = []
				calculate_poss(board_objects)

		#print_board()

		for i in range (0,9): 
			for j in range (0,9):
				boxX = i - (i%3)
				boxY = j - (j%3)
				box_possibility = []
				for p in range(boxX, boxX+3):
					for q in range(boxY, boxY+3):
						if k in board_objects[p][q].list:
							box_possibility.append((p,q))

				if len(box_possibility) == 1 :
					board_objects[box_possibility[0][0]][ box_possibility[0][1]].value = k
					board_objects[box_possibility[0][0]][ box_possibility[0][1]].list = []
					calculate_poss(board_objects)


def find_double_occuring_numbers(number_position):
	doubly_occuring_numbers = []
	for key,value in number_position.items():
		if value[0] == 2 :
			doubly_occuring_numbers.append((key,value[1]))

	return doubly_occuring_numbers


def hidden_pair_update_at_position(board_objects, dom,p,q):
	hidden_pair_location = []
	for i in range (len(dom[p][1])):
		board_objects[dom[p][1][i][0]][dom[p][1][i][1]].list = [dom[p][0],dom[q][0]]
		#hidden_pair_location.append(dom[p][1][i])
	
	#return hidden_pair_location



def hidden_pair_process(board_objects,row_column , hidden_pair_update_function):
	
	for i in range (0,9):
		if row_column == 'row':
			row = i
		else :
			column = i
		number_position = {}
		for k in range(1,10):
			number_position[k] = [0,[]]
		for j in range (0,9):
			
			if row_column == 'row':
				column = j
			else :
				row = j
			for elem in board_objects[row][column].list:
				number_position[elem][0] += 1
				number_position[elem][1].append((row,column))

		doubly_occuring_numbers = find_double_occuring_numbers(number_position)

		hidden_pair = []
		for p in range(len(doubly_occuring_numbers)):
			for q in range(p+1, len(doubly_occuring_numbers)):

				if doubly_occuring_numbers[p][1] == doubly_occuring_numbers[q][1]: 
					hidden_pair_update_at_position(board_objects,doubly_occuring_numbers,p,q)

	

def hidden_pairs(board_objects):
	
	# finding row hidden pairs
	hidden_pair_process(board_objects,'row',hidden_pair_update_row )	
	# finding column hidden pairs
	hidden_pair_process(board_objects,'column',hidden_pair_update_column )	

	
	# finding box hidden pairs
	for i in range (0,9,): 
		for j in range (0,9,3):
			boxX = i - (i%3)
			boxY = j - (j%3)
			number_position = {}
			box_possibility = []
			for k in range(1,10):
				number_position[k] = [0,[]]
			for p in range(boxX, boxX+3):
				for q in range(boxY, boxY+3):
					for elem in board_objects[p][q].list:
						number_position[elem][0] += 1
						number_position[elem][1].append((p,q))
		
			doubly_occuring_numbers = find_double_occuring_numbers(number_position)
			print (number_position)
			print (len(doubly_occuring_numbers))
			hidden_pair = []
			for p in range(len(doubly_occuring_numbers)):
				for q in range(p+1, len(doubly_occuring_numbers)):
					if doubly_occuring_numbers[p][1] == doubly_occuring_numbers[q][1]: 
						hidden_pair_update_at_position(board_objects,doubly_occuring_numbers,p,q)
	

def check_board_change(board_objects_before, board_objects):

	#print_board()
	for i in range(0,9):
		for j in range(0,9):
			if board_objects_before[i][j].list != board_objects[i][j].list:
				return True

	return False


def inference_rules (board_objects):

	board_objects_before = []
	for i in range(0,9):
		board_objects_before_row = []
		for j in range(0,9):
			board_objects_before_row.append(c.cell(board_objects[i][j].value, i, j))
			board_objects_before_row[j].list = board_objects[i][j].list[:]			

		board_objects_before.append(board_objects_before_row)
		
	naked_singles(board_objects)
	hidden_singles(board_objects)
	
	naked_doubles(board_objects)
	#hidden_pairs(board_objects)
	#hidden_triples(board_objects)

	print_board()
	
	if (check_sudoku(convert_to_numbers(board_objects))) : 
		return

	if check_board_change(board_objects_before,board_objects):
		print ("change occured")
		inference_rules(board_objects)
		

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
    print("\n")
    print(p.get_string(header=True, border=False))



################ BACKTRACKING FUNCTIONS ############

#print(board)
def board_complete(board):
    for x in range(9):
        for y in range(9):
            if board[x][y].value != 0:
                return False
            print(board[x][y].value)
    print('through the loops')
    return True

def select_var(board, n):
    if n == 1:
        for x in range(9):
            for y in range(9):
                if board[x][y].value == 0:
                    return board[x][y]
        return 0
    elif n == 2:
        return 0
        #run MRV to get var
    

    
def backtrack(board, i):
    #var = select_var(board, 1)
    #print('var', var.x, var.y, var.value)
    inference_rules(board)
    grid = convert_to_numbers(board)
    if check_sudoku(grid):
        print('board complete', i)
        return board
        
    if board_complete(board) or i == 1000:
        print('board complete', i)
        return board

    var = select_var(board, 1)
    #make a move on selected var
    #print('bar', var)
    try:
        if var == 0:
            #print('out of vars')
            return False
        #print('move', board[var.x][var.y].value, var.list[0])
        board[var.x][var.y].value = var.list[0]
        board[var.x][var.y].list = []
        calculate_poss(board)
        i+=1
        result = backtrack(board, i)
    except:
        #print('move failed', var.value, board[var.x][var.y].list)
        if len(board[var.x][var.y].list) > 0:
            #print('in if')
            board[var.x][var.y].value = 0
            board[var.x][var.y].list.remove(var.value)
            i+=1
            result = backtrack(board, i)
        else:
            #print('ran out of possibilities')
            return False
        #print('move', board[var.x][var.y].value, var.list[0])
        
    if result:
        #print('result true')
        return result
    #print('false result')
    return False
 

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
    # only doing 0, 3, 6 to traverse
    # thru 9 boxes
    for x in [0, 3, 6]:
        # calculate box range
        box_x = x - (x % 3)
        for y in [0, 3, 6]:
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
    print_board()

def remove_double(board, double, dubxy):
    x1 = dubxy[0][0]
    y1 = dubxy[0][1]
    x2 = dubxy[1][0]
    y2 = dubxy[1][1]
    for i in range(9):
        #print(board[x][i])
        try:
            board[x1][i].list.remove(double[0])
        except ValueError:
            pass
        try:
            board[x1][i].list.remove(double[1])
        except ValueError:
            pass
        try:
            board[i][y1].list.remove(double[0])
        except ValueError:
            pass
        try:
            board[i][y1].list.remove(double[1])
        except ValueError:
            pass
        try:
            board[x2][i].list.remove(double[0])
        except ValueError:
            pass
        try:
            board[x2][i].list.remove(double[1])
        except ValueError:
            pass
        try:
            board[i][y2].list.remove(double[0])
        except ValueError:
            pass
        try:
            board[i][y2].list.remove(double[1])
        except ValueError:
            pass

    boxX = x1 - (x1%3)
    boxY = y1 - (y1%3)

    for j in range(boxX, boxX+3):
        for k in range(boxY, boxY+3):
            try:
                board[j][k].list.remove(double[0])
            except ValueError:
                pass
            try:
                board[j][k].list.remove(double[1])
            except ValueError:
                pass
            try:
                board[j][k].list.remove(double[0])
            except ValueError:
                pass
            try:
                board[j][k].list.remove(double[1])
            except ValueError:
                pass

    boxX = x2 - (x2%3)
    boxY = y2 - (y2%3)

    for j in range(boxX, boxX+3):
        for k in range(boxY, boxY+3):
            try:
                board[j][k].list.remove(double[0])
            except ValueError:
                pass
            try:
                board[j][k].list.remove(double[1])
            except ValueError:
                pass
            try:
                board[j][k].list.remove(double[0])
            except ValueError:
                pass
            try:
                board[j][k].list.remove(double[1])
            except ValueError:
                pass

    board[x1][y1].list = double
    board[x2][y2].list = double

def remove_triple(board, triple, dubxy):
    temp = set()
    backup = set()
    for z in range(3):
        temp.add(triple[z][0])
        temp.add(triple[z][1])
        backup.add(tuple(triple[z]))
        
    double = list(temp)

    x1 = dubxy[0][0]
    y1 = dubxy[0][1]
    x2 = dubxy[1][0]
    y2 = dubxy[1][1]
    x3 = dubxy[2][0]
    y3 = dubxy[2][1]
    print('xy:', backup)
    for i in range(9):
        #print(board[x][i])
        try:
            board[x1][i].list.remove(double[0])
        except ValueError:
            pass
        try:
            board[x1][i].list.remove(double[1])
        except ValueError:
            pass
        try:
            board[x1][i].list.remove(double[2])
        except ValueError:
            pass
        try:
            board[i][y1].list.remove(double[0])
        except ValueError:
            pass
        try:
            board[i][y1].list.remove(double[1])
        except ValueError:
            pass
        try:
            board[i][y1].list.remove(double[2])
        except ValueError:
            pass
        try:
            board[x2][i].list.remove(double[0])
        except ValueError:
            pass
        try:
            board[x2][i].list.remove(double[1])
        except ValueError:
            pass
        try:
            board[x2][i].list.remove(double[2])
        except ValueError:
            pass
        try:
            board[i][y2].list.remove(double[0])
        except ValueError:
            pass
        try:
            board[i][y2].list.remove(double[1])
        except ValueError:
            pass
        try:
            board[i][y2].list.remove(double[2])
        except ValueError:
            pass
        try:
            board[x3][i].list.remove(double[0])
        except ValueError:
            pass
        try:
            board[x3][i].list.remove(double[1])
        except ValueError:
            pass
        try:
            board[x3][i].list.remove(double[2])
        except ValueError:
            pass
        try:
            board[i][y3].list.remove(double[0])
        except ValueError:
            pass
        try:
            board[i][y3].list.remove(double[1])
        except ValueError:
            pass
        try:
            board[i][y3].list.remove(double[2])
        except ValueError:
            pass

    
    boxX = x1 - (x1%3)
    boxY = y1 - (y1%3)

    for j in range(boxX, boxX+3):
        for k in range(boxY, boxY+3):
            try:
                board[j][k].list.remove(double[0])
            except ValueError:
                pass
            try:
                board[j][k].list.remove(double[1])
            except ValueError:
                pass
            try:
                board[j][k].list.remove(double[2])
            except ValueError:
                pass


    boxX = x2 - (x2%3)
    boxY = y2 - (y2%3)

    for j in range(boxX, boxX+3):
        for k in range(boxY, boxY+3):
            try:
                board[j][k].list.remove(double[0])
            except ValueError:
                pass
            try:
                board[j][k].list.remove(double[1])
            except ValueError:
                pass
            try:
                board[j][k].list.remove(double[2])
            except ValueError:
                pass
    boxX = x3 - (x3%3)
    boxY = y3 - (y3%3)

    for j in range(boxX, boxX+3):
        for k in range(boxY, boxY+3):
            try:
                board[j][k].list.remove(double[0])
            except ValueError:
                pass
            try:
                board[j][k].list.remove(double[1])
            except ValueError:
                pass
            try:
                board[j][k].list.remove(double[2])
            except ValueError:
                pass

    triple = list(backup)
    #print('add back', triple[0], triple[1], triple[2], x1, x2, x3, backup)
    
    
    board[x1][y1].list = list(triple[0])
    board[x2][y2].list = list(triple[1])
    board[x3][y3].list = list(triple[2])
    print_board()
        

    


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
            dubxy = []
            for y in range(9):
                # check if list of element = naked double
                if double == board_obj[x][y].list:
                    print("ENTERING THE ROW CELL: {}, {} ".format(x, y))
                    print("double: ", double)
                    dubxy.append((x,y))
                    # then run the possibilities to remove it from
                    # neighboring cells
                    #remove_double(board_obj, double, x, y)
                    #calculate_poss(board_obj)
            #print('dub',dubxy)
            remove_double(board_obj, double, dubxy)
            double = []

    print_board()

    # find by column
    for y in range(9):
        # func to check if size=2 of each item list in the row
        # return the naked double
        double_list = []
        for x in range(9):
            if len(board_obj[x][y].list) == 2:
                double_list.append(board_obj[x][y].list)

        double = get_duplicate(double_list, 2)
        # double = get_double(double_list)
        print(y)
        print(double)
        if len(double) == 0:
            continue
        else:
            dubxy = []
            print("ROW VALUE: ",double)
            for x in range(9):

                # check if list of element = naked double
                if double == board_obj[x][y].list:
                    print("ENTERING THE COL CELL: {}, {} ".format(x+1, y+1))
                    print("double: ", double)
                    dubxy.append((x,y))
                    # then run the possibilities to remove it from
                    # neighboring cells
            print('dub',dubxy)
            remove_double(board_obj, double, dubxy)
            double = []

    # find by box
    for x in [0, 3, 6]:
        # calculate box range
        box_x = x - (x % 3)
        for y in [0, 3, 6]:
            box_y = y - (y % 3)

            # traverse the box to find
            # the naked doubles
            double_list = []
            for j in range(box_x, box_x+3):
                for k in range(box_y, box_y+3):
                    if len(board_obj[j][k].list) == 2:
                        double_list.append(board_obj[j][k].list)

            # call duplicate function here and catch
            # the naked double
            #print("double list: ", double_list)
            duplicate = get_duplicate(double_list, 2)

            if len(duplicate) == 0:
                continue
            else:
                # remove the naked double from each
                # cell in the box
                dubxy = []
                for j in range(box_x, box_x+3):
                    for k in range(box_y, box_y+3):
                        if duplicate == board_obj[j][k].list:
                            # print("ENTERING THE BOX CELL: {}, {} ".format(j, k))
                            # print(duplicate)
                            dubxy.append((j,k))
                print('dubBBBBBBBBBB: ',dubxy)
                remove_double(board_obj, duplicate, dubxy)
                print("removed duplicate: ", duplicate)
                print_board()
                double = []


# set up naked triple -- PART 1, only checks for
# full triples
def naked_triple(board_obj):
    # find by row
    for x in range(9):
        # func to check if size=2 of each item list in the row
        # return the naked triple
        triple = get_triple(board_obj[x], [])
        print("tripleeeee:", triple)
        if len(triple) == 0:
            continue
        else:
            tripxy = []
            for y in range(9):
                # check if list of element = naked triple
                if triple == board_obj[x][y].list:
                    print("ENTERING THE ROW CELL: {}, {} ".format(x, y))
                    print("naked triple: ", triple)
                    tripxy.append((x,y))
                    #remove_double(board_obj, triple, x, y)
                    #calculate_poss(board_obj)
            #print('dub',tripxy)
            remove_triple(board_obj, triple, tripxy)
            triple = []

    # find by column
    for y in range(9):
        # func to check if size=2 of each item list in the row
        # return the naked triple
        pairs = []
        for x in range(9):
            if len(board_obj[x][y].list) == 2:
                pairs.append(board_obj[x][y].list)

        # get naked triple
        triple = get_triple([], pairs)
        # print(y)
        # print(triple)
        if len(triple) == 0:
            continue
        else:
            tripxy = []
            print("ROW VALUE: ",triple)
            for x in range(9):
                # check if list of element = naked triple
                if triple[0] == board_obj[x][y].list:
                    print("ENTERING THE COL CELL: {}, {} ".format(x, y))
                    print("triple: ", triple[0])
                    tripxy.append((x,y))
                elif triple[1] == board_obj[x][y].list:
                    print("ENTERING THE COL CELL: {}, {} ".format(x, y))
                    print("triple: ", triple[0])
                    tripxy.append((x,y))
                elif triple[2] == board_obj[x][y].list:
                    print("ENTERING THE COL CELL: {}, {} ".format(x, y))
                    print("triple: ", triple[0])
                    tripxy.append((x,y))
                    # then run the possibilities to remove it from
                    # neighboring cells
            print('triple: ',tripxy)
            remove_triple(board_obj, triple, tripxy)
            triple = []

    # find by box
    for x in [0, 3, 6]:
        # calculate box range
        box_x = x - (x % 3)
        for y in [0, 3, 6]:
            box_y = y - (y % 3)

            # traverse the box to find
            # the pairs
            pairs = []
            for j in range(box_x, box_x+3):
                for k in range(box_y, box_y+3):
                    if len(board_obj[j][k].list) == 2:
                        pairs.append(board_obj[j][k].list)

            # catch naked triple
            print("pair list: ", pairs)
            triple = get_triple([], pairs)

            if len(triple) == 0:
                continue
            else:
                # remove the naked double from each
                # cell in the box
                dubxy = []
                for j in range(box_x, box_x+3):
                    for k in range(box_y, box_y+3):
                        if triple == board_obj[j][k].list:
                            # print("ENTERING THE BOX CELL: {}, {} ".format(j, k))
                            # print(triple)
                            dubxy.append((j,k))
                print('dubBBBBBBBBBB: ',dubxy)
                remove_triple(board_obj, triple, tripxy)
                print("removed triple: ", triple)
                print_board()
                double = []


# function to get naked double row/column
def get_double(arr):
    if len(arr) == 0:
        return []

    # catch the lists with 2 element and store
    double_list = []
    for i in arr:
        if len(i.list) == 2:
            double_list.append(i.list)

    # get duplicate if exists
    # params: list, double/triple val
    return get_duplicate(double_list, 2)


# function to get naked triple row/column
def get_triple(arr, pair_list):
    if len(arr) == 0 and len(pair_list) == 0:
        return []

    double_list = []
    # catch all len 2 and append to double list
    if len(pair_list) == 0:
        for a in arr:
            if len(a.list) == 2:
                double_list.append(a.list)
    else:
        double_list = pair_list

    # if double list has a naked triple
    # possibility
    if len(double_list) >= 3:
        length = len(double_list)
        triple = []
        found = False

        # combo for all the possible values
        # pairs to make sure there are no
        # repeating pairs
        combo = set()
        pairs = set()

        #  get the combo triples
        for i in range(length):
            # add each number to combo
            combo.add(double_list[i][0])
            combo.add(double_list[i][1])

            # add tuple pair to set
            pairs.add((double_list[i][0], double_list[i][1]))

            # start at the next value in list
            for j in range(i+1, length):
                combo.add(double_list[j][0])
                combo.add(double_list[j][1])

                # if there is no overlap in possible
                # numbers, then they are not a naked triple
                if len(combo) > 3:
                    combo.remove(double_list[j][0])
                    combo.remove(double_list[j][1])
                    continue
                # if overlap
                elif len(combo) == 3:
                    pairs.add((double_list[j][0], double_list[j][1]))
                    for k in range(j+1, length):
                        combo.add(double_list[k][0])
                        combo.add(double_list[k][1])
                        if len(combo) > 3:
                            combo.remove(double_list[k][0])
                            combo.remove(double_list[k][1])
                            continue
                        elif len(combo) == 3:
                            # found naked triples, add to pairs set
                            # and triples list
                            found = True
                            pairs.add((double_list[k][0], double_list[k][1]))
                            triple.extend([double_list[k], double_list[j], double_list[i]])
                            break
                    if found:
                        break
            if found:
                break
        # if all the pairs are unique and naked triple
        if len(triple) == 3 and len(pairs) == 3:
            return triple
        else:
            return []
    else:
        return []


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
            dup = []

            # return the duplicate pair/trio
            for (row, freq) in freq_list.items():
                if freq == val:
                    dup = list(row)
                    break
            if len(dup) > 0:
                return dup
            else:
                return []
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







