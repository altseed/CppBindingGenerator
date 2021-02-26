import ctypes
from cbg.common.code import Code, IndentStyle, CodeBlock
from cbg.common.options import ArgCalledBy
from cbg.common.class_ import Class
from cbg.common.struct import Struct
from cbg.common.enum import Enum
from cbg.common.function import Function
from cbg.common.definition import Definition
import cbg.wrapper.type_name as type_name
import cbg.wrapper.type_cast as type_cast

def _generate_function(code:Code, func:Function, class_:Class, definition:Definition):
    # 関数名を定義
    name_list = ['cbg', str(class_), str(func)]
    if func.is_overload:
        for arg in func.arguments:
            ptr = 'p' if arg.called_by == ArgCalledBy.Out or arg.ccalled_by == ArgCalledBy.Ref else ''
            if arg.type_ == ctypes.c_byte: name_list.append('byte' + ptr)
            elif arg.type_ == int: name_list.append('int' + ptr)
            elif arg.type_ == float: name_list.append('float' + ptr)
            elif arg.type_ == bool: name_list.append('bool' + ptr)
            elif arg.type_ == ctypes.c_wchar_p: name_list.append('char16p')
            elif arg.type_ == ctypes.c_void_p: name_list.append('voidp')
            elif isinstance(arg.type_, Class): name_list.append(str(arg.type_))
            elif isinstance(arg.type_, Struct): name_list.append(str(arg.type_) + ptr)
            elif isinstance(arg.type_, Enum): name_list.append(str(arg.type_))
            elif arg.type_ is None: name_list.append('void')
            else: assert(False)
    name = '_'.join(name_list)
    # 関数の引数を定義
    arguments = [type_name._get_c_type(arg.type_, definition, arg.called_by) + ' ' + arg.name for arg in func.arguments]
    if not func.is_static and not func.is_constructor: arguments = ['void* cbg_self'] + arguments
    # 関数の戻り値を定義
    return_type = class_ if func.is_constructor else func.return_value.type_
    # 関数の内容の書き出し
    block_title = 'CBGEXPORT {} CBGSTDCALL {}({})'.format(type_name._get_c_type(return_type, definition), name, ', '.join(arguments))
    with CodeBlock(code, block_title, IndentStyle.KAndR):
        # this的なやつのキャスト
        if not func.is_static and not func.is_constructor:
            class_name = type_name._get_cpp_fullname(class_, definition)
            code('auto cbg_self_ = ({}*)(cbg_self);'.format(class_name))
        # その他引数のキャスト
        casted_args = []
        for arg in func.arguments:
            casted_arg = 'cbg_arg' + str(len(casted_args))
            if arg.type_ in definition.structs and arg.called_by != ArgCalledBy.Default:
                cpp_type = '{}::{}*'.format(arg.type_.namespace, arg.type_.alias)
                c_value = '({})'.format(cpp_type) + arg.name
                code('{} {} = {};'.format(cpp_type, casted_arg, c_value))
            else:
                cpp_type = type_name._get_cpp_type(arg.type_, definition, arg.called_by)
                c_value = type_cast._type_cast(arg.type_, definition, arg.name)
                code('{} {} = {};'.format(cpp_type, casted_arg, c_value))
            casted_args.append(casted_arg)
        # コンストラクタの書き出し
        if func.is_constructor:
            class_fullname = type_name._get_cpp_fullname(class_, definition)
            code('return new {}({});'.format(class_fullname, ', '.join(casted_args)))
        # その他のメソッドの書き出し
        else:
            caller = 'cbg_self_->'
            # 静的メソッド
            if func.is_static:
                class_fullname = type_name._get_cpp_fullname(class_, definition)
                caller = class_fullname + '::'
            # 戻り値のないメソッド
            if func.return_value.type_ is None:
                code('{}{}({});'.format(caller, func.name, ', '.join(casted_args)))
            # 戻り値のあるメソッド  
            else:
                return_type = type_name._get_cpp_type(func.return_value.type_, definition)
                return_value = type_cast._return_cast(func.return_value.type_, definition, 'cbg_ret')
                code('{} cbg_ret = {}{}({});'.format(return_type, caller, func.name, ', '.join(casted_args)))
                code('return {};'.format(return_value))
    code('')