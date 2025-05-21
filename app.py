from flask import Flask, request, jsonify, render_template
from lexer import Lexer
from parser import Parser
from ir_generator import IRGenerator
import uuid
import os


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        code = request.form.get('code')
        if not code:
            return jsonify({'error': 'No code provided'}), 400

        # Lexing and Parsing
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        parser = Parser(tokens)
        ast = parser.parse()

        # Generate IR
        ir_gen = IRGenerator()
        ir = ir_gen.generate(ast)
        ir = ir_gen.get_ir()

        # AST to JSON for jsTree
        def ast_to_dict(node):
            return {
                'text': f"<span style='font-weight:bold;color:#0066cc'>{node.node_type}</span>: <span style='color:#333'>{node.value}</span>",
                'children': [ast_to_dict(child) for child in node.children],
                'icon': 'jstree-icon'
            }

        ast_dict = ast_to_dict(ast)

        # AST to Graphviz
        if ir is None:
            ir = []

        return jsonify({
            'ast': ast_dict,
            'ir': ir,
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
