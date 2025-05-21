class IRGenerator:
    def __init__(self):
        self.ir = []
        self.temp_count = 0

    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def generate(self, node, indent=0):
        pad = '  ' * indent
        method = getattr(self, f'gen_{node.node_type.lower()}', self.gen_default)
        return method(node, pad)

    def gen_program(self, node, pad):
        for child in node.children:
            self.generate(child)

    def gen_function(self, node, pad):
        self.ir.append(f"{pad}.func {node.value}")
        for child in node.children:
            self.generate(child, indent=1)
        self.ir.append(f"{pad}.endfunc")

    def gen_block(self, node, pad):
        for child in node.children:
            self.generate(child, indent=1)

    def gen_declaration(self, node, pad):
        self.ir.append(f"{pad}.decl {node.value}")

    def gen_assignment(self, node, pad):
        var = node.value  # Left-hand side
        expr = node.children[0]  # Right-hand side
        rhs = self.generate(expr, pad)
        self.ir.append(f"{pad}{var} = {rhs}")

    def gen_binaryop(self, node, pad):
        left = self.generate(node.children[0], pad)
        right = self.generate(node.children[1], pad)
        temp = self.new_temp()
        self.ir.append(f"{pad}{temp} = {left} {node.value} {right}")
        return temp

    def gen_literal(self, node, pad):
        return str(node.value)

    def gen_identifier(self, node, pad):
        return node.value

    def gen_return(self, node, pad):
        val = self.generate(node.children[0], pad) if node.children else node.value
        self.ir.append(f"{pad}.return {val}")

    def gen_default(self, node, pad):
        self.ir.append(f"{pad}# Unhandled node: {node.type}")

    def get_ir(self):
        return self.ir
