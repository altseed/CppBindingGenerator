import cbg
import ctypes

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

func = ClassA.add_func('FuncReturnInt')
func.return_type = int

func = ClassA.add_func('FuncReturnBool')
func.return_type = bool

# define
define = cbg.Define()
define.classes.append(ClassA)

# generate
sharedObjectGenerator = cbg.SharedObjectGenerator(define)

sharedObjectGenerator.header = '''
#include "HelloWorld.h"
'''

sharedObjectGenerator.output_path = 'tests/results/so/so.cpp'
sharedObjectGenerator.generate()

bindingGenerator = cbg.BindingGeneratorCSharp(define)
bindingGenerator.output_path = 'tests/results/csharp/csharp.cs'
bindingGenerator.dll_name = 'Common'
bindingGenerator.namespace = 'HelloWorld'
bindingGenerator.generate()
