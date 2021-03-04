import ctypes
from cbg.common import *
import cbg.binding_cs.generate_binding as gen_binding
import cbg.binding_cs.type_name as type_name
import cbg.binding_cs.type_cast as type_cast

def _get_c_function_name(code:Code, func:Function, class_:Class):
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
    return '_'.join(name_list)

def _generate_unmanaged_function(code:Code, func:Function, class_:Class, definition:Definition):
    generator = gen_binding.BindingGeneratorCS()
    # 関数名を定義
    name = _get_c_function_name(code, func, class_)
    # 引数の設定
    args = [type_name._get_csc_type(arg.type_, definition, arg.called_by) + ' ' + arg.name for arg in func.arguments]
    if not func.is_static and not func.is_constructor: args = ['IntPtr {}'.format(generator.self_ptr_name)] + args
    # 諸々属性の出力
    code('[DllImport("{}")]'.format(generator.dll_name))
    code('[EditorBrowsable(EditorBrowsableState.Never)]')
    if(func.return_value.type_ == bool): code('[return: MarshalAs(UnmanagedType.U1)]')
    # 関数定義の出力
    ret_type = type_name._get_csc_type(func.return_value.type_, definition)
    code('private static extern {} {}({});\n'.format(ret_type, name, ', '.join(args)))

def _generate_managed_function(code:Code, func:Function, class_:Class, definition:Definition):
    generator = gen_binding.BindingGeneratorCS()
    # 関数名を定義
    name = _get_c_function_name(code, func, class_)
    # 引数の設定
    args = [type_name._get_cs_type(arg.type_, definition, arg.called_by) + ' ' + arg.name for arg in func.arguments]
    # XMLコメントを出力
    if func.brief[generator.language] != None:
        # 関数の説明
        code('/// <summary>\n/// {}\n/// </summary>'.format(func.brief[generator.language]))
        # 引数
        for arg in func.arguments:
            if arg.brief[generator.language] != None:
                code('/// <param name="{}">{}</param>'.format(arg.name, arg.brief[generator.language]))
        # 例外
        argcount = 0
        exception = ''
        for arg in func.arguments:
            if not arg.nullable and (isinstance(arg.type_) or arg.type_ == ctypes.c_wchar_p):
                if argcount > 0: exception += ', '
                exception += '<paramref name="{}"/>'.format(arg.name)
                argcount += 1
        if argcount == 1: exception += 'がnull'
        if argcount > 1: exception += 'のいずれかがnull'
        if exception != '': code('/// <exception cref="ArgumentNullException">{}</exception>'.format(exception))
        # 戻り値
        if func.return_value != None and func.return_value.brief[generator.language] != None:
            code('/// <returns>{}</returns>'.format(func.return_value.brief[generator.language]))
    # キャッシュ用の辞書
    cache_mode = func.return_value.cache_mode()
    if cache_mode != CacheMode.NoCache:
        return_type_name = type_name._get_cs_type(func.return_value.type_, definition)
        dictionary = ''
        if cache_mode == CacheMode.Cache: dictionary = 'Dictionary'
        if cache_mode == CacheMode.Cache_ThreadSafe: dictionary = 'ConcurrentDictionary'
        dictionary = '{}<IntPtr, WeakReference<{{0}}>>'.format(dictionary)
        cache_code = 'private {0} cache{{1}} = new {0}();'.format(dictionary)
        code('[EditorBrowsable(EditorBrowsableState.Never)]')
        code(cache_code.format(return_type_name, func.name))
    # 関数のアクセスレベル等々
    determines = ['public' if func.is_public else 'internal']
    if func.is_static: determines += ['static']
    if func.is_constructor:
        func_title = '{} {}({})'.format(' '.join(determines), type_name._get_alias_or_name(class_, definition), ', '.join(args)) 
        if class_.base_class != None: func_title += ' : base({})'.format(', '.join(['true'] + [arg.name for arg in func.args]))
        with CodeBlock(code, func_title, IndentStyle.BSDAllman): _write_managed_function_body(code, func, class_, definition)
        code('')
        func_title = 'protected {}({})'.format(type_name._get_alias_or_name(class_, definition), ', '.join(['bool calledByDerived'] + args))
        if class_.base_class != None: func_title += ' : base({})'.format(', '.join(['calledByDerived'] + [arg.name for arg in func.args]))
        with CodeBlock(code, func_title, IndentStyle.BSDAllman): _write_managed_function_body(code, func, class_, definition, True)
    else:
        func_title = '{} {} {}({})'.format(' '.join(determines), type_name._get_cs_type(func.return_value.type_, definition), func.name, ', '.join(args))
        with CodeBlock(code, func_title, IndentStyle.BSDAllman): _write_managed_function_body(code, func, class_, definition)
    code('')

def _write_managed_function_body(code:Code, func:Function, class_:Class, definition:Definition, call_by_derived:bool = False):
    generator = gen_binding.BindingGeneratorCS()
    # 関数名を定義
    name = _get_c_function_name(code, func, class_)
    # 関数の呼び出し処理
    args = [type_cast._type_cast(arg.type_, arg.name, definition, arg.called_by) for arg in func.args]
    if not func.is_static and not func.is_constructor: args = [generator.self_ptr_name] + args
    for arg in func.args:
        if not arg.nullable and (isinstance(arg.type_, Class) or arg.type_ == ctypes.c_wchar_p):
            code('if ({} == null) throw new ArgumentNullException(nameof({}), "引数がnullです");'.format(arg.name, arg.name))
    if func.is_constructor:
        if call_by_derived:
            code('// Dummy function.')
        else:
            code('{} = {}({});'.format(generator.self_ptr_name, name, ', '.join(args)))
    else:
        if func.return_value.type_ is None:
            code('{}({});'.format(name, ', '.join(args)))
        else:
            code('var ret = {}({});'.format(name, ', '.join(args)))
            code('return {};'.format(type_cast._return_cast(func.return_value.type_, 'ret')))