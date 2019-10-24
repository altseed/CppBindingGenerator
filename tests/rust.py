import cbg
import ctypes
import sys
import argparse

from definitions import define, ReplaceStructA

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--lang', type=str, default='en', required=False, choices=['ja', 'en'])
args = parser.parse_args()

bindingGenerator = cbg.BindingGeneratorRust(define, args.lang)
bindingGenerator.output_path = 'tests/results/rust/src/rust.rs'
bindingGenerator.dll_name = 'Common'
bindingGenerator.namespace = 'HelloWorld'
bindingGenerator.structsReplaceMap = {
    ReplaceStructA : "crate::ReplaceStruct<f32>"
}
bindingGenerator.generate()

# generate
sharedObjectGenerator = cbg.SharedObjectGenerator(define)

sharedObjectGenerator.header = '''
#include "HelloWorld.h"
'''

sharedObjectGenerator.func_name_create_and_add_shared_ptr = 'HelloWorld::CreateAndAddSharedPtr'
sharedObjectGenerator.func_name_add_and_get_shared_ptr = 'HelloWorld::AddAndGetSharedPtr'

sharedObjectGenerator.output_path = 'tests/results/so/so.cpp'
sharedObjectGenerator.generate()