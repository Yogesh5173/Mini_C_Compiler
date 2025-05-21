
from anytree import NodeMixin, RenderTree

class ASTNode(NodeMixin):
    def __init__(self, node_type, value=None, children=None, parent=None):
        self.node_type = node_type
        self.value = value
        self.name = f"{node_type}: {value}" if value is not None else node_type
        self.parent = parent
        self.children = []
        if children:
            for child in children:
                child.parent = self

    def display_ast_tree(root):
        for pre, fill, node in RenderTree(root):
            print(f"{pre}{node.name}")

    def __repr__(self, level=0):
        indent = '  ' * level
        result = f"{indent}{self.node_type}: {self.value}\n"
        for child in self.children:
            result += child.__repr__(level + 1)
        return result

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def eat(self, expected_type=None, expected_value=None):
        token = self.current_token()
        if not token:
            raise SyntaxError("Unexpected end of input")
        if expected_type and token.type != expected_type:
            raise SyntaxError(f"Expected token type {expected_type}, got {token.type}")
        if expected_value and token.value != expected_value:
            raise SyntaxError(f"Expected token value {expected_value}, got {token.value}")
        self.pos += 1
        return token

    def parse(self):
        return self.parse_program()

    def parse_program(self):
        nodes = []
        while self.current_token():
            node = self.parse_function()
            nodes.append(node)
        return ASTNode("Program", children=nodes)

    def parse_assignment(self):
        var_name = self.eat("IDENTIFIER").value
        self.eat("OPERATOR", "=")
        expr = self.parse_expression()
        self.eat("DELIMITER", ";")
        return ASTNode("Assignment", var_name, [expr])


    def parse_function(self):
        self.eat("KEYWORD", "int")
        self.eat("IDENTIFIER", "main")
        self.eat("DELIMITER", "(")
        self.eat("DELIMITER", ")")
        self.eat("DELIMITER", "{")
        body = self.parse_block()
        self.eat("DELIMITER", "}")
        return ASTNode("Function", "main", [body])


    def parse_block(self):
        children = []
        while self.current_token() and self.current_token().value != "}":
            tok = self.current_token()
            if tok.type == "KEYWORD" and tok.value in ("int", "float", "char"):
                children.append(self.parse_declaration())
            elif tok.type == "KEYWORD" and tok.value == "return":
                children.append(self.parse_return())
            elif tok.type == "KEYWORD" and tok.value == "if":
                children.append(self.parse_if())
            elif tok.type == "KEYWORD" and tok.value == "while":
                children.append(self.parse_while())
            else:
                self.eat()  # Skip unknowns
        return ASTNode("Block", children=children)

    def parse_declaration(self):
        type_tok = self.eat("KEYWORD")
        id_tok = self.eat("IDENTIFIER")
        self.eat("DELIMITER", ";")
        return ASTNode("Declaration", f"{type_tok.value} {id_tok.value}")

    def parse_return(self):
        self.eat("KEYWORD", "return")
        expr = self.eat("NUMBER")  # Just number for simplicity
        self.eat("DELIMITER", ";")
        return ASTNode("Return", expr.value)

    def parse_if(self):
        self.eat("KEYWORD", "if")
        self.eat("DELIMITER", "(")
        cond = self.eat("IDENTIFIER")  # Simplified
        self.eat("DELIMITER", ")")
        self.eat("DELIMITER", "{")
        block = self.parse_block()
        self.eat("DELIMITER", "}")
        return ASTNode("If", cond.value, [block])

    def parse_while(self):
        self.eat("KEYWORD", "while")
        self.eat("DELIMITER", "(")
        cond = self.eat("IDENTIFIER")  # Simplified
        self.eat("DELIMITER", ")")
        self.eat("DELIMITER", "{")
        block = self.parse_block()
        self.eat("DELIMITER", "}")
        return ASTNode("While", cond.value, [block])
