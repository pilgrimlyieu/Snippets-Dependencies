import vim

external_environments = ['sympy', 'wolfram']

# 数学模式 Math Mode
def math():
    except_conditions = [
        extcal(),
        # roman(),
        cmd("textcolor")
    ]
    return all([
        vim.eval('vimtex#syntax#in_mathzone()') == '1',
        not any(except_conditions)
    ])

# 纯数学模式 Pure Math Mode
def pure_math():
    extra_conditions = [
        not_chem(),
        not_unit()
    ]
    return all([
        math(),
        all(extra_conditions)
    ])

def extcal():
    for environment in external_environments:
        if env(environment):
            return True
    return False

# 行内公式模式 Inline Math Mode
def inline_math() -> bool:
    return vim.eval("vimtex#syntax#in('texMathZone[LT]I')") == '1'

# 行间公式模式 Display Math Mode
def display_math() -> bool:
    return vim.eval("vimtex#syntax#in('texMathZone[LT]D')") == '1'

# 化学模式 Chemistry Mode
def chem() -> bool:
    return vim.eval("get(vimtex#cmd#get_current(), 'name')") == '\\ce' and math()

# 非化学模式 Not Chemistry Mode
def not_chem() -> bool:
    return vim.eval("get(vimtex#cmd#get_current(), 'name')") != '\\ce'

# 单位模式 Unit Mode
def unit() -> bool:
    return vim.eval("get(vimtex#cmd#get_current(), 'name')") == '\\pu' and math()

# 非单位模式 Not Unit Mode
def not_unit() -> bool:
    return vim.eval("get(vimtex#cmd#get_current(), 'name')") != '\\pu'

# 罗马模式 Roman Mode
def roman() -> bool:
    return vim.eval("get(vimtex#cmd#get_current(), 'name')") == '\\mathrm'

# 文本模式 Text Mode
def text() -> bool:
    return vim.eval('vimtex#syntax#in_mathzone()') == '0'

# 注释模式 Comment Mode
def comment() -> bool: 
    return vim.eval('vimtex#syntax#in_comment()') == '1'

# 特殊命令 Specific Commands
def cmd(name) -> bool:
    return vim.eval("get(vimtex#cmd#get_current(), 'name')") == f'\\{name}'

# 特殊环境 Specific Environments
def env(name) -> bool:
    [x, y] = vim.eval("vimtex#env#is_inside('" + name + "')") 
    return x != '0' and y != '0'
