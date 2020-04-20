# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 14:25:06 2020

@author: Vinzenz von Teufenstein
"""

# Import required libraries
import numpy as np
import time


# --------------------- Functions ----------------------
def initalize_solver():
    global grid_result
    global full_set
    global grid_possibilities
    global grid_output
    # Create a grid and format it as an np.object so it can hold all possibilites for each cell
    grid_possibilities = np.empty(shape=[9, 9], dtype=object)
    # Fill the grid up with empty cells []
    for row in range(0, 9):
        for column in range(0, 9):
            grid_possibilities[row, column] = []

    # Create a copy of original grid to later update with result
    grid_result = grid_input.copy()

    grid_output = grid_input.copy()
    # Creat np array with full set of possible values for each cell (1-9)
    full_set = np.arange(1, 10, 1)

    return


def create_possible_values():
    global grid_result
    global grid_possibilities
    for row in range(0, 9):
        for column in range(0, 9):
            if grid_result[row][column] == 0:
                # Take full Grid and substract values that are already in the row
                poss_r = np.setdiff1d(full_set, grid_result[row])
                # Take all values that are possible in a row and substract those already in the column
                poss_c = np.setdiff1d(poss_r, grid_result[:, column])

                # Check for values in subgrid
                row_ind = (row // 3) * 3      # Use //3 to get whole numbers
                col_ind = (column // 3) * 3
                poss_overall = np.setdiff1d(
                    poss_c, grid_result[row_ind:row_ind + 3, col_ind:col_ind + 3].flatten())
                grid_possibilities[row, column] = list(poss_overall)
    remove_pairs()
    return


def check_single():
    global grid_result
    global grid_possibilities
    for row in range(0, 9):
        for column in range(0, 9):
            # Check if only one value is possible for a cell! If so, assign it to the cell
            if np.size(grid_possibilities[row, column]) == 1:
                result = grid_possibilities[row][column][0]
                grid_result[row, column] = result
                grid_possibilities[row, column] = []
                create_possible_values()
                check_single()
    return


def check_unique():
    global grid_possibilities
    global grid_result
    # Check for values that only appear once to be possible in each row
    for row in range(0, 9):
        row_poss = np.concatenate(
            grid_possibilities[row], axis=None).astype(int)
        poss_list = list(row_poss)
        unique_value = [x for x in poss_list if poss_list.count(x) == 1]
        for column in range(0, 9):
            if len(unique_value) >= 1:
                for i in range(0, len(unique_value)):
                    if unique_value[i] in grid_possibilities[row, column]:
                        grid_possibilities[row, column] = []
                        grid_result[row, column] = unique_value[i]
                        create_possible_values()

    # Check for values that only appear once to be possible in each row
    for column in range(0, 9):
        column_poss = np.concatenate(
            grid_possibilities[0:, column], axis=None).astype(int)
        column_list = list(column_poss)
        unique_value = [x for x in column_list if column_list.count(x) == 1]
        for row in range(0, 9):
            if len(unique_value) >= 1:
                for i in range(0, len(unique_value)):
                    if unique_value[i] in grid_possibilities[row, column]:
                        grid_possibilities[row, column] = []
                        grid_result[row, column] = unique_value[i]
                        create_possible_values()

    # Check for values that only appear once to be possible in each subgrid
    for sub_row in np.arange(0, 9, 3):
        for sub_col in np.arange(0, 9, 3):
            row_ind = (sub_row // 3) * 3
            col_ind = (sub_col // 3) * 3
            subgrid_possibilities = grid_possibilities[row_ind:row_ind +
                                                       3, col_ind:col_ind + 3].flatten()
            subgrid_poss = np.concatenate(
                subgrid_possibilities, axis=None).astype(int)
            subgrid_list = list(subgrid_poss)
            unique_value = [
                x for x in subgrid_list if subgrid_list.count(x) == 1]
            for subcol in range(col_ind, col_ind + 3):
                for subrow in range(row_ind, row_ind + 3):
                    if len(unique_value) >= 1:
                        for i in range(0, len(unique_value)):
                            if unique_value[i] in grid_possibilities[subrow, subcol]:
                                grid_possibilities[subrow, subcol] = []
                                grid_result[subrow, subcol] = unique_value[i]
                                create_possible_values()
    check_single()
    return


def remove_pairs():
    global grid_possibilities
    # Remove Pairs from rows
    for row in range(0, 9):
        pair = find_pairs(grid_possibilities[row])
        if pair != []:
            value_1 = pair[0]
            value_2 = pair[1]
            for c in range(0, 9):
                if (grid_possibilities[row, c] != pair and grid_possibilities[row, c] != []):
                    if value_1 in grid_possibilities[row, c]:
                        grid_possibilities[row, c].remove(value_1)
                    if value_2 in grid_possibilities[row, c]:
                        grid_possibilities[row, c].remove(value_2)

    # Remove Pairs from columns
    for column in range(0, 9):
        pair = find_pairs(grid_possibilities.T[column])
        if pair != []:
            value_1 = pair[0]
            value_2 = pair[1]
            for c in range(0, 9):
                if (grid_possibilities.T[column, c] != pair and grid_possibilities.T[column, c] != []):
                    if value_1 in grid_possibilities.T[column, c]:
                        grid_possibilities.T[column, c].remove(value_1)
                    if value_2 in grid_possibilities.T[column, c]:
                        grid_possibilities.T[column, c].remove(value_2)

    return


def solve_sudoku():
    global grid_result
    global grid_output
    global grid_possibilities
    global full_set
    iterration = 0
    tries = 5
    start_time = time.time()
    initalize_solver()
    while 0 in grid_result and tries > 0:
        create_possible_values()
        check_single()
        check_unique()
        iterration += 1
        tries -= 1
        grid_output = grid_result.copy()
    if solution_is_valid() == True:
        print('Great! The Sudoku has been successfully solved using human like logic!')
    else:
        bf_solve()
        if solution_is_valid() == True:
            print(
                'Great! The Sudoku has beed successfully solved! However, we had to use brute force!')
    print("Time to solve Sudoku: %s seconds!" % (time.time() - start_time))
    print(str(iterration) + " iterrations used to solve the soduko!")
    print(np.matrix(grid_output))
    del full_set
    del grid_possibilities
    del grid_result
    return


# ----- Helper Function
def find_pairs(row):
    pair = []
    to_compare = []
    for col in row:
        if np.size(col) == 2:
            to_compare.append(col)
            if len(to_compare) > 1:
                try:
                    pair = [x for x in to_compare if to_compare.count(x) == 2]
                    pair = pair[0]
                except:
                    continue
    return pair


def solution_is_valid():
    global grid_output
    global full_set
    valid_rows = 0
    valid_columns = 0
    valid_subgrids = 0
    for row in grid_output:
        if np.array_equal(np.sort(row), full_set) == True:
            valid_rows += 1

    for column in grid_output.T:
        if np.array_equal(np.sort(column), full_set) == True:
            valid_columns += 1

    for subcol in np.arange(0, 9, 3):
        for subrow in np.arange(0, 9, 3):
            sorted_grid = np.sort(
                grid_output[subcol:subcol + 3, subrow:subrow + 3].flatten())
            if np.array_equal(sorted_grid, full_set) == True:
                valid_subgrids += 1
    if valid_rows == 9 and valid_subgrids == 9 and valid_subgrids == 9:
        return True
    else:
        return False


def is_possible(row, column, value):
    # Check row
    global grid_result
    for i in range(0, 9):
        if grid_result[row][i] == value:
            return False
    # Check column
    for i in range(0, 9):
        if grid_result[i][column] == value:
            return False
    # Check subgrid
    row0 = (row // 3) * 3
    column0 = (column // 3) * 3
    for i in range(0, 3):
        for j in range(0, 3):
            if grid_result[row0 + i][column0 + j] == value:
                return False

    return True


def bf_solve():
    global grid_output
    for row in range(0, 9):
        for column in range(0, 9):
            global grid_result
            if grid_result[row][column] == 0:
                for value in grid_possibilities[row][column]:
                    if is_possible(row, column, value):
                        grid_result[row][column] = value
                        bf_solve()
                        grid_result[row][column] = 0
                return
    grid_output = grid_result.copy()


# -------------------------- SUDOKUS ----------------------
# -------- Logically Solvable ---------------
# Creat inital sudoku - Later taken from input
grid_input = np.array([
    [2, 9, 0, 8, 7, 3, 0, 1, 0],
    [4, 0, 0, 0, 0, 5, 9, 2, 0],
    [0, 1, 0, 0, 2, 4, 0, 0, 0],
    [0, 0, 0, 0, 8, 9, 6, 0, 0],
    [0, 0, 4, 0, 0, 0, 8, 3, 0],
    [0, 8, 2, 3, 1, 0, 5, 0, 0],
    [0, 0, 9, 2, 3, 8, 0, 0, 7],
    [8, 0, 0, 0, 4, 7, 0, 0, 0],
    [3, 0, 5, 0, 9, 0, 2, 8, 4]])


# Test Sudoku 1
grid_input = np.array([
    [6, 0, 3, 0, 0, 0, 0, 0, 4],
    [9, 2, 0, 6, 1, 0, 7, 0, 3],
    [0, 0, 0, 9, 0, 0, 2, 5, 0],
    [5, 0, 0, 0, 0, 8, 0, 0, 2],
    [0, 8, 0, 4, 3, 1, 0, 7, 0],
    [7, 0, 0, 5, 0, 0, 0, 0, 8],
    [0, 5, 1, 0, 0, 9, 0, 0, 0],
    [3, 0, 7, 0, 5, 2, 0, 6, 1],
    [8, 0, 0, 0, 0, 0, 9, 0, 5]])


# Test Sudoku 2
grid_input = np.array([
    [0, 0, 8, 6, 0, 0, 2, 5, 9],
    [3, 0, 2, 0, 1, 0, 0, 7, 4],
    [0, 7, 0, 2, 0, 0, 0, 0, 8],
    [0, 0, 0, 0, 3, 1, 5, 6, 0],
    [0, 0, 0, 9, 0, 7, 0, 0, 0],
    [0, 3, 1, 5, 6, 0, 0, 0, 0],
    [9, 0, 0, 0, 0, 6, 0, 4, 0],
    [7, 6, 0, 0, 8, 0, 9, 0, 5],
    [1, 8, 5, 0, 0, 4, 7, 0, 0]])


# Test Sudoku 3
grid_input = np.array([
    [0, 0, 0, 2, 6, 0, 7, 0, 1],
    [6, 8, 0, 0, 7, 0, 0, 9, 0],
    [1, 9, 0, 0, 0, 4, 5, 0, 0],
    [8, 2, 0, 1, 0, 0, 0, 4, 0],
    [0, 0, 4, 6, 0, 2, 9, 0, 0],
    [0, 5, 0, 0, 0, 3, 0, 2, 8],
    [0, 0, 9, 3, 0, 0, 0, 7, 4],
    [0, 4, 0, 0, 5, 0, 0, 3, 6],
    [7, 0, 3, 0, 1, 8, 0, 0, 0]])


# Test Sudoku 4
grid_input = np.array([
    [1, 0, 0, 4, 8, 9, 0, 0, 6],
    [7, 3, 0, 0, 0, 0, 0, 4, 0],
    [0, 0, 0, 0, 0, 1, 2, 9, 5],
    [0, 0, 7, 1, 2, 0, 6, 0, 0],
    [5, 0, 0, 7, 0, 3, 0, 0, 8],
    [0, 0, 6, 0, 9, 5, 7, 0, 0],
    [9, 1, 4, 6, 0, 0, 0, 0, 0],
    [0, 2, 0, 0, 0, 0, 0, 3, 7],
    [8, 0, 0, 5, 1, 2, 0, 0, 4]])


# Test Sudoku 6
grid_input = np.array([
    [3, 5, 0, 0, 8, 6, 0, 0, 0],
    [0, 9, 7, 0, 0, 0, 0, 0, 0],
    [4, 0, 0, 0, 0, 7, 2, 0, 0],
    [2, 1, 8, 0, 0, 3, 0, 0, 9],
    [6, 0, 0, 0, 2, 0, 0, 0, 1],
    [9, 0, 0, 1, 0, 0, 8, 3, 2],
    [0, 0, 9, 8, 0, 0, 0, 0, 3],
    [0, 0, 0, 0, 0, 0, 9, 2, 0],
    [0, 0, 0, 2, 3, 0, 0, 7, 8]])


# Sudoku.com(medium)
grid_input = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 7],
    [6, 4, 9, 2, 0, 0, 8, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 9, 0],
    [0, 6, 2, 0, 7, 0, 0, 5, 1],
    [0, 8, 5, 0, 0, 9, 0, 0, 6],
    [3, 0, 4, 0, 0, 0, 0, 0, 0],
    [4, 0, 0, 0, 0, 0, 0, 7, 5],
    [0, 1, 8, 0, 0, 0, 3, 0, 0],
    [0, 5, 0, 1, 0, 6, 2, 0, 8]])


# Sudoku.com(hard)
grid_input = np.array([
    [0, 8, 7, 0, 2, 0, 0, 5, 0],
    [0, 0, 0, 0, 0, 6, 0, 0, 4],
    [2, 5, 0, 0, 0, 9, 0, 0, 0],
    [3, 4, 5, 0, 0, 0, 0, 0, 0],
    [0, 0, 6, 0, 0, 0, 4, 0, 3],
    [8, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 3, 9, 8, 0],
    [0, 0, 9, 6, 5, 8, 3, 0, 0],
    [5, 0, 0, 2, 9, 0, 6, 0, 0]])

# Sudoku.com(hard)
grid_input = np.array([
    [8, 7, 0, 0, 4, 5, 0, 2, 0],
    [0, 0, 0, 7, 2, 0, 0, 0, 0],
    [0, 0, 6, 0, 0, 0, 0, 7, 0],
    [0, 0, 0, 0, 0, 0, 6, 0, 5],
    [0, 0, 0, 1, 0, 2, 0, 0, 0],
    [7, 6, 4, 0, 0, 8, 0, 0, 0],
    [0, 0, 0, 6, 0, 0, 3, 0, 0],
    [4, 2, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 0, 5, 4, 1, 0, 0]])

# Sudoku.com(expert_2)
grid_input = np.array([
    [0, 0, 0, 0, 0, 2, 0, 0, 0],
    [7, 3, 0, 0, 5, 0, 1, 0, 0],
    [0, 1, 0, 0, 0, 0, 5, 3, 0],
    [5, 0, 0, 0, 4, 0, 0, 0, 0],
    [3, 4, 2, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 8, 6, 0, 0, 5, 0],
    [9, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 4, 3, 0, 0, 0, 6],
    [0, 0, 0, 0, 0, 0, 8, 0, 0]])

# ------------ Brute Force --------------

# Test Sudoku 5
grid_input = np.array([
    [0, 2, 0, 6, 0, 8, 0, 0, 0],
    [5, 8, 0, 0, 0, 9, 7, 0, 0],
    [0, 0, 0, 0, 4, 0, 0, 0, 0],
    [3, 7, 0, 0, 0, 0, 5, 0, 0],
    [6, 0, 0, 0, 0, 0, 0, 0, 4],
    [0, 0, 8, 0, 0, 0, 0, 1, 3],
    [0, 0, 0, 0, 2, 0, 0, 0, 0],
    [0, 0, 9, 8, 0, 0, 0, 3, 6],
    [0, 0, 0, 3, 0, 6, 0, 9, 0]])


# Hard Sudoku!
grid_input = np.array([
    [6, 0, 0, 0, 0, 0, 5, 3, 0],
    [0, 0, 0, 0, 0, 2, 7, 0, 0],
    [5, 0, 7, 0, 9, 6, 0, 1, 8],
    [0, 0, 6, 0, 0, 1, 0, 8, 0],
    [0, 9, 8, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 9, 0, 0],
    [0, 0, 0, 2, 0, 0, 0, 4, 3],
    [3, 1, 0, 0, 0, 9, 0, 6, 2]])


# Sudoku.com(expert_Maybe_wrong!)
grid_input = np.array([
    [0, 0, 0, 0, 0, 0, 3, 9, 6],
    [7, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 2, 0, 8, 0, 0, 0],
    [0, 0, 0, 0, 0, 9, 6, 7, 0],
    [8, 0, 0, 3, 0, 6, 0, 0, 9],
    [0, 4, 0, 0, 0, 0, 0, 0, 0],
    [3, 0, 0, 0, 0, 5, 0, 0, 0],
    [0, 0, 5, 0, 2, 0, 7, 0, 0],
    [9, 0, 0, 0, 7, 0, 4, 1, 0]])


# Other hard one
grid_input = np.array([
    [0, 0, 2, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 5, 1, 0, 6, 9, 7, 4],
    [0, 7, 0, 0, 0, 5, 0, 0, 1],
    [0, 2, 6, 3, 9, 1, 8, 4, 0],
    [4, 0, 0, 8, 0, 0, 0, 5, 0],
    [1, 8, 4, 9, 0, 3, 5, 0, 0],
    [0, 9, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 4, 0, 0]])


# Sudoku.com(expert_3)
grid_input = np.array([
    [0, 0, 0, 0, 0, 2, 0, 0, 0],
    [0, 0, 9, 1, 0, 0, 0, 0, 7],
    [0, 6, 1, 0, 0, 4, 0, 0, 0],
    [0, 0, 2, 0, 9, 0, 0, 0, 1],
    [7, 0, 5, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 3, 8, 4, 0],
    [0, 8, 0, 0, 3, 0, 0, 2, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 8],
    [0, 0, 0, 0, 0, 7, 4, 9, 0]])

# Sudoku.com(expert_4)
grid_input = np.array([
    [0, 0, 0, 0, 0, 0, 5, 0, 0],
    [0, 7, 0, 9, 0, 0, 0, 0, 2],
    [0, 4, 0, 6, 8, 0, 1, 0, 0],
    [0, 0, 0, 0, 3, 2, 0, 0, 0],
    [0, 0, 6, 0, 9, 0, 0, 0, 4],
    [5, 0, 3, 0, 0, 4, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 6],
    [7, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 9, 0, 0, 0, 0, 7, 0]])

# finnish guy claims to have created hardest sudoku:
grid_input = np.array([
    [8, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 6, 0, 0, 0, 0, 0],
    [0, 7, 0, 0, 9, 0, 2, 0, 0],
    [0, 5, 0, 0, 0, 7, 0, 0, 0],
    [0, 0, 0, 0, 4, 5, 7, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 3, 0],
    [0, 0, 1, 0, 0, 0, 0, 6, 8],
    [0, 0, 8, 5, 0, 0, 0, 1, 0],
    [0, 9, 0, 0, 0, 0, 4, 0, 0]])


# --------------------- Execution ------------

solve_sudoku()
