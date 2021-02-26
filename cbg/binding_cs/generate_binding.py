from cbg.common.code import Code, IndentStyle, CodeBlock
from cbg.common.definition import Definition
import cbg.binding_cs.generate_enum as gen_enum
import cbg.binding_cs.generate_class as gen_class

class BindingGeneratorCS(object):
    
    # このクラスをシングルトンパターンで設計
    def __new__(cls, *args, **kargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(BindingGeneratorCS, cls).__new__(cls)
        return cls._instance

    # 初期化は一回だけ
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.definition:Definition = None
            self.output_path:str = ''
            self.dll_name:str = ''
            self.self_ptr_name:str = 'selfPtr'
            self.language = 'ja'
        self._initialized = True
        
    # define を元に wrapper のソースコードを自動生成
    def generate(self, language:str = 'ja'):
        self.language = language
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

using System;
using System.ComponentModel;
using System.Collections.Generic;
using System.Collections.Concurrent;
using System.Runtime.InteropServices;
using System.Runtime.Serialization;
''')
        # 名前空間始まり
        if self.definition.namespace != '':
            code('namespace ' + self.definition.namespace + '\n{')
            code.indent += 1
        # メモリ管理用の構造体
        code('''[EditorBrowsable(EditorBrowsableState.Never)]
struct MemoryHandle
{
    internal IntPtr selfPtr;

    internal MemoryHandle(IntPtr p)
    {
        this.selfPtr = p;
    }
}
''')
        # 列挙型
        for enum in self.definition.enums: gen_enum._generate_enum(code, enum, self.definition)
        # クラス
        for class_ in self.definition.classes: gen_class._generate_class(code, class_, self.definition)
        # 名前空間終わり
        if self.definition.namespace != '':
            code.indent -= 1
            code('}')
        # ファイルに書き出し
        with open(self.output_path, mode='w', encoding='utf-8', newline="\r\n") as f: f.write(str(code))