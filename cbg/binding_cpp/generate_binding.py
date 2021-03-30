import os
from cbg.common import *
from cbg.binding_cpp.binding_generator import BindingGeneratorCPP

# define を元に bindings のソースコードを自動生成
def _generate(self:BindingGeneratorCPP, language:str = 'ja'):
    self.language = language
    if self.output_path == None or self.output_path == '':
        print('please specify an output path')
        return
    code_hdr = Code()
    code_hdr('''// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
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

#pragma once

#include <memory>
#include <mutex>
#include <string>
#include <unordered_map>

#include "DyLib.h"

{}'''.format('\n'.join(['#include "{}"'.format(i) for i in self.includes])))
    code_src = Code()
    code_src('''// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
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

#include "{}"
'''.format(os.path.basename(self.header_path)))
    # 名前空間始まり
    with CodeBlock(code_hdr, 'namespace {}'.format(self.namespace)):
        for enum in self.definition.enums: self._generate_enum(code_hdr, enum, self.definition)
        for class_ in self.definition.classes: self._generate_class(code_hdr, class_, self.definition)
    # ファイルに書き出し
    with open(self.output_header_path, mode='w', encoding='utf-8', newline="\r\n") as f: f.write(str(code_hdr))

BindingGeneratorCPP.generate = _generate