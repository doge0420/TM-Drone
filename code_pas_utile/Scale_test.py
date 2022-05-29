current_row = 0
current_column = 0

for i in range(6):
    row = current_row % 2
    column = int(current_column)
    print(f"({row},{column})")
    current_row += 1
    current_column += 0.5

