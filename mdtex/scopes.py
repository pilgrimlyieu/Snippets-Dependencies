import vim

# 数学模式 Math Mode
def math():
    return vim.eval('vimtex#syntax#in_mathzone()') == '1'

# 纯数学模式 Pure Math Mode
def pure_math():
    return math() and not_chem() and not_unit()

# 行内公式模式 Inline Math Mode
def inline_math():
    return vim.eval("vimtex#syntax#in('texMathZone[LT]I')") == '1'

# 行间公式模式 Display Math Mode
def display_math():
    return vim.eval("vimtex#syntax#in('texMathZone[LT]D')") == '1'

# 化学模式 Chemistry Mode
def chem():
    return vim.eval("get(vimtex#cmd#get_current(), 'name')") == '\\ce' and math()

# 非化学模式 Not Chemistry Mode
def not_chem():
    return vim.eval("get(vimtex#cmd#get_current(), 'name')") != '\\ce'

# 单位模式 Unit Mode
def unit():
    return vim.eval("get(vimtex#cmd#get_current(), 'name')") == '\\pu' and math()

# 非单位模式 Not Unit Mode
def not_unit():
    return vim.eval("get(vimtex#cmd#get_current(), 'name')") != '\\pu'

# 文本模式 Text Mode
def text():
    return vim.eval('vimtex#syntax#in_mathzone()') == '0'

# 注释模式 Comment Mode
def comment(): 
    return vim.eval('vimtex#syntax#in_comment()') == '1'

# 特殊环境 Specific Environment
def env(name):
    [x, y] = vim.eval("vimtex#env#is_inside('" + name + "')") 
    return x != '0' and y != '0'
