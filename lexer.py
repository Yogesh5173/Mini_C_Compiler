import re

keywords = {
    'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do', 'double', 'else',
    'enum', 'extern', 'float', 'for', 'goto', 'if', 'int', 'long', 'register', 'return',
    'short', 'signed', 'sizeof', 'static', 'struct', 'switch', 'typedef', 'union',
    'unsigned', 'void', 'volatile', 'while'
}

token_specification = [
    ('COMMENT', r'//.*?$|/\*.*?\*/'),
    ('STRING', r'"([^"\\]|\\.)*"'),
    ('CHAR', r"'([^'\\]|\\.)'"), # <--- Add this line
    ('NUMBER', r'\b\d+(\.\d+)?\b'),
    ('IDENTIFIER', r'\b[A-Za-z_][A-Za-z0-9_]*\b'),
    ('OPERATOR', r'(\+\+|--|==|!=|<=|>=|&&|\|\||<<|>>|->|[-+*/%=<>&^|!~])'),
    ('DELIMITER', r'[{}\[\]();,:]'),
    ('PREPROCESS', r'#\s*include\s*[<"][^>\n"]*[>"]'),
    ('WHITESPACE', r'\s+'),
    ('MISMATCH', r'.'),
]


master_pattern = re.compile(
    '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification),
    re.MULTILINE | re.DOTALL
)


class Token:
    def __init__(self, type_, value, line, column):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type}, {self.value}, {self.line}:{self.column})"

class Lexer:
    def __init__(self, code):
        self.code = code

    def tokenize(self):
        tokens = []
        line_num = 1
        line_start = 0

        for match in master_pattern.finditer(self.code):
            kind = match.lastgroup
            value = match.group()
            column = match.start() - line_start

            if kind == 'WHITESPACE':
                if '\n' in value:
                    line_num += value.count('\n')
                    line_start = match.end()
                continue
            elif kind == 'COMMENT':
                continue
            elif kind == 'IDENTIFIER' and value in keywords:
                kind = 'KEYWORD'
            elif kind == 'MISMATCH':
                raise RuntimeError(f'Unexpected character {value!r} at {line_num}:{column}')

            tokens.append(Token(kind, value, line_num, column))
            print(kind,value,line_num,column)

        return tokens