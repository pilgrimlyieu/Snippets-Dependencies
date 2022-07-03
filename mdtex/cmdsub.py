from builtin import choose_next

command_mapping = ['🚀', '🚁', '🚂', '🚃', '🚄', '🚅', '🚆', '🚇', '🚈', '🚉', '🚊', '🚋', '🚌', '🚍', '🚎', '🚏']

def command_cycle(target, commands, bracketnum = 1):
    length      = len(commands)
    command_map = command_mapping[:length]
    progress    = target
    for i in range(length):
        progress = progress.replace(commands[i], command_map[i])
    string = list(progress)
    depth  = braces = 0

    for i in range(len(string) - 1, -1, -1):
        if   string[i] == '}': depth += 1; braces += 0 if depth else 1
        elif string[i] == '{': depth -= 1; braces += 0 if depth else 1
        elif braces == bracketnum and not depth:
            try:
                string[i] = choose_next(string[i], command_map, length)
                break
            except ValueError:
                return target

    result = ''.join(string)
    for i in range(length):
        result = result.replace(command_map[i], commands[i])
    return result

def command_swap(target, command_1, command_2, bracketnum = 1):
    string = list(target.replace(command_1, '🚀').replace(command_2, '🚁'))
    depth  = braces = 0

    for i in range(len(string) - 1, -1, -1):
        if   string[i] == '}': depth += 1; braces += 0 if depth else 1
        elif string[i] == '{': depth -= 1; braces += 0 if depth else 1
        elif braces == bracketnum and not depth:
            if   string[i] == '🚀': string[i] = '🚁'
            elif string[i] == '🚁': string[i] = '🚀'
            else: return target
            break

    return ''.join(string).replace('🚀', command_1).replace('🚁', command_2)

def command_triple(target, command_1, command_2, command_3, bracketnum = 1):
    string = list(target.replace(command_1, '🚀').replace(command_2, '🚁').replace(command_3, '🚂'))
    depth  = braces = 0

    for i in range(len(string) - 1, -1, -1):
        if   string[i] == '}': depth += 1; braces += 0 if depth else 1
        elif string[i] == '{': depth -= 1; braces += 0 if depth else 1
        elif braces == bracketnum and not depth:
            if   string[i] == '🚀': string[i] = '🚁'
            elif string[i] == '🚁': string[i] = '🚂'
            elif string[i] == '🚂': string[i] = '🚀'
            else: return target
            break

    return ''.join(string).replace('🚀', command_1).replace('🚁', command_2).replace('🚂', command_3)

# Test {{{1
if __name__ == '__main__':
    import timeit

    num = 3
    target = '\\dfrac{\\dfrac{' + ''.join(['{' + str(i) + '}' for i in range(num)]) + '}{' + ''.join(['{' + str(i) + '}' for i in range(num)]) + '}'
    repeat = 200000
    cmds2 = ['\\frac', '\\dfrac']
    cmds3 = ['\\frac', '\\dfrac', '\\cfrac']
    cmds4 = ['\\frac', '\\dfrac', '\\cfrac', '\\tfrac']

    def choose_next(string, array, length = 0):
        return array[array.index(string) - (length or len(array)) + 1]
    def test1():
        '''Swap    '''
        command_swap(target, '\\frac', '\\dfrac', 2)
    def test2():
        '''Cycle2  '''
        command_cycle(target, cmds2, 2)
    def test3():
        '''Triple  '''
        command_triple(target, '\\frac', '\\dfrac', '\\cfrac', 2)
    def test4():
        '''Cycle3  '''
        command_cycle(target, cmds3, 2)
    def test5():
        '''Cycle4  '''
        command_cycle(target, cmds4, 2)
    def test(repeat):
        '''
        num    = 3
        repeat = 200000

        Swap    1.7969521000013629
        Cycle2  2.038432200002717
        Triple  1.7464822000001732
        Cycle3  2.147127599997475
        Cycle4  2.230857400001696
        '''
        print(test1.__doc__ + str(timeit.timeit(test1, number = repeat, globals = globals()))) 
        print(test2.__doc__ + str(timeit.timeit(test2, number = repeat, globals = globals()))) 
        print(test3.__doc__ + str(timeit.timeit(test3, number = repeat, globals = globals()))) 
        print(test4.__doc__ + str(timeit.timeit(test4, number = repeat, globals = globals()))) 
        print(test5.__doc__ + str(timeit.timeit(test5, number = repeat, globals = globals()))) 

    test(repeat)
# }}}1
