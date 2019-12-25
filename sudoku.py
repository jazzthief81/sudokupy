grid = []
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
    elif (command == "solve"):
        solve(0)
    elif (command == "validate"):
        validate_grid(True)
    elif (command == "variant"):
        set_variant()
    else:
        print("'"+command+"' is not recognized as a command.")
        print("Type 'help' for more information.")

def print_help():    
    print("clear    Clears the grid.")
    print("export   Exports a grid to a file.")
    print("help     Provides help for SudokuPy commands.")
    print("import   Imports a grid from a file.")
    print("input    Inputs a grid from the command line.")
    print("move     Fills out one value on the grid.")
    print("print    Prints the grid.")
    print("solve    Solves the grid.")
    print("quit     Quits SudokuPy.")
    print("validate Validates the grid.")
    print("variant  Sets the Sudoku variant being played.")

def init_grid():
    for col in range(9):
        column = []
        grid.append(column)
        for row in range(9):
        	column.append(0)

def clear_grid():
    for col in range(9):
        for row in range(9):
            grid[col][row] = 0

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
        new_row = input("  Row " + str(row+1) + "> ")
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

def input_value(name, min, max):
    value = None
    while(value == None):
        value_str = input("  " + name + " (" + str(min) + "-" + str(max) + ")> ")
        try:
            value = int(value_str)
            if (value<min or value>max):
                print("'" + value_str + "' is out of range (" + str(min) + "-" + str(max) + ")")
                value = None
        except:
            print("'" + value_str + "' is not a number")
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
        row_frequency = []
        row_frequencies.append(row_frequency)
        column_frequency = []
        column_frequencies.append(column_frequency)
        for value in range(10):
            row_frequency.append(0)
            column_frequency.append(0)

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
                    print("Value " + str(value) + 
                          " occurs " + str(row_frequencies[index][value]) + 
                          " times in row " + str(index+1))
            if (column_frequencies[index][value] > 1):
                valid = False
                if (print_violations):
                    print("Value " + str(value) + 
                          " occurs " + str(column_frequencies[index][value]) +
                          " times in column " + str(index+1))

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
        diagonal1_frequencies = []
        diagonal2_frequencies = []
        for value in range(10):
            diagonal1_frequencies.append(0)
            diagonal2_frequencies.append(0)

        for index in range(9):
            diagonal1_frequencies[grid[index][index]] += 1
            diagonal2_frequencies[grid[index][8-index]] += 1

        # Print out duplicate values in each diagonal.
        for value in range(1, 10):
            if (diagonal1_frequencies[value] > 1):
                valid = False
                if (print_violations):
                    print("Value " + str(value) + 
                          " occurs " + str(diagonal1_frequencies[value]) + 
                          " times in the first diagonal")
            if (diagonal2_frequencies[value] > 1):
                valid = False
                if (print_violations):
                    print("Value " + str(value) + 
                          " occurs " + str(diagonal2_frequencies[value]) + 
                          " times in the second diagonal")

    # Calculate possibles moves for each cell.
    moves = calculate_moves()

    # Print out cells that have no possible move.
    for col in range(9):
        for row in range(9):
            if (len(moves[col][row]) == 0 and grid[col][row] == 0):
                valid = False
                if (print_violations):
                    print("Cell at column " + str(col+1) +
                          " and row " + str(row+1) + 
                          " has no valid move.")

    return valid

def set_variant():
    global selected_variant
    for variant in range(len(variants)):
        print("[" + str(variant+1) + "] " + variants[variant], end="")
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
        for row in range(9):
            values = []
            if (grid[col][row] == 0):
                for value in range(1, 10):
                    values.append(value)
            column.append(values)
        moves.append(column)
    
    # Remove values that would introduce duplicates in the row, column, diagonal or subgrid it is in.
    for col in range(9):
        for row in range(9):
            cell = grid[col][row]

            # Remove values in the same row.
            for index in range(9):
                try:
                    moves[index][row].remove(cell)
                finally:
                    continue  

            # Remove values in the same column.
            for index in range(9):
                try:
                    moves[col][index].remove(cell)
                finally:
                    continue     

            if (variants[selected_variant] == "Sudoku X"):
                if(row == col):
                    # Remove values in the same diagonal.
                    for index in range(9):
                        try:
                            moves[index][index].remove(cell)
                        finally:
                            continue  
                if(row == 8-col):
                    # Remove values in the same diagonal.
                    for index in range(9):
                        try:
                            moves[index][8-index].remove(cell)
                        finally:
                            continue  

            # Remove values in the same subgrid.
            left_col = int(col/3)*3
            top_row = int(row/3)*3
            for other_row in range(3):       
                for other_col in range(3):
                    try:
                        moves[left_col+other_col][top_row+other_row].remove(cell)
                    finally:
                        continue 

    return moves

def solve(depth):  
    moves = None

    # Keep solving cells that have only one valid move.
    while(True): 
        moves = calculate_moves()    

        move_applied = False
        for col in range(9):
            for row in range(9):
                if (len(moves[col][row]) == 1):
                    grid[col][row] = moves[col][row][0]
                    move_applied = True
        
        if (not move_applied):
            break;

    if(validate_grid(False)):    
        if (is_grid_solved()):
            return True
        else:
            # Try out uncertain moves and recursively try to solve from there.
            for branch_factor in range(2,10):
                for col in range(9):
                    for row in range(9):
                        branches = moves[col][row]
                        if (len(branches) == branch_factor):
                            for branch_index in range(len(branches)):
                                saved_grid = save_grid()
                                grid[col][row] = branches[branch_index]
                                solved = solve(depth+1)
                                if (solved):
                                    return True
                                else:
                                    load_grid(saved_grid)

                            # If none of the gambles worked out, the solver needs to backtrack.
                            return False

            # It should never reach this point since there should have been one unsolved cell.
            raise RuntimeError("Solver failed")              
    else:
        # If no more moves are possible, the solver needs to backtrack.
        return False


main()
