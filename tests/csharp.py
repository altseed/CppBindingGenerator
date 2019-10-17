import cbg
import ctypes
import sys

from definitions import define

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
