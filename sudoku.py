"""
Christopher Mendez, Rupika Dikkala & Rajesh Mangannavar
Programming Assignment 3
Sudoku
CS 531 - AI
February 17, 2020
***********************************
This file contains the logic for backtracking,
and all the inference rules.
"""

import cell as c
from prettytable import PrettyTable
from collections import Counter
import numpy as np
import itertools


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



def hidden_pair_process(board_objects,row_column ):#, hidden_pair_update_function):
	
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
    hidden_pair_process(board_objects,'row')#,hidden_pair_update_row )	
    # finding column hidden pairs
    hidden_pair_process(board_objects,'column')#,hidden_pair_update_column )	

    
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
            #print (number_position)
            #print (len(doubly_occuring_numbers))
            hidden_pair = []
            for p in range(len(doubly_occuring_numbers)):
                for q in range(p+1, len(doubly_occuring_numbers)):
                    if doubly_occuring_numbers[p][1] == doubly_occuring_numbers[q][1]: 
                        hidden_pair_update_at_position(board_objects,doubly_occuring_numbers,p,q)


def hidden_triples_process(board_objects,row_column):
	
    for i in range(0,9):
            if row_column == 'row':
                    row = i
                    empty_positions = [(row,k) for k in range(0,9)]
            else :
                    column = i
                    empty_positions = [(k,column) for k in range(0,9)]
            existing_values = [k for k in range(1,10)]
            pos_triplets = {}
            nos_triplets = {}
            #print ("em,pty positiosn", empty_positions)
            for j in range(0,9):
                    if row_column == 'row':
                            column = j
                    else :
                            row = j
                    if board_objects[row][column].value != 0 :
                            if board_objects[row][column].value in existing_values:        
                                existing_values.remove(board_objects[row][column].value)
                            empty_positions.remove((row,column))
                            
            combinations = list(itertools.combinations(existing_values, 3))
            combinations_positions = list(itertools.combinations(empty_positions, 3))
            #print (combinations_row)
            #print (combinations_row_positions)
            
            for elem in combinations :
                    nos_triplets[elem] = [0,[]] 

            for elem in combinations_positions :
                    pos_triplets[elem] = [] 
            
            
            for key_pos, value_pos in pos_triplets.items():	
                    for elem in key_pos :
                            for number in board_objects[elem[0]][elem[1]].list:
                                    if number not in value_pos :
                                            pos_triplets[key_pos].append(number)


            for key_pos, value_pos in pos_triplets.items():	
                    for key_nos, value_nos in nos_triplets.items():
                            if all(x in value_pos for x in list(key_nos)):
                                    flag_all = []
                                    for elem in key_pos :
                                            flag = 0
                                            #for number in board_objects[elem[0]][elem[1]].list:
                                            for item in key_nos : 
                                                    if item in  board_objects[elem[0]][elem[1]].list:
                                                            flag = 1
                                            flag_all.append(flag)
                                    if sum(flag_all) == 3:
                                            nos_triplets[key_nos][0] += 1
                                            nos_triplets[key_nos][1].append(key_pos)
                                    

                            
            for key_nos, value_pos in nos_triplets.items():
                    #print ("Value pos : ", value_pos[0])
                    if value_pos[0] == 1 :
                            for item in value_pos[1][0]:
                                    #board_objects[item[0]][item[1]].list = list(key_nos)
                                    for elem in board_objects[item[0]][item[1]].list:
                                            if elem not in list(key_nos):	
                                                    board_objects[item[0]][item[1]].list.remove(elem)
                            #	print ("Removing triples", key_nos, value_pos)


def hidden_triples(board_objects):
	
	hidden_triples_process(board_objects,'row')
	hidden_triples_process(board_objects,'column')

	for i in range(0,9,3):

		#print ("em,pty positiosn", empty_positions)
            for j in range(0,9,3):

                existing_values = [k for k in range(1,10)]
                pos_triplets = {}
                nos_triplets = {}

                boxX = i - (i%3)
                boxY = j - (j%3)
                empty_positions = []
                for p in range(boxX, boxX+3):
                    for q in range(boxY, boxY+3):
                        empty_positions.append((p,q))#[(k,column) for k in range(0,9)]
                for p in range(boxX, boxX+3):
                    for q in range(boxY, boxY+3):
                        if board_objects[p][q].value != 0 :
                            existing_values.remove(board_objects[p][q].value)
                            empty_positions.remove((p,q))
                        
                combinations = list(itertools.combinations(existing_values, 3))
                combinations_positions = list(itertools.combinations(empty_positions, 3))
                #print (combinations_row)
                #print (combinations_row_positions)
                
                for elem in combinations :
                    nos_triplets[elem] = [0,[]] 

                for elem in combinations_positions :
                    pos_triplets[elem] = [] 
                
                
                for key_pos, value_pos in pos_triplets.items():	
                    for elem in key_pos :
                        for number in board_objects[elem[0]][elem[1]].list:
                            if number not in value_pos :
                                pos_triplets[key_pos].append(number)


                for key_pos, value_pos in pos_triplets.items():	
                    for key_nos, value_nos in nos_triplets.items():
                        if all(x in value_pos for x in list(key_nos)):
                            flag_all = []
                            for elem in key_pos :
                                flag = 0
                                #for number in board_objects[elem[0]][elem[1]].list:
                                for item in key_nos : 
                                    if item in  board_objects[elem[0]][elem[1]].list:
                                        flag = 1
                                flag_all.append(flag)
                            if sum(flag_all) == 3:
                                nos_triplets[key_nos][0] += 1
                                nos_triplets[key_nos][1].append(key_pos)
                            

                                
                for key_nos, value_pos in nos_triplets.items():
                    #print ("Value pos : ", value_pos[0])
                    if value_pos[0] == 1 :
                        for item in value_pos[1][0]:
                            #board_objects[item[0]][item[1]].list = list(key_nos)
                            for elem in board_objects[item[0]][item[1]].list:
                                if elem not in list(key_nos):	
                                    board_objects[item[0]][item[1]].list.remove(elem)
                            #print ("Removing triples", key_nos, value_pos)



def naked_triples_process(board_objects , row_column):
    print ("in triples 2")
    for i in range(0,9):
	    if row_column == 'row':
		    row = i
		    empty_positions = [(row,k) for k in range(0,9)]
	    else :
		    column = i
		    empty_positions = [(k,column) for k in range(0,9)]

	    existing_values = [k for k in range(1,10) ]
	    pos_triplets = {}
	    nos_triplets = {}
	    for j in range(0,9):
		    if row_column == 'row':
			    column = j
		    else :
			    row = j
		    if board_objects[row][column].value != 0 :
			    if board_objects[row][column].value in existing_values:        
			            existing_values.remove(board_objects[row][column].value)
			    empty_positions.remove((row,column))
	    combinations = list(itertools.combinations(existing_values, 3))
	    combinations_positions = list(itertools.combinations(empty_positions, 3))

	    #for elem in combinations :
	    #        nos_triplets[elem] = [0,[]] 

	    for elem in combinations_positions :
		    pos_triplets[elem] = [] 

	    for key_pos, value_pos in pos_triplets.items():	
		    for elem in key_pos :
			    for number in board_objects[elem[0]][elem[1]].list:
				    if number not in value_pos :
					    pos_triplets[key_pos].append(number)

	    #for key_pos , value_pos in pos_triples.items():
	    #print (pos_triplets)
	    triples_location = {}
           	    
	    for key_pos, value_pos in pos_triplets.items():	
                    if len(value_pos) == 3 :
                            triples_location[tuple(value_pos)] = list(key_pos)

	    print_board()
	    print (triples_location)
	    for key, value in triples_location.items():
		    triples_lists = []
		    print (value)
		    for item in value:
			     triples_lists.append(board_objects[item[0]][item[1]].list)
		    print (triples_lists)
		    remove_triple_rajesh(board_objects, triples_lists,value, row_column)

def naked_triples_rajesh(board_objects):
	naked_triples_process(board_objects, 'row')



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

	if check_board_change(board_objects_before,board_objects):
		print ("change occured")
		print_board()
		inference_rules(board_objects)

	#print('doing doubles')
	#print_board()
	naked_doubles(board_objects)
	#print_board()
	hidden_pairs(board_objects)
	naked_triples_rajesh(board_objects)

#	naked_triple(board_objects)
	hidden_triples(board_objects)

	#print_board()
	
	if (check_sudoku(convert_to_numbers(board_objects))) : 
		return

	if check_board_change(board_objects_before,board_objects):
		print ("change occured")
		print_board()
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
def create_board(board):
    global board_objects
    board_objects = []
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

def select_var(board, n):
    if n == 1:
        for x in range(9):
            for y in range(9):
                if board[x][y].value == 0:
                    return board[x][y]
        return 0
    elif n == 2:
        minVar = 10
        minVarLocation = 0
        for x in range(9):
            for y in range(9):
                if len(board[x][y].list) < minVar and len(board[x][y].list) != 0:
                    minVar = len(board[x][y].list)
                    minVarLocation = board[x][y]

        return minVarLocation
        #run MRV to get var
    

    
def backtrack(board, i):
    #board_objects = []
    #var = select_var(board, 1)
    #print('var', var.x, var.y, var.value)
    #print('solving this board', board)
    inference_rules(board)
    grid = convert_to_numbers(board)
    #print('grid', grid)
    if check_sudoku(grid) or i == 1000:
        print('board complete', i)
        return i

    var = select_var(board, 1)
    #make a move on selected var
    #print('bar', var.x, var.y, var.value)
    try:
        if var == 0:
            print('out of vars')
            return i
        
        #print('move', board[var.x][var.y].value, var.list[0])
        board[var.x][var.y].value = var.list[0]
        board[var.x][var.y].list = []
        calculate_poss(board)
        i+=1
        result = backtrack(board, i)
    except:
        print('var', var)
        if var == 0:
            print('out of vars')
            return i
        #print('move failed', var.value, board[var.x][var.y].list)
        if len(board[var.x][var.y].list) > 0:
            #print('in if')
            board[var.x][var.y].value = 0
            board[var.x][var.y].list.remove(var.value)
            i+=1
            result = backtrack(board, i)
        else:
            print('ran out of possibilities', board[var.x][var.y].value)
            return i
        #print('move', board[var.x][var.y].value, var.list[0])
        
    if result:
        print('result true', result)
        return result
    print('false result')
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
                #print("\nrow single value found: ", val)

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
                #print("\ncol single value found: ", val)
                # print_board()

    #print("\n*********PRINTING AFTER COL BOARD********")
    #print_board()

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
                        #print("\nbox single value found: ", val)
                        #print_board()

    #print("\n*********PRINTING BOX BOARD********")
    #print_board()

def remove_double(board, double, dubxy, where):
    x1 = dubxy[0][0]
    y1 = dubxy[0][1]
    x2 = dubxy[1][0]
    y2 = dubxy[1][1]

    if where == 'row':
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
                board[x2][i].list.remove(double[0])
            except ValueError:
                pass
            try:
                board[x2][i].list.remove(double[1])
            except ValueError:
                pass
            
    elif where == 'col':
        for i in range(9):
            try:
                board[i][y1].list.remove(double[0])
            except ValueError:
                pass
            try:
                board[i][y1].list.remove(double[1])
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
    elif where == 'box':
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
    print('double removed')
    print_board()

def remove_triple(board, triple, dubxy, where):
    print('removing triple', triple, dubxy, where)
    temp = set()
    backup = set()
    order = []
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

    if where == 'row':
        for i in range(9):
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
    elif where == 'col':
        for i in range(9):
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
    elif where == 'box':
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
    print('add back', triple, triple[1], triple[2], backup)
    board[x1][y1].list = list(triple[2])
    board[x2][y2].list = list(triple[0])
    board[x3][y3].list = list(triple[1])
    print_board()
        

def remove_triple_rajesh(board, triple, dubxy, where):
    print('removing triple', triple, dubxy, where)
    temp = set()
    backup = set()
    order = []
    for z in range(3):
        for z2 in range(len(triple[z])):
            temp.add(triple[z][z2])
            temp.add(triple[z][z2])
        backup.add(tuple(triple[z]))
        if z == 2:
            if triple[z] == triple[z-1] and triple[z] == triple[z-2]:
                order = [0,0,0]
                #all 3 same
            elif triple[z] == triple[z-1]:
                order = [0, 1, 1]
                #two same
            elif triple[z] == triple[z-2]:
                #two same
                order = [1, 0, 1]
            elif triple[z-1] == triple[z-2]:
                #two same
                order = [0, 0, 1]
            else:
                order = [0,1,2]
            print('order', order)
        
    double = list(temp)

    x1 = dubxy[0][0]
    y1 = dubxy[0][1]
    x2 = dubxy[1][0]
    y2 = dubxy[1][1]
    x3 = dubxy[2][0]
    y3 = dubxy[2][1]

    if where == 'row':
        for i in range(9):
            for j in range(len(double)):
                try:
                    board[x1][i].list.remove(double[j])               
                except ValueError:
                    pass
                try:
                    board[x2][i].list.remove(double[j])
                except ValueError:
                    pass
                try:
                    board[x3][i].list.remove(double[j])
                except ValueError:
                    pass
              
    elif where == 'col':
        for i in range(9):
            for j in range(len(double)):
                try:
                    board[i][y1].list.remove(double[j])
                except ValueError:
                    pass
                try:
                    board[i][y2].list.remove(double[j])
                except ValueError:
                    pass
                try:
                    board[i][y3].list.remove(double[j])
                except ValueError:
                    pass
    elif where == 'box':
        boxX = x1 - (x1%3)
        boxY = y1 - (y1%3)

        for j in range(boxX, boxX+3):
            for k in range(boxY, boxY+3):
                for l in range(len(double)):
                    try:
                        board[j][k].list.remove(double[l])
                    except ValueError:
                        pass


        boxX = x2 - (x2%3)
        boxY = y2 - (y2%3)

        for j in range(boxX, boxX+3):
            for k in range(boxY, boxY+3):
                for l in range(len(double)):
                    try:
                        board[j][k].list.remove(double[l])
                    except ValueError:
                        pass
        boxX = x3 - (x3%3)
        boxY = y3 - (y3%3)

        for j in range(boxX, boxX+3):
            for k in range(boxY, boxY+3):
                for l in range(len(double)):
                    try:
                        board[j][k].list.remove(double[l])
                    except ValueError:
                        pass



    triple = list(backup)
    print('add back', triple, backup, order)    
    board[x1][y1].list = list(triple[order[0]])
    board[x2][y2].list = list(triple[order[1]])
    board[x3][y3].list = list(triple[order[2]])
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
                    #print("ENTERING THE ROW CELL: {}, {} ".format(x, y))
                    #print("double: ", double)
                    dubxy.append((x,y))
                    # then run the possibilities to remove it from
                    # neighboring cells
                    #remove_double(board_obj, double, x, y)
                    #calculate_poss(board_obj)
            #print('dubrow',dubxy, double)
            remove_double(board_obj, double, dubxy, 'row')
            double = []
            return board_obj

    #print_board()

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
        #print(y)
        #print(double)
        if len(double) == 0:
            continue
        else:
            dubxy = []
            #print("ROW VALUE: ",double)
            for x in range(9):

                # check if list of element = naked double
                if double == board_obj[x][y].list:
                    #print("ENTERING THE COL CELL: {}, {} ".format(x+1, y+1))
                    #print("double: ", double)
                    dubxy.append((x,y))
                    # then run the possibilities to remove it from
                    # neighboring cells
            #print('dubcol',dubxy, double)
            remove_double(board_obj, double, dubxy, 'col')
            double = []
            return board_obj


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
                #print('dubbox: ',dubxy, duplicate)
                remove_double(board_obj, duplicate, dubxy, 'box')
                #print("removed duplicate: ", duplicate)
                #print_board()
                double = []
                return board_obj



# set up naked triple -- PART 1, only checks for
# full triples
def naked_triple(board_obj):
    # find by row
    for x in range(9):
        # func to check if size=2 of each item list in the row
        # return the naked triple
        triple = get_triple(board_obj[x], [])
       # print("triplerow:", triple)
        if len(triple) == 0:
            continue
        else:
            tripxy = []
            for y in range(9):
                # check if list of element = naked triple
                if triple[0] == board_obj[x][y].list:
                    #print("ENTERING THE ROW CELL: {}, {} ".format(x, y))
                    #print("naked triple: ", triple)
                    tripxy.append((x,y))
                elif triple[1] == board_obj[x][y].list:
                    tripxy.append((x,y))
                elif triple[2] == board_obj[x][y].list:
                    tripxy.append((x,y))
                    #remove_double(board_obj, triple, x, y)
                    #calculate_poss(board_obj)
            #print('trip row',tripxy)
            remove_triple(board_obj, triple, tripxy, 'row')
            triple = []
            return board_obj

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
            #print("ROW VALUE: ",triple)
            for x in range(9):
                # check if list of element = naked triple
                if triple[0] == board_obj[x][y].list:
                   # print("ENTERING THE COL CELL: {}, {} ".format(x, y))
                    #print("triple: ", triple[0])
                    tripxy.append((x,y))
                elif triple[1] == board_obj[x][y].list:
                   # print("ENTERING THE COL CELL: {}, {} ".format(x, y))
                    #print("triple: ", triple[0])
                    tripxy.append((x,y))
                elif triple[2] == board_obj[x][y].list:
                   # print("ENTERING THE COL CELL: {}, {} ".format(x, y))
                    #print("triple: ", triple[0])
                    tripxy.append((x,y))
                    # then run the possibilities to remove it from
                    # neighboring cells
            #print('triple col: ',tripxy)
            remove_triple(board_obj, triple, tripxy, 'col')
            triple = []
            return board_obj

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
            #print("pair list: ", pairs)
            triple = get_triple([], pairs)

            if len(triple) == 0:
                continue
            else:
                # remove the naked double from each
                # cell in the box
                tripxy= []
                for j in range(box_x, box_x+3):
                    for k in range(box_y, box_y+3):
                        if triple[0] == board_obj[j][k].list:
                            # print("ENTERING THE BOX CELL: {}, {} ".format(j, k))
                            # print(triple)
                            tripxy.append((j,k))
                        elif triple[1] == board_obj[j][k].list:
                            # print("ENTERING THE BOX CELL: {}, {} ".format(j, k))
                            # print(triple)
                            tripxy.append((j,k))
                        elif triple[2] == board_obj[j][k].list:
                            # print("ENTERING THE BOX CELL: {}, {} ".format(j, k))
                            # print(triple)
                            tripxy.append((j,k))
                            
                #print('dubBBBtrtrtrBBBBBBB: ',triple, tripxy)
                remove_triple(board_obj, triple, tripxy, 'box')
                #print("removed triple: ", triple)
                print_board()
                triple = []
                return board_obj


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
    #[2,6] [2,7] [3,6] [3,7]
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
            if i > 1:
                test_var = double_list[i] and double_list[i-1] and double_list[i-2]
                if test_var == 3:
                    pairs.add((double_list[i][0], double_list[i][1]))
                    pairs.add((double_list[i-1][0], double_list[i-1][1]))
                    pairs.add((double_list[i-2][0], double_list[i-2][1]))

            # start at the next value in list
            for j in range(i+1, length):
                combo.add(double_list[j][0])
                combo.add(double_list[j][1])
                #print('combo', combo)

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
            print('double list', double_list)
            print_board()
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


def naked_triples_process(board_objects, row_column):
    print("in triples 2")
    for i in range(0, 9):
        if row_column == 'row':
            row = i
            empty_positions = [(row, k) for k in range(0, 9)]
        else:
            column = i
            empty_positions = [(k, column) for k in range(0, 9)]

        existing_values = [k for k in range(1, 10)]
        pos_triplets = {}
        nos_triplets = {}
        for j in range(0, 9):
            if row_column == 'row':
                column = j
            else:
                row = j
            if board_objects[row][column].value != 0:
                if board_objects[row][column].value in existing_values:
                    existing_values.remove(board_objects[row][column].value)
                empty_positions.remove((row, column))
        combinations = list(itertools.combinations(existing_values, 3))
        combinations_positions = list(itertools.combinations(empty_positions, 3))

        # for elem in combinations :
        #        nos_triplets[elem] = [0,[]]

        for elem in combinations_positions:
            pos_triplets[elem] = []

        for key_pos, value_pos in pos_triplets.items():
            for elem in key_pos:
                for number in board_objects[elem[0]][elem[1]].list:
                    if number not in value_pos:
                        pos_triplets[key_pos].append(number)

        # for key_pos , value_pos in pos_triples.items():
        # print (pos_triplets)
        triples_location = {}

        for key_pos, value_pos in pos_triplets.items():
            if len(value_pos) == 3:
                triples_location[tuple(value_pos)] = list(key_pos)

        print_board()
        print(triples_location)
        for key, value in triples_location.items():
            triples_lists = []
            print(value)
            for item in value:
                triples_lists.append(board_objects[item[0]][item[1]].list)
            print(triples_lists)
            remove_triple_rajesh(board_objects, triples_lists, value, row_column)


def naked_triples_rajesh(board_objects):
    naked_triples_process(board_objects, 'row')














