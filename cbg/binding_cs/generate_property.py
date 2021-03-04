import ctypes
from cbg.common import *
import cbg.binding_cs.generate_binding as gen_binding
import cbg.binding_cs.type_name as type_name
import cbg.binding_cs.type_cast as type_cast
import cbg.binding_cs.generate_function as gen_func

def _generate_unmanaged_property(code:Code, prop:Property, class_:Class, definition:Definition):
    if prop.has_getter: gen_func._generate_unmanaged_func(code, prop.getter_as_func(), class_, definition)
    if prop.has_setter: gen_func._generate_unmanaged_func(code, prop.setter_as_func(), class_, definition)

def _generate_managed_property(code:Code, prop:Property, class_:Class, definition:Definition):
    generator = gen_binding.BindingGeneratorCS()
    # プロパティの生成にはゲッタとセッタのいずれかが必要
    if not prop.has_getter and not prop.has_setter: return
    is_reference_type = isinstance(prop.type_, Class) or prop.type_ == ctypes.c_wchar_p
    # XMLコメント
    if prop.brief[generator.language] != '':
        # 関数の説明
        code('/// <summary>\n/// {}\n/// </summary>'.format(prop.brief[generator.language]))
        if not prop.nullable and is_reference_type:
            code('/// <exception cref="ArgumentNullException">設定しようとした値がnull</exception>')
    # プロパティ本体
    name = type_name._get_cs_type(prop.type_, definition)
    access = 'public' if prop.is_public else 'internal'
    with CodeBlock(code, '{} {} {}'.format(access, name, prop.name), IndentStyle.BSDAllman):
        # ゲッタ
        if prop.has_getter:
            with CodeBlock(code, 'get'):
                with CodeBlock(code, 'if (_{} != null)'.format(prop.name)):
                    get_code = 'return _{};' if is_reference_type else 'return _{}.Value;'
                    code(get_code.format(prop.name))
                gen_func._write_managed_function_body(code, prop.getter_as_func(), class_, definition)
        # セッタ
        if prop.has_setter:
            with CodeBlock(code, 'set'):
                exception = ' ?? throw new ArgumentNullException(nameof(value), "設定しようとした値がnullです");'
                set_code = '_{{}} = value{};'.format(exception if not prop.is_nullable and is_reference_type else '').format(prop.name)
                gen_func._write_managed_function_body(code, prop.setter_as_func(), class_, definition)
    # 内部変数
    if prop.has_setter and prop.has_getter:
        if not is_reference_type: type_name += '?'
        code('private {} _{};'.format(type_name, prop.name))
        