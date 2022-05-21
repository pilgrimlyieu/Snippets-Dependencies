from builtin import choose_next

command_mapping = ['🚀', '🚁', '🚂', '🚃', '🚄', '🚅', '🚆', '🚇', '🚈', '🚉', '🚊', '🚋', '🚌', '🚍', '🚎', '🚏']

def command_cycle(target, commands, bracketnum = 1):
    length = len(commands)
    command_map = command_mapping[:length]
    for i in range(length):
        target = target.replace(commands[i], command_map[i])
    string = list(target)
    depth = brackets = 0
    for i in range(len(string) - 1, -1, -1):
        cut = string[i]
        if cut == '}': depth += 1
        elif cut == '{': depth -= 1
        elif brackets == bracketnum and not depth and cut in command_map: string[i] = choose_next(cut, command_map, length)
        brackets += 0 if depth else 1
    result = ''.join(string)
    for i in range(length):
        result = result.replace(command_map[i], commands[i])
    return result
