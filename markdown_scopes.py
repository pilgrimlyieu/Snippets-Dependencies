import vim

# 数学模式 Math Mode
def math():
	return vim.eval('vimtex#syntax#in_mathzone()') == '1'

# 文本模式 Text Mode
def text():
    return vim.eval('vimtex#syntax#in_mathzone()') == '0'

# 注释模式 Comment Mode
def comment(): 
	return vim.eval('vimtex#syntax#in_comment()') == '1'

# 行内公式模式 Inline Math Mode
def inline_math():
	return vim.eval("vimtex#syntax#in('texMathZoneX$')") == '1'

# 行间公式模式 Display Math Mode
def display_math():
	return vim.eval("vimtex#syntax#in('texMathZoneXX')") == '1'

# 化学模式 Chemistry Mode
def chem():
	return vim.eval("get(vimtex#cmd#get_current(), 'name')") == '\\ce' and math()

# 特殊环境 Specific Environment
def env(name):
	[x, y] = vim.eval("vimtex#env#is_inside('" + name + "')") 
	return x != '0' and y != '0'
