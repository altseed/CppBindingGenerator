from typing import TypeVar
from cbg.common.options import CacheMode, CallBackType, SerializeType
from cbg.common.function import Function, ReturnValue
from cbg.common.property import Property

class Class:

    def __init__(self, name:str):
        self.namespace:str = ''
        self.brief:dict[str,str] = {'ja':None, 'en':None}
        self.note:dict[str,str] = {'ja':None, 'en':None}
        self.name:str = name
        self.alias:str = None
        self.base_class:Class = None
        self.is_public:bool = True
        self.is_sealed:bool = False
        self.handle_cache:bool = True
        self.functions:list[Function] = []
        self.properties:list[Property] = []
        self.cache_mode = CacheMode.Cache
        self.serialize_type = SerializeType.Disable
        self.call_back_type = CallBackType.Disable
        self.targets:list[str] = []
        self.__constructor_count = 0

    def add_constructor(self):
        func = Function("Constructor" + str(self.__constructor_count))
        func.is_constructor = True
        func.return_value = ReturnValue(self)
        self.functions.append(func)
        self.__constructor_count += 1
        return func

    def add_function(self, name:str):
        func = Function(name)
        self.functions.append(func)
        return func

    T = TypeVar('T')
    def add_property(self, type_:T, name:str):
        prop = Property(type_, name)
        self.properties.append(prop)
        return prop

    def __enter__(self):
        return self

    def __exit__(self, exit_type, exit_value, traceback):
        return self

    def __str__(self):
        return self.name
