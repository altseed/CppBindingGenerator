import cbg
import ctypes
import sys

# Struct
StructA = cbg.Struct('HelloWorld', 'StructA')
StructA.add_field(float, 'X')
StructA.add_field(float, 'Y')
StructA.add_field(float, 'Z')

# EnumA
EnumA = cbg.Enum('HelloWorld', 'EnumA')
EnumA.add('Mosue')
EnumA.add('Cow')
EnumA.add('Tiger', '3')

# ClassB
ClassB = cbg.Class('HelloWorld', 'ClassB')

constructor = ClassB.add_constructor()

func = ClassB.add_func('SetValue')
func.add_arg(float, 'value')

func = ClassB.add_func('SetEnum')
func.add_arg(EnumA, 'enumValue')

func = ClassB.add_func('GetEnum')
func.return_value = cbg.ReturnValue(EnumA, False)
func.add_arg(int, 'id')

prop = cbg.Property(int, 'MyProperty', True, True)
ClassB.add_property(prop)
brief = cbg.Description()
brief.add('ja', 'Gets or sets some integer.')
prop.brief = brief

prop = cbg.Property(float, 'MyFloat', False, False)
ClassB.add_property(prop)

prop = cbg.Property(bool, 'MyBool', False, True)
ClassB.add_property(prop)

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
arg = func.add_arg(StructA, 'value1')
brief = cbg.Description()
brief.add('en', 'Processes a structA.')
func.brief = brief
brief = cbg.Description()
brief.add('en', 'StructA input.')
arg.desc = brief

func = ClassA.add_func('FuncArgClass')
func.add_arg(ClassB, 'value1')

func = ClassA.add_func('FuncReturnInt')
func.return_value = cbg.ReturnValue(int)
brief = cbg.Description()
brief.add('en', 'Returns some integer.')
func.brief = brief

func = ClassA.add_func('FuncReturnBool')
func.return_value.type_ = bool

func = ClassA.add_func('FuncReturnFloat')
func.return_value.type_ = float

func = ClassA.add_func('FuncReturnStruct')
func.return_value.type_ = StructA

func = ClassA.add_func('FuncReturnClass')
func.return_value.type_ = ClassB
func.return_value.cache = True

func = ClassA.add_func('FuncReturnString')
func.return_value.type_ = ctypes.c_wchar_p

prop = cbg.Property(ClassB, 'BReference', True, False)
ClassA.add_property(prop)

# define
define = cbg.Define()
define.classes.append(ClassA)
define.classes.append(ClassB)
define.structs.append(StructA)
define.enums.append(EnumA)

# generate
sharedObjectGenerator = cbg.SharedObjectGenerator(define)

sharedObjectGenerator.header = '''
#include "HelloWorld.h"
'''

sharedObjectGenerator.func_name_create_and_add_shared_ptr = 'HelloWorld::CreateAndAddSharedPtr'
sharedObjectGenerator.func_name_add_and_get_shared_ptr = 'HelloWorld::AddAndGetSharedPtr'

sharedObjectGenerator.output_path = 'tests/results/so/so.cpp'
sharedObjectGenerator.generate()

args = sys.argv
lang = 'en'
if len(args) >= 3 and args[1] == '-lang':
    if args[2] in ['ja', 'en']:
        lang = args[2]
    else:
        print('python csharp.py -lang [ja|en]')

bindingGenerator = cbg.BindingGeneratorCSharp(define, lang)
bindingGenerator.output_path = 'tests/results/csharp/csharp.cs'
bindingGenerator.dll_name = 'Common'
bindingGenerator.namespace = 'HelloWorld'
bindingGenerator.generate()
