import ctypes
from cbg.common import *
from cbg.wrapper.wrapper_generator import WrapperGenerator

def _generate_function(self:WrapperGenerator, code:Code, func:Function, class_:Class):
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
    arguments = [self._get_c_type(arg.type_, arg.called_by) + ' ' + arg.name for arg in func.arguments]
    if not func.is_static and not func.is_constructor: arguments = ['void* cbg_self'] + arguments
    # 関数の戻り値を定義
    return_type = class_ if func.is_constructor else func.return_value.type_
    # 関数の内容の書き出し
    block_title = 'CBGEXPORT {} CBGSTDCALL {}({})'.format(self._get_c_type(return_type), name, ', '.join(arguments))
    with CodeBlock(code, block_title, IndentStyle.KAndR):
        # this的なやつのキャスト
        if not func.is_static and not func.is_constructor:
            class_name = self._get_cpp_fullname(class_)
            code('auto cbg_self_ = ({}*)(cbg_self);'.format(class_name))
        # その他引数のキャスト
        casted_args = []
        for arg in func.arguments:
            casted_arg = 'cbg_arg' + str(len(casted_args))
            if arg.type_ in self.definition.structs and arg.called_by != ArgCalledBy.Default:
                cpp_type = '{}::{}*'.format(arg.type_.namespace, arg.type_.alias)
                c_value = '({})'.format(cpp_type) + arg.name
                code('{} {} = {};'.format(cpp_type, casted_arg, c_value))
            else:
                cpp_type = self._get_cpp_type(arg.type_, arg.called_by)
                c_value = self._type_cast(arg.type_, arg.name)
                code('{} {} = {};'.format(cpp_type, casted_arg, c_value))
            casted_args.append(casted_arg)
        # コンストラクタの書き出し
        if func.is_constructor:
            class_fullname = self._get_cpp_fullname(class_)
            code('return new {}({});'.format(class_fullname, ', '.join(casted_args)))
        # その他のメソッドの書き出し
        else:
            caller = 'cbg_self_->'
            # 静的メソッド
            if func.is_static:
                class_fullname = self._get_cpp_fullname(class_)
                caller = class_fullname + '::'
            # 戻り値のないメソッド
            if func.return_value.type_ is None:
                code('{}{}({});'.format(caller, func.name, ', '.join(casted_args)))
            # 戻り値のあるメソッド  
            else:
                return_type = self._get_cpp_type(func.return_value.type_)
                return_value = self._return_cast(func.return_value.type_, 'cbg_ret')
                code('{} cbg_ret = {}{}({});'.format(return_type, caller, func.name, ', '.join(casted_args)))
                code('return {};'.format(return_value))
    code('')

WrapperGenerator._generate_function = _generate_function