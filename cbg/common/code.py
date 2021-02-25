from enum import IntEnum

class Code:
    
    def __init__(self):
        self.lines:list[str] = []
        self.indent:int = 0

    def __call__(self, code:str):
        self.lines += [('    ' * self.indent) + line for line in code.split('\n')]

    def __enter__(self):
        return self

    def __exit__(self, exit_type, exit_value, traceback):
        return self

    def __str__(self):
        return '\n'.join(self.lines)

class IndentStyle(IntEnum):
    KAndR = 0
    BSDAllman = 1

class CodeBlock:

    def __init__(self, code:Code, title:str, indent_style:IndentStyle = IndentStyle.KAndR):
        self.code:Code = code
        self.title:str = title
        self.indent_style:IndentStyle = indent_style

    def __enter__(self):
        if self.indent_style == IndentStyle.KAndR:
            self.code(self.title + ' {')
            self.code.indent += 1
        if self.indent_style == IndentStyle.BSDAllman:
            self.code(self.title + '\n{')
            self.code.indent += 1
        return self

    def __exit__(self, exit_type, exit_value, traceback):
        self.code.indent -= 1
        self.code('}\n')
        return self