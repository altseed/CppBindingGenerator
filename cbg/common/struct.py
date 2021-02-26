from typing import TypeVar
from cbg.common.field import Field

class Struct:

    def __init__(self, name:str):
        self.namespace:str = ''
        self.brief:dict[str,str] = {'ja':None, 'en':None}
        self.note:dict[str,str] = {'ja':None, 'en':None}
        self.name:str = name
        self.alias:str = None
        self.fields:list[Field] = []
        self.targets:list[str] = []

    T = TypeVar('T')
    def add_field(self, type_:T, name:str):
        field = Field(type_, name)
        return field

    def __enter__(self):
        return self

    def __exit__(self, exit_type, exit_value, traceback):
        return self

    def __str__(self):
        return self.name
