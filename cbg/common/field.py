from typing import TypeVar

class Field:

    T = TypeVar('T')
    def __init__(self, type_:T, name:str):
        self.brief:dict[str,str] = {'ja':None, 'en':None}
        self.note:dict[str,str] = {'ja':None, 'en':None}
        self.name:str = name
        self.type_:T = type_

    def __enter__(self):
        return self

    def __exit__(self, exit_type, exit_value, traceback):
        return self

    def __str__(self):
        return self.name