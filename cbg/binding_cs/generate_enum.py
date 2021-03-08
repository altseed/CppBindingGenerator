from cbg.common import *
from cbg.binding_cs.binding_generator import BindingGeneratorCS

def _generate_enum(self:BindingGeneratorCS, code:Code, enum:Enum, definition:Definition):
    # XMLコメントを出力
    if enum.brief[self.language] != None:
        code('/// <summary>\n/// {}\n/// </summary>'.format(enum.brief[self.language]))
    # 属性を出力
    if enum.is_flag: code('[Flags]')
    code('[Serializable]')
    # 列挙型本体を出力
    name = self._get_alias_or_name(enum, definition)
    with CodeBlock(code, 'public enum ' + name + ' : int', IndentStyle.BSDAllman):
        for val in enum.values:
            # XMLコメントを出力
            if val.brief[self.language] != None:
                code('/// <summary>\n/// {}\n/// </summary>'.format(val.brief[self.language]))
            # 値を出力
            code(val.name + (' = ' + val.value if val.value != None else '') + ',')

BindingGeneratorCS._generate_enum = _generate_enum