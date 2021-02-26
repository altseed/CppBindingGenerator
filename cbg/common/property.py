from typing import TypeVar
from cbg.common.function import Function

class Property:

    T = TypeVar('T')
    def __init__(self, type_:T, name:str, has_getter:bool=True, has_setter:bool=True):
        self.brief:dict[str,str] = {'ja':None, 'en':None}
        self.note:dict[str,str] = {'ja':None, 'en':None}
        self.name:str = name
        self.type_:T = type_
        self.is_only_extern:bool = False
        self.is_public:bool = True
        self.has_getter:bool = has_getter
        self.has_setter:bool = has_setter
        self.cache_set_value:bool = False
        self.is_nullable:bool = True
        self.is_serialized:bool = False
        self.is_null_deserialized:bool = True
        self.targets:list[str] = []

    def getter_as_func(self):
        func = Function('Get' + self.name)
        func.set_return(self.type_)
        return func

    def setter_as_func(self):
        func = Function('Set' + self.name)
        func.add_argument(self.type_, 'value')
        return func

    def __enter__(self):
        return self

    def __exit__(self, exit_type, exit_value, traceback):
        return self

    def __str__(self):
        return self.name