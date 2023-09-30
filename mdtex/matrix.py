default_row    = 3
default_column = 3

def generate_matrix(form, matrix, display):
    space  = "\n" if display else " "
    indent = "  " if display else ""
    result = "\\begin{" + form + "matrix}" + space
    for row_vector in matrix[:-1]:
        result += indent + " & ".join(row_vector) + " \\\\" + space
    return result + indent + " & ".join(matrix[-1]) + space + "\\end{" + form + "matrix}"

if __name__ == "__main__":
    print(generate_matrix("b", [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]], True))
    print(generate_matrix("b", [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]], False))