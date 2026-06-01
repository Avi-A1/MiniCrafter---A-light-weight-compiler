from flask import Flask, render_template, request
from lexer import tokenize
from Parser import Parser
from compiler import Compiler
from vm import VM

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    code = ""
    output = ""
    bytecode_str = ""

    if request.method == "POST":
        code = request.form["code"]

        try:
            tokens = tokenize(code)
            ast = Parser(tokens).parse()

            compiler = Compiler()
            bytecode = compiler.compile(ast)

            bytecode_str = "\n".join([f"{i}: {instr}" for i, instr in enumerate(bytecode)])

            import io, sys
            old_stdout = sys.stdout
            sys.stdout = buffer = io.StringIO()

            VM().run(bytecode)

            sys.stdout = old_stdout
            output = buffer.getvalue()

        except Exception as e:
            output = str(e)

    return render_template("index.html", code=code, output=output, bytecode=bytecode_str)

if __name__ == "__main__":
    app.run(debug=True)