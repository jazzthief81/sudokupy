import random

grid = []
all_solutions = True
variants = ["Sudoku", "Sudoku X"]
selected_variant = 0

def main():
    welcome()
    init_grid()
    while(True):
        read_command()

def welcome():
    print("SudokuPy - by jazzthief81 (c) 2019.")
    print("Type 'help' for more information.")
    
def read_command():
    command = input("SudokuPy>>> ")
    if(command == ""):
        return
    elif (command == "clear"):
        clear_grid()
    elif (command == "export"):
        export_grid()
    elif (command == "generate"):
        generate_grid()
    elif (command == "help"):
        print_help()
    elif (command == "import"):
        import_grid()
    elif (command == "input"):
        input_grid()
    elif (command == "move"):
        move()
    elif (command == "print"):
        print_grid()
    elif (command == "quit"):
        quit()
    elif (command == "remove"):
        remove()
    elif (command == "solve"):
        solve(0, all_solutions, True)
    elif (command == "validate"):
        validate_grid(True)
    elif (command == "variant"):
        set_variant()
    else:
        print("'{}' is not recognized as a command.".format(command))
        print("Type 'help' for more information.")

def print_help():    
    print("clear    Clears the grid.")
    print("export   Exports a grid to a file.")
    print("generate Generates a grid with clues.")
    print("help     Provides help for SudokuPy commands.")
    print("import   Imports a grid from a file.")
    print("input    Inputs a grid from the command line.")
    print("move     Fills out one value on the grid.")
    print("print    Prints the grid.")
    print("quit     Quits SudokuPy.")
    print("remove   Removes one value from the grid.")
    print("solve    Solves the grid.")
    print("validate Validates the grid.")
    print("variant  Sets the Sudoku variant being played.")

def init_grid():
    for col in range(9):
        grid.append([0]*9)

def clear_grid():
    for col in range(9):
        for row in range(9):
            grid[col][row] = 0

def generate_grid():
    nb_clues = input_value("Number of clues", 0, 9*9)
    clear_grid()
    for clue_index in range(nb_clues):
        moves = calculate_moves()
        cell_index = random.randrange(9*9 - clue_index)
        [col,row] = get_empty_cell(cell_index)
        moves_for_cell = moves[col][row]
        if(len(moves_for_cell) > 0):
            random_moves = random.sample(moves_for_cell, len(moves_for_cell))
            saved_grid = save_grid()
            for move_index in range(len(random_moves)):
                #print("Trying move {} out of {}".format(move_index+1,len(random_moves)))
                grid[col][row] = random_moves[move_index]
                moved_grid = save_grid()
                if (solve(0, False, False)):
                    #print("Clue {}".format(clue_index + 1))
                    load_grid(moved_grid)
                    break
                else:
                    load_grid(saved_grid)
        else:
            raise RuntimeError("Generator failed")

def get_empty_cell(cell_index):
    for col in range(9):
        for row in range(9):
            if(grid[col][row] == 0):
                cell_index -= 1
                if(cell_index<0):
                    return [col,row]

def save_grid():
    saved_grid = []
    for col in range(9):
        column = []
        saved_grid.append(column)
        for row in range(9):
            column.append(grid[col][row])
    return saved_grid

def load_grid(saved_grid):   
    for col in range(9):
        for row in range(9):
            grid[col][row] = saved_grid[col][row]

def import_grid():
    file_name = input("  File name> ")
    file = open(file_name)
    for row in range(9):
        new_row = file.readline()
        import_row(row, new_row)

def export_grid():
    file_name = input("  File name> ")
    file = open(file_name, "w")
    for row in range(9):
        row_str = ""
        for col in range(9):
            if (grid[col][row] == 0):
                row_str += "."
            else:
                row_str += str(grid[col][row])
        file.write(row_str)
        file.write('\n')
    file.close()

def input_grid():
    for row in range(9):
        new_row = input("  Row {}> ".format(row+1))
        import_row(row, new_row)

def import_row(row, new_row):
    for col in range(9):
        newCell = new_row[col:col+1]
        if (ord("0") < ord(newCell) and ord(newCell) <= ord("9")):
            grid[col][row] = int(newCell)     
        else:
            grid[col][row] = 0

def move():
    col = input_value("Column", 1, 9)
    row = input_value("Row", 1, 9)
    value = input_value("Value", 1, 9)
    grid[col-1][row-1] = value

def remove():
    col = input_value("Column", 1, 9)
    row = input_value("Row", 1, 9)
    grid[col-1][row-1] = 0

def input_value(name, min, max):
    value = None
    while(value == None):
        value_str = input("  {} ({}-{})> ".format(name, min, max))
        try:
            value = int(value_str)
            if (value<min or value>max):
                print("'{}' is out of range ({}-{})".format(value_str, min, max))
                value = None
        except:
            print("'{}' is not a number".format(value_str))
    return value
                
def print_grid():
    # Print column numbers.
    print_separator(short = True)
    print("  |", end = "")
    for col in range(9):
        print(str(col+1), end = "")
        if (col%3 == 2):
            print("|", end = "")
    print()

    # Leave separator row after column numbers.
    print_separator()

    for row in range(9):
        # Print row number.
        print("|", end = "")
        print(str(row+1), end = "|")

        for col in range(9):
            # Print cell value.
            cell = grid[col][row]
            cell_as_string =  "." if cell == 0 else cell
            print(cell_as_string, end = "")

            # Leave open column between subgrids.
            if (col%3 == 2):
                print("|", end = "")
        print()

        # Leave separator row between subgrids.
        if (row < 8 and row%3 == 2):
            print_separator()

    # Leave separator row after all subgrids.
    print_separator()

def print_separator(short = False):
    if(not short):
        print("+-+", end = "")
    else:
        print("  +", end = "")

    for col in range(9):
        print("-", end = "")
        if (col%3 == 2):
            print("+", end = "")
    print()

def validate_grid(print_violations):
    valid = True

    # Count how many times the values 1-9 appear in each row and column.
    row_frequencies = []
    column_frequencies = []
    for index in range(9):
        row_frequencies.append([0] * 10)
        column_frequencies.append([0] * 10)

    for col in range(9):
        for row in range(9):
            cell = grid[col][row]
            row_frequencies[row][cell] += 1
            column_frequencies[col][cell] += 1
    
    # Print out duplicate values in each row and column.
    for index in range(9):
        for value in range(1, 10):
            if (row_frequencies[index][value] > 1):
                valid = False
                if (print_violations):
                    print("Value {} occurs {} times in row {}".format(
                        value, row_frequencies[index][value], index+1))
            if (column_frequencies[index][value] > 1):
                valid = False
                if (print_violations):
                    print("Value {} occurs {} times in column {}".format(
                        value, column_frequencies[index][value], index+1))

    # Count how many times the values 1-9 appear in each subgrid.
    subgrid_frequencies = []
    for sub_col in range(3):
        subgrid_col_frequencies = []
        subgrid_frequencies.append(subgrid_col_frequencies)
        for sub_row in range(3):
            subgrid_row_frequencies = []
            subgrid_col_frequencies.append(subgrid_row_frequencies)
            for value in range(10):
                subgrid_row_frequencies.append(0)

    if (variants[selected_variant] == "Sudoku X"):
        # Count how many times the values 1-9 appear in each diagonal.
        diagonal1_frequencies = [0] * 10
        diagonal2_frequencies = [0] * 10

        for index in range(9):
            diagonal1_frequencies[grid[index][index]] += 1
            diagonal2_frequencies[grid[index][8-index]] += 1

        # Print out duplicate values in each diagonal.
        for value in range(1, 10):
            if (diagonal1_frequencies[value] > 1):
                valid = False
                if (print_violations):
                    print("Value {} occurs {} times in the first diagonal".format(
                        value, diagonal1_frequencies[value]))
            if (diagonal2_frequencies[value] > 1):
                valid = False
                if (print_violations):
                    print("Value {} occurs {} times in the second diagonal".format(
                        value, diagonal2_frequencies[value]))

    # Calculate possibles moves for each cell.
    moves = calculate_moves()

    # Print out cells that have no possible move.
    for col in range(9):
        for row in range(9):
            if (len(moves[col][row]) == 0 and grid[col][row] == 0):
                valid = False
                if (print_violations):
                    print("Cell at column {} and row {} has no valid move".format(
                            col+1, row+1))

    return valid

def set_variant():
    global selected_variant
    for variant in range(len(variants)):
        print("[{}] {}".format(variant+1, variants[variant]), end="")
        if (variant == selected_variant):
            print(" (selected)")
        else:
            print()
    selected_variant = input_value("Choose variant", 1, len(variants))-1

def is_grid_solved():    
    # If any if the cells is not filled out yet, the grid is not solved.
    for col in range(9):
        for row in range(9):
            if (grid[col][row] == 0):
                return False
    return True

def calculate_moves():
    # Start off with all values from 1-9 in each empty cell.
    moves = []
    for col in range(9):
        column = []
        moves.append(column)
        for row in range(9):
            if (grid[col][row] == 0):
                column.append(set(range(1, 10)))
            else:
                column.append(set())
    
    # Remove values that would introduce duplicates in the row, column, diagonal or subgrid it is in.
    for col in range(9):
        for row in range(9):
            cell = grid[col][row]

            # Remove values in the same row.
            for index in range(9):
                moves[index][row].discard(cell)

            # Remove values in the same column.
            for index in range(9):
                moves[col][index].discard(cell)

            if (variants[selected_variant] == "Sudoku X"):
                if(row == col):
                    # Remove values in the same diagonal.
                    for index in range(9):
                        moves[index][index].discard(cell)
                if(row == 8-col):
                    # Remove values in the same diagonal.
                    for index in range(9):
                        moves[index][8-index].discard(cell)

            # Remove values in the same subgrid.
            left_col = int(col/3)*3
            top_row = int(row/3)*3
            for other_row in range(3):       
                for other_col in range(3):
                    moves[left_col+other_col][top_row+other_row].discard(cell)

    return moves

def solve(depth, all_solutions, print_solutions):  
    moves = None

    # Keep solving cells that have only one valid move.
    while(True): 
        moves = calculate_moves()    

        move_applied = False
        for col in range(9):
            for row in range(9):
                if (len(moves[col][row]) == 1):
                    for move in moves[col][row]:
                        grid[col][row] = move
                        move_applied = True
        
        if (not move_applied):
            break

    if(validate_grid(False)):    
        if (is_grid_solved()):
            if (print_solutions):
                print_grid()
                print("Depth: {}".format(depth))
            return True
        else:
            # Try out uncertain moves and recursively try to solve from there.
            for branch_factor in range(2,10):
                for col in range(9):
                    for row in range(9):
                        if (len(moves[col][row]) == branch_factor):
                            nb_solved_branches = 0
                            for move in moves[col][row]:
                                saved_grid = save_grid()
                                grid[col][row] = move
                                solved = solve(depth+1, all_solutions, print_solutions)
                                if (solved):
                                    nb_solved_branches += 1
                                    if(not all_solutions):
                                        break
                                load_grid(saved_grid)

                            # If none of the gambles worked out, the solver needs to backtrack.
                            return nb_solved_branches > 0

            # It should never reach this point since there should have been one unsolved cell.
            raise RuntimeError("Solver failed")              
    else:
        # If no more moves are possible, the solver needs to backtrack.
        return False


main()
