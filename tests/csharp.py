import cbg
import ctypes

# Struct
StructA = cbg.Struct('HelloWorld', 'StructA')
StructA.add_field(float, 'X')
StructA.add_field(float, 'Y')
StructA.add_field(float, 'Z')

# ClassB
ClassB = cbg.Class('HelloWorld', 'ClassB')

constructor = ClassB.add_constructor()

func = ClassB.add_func('SetValue')
func.add_arg(int, 'value')

# ClassA
ClassA = cbg.Class('HelloWorld', 'ClassA')

constructor = ClassA.add_constructor()

func = ClassA.add_func('FuncSimple')

func = ClassA.add_func('FuncArgInt')
func.add_arg(int, 'value')

func = ClassA.add_func('FuncArgFloatBoolStr')
func.add_arg(float, 'value1')
func.add_arg(bool, 'value2')
func.add_arg(ctypes.c_wchar_p, 'value3')

func = ClassA.add_func('FuncArgStruct')
func.add_arg(StructA, 'value1')

func = ClassA.add_func('FuncArgClass')
func.add_arg(ClassB, 'value1')

func = ClassA.add_func('FuncReturnInt')
func.return_type = int

func = ClassA.add_func('FuncReturnBool')
func.return_type = bool

func = ClassA.add_func('FuncReturnFloat')
func.return_type = float

func = ClassA.add_func('FuncReturnStruct')
func.return_type = StructA

func = ClassA.add_func('FuncReturnString')
func.return_type = ctypes.c_wchar_p

# define
define = cbg.Define()
define.classes.append(ClassA)
define.classes.append(ClassB)
define.structs.append(StructA)

# generate
sharedObjectGenerator = cbg.SharedObjectGenerator(define)

sharedObjectGenerator.header = '''
#include "HelloWorld.h"
'''

sharedObjectGenerator.func_name_create_and_add_shared_ptr = 'HelloWorld::CreateAndAddSharedPtr'

sharedObjectGenerator.output_path = 'tests/results/so/so.cpp'
sharedObjectGenerator.generate()

bindingGenerator = cbg.BindingGeneratorCSharp(define)
bindingGenerator.output_path = 'tests/results/csharp/csharp.cs'
bindingGenerator.dll_name = 'Common'
bindingGenerator.namespace = 'HelloWorld'
bindingGenerator.generate()
