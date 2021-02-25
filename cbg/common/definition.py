from cbg.common.enum import Enum
from cbg.common.struct import Struct
from cbg.common.class_ import Class

class Definition:
    
    def __init__(self):
        self.namespace:str = ''
        self.enums:list[Enum] = []
        self.structs:list[Struct] = []
        self.classes:list[Class] = []
        self.dependencies:list[Definition] = []