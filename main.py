from lexer import tokenize
from parser import Parser
from ir_generator import IRGenerator
code = '''
int main() {
    int a;
    int b;
    a = 5;
    b = a + 3;
    return 0;
}

'''

tokens = tokenize(code)
for token in tokens:
    print(token)
parser = Parser(tokens)
ast = parser.parse()
generator = IRGenerator()
generator.generate(ast)
for line in generator.get_ir():
    print(line)

print(ast)
