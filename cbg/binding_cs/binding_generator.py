from cbg.common import *

class BindingGeneratorCS(object):
    def __init__(self):
        self.definition:Definition = None
        self.output_path:str = ''
        self.dll_name:str = ''
        self.self_ptr_name:str = 'selfPtr'
        self.language:str = 'ja'