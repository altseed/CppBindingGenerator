import cbg
import ctypes
import sys
import argparse

from definitions import define

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--lang', type=str, default='en', required=False, choices=['ja', 'en'])
args = parser.parse_args()

bindingGenerator = cbg.BindingGeneratorCSharp(define, args.lang)
bindingGenerator.output_path = 'tests/results/csharp/csharp.cs'
bindingGenerator.dll_name = 'Common'
bindingGenerator.namespace = 'HelloWorld'
bindingGenerator.generate()
