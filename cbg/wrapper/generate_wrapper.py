import os
from cbg.common import *
from cbg.wrapper.wrapper_generator import WrapperGenerator

# define を元に wrapper のソースコードを自動生成
def _generate(self:WrapperGenerator):
    if self.output_path == None or self.output_path == '':
        print('please specify an output path')
        return
    code = Code()
    code('''// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
//
//   このファイルは自動生成されました。
//   このファイルへの変更は消失することがあります。
//
//   THIS FILE IS AUTO GENERATED.
//   YOUR COMMITMENT ON THIS FILE WILL BE WIPED.
//
// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#include <stdint.h>
#include <stdio.h>

#if defined(_WIN32) || defined(__WIN32__) || defined(__CYGWIN__)
#include <Windows.h>
#endif

#ifndef CBGEXPORT
#if defined(_WIN32) || defined(__WIN32__) || defined(__CYGWIN__)
#define CBGEXPORT __declspec(dllexport)
#else
#define CBGEXPORT
#endif
#endif

#ifndef CBGSTDCALL
#if defined(_WIN32) || defined(__WIN32__) || defined(__CYGWIN__)
#define CBGSTDCALL __stdcall
#else
#define CBGSTDCALL
#endif
#endif

{}
'''.format(self.header))
    with CodeBlock(code, 'extern "C"'):
        code('')
        for class_ in self.definition.classes:
            self._generate_class(code, class_, self.definition)
    with open(self.output_path, mode='w', encoding='utf-8') as file:
        file.write(str(code))

WrapperGenerator.generate = _generate