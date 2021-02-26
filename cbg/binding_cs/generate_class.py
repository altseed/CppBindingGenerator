import ctypes
from cbg.common.definition import Definition
from cbg.common.options import ArgCalledBy, SerializeType, CallBackType
from cbg.common.code import Code, IndentStyle, CodeBlock
from cbg.common.class_ import Class, CacheMode
from cbg.common.enum import Enum
from cbg.common.struct import Struct
from cbg.common.function import Function
from cbg.common.definition import Definition
import cbg.binding_cs.generate_binding as gen_binding
import cbg.binding_cs.generate_function as gen_func
import cbg.binding_cs.generate_property as gen_prop
import cbg.binding_cs.type_name as type_name
import cbg.binding_cs.type_cast as type_cast

def _generate_class(code:Code, class_:Class, definition:Definition):
    generator = gen_binding.BindingGeneratorCS()
    # XMLコメントを出力
    if class_.brief[generator.language] != None:
        code('/// <summary>\n/// {}\n/// </summary>'.format(class_.brief[generator.language]))
    # クラス名を取得
    class_name = type_name._get_alias_or_name(class_, definition)
    # Serializable属性
    if class_.serialize_type != SerializeType.Disable: code('[Serializable]')
    # 継承
    inherit = ' : ' + class_.name if class_.base_class != None else ''
    # ISerializableの実装
    if class_.serialize_type != SerializeType.Disable:
        inherit += (' : ' if inherit == '' else ', ') + 'ISerializable'
        if class_.handle_cache: inherit += ', ICacheKeeper<{}>'.format(class_name)
    # IDeserializationCallBackの実装
    if class_.call_back_type != CallBackType.Disable:
        inherit += (' : ' if inherit == '' else ', ') + 'IDeserializationCallback'
    # クラス本体
    access = 'public' if class_.is_public else 'internal'
    if class_.is_sealed: access += ' sealed'
    with CodeBlock(code, '{} partial class {}{}'.format(access, class_name, inherit), IndentStyle.BSDAllman):
        code('#region unmanaged\n')
        # キャッシュ用の辞書
        if class_.cache_mode != CacheMode.NoCache:
            dictionary = ''
            if class_.cache_mode == CacheMode.Cache: dictionary = 'Dictionary'
            if class_.cache_mode == CacheMode.Cache_ThreadSafe: dictionary = 'ConcurrentDictionary'
            dictionary = '{}<IntPtr, WeakReference<{}>>'.format(dictionary, class_name)
            cache_code = 'private {0} cacheRepo = new {0}();'.format(dictionary)
            code('[EditorBrowsable(EditorBrowsableState.Never)]\n' + cache_code + '\n')
            release_func_name = 'cbg_{}_Release'.format(class_.name)
            new_ = 'new' if class_.base_class != None else ''
            remove_func = 'TryRemove' if class_.cache_mode == CacheMode.Cache_ThreadSafe else 'Remove'
            add_func = 'TryAdd' if class_.cache_mode == CacheMode.Cache_ThreadSafe else 'Add'
            body = '''[EditorBrowsable(EditorBrowsableState.Never)]
public static {2} {0} TryGetFromCache(IntPtr native)
{{
    if(native == IntPtr.Zero) return null;

    if(cacheRepo.ContainsKey(native))
    {{
        {0} cacheRet;
        cacheRepo[native].TryGetTarget(out cacheRet);
        if(cacheRet != null)
        {{
            {1}(native);
            return cacheRet;
        }}
        else
        {{
            cacheRepo.{4}(native, out _);
        }}
    }}

    var newObject = new {0}(new MemoryHandle(native));
    cacheRepo.{3}(native, new WeakReference<{0}>(newObject));
    return newObject;
}}
'''.format(type_name._get_alias_or_name(class_, definition), release_func_name, new_, add_func, remove_func)
            code(body)
        # Coreインスタンスに対するポインタ
        if class_.base_class == None:
            code('[EditorBrowsable(EditorBrowsableState.Never)]')
            code('internal IntPtr {} = IntPtr.Zero;'.format(generator.self_ptr_name))
            code('')
        # Coreメソッド
        for func in [f for f in class_.functions if len(f.targets) == 0 or 'csharp' in f.targets]:
            gen_func._generate_unmanaged_function(code, func, class_, definition)
        for prop in class_.properties:
            gen_prop._generate_unmanaged_property(code, prop, class_, definition)
        gen_func._generate_unmanaged_function(code, Function('Release'), class_, definition)
        code('#endregion\n')
        # コンストラクタの出力
        code('[EditorBrowsable(EditorBrowsableState.Never)]')
        title = 'internal {}(MemoryHandle handle)'
        if class_.base_class != None: title += ' : base(handle)'
        with CodeBlock(code, title.format(class_name), IndentStyle.BSDAllman):
            code('{} = handle.selfPtr;'.format(generator.self_ptr_name))
        # プロパティ呼び出し
        for prop in [p for p in class_.properties if p.is_only_extern]:
            gen_prop._generate_managed_property(code, prop, class_, definition)
        # 関数呼び出し
        for func in [f for f in class_.functions if not f.onlyExtern and (len(f.targets) == 0 or 'csharp' in f.targets)]:
            gen_func._generate_managed_func(code, func, class_, definition)
        # ISerializableの実装部分
        if class_.serialize_type in [SerializeType.Interface, SerializeType.Interface_Usebase]:
            code('#region ISerialiable')