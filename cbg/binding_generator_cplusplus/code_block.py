from ..cpp_binding_generator import *
from ..cpp_binding_generator import __get_c_func_name__
from ..cpp_binding_generator import __get_c_release_func_name__

class CodeBlock:
    def __init__(self, coder: Code, title: str, after_space: bool = False, after_comma: bool = False):
        '''
        a class for generating code block easily
        '''
        self.title = title
        self.coder = coder
        self.after_space = after_space
        self.after_comma = after_comma

    def __enter__(self):
        self.coder(self.title)
        self.coder('{')
        self.coder.inc_indent()
        return self

    def __exit__(self, exit_type, exit_value, traceback):
        self.coder.dec_indent()
        if self.after_comma:
            self.coder('};')
        else:
            self.coder('}')
        if self.after_space:
            self.coder('')