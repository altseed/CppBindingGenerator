from cbg.common.definition import Definition
from cbg.common.code import Code, IndentStyle, CodeBlock
from cbg.common.enum import Enum
import cbg.binding_cs.generate_binding as gen_binding
import cbg.binding_cs.type_name as type_name

def _generate_enum(code:Code, enum:Enum, definition:Definition):
    generator = gen_binding.BindingGeneratorCS()
    # XMLコメントを出力
    if enum.brief[generator.language] != None:
        code('/// <summary>\n/// {}\n/// </summary>'.format(enum.brief[generator.language]))
    # 属性を出力
    if enum.is_flag: code('[Flags]')
    code('[Serializable]')
    # 列挙型本体を出力
    name = type_name._get_alias_or_name(enum, definition)
    with CodeBlock(code, 'public enum ' + name + ' : int', IndentStyle.BSDAllman):
        for val in enum.values:
            # XMLコメントを出力
            if val.brief[generator.language] != None: code('/// <summary>\n/// {}\n/// </summary>'.format(val.brief[generator.language]))
            # 値を出力
            code(val.name + (' = ' + val.value if val.value != None else '') + ',')
