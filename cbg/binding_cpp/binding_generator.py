from cbg.common import *

class BindingGeneratorCPP(object):
    def __init__(self):
        self.definition:Definition = None
        self.namespace = ''
        self.output_path = ''
        self.dll_name = ''
        self.self_ptr_name = 'this'
        self.lang = lang
        self.includes = []

    