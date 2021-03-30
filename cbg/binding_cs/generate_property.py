import ctypes
from cbg.common import *
from cbg.binding_cs.binding_generator import BindingGeneratorCS

def _generate_unmanaged_property(self:BindingGeneratorCS, code:Code, prop:Property, class_:Class):
    if prop.has_getter: self._generate_unmanaged_func(code, prop.getter_as_func(), class_)
    if prop.has_setter: self._generate_unmanaged_func(code, prop.setter_as_func(), class_)

BindingGeneratorCS._generate_unmanaged_property = _generate_unmanaged_property

def _generate_managed_property(self:BindingGeneratorCS, code:Code, prop:Property, class_:Class):
    # プロパティの生成にはゲッタとセッタのいずれかが必要
    if not prop.has_getter and not prop.has_setter: return
    is_reference_type = isinstance(prop.type_, Class) or prop.type_ == ctypes.c_wchar_p
    # XMLコメント
    if prop.brief[self.language] != '':
        # 関数の説明
        code('/// <summary>\n/// {}\n/// </summary>'.format(prop.brief[self.language]))
        if not prop.nullable and is_reference_type:
            code('/// <exception cref="ArgumentNullException">設定しようとした値がnull</exception>')
    # プロパティ本体
    name = self._get_cs_type(prop.type_)
    access = 'public' if prop.is_public else 'internal'
    with CodeBlock(code, '{} {} {}'.format(access, name, prop.name), IndentStyle.BSDAllman):
        # ゲッタ
        if prop.has_getter:
            with CodeBlock(code, 'get'):
                with CodeBlock(code, 'if (_{} != null)'.format(prop.name)):
                    get_code = 'return _{};' if is_reference_type else 'return _{}.Value;'
                    code(get_code.format(prop.name))
                self._write_managed_function_body(code, prop.getter_as_func(), class_)
        # セッタ
        if prop.has_setter:
            with CodeBlock(code, 'set'):
                exception = ' ?? throw new ArgumentNullException(nameof(value), "設定しようとした値がnullです");'
                set_code = '_{{}} = value{};'.format(exception if not prop.is_nullable and is_reference_type else '').format(prop.name)
                self._write_managed_function_body(code, prop.setter_as_func(), class_)
    # 内部変数
    if prop.has_setter and prop.has_getter:
        if not is_reference_type: name += '?'
        code('private {} _{};'.format(name, prop.name))
        
BindingGeneratorCS._generate_managed_property = _generate_managed_property