if __name__ != "__main__":
    from mdtex.scopes import display_math
else:
    display_math = lambda: True
import re
from itertools import product

default_row_num = 3
default_col_num = 3

def matrix_template(form, matrix, display):
    space  = "\n" if display else " "
    indent = "  " if display else ""
    result = "\\begin{" + form + "matrix}" + space
    for row_vector in matrix[:-1]:
        result += indent + " & ".join(row_vector) + " \\\\" + space
    return result + indent + " & ".join(matrix[-1]) + space + "\\end{" + form + "matrix}"

def debug(matrix, snip = None):
    if __name__ == "__main__":
        print(matrix_template('p', matrix, 1))
    else:
        snip.expand_anon(matrix_template('p', matrix, 1))

rcn_replace    = lambda content, row, col, row_num: content.replace('\\r', str(row + 1)).replace('\\c', str(col + 1)).replace('\\n', str(row * row_num + col + 1))
dynvar_replace = lambda content, row, col, row_num, dyn = 1: re.sub(r'`([\s\d+*/-]*)`', lambda m: str(eval(m.group(1))), rcn_replace(content, row, col, row_num)) if dyn else rcn_replace(content, row, col, row_num)
placeholder    = lambda tabstop, content: (tabstop + 1, "${%d:%s" % (tabstop + 1, content) + "}")
row_vec        = lambda matrix,  row: matrix[row - 1]
col_vec        = lambda matrix,  col: [row[col - 1] for row in matrix]

def generate_matrix(form, options, size, content, snip):
    display = 1 if display_math() else 0
    if options:
        if   '0' in options: matrix_style = '0'
        elif 'i' in options: matrix_style = 'i'
        elif 'd' in options: matrix_style = 'd'
        elif 'D' in options: matrix_style = 'D'
        elif 't' in options: matrix_style = 't'
        elif 'T' in options: matrix_style = 'T'
        elif 'c' in options: matrix_style = 'c'
        elif 's' in options: matrix_style = 's'
        else               : matrix_style = ''
    else: matrix_style = ''
    fill_zero         = 0 if '-' in options else 1
    auto_dots         = 1 if '.' in options else 0
    tabstop_for_0_all = 1 if '1' in options else 0
    tabstop_for_0_sep = 1 if '2' in options else 0
    tabstop_in_style  = 0 if '3' in options else 1

    empty_element = "0" if fill_zero else ""

    if size:
        if len(size) == 1: row_num= col_num = int(size)
        elif len(size) == 2: row_num, col_num = int(size[0]), int(size[1])
    else: row_num, col_num = default_row_num, default_col_num

    matrix = [[empty_element for j in range(col_num)] for i in range(row_num)]

    tabstop   = 0
    if matrix_style == '0':
        if tabstop_for_0_sep:
            for i, j in product(range(row_num), range(col_num)):
                tabstop, matrix[i][j] = placeholder(tabstop, matrix[i][j])
        elif tabstop_for_0_all:
            for i, j in product(range(row_num), range(col_num)):
                _, matrix[i][j] = placeholder(0, matrix[i][j])
        debug(matrix, snip)
    elif row_num == col_num:
        if matrix_style in 'id':
            for i, j in product(range(row_num), range(col_num)):
                if i == j:
                    matrix[i][j] = dynvar_replace(content, i, j, col_num)
                    if matrix_style == 'i' and not content:
                        tabstop, matrix[i][j] = placeholder(0, matrix[i][j])
                    elif matrix_style == 'd' and tabstop_in_style:
                        tabstop, matrix[i][j] = placeholder(tabstop, matrix[i][j])
                elif tabstop_for_0_sep:
                    tabstop, matrix[i][j] = placeholder(tabstop, matrix[i][j])
                elif tabstop_for_0_all:
                    _, matrix[i][j] = placeholder(row_num if tabstop_in_style else 0, matrix[i][j])
            debug(matrix, snip)
        elif matrix_style == 'D':
            for i, j in product(range(row_num), range(col_num)):
                if i == row_num - 1 - j:
                    matrix[i][j] = dynvar_replace(content, i, j, col_num)
                    if matrix_style == 'i' and not content:
                        tabstop, matrix[i][j] = placeholder(0, matrix[i][j])
                    elif matrix_style == 'd' and tabstop_in_style:
                        tabstop, matrix[i][j] = placeholder(tabstop, matrix[i][j])
                elif tabstop_for_0_sep:
                    tabstop, matrix[i][j] = placeholder(tabstop, matrix[i][j])
                elif tabstop_for_0_all:
                    _, matrix[i][j] = placeholder(row_num if tabstop_in_style else 0, matrix[i][j])
            debug(matrix, snip)
        elif matrix_style == 't':
            for i, j in product(range(row_num), range(col_num)):
                if i <= j:
                    matrix[i][j] = dynvar_replace(content, i, j, col_num)
                    if tabstop_in_style or not content:
                        tabstop, matrix[i][j] = placeholder(tabstop, matrix[i][j])
                elif tabstop_for_0_sep:
                    tabstop, matrix[i][j] = placeholder(tabstop, matrix[i][j])
            debug(matrix, snip)
        elif matrix_style == 'T':
            for i, j in product(range(row_num), range(col_num)):
                if i >= j:
                    matrix[i][j] = dynvar_replace(content, i, j, col_num)
                    if tabstop_in_style or not content:
                        tabstop, matrix[i][j] = placeholder(tabstop, matrix[i][j])
                elif tabstop_for_0_sep:
                    tabstop, matrix[i][j] = placeholder(tabstop, matrix[i][j])
            debug(matrix, snip)
        elif matrix_style == 'c': # 常对角矩阵，对角线使用相同 tabstop
            for i in range(row_num):
                

if __name__ == "__main__":
    # print(matrix_template("b", [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]], True))
    # print(matrix_template(jj"b", [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]], False))
    generate_matrix("b", "i2", "4", "a", None)

# Adapted from https://github.com/sillybun/zyt-snippet
def generate_matrix_element(i, j, row, column, virtual_row, virtual_column, ht, vt):
    vdot = False
    hdot = False
    leftp = "{"
    rightp = "}"
    # print(i, j, row, column, virtual_row, virtual_column)
    # print(ht)
    # print(vt)
    if i > 1 and ht[j].strip() == "\\cdots":
        vdot = True
    if j > 1 and vt[i].strip() == "\\vdots":
        hdot = True
    if vdot and hdot:
        return "\\ddots"
    elif vdot:
        return "\\cdots"
    elif hdot:
        return "\\vdots"
    elif i > 1 or j > 1:
        if virtual_row == "0":
            if i > 1 and j > 1:
                value = ""
                if re.sub("\d", "*", ht[1]) == re.sub("\d", "*", ht[2]) == re.sub("\d", "*", vt[2]):
                    for index in range(len(ht[1])):
                        if not ht[1][index].isnumeric():
                            value += ht[1][index]
                        else:
                            x1 = int(ht[1][index])
                            x2 = int(ht[2][index])
                            x3 = int(vt[2][index])
                            value += str((x2 - x1) * (j-1) + (x3 - x1) * (i-1) + x1)
                    return value
                elif re.match(".*[a-zA-Z]_\{11\}", ht[1]):
                    return re.sub("([a-zA-Z])_\{11\}", "\\g<1>_{" + str(i) + str(j) + "}", ht[1])
                else:
                    return ""
            elif i > 2:
                value = ""
                if re.sub("\d", "*", ht[1]) == re.sub("\d", "*", vt[2]):
                    for index in range(len(ht[1])):
                        if not ht[1][index].isnumeric():
                            value += ht[1][index]
                        else:
                            x1 = int(ht[1][index])
                            x3 = int(vt[2][index])
                            value += str((x3 - x1) * (i - 1) + x1)
                    return value
                elif re.match(".*[a-zA-Z]_\{11\}", ht[1]):
                    return re.sub("([a-zA-Z])_\{11\}", "\\g<1>_{" + str(i) + str(j) + "}", ht[1])
                else:
                    return ""
            elif j > 2:
                value = ""
                if re.sub("\d", "*", ht[1]) == re.sub("\d", "*", ht[2]):
                    for index in range(len(ht[1])):
                        if not ht[1][index].isnumeric():
                            value += ht[1][index]
                        else:
                            x1 = int(ht[1][index])
                            x2 = int(ht[2][index])
                            value += str((x2 - x1) * (j-1) + x1)
                    return value
                elif re.match(".*[a-zA-Z]_\{11\}", ht[1]):
                    return re.sub("([a-zA-Z])_\{11\}", "\\g<1>_{" + str(i) + str(j) + "}", ht[1])
                else:
                    return ""
            elif re.match(".*[a-zA-Z]_\{11\}", ht[1]):
                return re.sub("([a-zA-Z])_\{11\}", "\\g<1>_{" + str(i) + str(j) + "}", ht[1])
            else:
                return ht[1]
        else:
            vdot = False
            hdot = False
            if any([x.strip() == "\\vdots" for x in vt[:-1]]):
                hdot = True
            if any([x.strip() == "\\cdots" for x in ht[:-1]]):
                vdot = True
            flag = False
            biasandvirtualbias = False
            if i > 1 and j > 1:
                value = ""
                underline = False
                if re.sub("\d", "*", ht[1]) == re.sub("\d", "*", ht[2]) == re.sub("\d", "*", vt[2]):
                    for index in range(len(ht[1])):
                        if not ht[1][index].isnumeric():
                            value += ht[1][index]
                            biasandvirtualbias = False
                            if ht[1][index] == "_":
                                underline = True
                            else:
                                underline = False
                        else:
                            x1 = int(ht[1][index])
                            x2 = int(ht[2][index])
                            x3 = int(vt[2][index])
                            virtual_bias = ""
                            bias = x1
                            if underline and ht[1][index-1] == "_":
                                value += leftp
                            if not vdot:
                                bias += (x2 - x1) * (j - 1)
                            else:
                                bias += -(column - j) * (x2 - x1) - (x2 - x1)
                                if x2 != x1:
                                    if x2 == x1 + 1:
                                        virtual_bias += virtual_column
                                    elif x1 == x2 + 1:
                                        virtual_bias += "-" + virtual_column
                                    else:
                                        virtual_bias += str(x2 - x1) + virtual_column
                            if not hdot:
                                bias += (x3 - x1) * (i - 1)
                            else:
                                bias += -(row - i) * (x3 - x1) - (x3 - x1)
                                if x3 != x1:
                                    if x3 == x1 + 1:
                                        virtual_bias += ("+" if virtual_bias else "") + virtual_row
                                    elif x1 == x3 + 1:
                                        virtual_bias += "-" + virtual_row
                                    else:
                                        virtual_bias += ("+" if virtual_bias and x3 > x1 else "") + str(x3 - x1) + virtual_row
                            if index > 0 and ht[1][index-1].isnumeric() and (biasandvirtualbias or (bias and virtual_bias)):
                                value += ","
                            biasandvirtualbias = bias and virtual_bias
                            if bias == 0:
                                value += virtual_bias
                            else:
                                value += virtual_bias + ("+" if virtual_bias and bias > 0 else "") + str(bias)
                            if underline and (index == len(ht[1])-1 or not ht[1][index+1].isnumeric()):
                                value += rightp
                    return value
                    flag = True
            elif i > 2:
                value = ""
                underline = False
                if re.sub("\d", "*", ht[1]) == re.sub("\d", "*", vt[2]):
                    for index in range(len(ht[1])):
                        if not ht[1][index].isnumeric():
                            biasandvirtualbias = False
                            value += ht[1][index]
                            if ht[1][index] == "_":
                                underline = True
                            else:
                                underline = False
                        else:
                            x1 = int(ht[1][index])
                            x3 = int(vt[2][index])
                            virtual_bias = ""
                            bias = x1
                            if underline and ht[1][index-1] == "_":
                                value += leftp
                            if not hdot:
                                bias += (x3 - x1) * (i - 1)
                            else:
                                bias += -(row - i) * (x3 - x1) - (x3 - x1)
                                if x3 != x1:
                                    if x3 == x1 + 1:
                                        virtual_bias += ("+" if virtual_bias else "") + virtual_row
                                    elif x1 == x3 + 1:
                                        virtual_bias += "-" + virtual_row
                                    else:
                                        virtual_bias += ("+" if virtual_bias and x3 > x1 else "") + str(x3 - x1) + virtual_row
                            if index > 0 and ht[1][index-1].isnumeric() and (biasandvirtualbias or (bias and virtual_bias)):
                                value += ","
                            biasandvirtualbias = bias and virtual_bias
                            if bias == 0:
                                value += virtual_bias
                            else:
                                value += virtual_bias + ("+" if virtual_bias and bias > 0 else "") + str(bias)
                            if underline and (index == len(ht[1])-1 or not ht[1][index+1].isnumeric()):
                                value += rightp
                    return value
                    flag = True
            elif j > 2:
                value = ""
                underline = False
                if re.sub("\d", "*", ht[1]) == re.sub("\d", "*", ht[2]):
                    for index in range(len(ht[1])):
                        if not ht[1][index].isnumeric():
                            biasandvirtualbias = False
                            value += ht[1][index]
                            if ht[1][index] == "_":
                                underline = True
                            else:
                                underline = False
                        else:
                            x1 = int(ht[1][index])
                            x2 = int(ht[2][index])
                            virtual_bias = ""
                            bias = x1
                            if underline and ht[1][index-1] == "_":
                                value += leftp
                            if not vdot:
                                bias += (x2 - x1) * (j - 1)
                            else:
                                bias += -(column - j) * (x2 - x1) - (x2 - x1)
                                if x2 != x1:
                                    if x2 == x1 + 1:
                                        virtual_bias += virtual_column
                                    elif x1 == x2 + 1:
                                        virtual_bias += "-" + virtual_column
                                    else:
                                        virtual_bias += str(x2 - x1) + virtual_column
                            if index > 0 and ht[1][index-1].isnumeric() and (biasandvirtualbias or (bias and virtual_bias)):
                                value += ","
                            biasandvirtualbias = bias and virtual_bias
                            if bias == 0:
                                value += virtual_bias
                            else:
                                value += virtual_bias + ("+" if virtual_bias and bias > 0 else "") + str(bias)
                            if underline and (index == len(ht[1])-1 or not ht[1][index+1].isnumeric()):
                                value += rightp
                    return value
                    flag = True
            if not flag and re.match(".*[a-zA-Z]_\{11\}", ht[1]):
                if not vdot and not hdot:
                    return re.sub("([a-zA-Z])_\{11\}", "\\g<1>_{" + str(i) + str(j) + "}", ht[1])
                elif vdot and hdot:
                    return re.sub("([a-zA-Z])_\{11\}", "\\g<1>_{" + virtual_row + ("-" + str(row - i) if i != row else "") + "," + virtual_column + ("-" + str(column - j) if j != column else "") + "}", ht[1])
                elif vdot:
                    return re.sub("([a-zA-Z])_\{11\}", "\\g<1>_{" + str(i) + "," + virtual_column + ("-" + str(column - j) if j != column else "") + "}", ht[1])
                else:
                    return re.sub("([a-zA-Z])_\{11\}", "\\g<1>_{" + virtual_row + ("-" + str(row - i) if i != row else "") + "," + str(j) + "}", ht[1])
                flag = True
            elif not flag and (i == 1 or j == 1):
                return ht[1]
                flag = True
            if not flag:
                return ""
    else:
        return ""

def intelligent_generate_matrix(prefix, snip):
    display = "\n" if display_math() else " "
    info = snip.buffer[snip.line]
    spacelen = len(info) - len(info.lstrip())
    linfo = info[:snip.snippet_start[1]]
    rinfo = info[snip.snippet_end[1]:]
    info = info[snip.snippet_start[1]:snip.snippet_end[1]]
    # print([linfo, rinfo, info])
    if len(info) > 1 and info[1].isnumeric():
        real_shape = info[:2]
        virtual_shape = info[2:]
    else:
        real_shape = info[0]
        virtual_shape = info[1:]
    if len(real_shape) == 1:
        row_amount = int(real_shape)
        column_amount = int(real_shape)
    else:
        row_amount = int(real_shape[0])
        column_amount = int(real_shape[1])
    if len(virtual_shape) == 0:
        virtual_row_amount = "0"
        virtual_column_amount = "0"
    elif len(virtual_shape) == 1:
        virtual_row_amount = virtual_shape[0]
        virtual_column_amount = virtual_shape[0]
    else:
        virtual_row_amount = virtual_shape[0]
        virtual_column_amount = virtual_shape[1]
    snip.buffer[snip.line] = ''
    displayed = re.sub(r"\\", r"\\\\", linfo) + "\\begin{%cmatrix}" % prefix + display
    def generate_code(i, j, row, column, virtual_row, virtual_column):
        if i == 1 and j == 1:
            return ""
        else:
            code = """`!p
from mdtex.matrix import generate_matrix_element
snip.rv = generate_matrix_element(%d, %d, %d, %d, '%c', '%c', [%s], [%s])
`""" % (i, j, row, column, virtual_row, virtual_column, "''," + ",".join("t[%d]" % x for x in range(1, j+1)), "''," + ",".join("t[%d]" % (1 + column * (x-1)) for x in range(1, i+1)))
        return code
    if row_amount > 0 and column_amount > 0:
        displayed += " " * (4 + len(linfo)) + "$1 " + ("& " if column_amount > 1 else "\\" * 4)
        index = 2
        for i in range(2, column_amount + 1):
            displayed += "${" + "{}".format(index) + ":" + generate_code(1, i, row_amount, column_amount, virtual_row_amount, virtual_column_amount) + "} " + ("& " if i < column_amount else "\\" * 4)
            index += 1
        displayed += display
        for j in range(2, row_amount + 1):
            displayed += " " * (4 + len(linfo))
            for i in range(1, column_amount + 1):
                displayed += "${" + "{}".format(index) + ":" + generate_code(j, i, row_amount, column_amount, virtual_row_amount, virtual_column_amount) + "} " + ("& " if i < column_amount else "\\" * 4)
                index += 1
            displayed += display
    displayed += " " * len(linfo) + "\\end{%cmatrix}$0" % prefix + (" " + re.sub(r"\\", r"\\\\", rinfo) if rinfo else "")
    snip.expand_anon(displayed)