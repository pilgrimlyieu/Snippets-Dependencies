from unicodedata import east_asian_width

def display_width(str):
    """Return the required over-/underline length for str."""
    result = 0
    for c in str:
        result += 2 if east_asian_width(c) in ('W', 'F') else 1
    return result

def choose_next(string, array, length = 0):
    return array[array.index(string) - (length or len(array)) + 1]
