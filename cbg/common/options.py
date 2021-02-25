from enum import IntEnum

class ArgCalledBy(IntEnum):
    Default = 0
    Ref = 1
    Out = 2

class CacheMode(IntEnum):
    NoCache = 0
    Cache = 1
    Cache_ThreadSafe = 2

class SerializeType(IntEnum):
    Disable = 0
    AttributeOnly = 1
    Interface = 2
    Interface_Usebase = 3

class CallBackType(IntEnum):
    Disable = 0
    Enable = 1
    Enable_Usebase = 2