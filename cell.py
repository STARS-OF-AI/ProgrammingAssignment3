"""
Christopher Mendez, Rupika Dikkala & Rajesh Mangannavar
Programming Assignment 3
Sudoku
CS 531 - AI
February 17, 2020
***********************************
This file contains the cell class which is
each square in the sudoku board.
"""


class cell(object):
    def __init__(self, value, x, y):
        self.value = value
        if value != 0 :
            self.list = []
        else:
            self.list = [i+1 for i in range(9)]
        self.x = x
        self.y = y

