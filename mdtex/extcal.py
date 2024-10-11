from mdtex.scopes import display_math
from sympy import latex
from re import sub
from subprocess import check_output, TimeoutExpired
import os

wolframscript_timeout_default = 10

def pre_process_text(text):
    return text.replace('\\', '') \
               .replace('^', '**') \
               .replace('{', '(') \
               .replace('}', ')')

def pre_process_latex(text):
    return text.replace(r'\e', r' e') \
               .replace(r'\d ', r'\, d') \
               .replace('\\', '\\\\')

def process_latex(text):
    return sub(r'(\s|\W?)e(?=\W)', r'\g<1>\\e', text) \
               .replace(r'\, d', r'\d ')

def get_environment(env, snip):
    if display_math():
        stack = -1
        for index, line in enumerate(snip.buffer[:snip.line]):
            if '\\begin{{{}}}'.format(env) == line.strip():
                stack += 1
                if stack == 0:
                    start = index
            elif '\\end{{{}}}'.format(env) == line.strip():
                stack -= 1
                if stack == 0:
                    start = index
        if stack == 0:
            return (start, '\n'.join(snip.buffer[start + 1:snip.line]))

def calculate_sympy(snip, from_latex=False):
    environment = get_environment('sympy', snip)
    if environment:
        index, block = environment
    else:
        return
    snip.buffer[index:snip.line + 1] = ['']
    pre_define = '''
from sympy import *
x, y, z, t = symbols('x y z t')
k, m, n = symbols('k m n', integer = True)
f, g, h = symbols('f g h', cls = Function)
'''
    sympy_result = {}
    exec(pre_define + pre_process_text(block), sympy_result)
    result = process_latex(latex(sympy_result['rv'] or ''))
    snip.cursor.set(index, len(result))
    snip.buffer[index] = result

def calculate_wolfram(snip, from_latex=False, timeout=wolframscript_timeout_default):
    environment = get_environment('latex_wolfram' if from_latex else 'wolfram', snip)
    if environment:
        index, block = environment
    else:
        return
    snip.buffer[index:snip.line + 1] = ['']
    if from_latex:
        code = 'ToString[ToExpression["' + pre_process_latex(block) + '", TeXForm], TeXForm]'
    else:
        code = 'ToString[' + block.replace('\n', ';') + ', TeXForm]'
    kwargs = {
        'encoding': 'utf-8',
        'timeout': int(timeout or wolframscript_timeout_default)
    }
    if os.name == 'nt':  # Windows
        kwargs['creationflags'] = 0x08000000
    try:
        result = check_output(['wolframscript', '-code', code], **kwargs).strip()
    except TimeoutExpired:
        result = ''
    result = process_latex(result)
    snip.cursor.set(index, len(result))
    snip.buffer[index] = result.replace("\n", " ") # Quick fix
