import os
from cbg.common import *
import cbg.wrapper.generate_class as gen_class

class WrapperGenerator(object):

    # このクラスをシングルトンパターンで設計
    def __new__(cls, *args, **kargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(WrapperGenerator, cls).__new__(cls)
        return cls._instance

    # 初期化は一回だけ
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.definition:Definition = None
            self.output_path:str = ''
            self.header:str = ''
            self.shared_ptr_creator_name:str = 'CreateAndAddSharedPtr'
            self.shared_ptr_creator_name_dependence:str = 'CreateAndAddSharedPtrDependence'
            self.shared_ptr_getter_name:str = 'AddAndGetSharedPtr'
            self.shared_ptr_getter_name_dependence:str = 'AddAndGetSharedPtrDependence'
        self._initialized = True
        
    # define を元に wrapper のソースコードを自動生成
    def generate(self):
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
                gen_class._generate_class(code, class_, self.definition)
        with open(self.output_path, mode='w', encoding='utf-8') as file:
            file.write(str(code))
