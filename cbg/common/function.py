from typing import TypeVar
from cbg.common.options import ArgCalledBy, CacheMode

class Argument:

    T = TypeVar('T')
    def __init__(self, type_:T, name:str):
        self.brief:dict[str,str] = {'ja':None, 'en':None}
        self.note:dict[str,str] = {'ja':None, 'en':None}
        self.name:str = name
        self.type_:T = type_
        self.called_by:ArgCalledBy = ArgCalledBy.Default
        self.is_nullable:bool = False

    def __enter__(self):
        return self

    def __exit__(self, exit_type, exit_value, traceback):
        return self

    def __str__(self):
        return self.name

class ReturnValue:
    
    T = TypeVar('T')
    def __init__(self, type_:T):
        self.brief:str = None
        self.note:str = None
        self.type_:T = type_

    def cache_mode(self):
        has_attr = hasattr(self.type_, 'cache_mode')
        return self.type_.cache_mode if has_attr else CacheMode.NoCache

    def __enter__(self):
        return self

    def __exit__(self, exit_type, exit_value, traceback):
        return self

class Function:

    def __init__(self, name:str):
        self.brief:dict[str,str] = {'ja':None, 'en':None}
        self.note:dict[str,str] = {'ja':None, 'en':None}
        self.name:str = name
        self.arguments:list[Argument] = []
        self.return_value:ReturnValue = ReturnValue(None)
        self.is_public:bool = True
        self.is_static:bool = False
        self.is_constructor:bool = False
        self.is_only_extern:bool = False
        self.is_overload:bool = True
        self.targets:list[str] = []

    T = TypeVar('T')
    def add_argument(self, type_:T, name:str):
        argument = Argument(type_, name)
        self.arguments.append(argument)
        return argument

    U = TypeVar('U')
    def set_return(self, type_:T):
        self.return_value = ReturnValue(type_)
        return self.return_value

    def __enter__(self):
        return self

    def __exit__(self, exit_type, exit_value, traceback):
        return self

    def __str__(self):
        return self.name
