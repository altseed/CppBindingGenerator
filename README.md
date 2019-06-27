
# CppBindingGenerator

Generate cpp wrapper codes and sprcified language wrapper codes.

# How to use

**CppBindingGenerator**(CBG) generates some binding codes from C++ to various other language, according to setting file customized by user.

For C++, CBG generate some codes exposing your functionality into DLL.
For target languages, CBG generate some classes to load and invoke your functionality from DLL.

You can write setting file using Python.

# Run/Test

Add ``` PYTHONPATH . ``` in environment variable.

Call ```python tests/csharp.py ``` from a root directory

Call ```tests/build/GenerateProjects.bat```

# TODO

Make struct in arguments treat safely

## C#

```
Enum (Argument, Resutn, Generate)
Proprety
Document
CacheSystem
```

