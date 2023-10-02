from mdtex.scopes import display_math
import re

default_row    = 3
default_column = 3

def generate_matrix(form, matrix, display):
    space  = "\n" if display else " "
    indent = "  " if display else ""
    result = "\\begin{" + form + "matrix}" + space
    for row_vector in matrix[:-1]:
        result += indent + " & ".join(row_vector) + " \\\\" + space
    return result + indent + " & ".join(matrix[-1]) + space + "\\end{" + form + "matrix}"

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

if __name__ == "__main__":
    print(generate_matrix("b", [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]], True))
    print(generate_matrix("b", [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]], False))