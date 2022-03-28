import cbg
import ctypes
import sys
import argparse

from definitions import define, define_cpp

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--lang', type=str, default='en',
                    required=False, choices=['ja', 'en'])
args = parser.parse_args()

# generate
bindingGenerator = cbg.BindingGeneratorCPlusPlus(define, args.lang)
bindingGenerator.output_path = 'tests/results/cplusplus/AutoGeneratedCoreBindings.h'
bindingGenerator.dll_name = 'CoreLib'
bindingGenerator.namespace = 'HelloWorldA'
bindingGenerator.includes = ['Additional.h']
bindingGenerator.generate()

# generate
sharedObjectGenerator = cbg.SharedObjectGenerator(define, [])

sharedObjectGenerator.header = '''
#include "HelloWorld.h"
'''

sharedObjectGenerator.func_name_create_and_add_shared_ptr = 'HelloWorld::CreateAndAddSharedPtr'
sharedObjectGenerator.func_name_add_and_get_shared_ptr = 'HelloWorld::AddAndGetSharedPtr'

sharedObjectGenerator.output_path = 'tests/results/so/AutoGeneratedCoreWrapper.cpp'
sharedObjectGenerator.generate()

# generate
dependencies = [cbg.DefineDependency()]
dependencies[0].define = define
dependencies[0].namespace = bindingGenerator.namespace

sharedObjectGeneratorCplusplus = cbg.SharedObjectGenerator(define_cpp, dependencies)

sharedObjectGeneratorCplusplus.header = '''
#include "cplusplus.h"
'''

sharedObjectGeneratorCplusplus.func_name_create_and_add_shared_ptr = 'HelloWorldCpp::CreateAndAddSharedPtr'
sharedObjectGeneratorCplusplus.func_name_add_and_get_shared_ptr = 'HelloWorldCpp::AddAndGetSharedPtr'
sharedObjectGeneratorCplusplus.func_name_create_and_add_shared_ptr_dependence = 'HelloWorldCpp::CreateAndAddSharedPtr_Dependence'
sharedObjectGeneratorCplusplus.func_name_add_and_get_shared_ptr_dependence = 'HelloWorldCpp::AddAndGetSharedPtr_Dependence'

sharedObjectGeneratorCplusplus.output_path = 'tests/results/cplusplus/AutoGeneratedCplusCPlusWrapper.cpp'
sharedObjectGeneratorCplusplus.generate()
