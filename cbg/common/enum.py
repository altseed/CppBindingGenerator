class EnumValue:

    def __init__(self, name:str, value:int = None):
        self.brief:str = None
        self.note:str = None
        self.name:str = name
        self.value:int = None

    def __str__(self):
        return self.name

class Enum:

    def __init__(self, name:str):
        self.namespace:str = ''
        self.brief:str = None
        self.note:str = None
        self.name:str = name
        self.alias:str = None
        self.is_flag:bool = False
        self.values:list[EnumValue] = []

    def add_value(self, name:str, value:int = None):
        enum_value = EnumValue(name, value)
        self.values.append(enum_value)
        return enum_value

    def __enter__(self):
        return self

    def __exit__(self, exit_type, exit_value, traceback):
        return self

    def __str__(self):
        return self.name