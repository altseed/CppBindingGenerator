from ..cpp_binding_generator import Define

from .binding_generator_hdr import BindingGeneratorCPlusPlusHdr
from .binding_generator_src import BindingGeneratorCPlusPlusSrc

class BindingGeneratorCPlusPlus:
    def __init__(self, define: Define, lang: str):
        '''
        generator for C++

        Parameters
        ----------
        self_ptr_name : str
            pointer name in the Class

        ''' 
        self.define = define
        self.lang = lang
        self.namespace = ''
        self.output_path = ''
        self.dll_name = ''
        self.self_ptr_name = 'selfPtr'
        self.includes = []

    def generate(self):

        bg_hdr = BindingGeneratorCPlusPlusHdr(self.define, self.lang)
        bg_hdr.namespace = self.namespace
        bg_hdr.output_path = self.output_path
        bg_hdr.dll_name = self.dll_name
        bg_hdr.self_ptr_name = self.self_ptr_name
        bg_hdr.includes = self.includes
        bg_hdr.generate()
        
        bg_src = BindingGeneratorCPlusPlusSrc(self.define, self.lang)
        bg_src.namespace = self.namespace
        bg_src.output_path = self.output_path
        bg_src.dll_name = self.dll_name
        bg_src.self_ptr_name = self.self_ptr_name
        bg_src.generate()