if __name__ == "__main__":
    display_math = lambda: 1
else:
    from mdtex.scopes import display_math
import re
from itertools import product

default_row_num = 3
default_col_num = 3
default_auto_dots = 1
default_fill_zero = 1
default_tabstop_for_0_all = 0
default_tabstop_for_0_sep = 0
default_tabstop_in_style = 1

def matrix_template(form, matrix, display):
    space  = "\n" if display else " "
    indent = "    " if display else ""
    result = "\\begin{" + form + "matrix}" + space
    for row_vector in matrix[:-1]:
        result += indent + " & ".join(row_vector) + " \\\\" + space
    return result + indent + " & ".join(matrix[-1]) + space + "\\end{" + form + "matrix}"

def debug(form, matrix, snip, display):
    if __name__ == "__main__":
        print(matrix_template(form, matrix, display))
    else:
        snip.expand_anon(matrix_template(form, matrix, display).replace("\\", "\\\\"))

def rcn_replace(content, row, col, row_num):
    return content.replace('\\r', str(row + 1)).replace('\\c', str(col + 1)).replace('\\n', str(row * row_num + col + 1))
def dynvar_replace(content, coordinate, row_num):
    return re.sub(r'`([\s\d+*/-]*)`', lambda m: str(eval(m.group(1))), rcn_replace(content, *coordinate, row_num)).replace("}", "\\}")
def add_tabstop(tabstop, coordinate, placeholders):
    content = placeholders[tabstop][2]
    return "${%d:%s" % (tabstop, content) + "}" if (coordinate == placeholders[tabstop][0:2] and content) else "$%d" % tabstop if tabstop else content

row_vec = lambda matrix,  row: matrix[row - 1]
col_vec = lambda matrix,  col: [row[col - 1] for row in matrix]

def generate_matrix(form, options, size, content, snip):
    display = 1 if display_math() else 0
    matrix_style = ''
    if options:
        if   '0' in options: matrix_style = '0'
        elif 'i' in options: matrix_style = 'i'
        elif 'd' in options: matrix_style = 'd'
        elif 'D' in options: matrix_style = 'D'
        elif 't' in options: matrix_style = 't'
        elif 'T' in options: matrix_style = 'T'
        elif 'c' in options: matrix_style = 'c'
        elif 'C' in options: matrix_style = 'C'
        elif 's' in options: matrix_style = 's'
    # auto_dotes = not default_auto_dots if '.' in options else default_auto_dots
    fill_zero         = not default_fill_zero if '-' in options else default_fill_zero
    tabstop_for_0_all = not default_tabstop_for_0_all if '1' in options else default_tabstop_for_0_all
    tabstop_for_0_sep = not default_tabstop_for_0_sep if '2' in options else default_tabstop_for_0_sep
    tabstop_in_style  = not default_tabstop_in_style if '3' in options else default_tabstop_in_style

    empty_element = "0" if fill_zero else ""
    if   len(size) == 1: row_num = col_num = int(size)
    elif len(size) == 2: row_num,  col_num = int(size[0]), int(size[1])
    else:                row_num,  col_num = default_row_num, default_col_num
    matrix = [[empty_element for j in range(col_num)] for i in range(row_num)]
    placeholders = [(-1, -1, "")]
    tabstop = 1
    if matrix_style == '' or row_num != col_num:
        if tabstop_in_style:
            for i, j in product(range(row_num), range(col_num)):
                placeholders.append((i, j, dynvar_replace(content, (i, j), col_num)))
                matrix[i][j] = add_tabstop(tabstop, (i, j), placeholders)
                tabstop += 1
        else:
            for i, j in product(range(row_num), range(col_num)):
                matrix[i][j] = dynvar_replace(content, (i, j), col_num)
    else:
        match matrix_style:
            case 'i':
                if tabstop_in_style:
                    content = "1" if content.isspace() else content
                    placeholders.append((0, 0, dynvar_replace(content, (0, 0), col_num)))
                    for i in range(row_num):
                        matrix[i][i] = add_tabstop(tabstop, (i, i), placeholders)
                    tabstop += 1
                else:
                    for i in range(row_num):
                        matrix[i][i] = dynvar_replace(content, (0, 0), col_num)
            case 'd':
                if tabstop_in_style:
                    for i in range(row_num):
                        placeholders.append((i, i, dynvar_replace(content, (i, i), col_num)))
                        matrix[i][i] = add_tabstop(tabstop, (i, i), placeholders)
                        tabstop += 1
                else:
                    for i in range(row_num):
                        matrix[i][i] = dynvar_replace(content, (i, i), col_num)
            case 'D':
                if tabstop_in_style:
                    for i in range(row_num):
                        placeholders.append((i, row_num - 1 - i, dynvar_replace(content, (i, row_num - 1 - i), col_num)))
                        matrix[i][row_num - 1 - i] = add_tabstop(tabstop, (i, row_num - 1 - i), placeholders)
                        tabstop += 1
                else:
                    for i in range(row_num):
                        matrix[i][row_num - 1 - i] = dynvar_replace(content, (i, row_num - 1 - i), col_num)
            case 't':
                if tabstop_in_style:
                    for i, j in product(range(row_num), range(col_num)):
                        if i <= j:
                            placeholders.append((i, j, dynvar_replace(content, (i, j), col_num)))
                            matrix[i][j] = add_tabstop(tabstop, (i, j), placeholders)
                            tabstop += 1
                else:
                    for i, j in product(range(row_num), range(col_num)):
                        if i <= j:
                            matrix[i][j] = dynvar_replace(content, (i, j), col_num)
            case 'T':
                if tabstop_in_style:
                    for i, j in product(range(row_num), range(col_num)):
                        if i >= j:
                            placeholders.append((i, j, dynvar_replace(content, (i, j), col_num)))
                            matrix[i][j] = add_tabstop(tabstop, (i, j), placeholders)
                            tabstop += 1
                else:
                    for i, j in product(range(row_num), range(col_num)):
                        if i >= j:
                            matrix[i][j] = dynvar_replace(content, (i, j), col_num)
            case 'c':
                if tabstop_in_style:
                    for j in range(col_num):
                        placeholders.append((0, j, dynvar_replace(content, (0, j), col_num)))
                        for k in range(j, row_num):
                            matrix[k - j][k] = add_tabstop(tabstop, (k - j, k), placeholders)
                        tabstop += 1
                    for i in range(1, row_num):
                        placeholders.append((i, 0, dynvar_replace(content, (i, 0), col_num)))
                        for k in range(i, col_num):
                            matrix[k][k - i] = add_tabstop(tabstop, (k, k - i), placeholders)
                        tabstop += 1
                else:
                    for j in range(col_num):
                        for k in range(j, row_num):
                            matrix[k - j][k] = dynvar_replace(content, (0, j), col_num)
                    for i in range(1, row_num):
                        for k in range(i, col_num):
                            matrix[k][k - i] = dynvar_replace(content, (i, 0), col_num)
            case 'C':
                if tabstop_in_style:
                    for j in range(col_num - 1, -1, -1):
                        placeholders.append((0, j, dynvar_replace(content, (0, j), col_num)))
                        for k in range(j, -1, -1):
                            matrix[j - k][k] = add_tabstop(tabstop, (j - k, k), placeholders)
                        tabstop += 1
                    for i in range(1, row_num):
                        placeholders.append((i, col_num - 1, dynvar_replace(content, (i, col_num - 1), col_num)))
                        for k in range(i, row_num):
                            matrix[k][col_num - 1 + i - k] = add_tabstop(tabstop, (k, col_num - 1 + i - k), placeholders)
                        tabstop += 1
                else:
                    for j in range(col_num - 1, -1, -1):
                        for k in range(j, -1, -1):
                            matrix[j - k][k] = dynvar_replace(content, (0, j), col_num)
                    for i in range(1, row_num):
                        for k in range(i, row_num):
                            matrix[k][col_num - 1 + i - k] = dynvar_replace(content, (i, col_num - 1), col_num)
            case 's':
                if tabstop_in_style:
                    placeholders.append((0, 0, dynvar_replace(content, (0, 0), col_num)))
                    for i in range(row_num):
                        matrix[i][i] = add_tabstop(tabstop, (i, i), placeholders)
                    tabstop += 1
                    for i, j in product(range(row_num), range(col_num)):
                        if i < j:
                            placeholders.append((i, j, dynvar_replace(content, (i, j), col_num)))
                            matrix[i][j] = add_tabstop(tabstop, (i, j), placeholders)
                            matrix[j][i] = add_tabstop(tabstop, (j, i), placeholders)
                            tabstop += 1
                else:
                    for i, j in product(range(row_num), range(col_num)):
                        if i == j:
                            matrix[i][j] = dynvar_replace(content, (0, 0), col_num)
                        elif i < j:
                            matrix[i][j] = dynvar_replace(content, (i, j), col_num)
                            matrix[j][i] = dynvar_replace(content, (j, i), col_num)
            case 'S':
                if tabstop_in_style:
                    for i, j in product(range(row_num), range(col_num)):
                        if i <= j:
                            placeholders.append((i, j, dynvar_replace(content, (i, j), col_num)))
                            matrix[i][j] = add_tabstop(tabstop, (i, j), placeholders)
                            matrix[j][i] = add_tabstop(tabstop, (j, i), placeholders)
                            tabstop += 1
                else:
                    for i, j in product(range(row_num), range(col_num)):
                        if i <= j:
                            matrix[i][j] = dynvar_replace(content, (i, j), col_num)
                            matrix[j][i] = add_tabstop(tabstop, (j, i), placeholders)
    if tabstop_for_0_sep:
        for i, j in product(range(row_num), range(col_num)):
            if matrix[i][j] == empty_element:
                placeholders.append((i, j, empty_element))
                matrix[i][j] = add_tabstop(tabstop, (i, j), placeholders)
                tabstop += 1
    elif tabstop_for_0_all:
        have_0 = 0
        for i, j in product(range(row_num), range(col_num)):
            if not have_0 and matrix[i][j] == empty_element:
                placeholders.append((i, j, empty_element))
                have_0 = 1
            if matrix[i][j] == empty_element:
                matrix[i][j] = add_tabstop(tabstop, (i, j), placeholders)
    debug("" if form == "m" else form, matrix, snip, display)

if __name__ == "__main__":
    # print(matrix_template("b", [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]], True))
    # print(matrix_template("b", [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]], False))
    generate_matrix("m", "s", "", "a", None)

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
