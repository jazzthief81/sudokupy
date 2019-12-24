grid = []

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
        init_grid()
    elif (command == "help"):
        print_help()
    elif (command == "import"):
        import_grid()
    elif (command == "input"):
        input_grid()
    elif (command == "print"):
        print_grid()
    elif (command == "quit"):
        quit()
    elif (command == "solve"):
        solve()
    elif (command == "validate"):
        validate_grid()
    else:
        print("'"+command+"' is not recognized as a command.")
        print("Type 'help' for more information.")

def print_help():    
    print("clear    Clears the grid.")
    print("help     Provides help for SudokuPy commands.")
    print("import   Imports a grid from a file.")
    print("input    Inputs a grid from the command line.")
    print("print    Prints the grid.")
    print("solve    Solves the grid.")
    print("quit     Quits SudokuPy.")
    print("validate Validates the grid.")

def init_grid():
    for col in range(9):
        column = []
        grid.append(column)
        for row in range(9):
        	column.append(0)

def import_grid():
    file_name = input("  File name> ")
    file = open(file_name)
    for row in range(9):
        new_row = file.readline()
        import_row(row, new_row)

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
                
def print_grid():
    for row in range(9):
        for col in range(9):
            # Print cell value
            cell = grid[col][row]
            cell_as_string =  "." if cell == 0 else cell
            print(cell_as_string, end = "")

            # Leave open column between subgrids.
            if (col%3 == 2):
                print(" ", end = "")
        print()

        # Leave open row between subgrids.
        if (row < 8 and row%3 == 2):
            print()

def validate_grid():
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
                print("Value " + str(value) + 
                      " occurs " + str(row_frequencies[index][value]) + 
                      " times in row " + str(index+1))
            if (column_frequencies[index][value] > 1):
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

    # Calculate possibles moves for each cell.
    moves = calculate_moves()

    # Print out cells that have no possible move.
    for col in range(9):
        for row in range(9):
            if (len(moves[col][row]) == 0 and grid[col][row] == 0):
                print("Cell at column " + str(col+1) +
                      " and row " + str(row+1) + 
                      " has no valid move.")

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
    
    # Remove values that would introduce duplicates in the row, column or subgrid it is in.
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

def solve():   
    moves = None

    # Keep solving cells that have only one valid move.
    while(True): 
        moves = calculate_moves()    

        move_applied = False
        for col in range(9):
            for row in range(9):
                if(len(moves[col][row]) == 1):
                    grid[col][row] = moves[col][row][0]
                    move_applied = True
                    print_grid()
                    print() 
                    print() 
        
        if (not move_applied):
            break;

main()