import cbg
import ctypes
import sys

from definitions import define, ReplaceStructA

args = sys.argv
lang = 'en'
if len(args) >= 3 and args[1] == '-lang':
    if args[2] in ['ja', 'en']:
        lang = args[2]
    else:
        print('python rust.py -lang [ja|en]')

bindingGenerator = cbg.BindingGeneratorRust(define, lang)
bindingGenerator.output_path = 'tests/results/rust/src/rust.rs'
bindingGenerator.dll_name = 'Common'
bindingGenerator.namespace = 'HelloWorld'
bindingGenerator.structsReplaceMap = {
    ReplaceStructA : "crate::ReplaceStruct<f32>"
}
bindingGenerator.generate()
