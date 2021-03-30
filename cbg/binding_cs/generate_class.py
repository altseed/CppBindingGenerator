import ctypes
from cbg.common import *
from cbg.binding_cs.binding_generator import BindingGeneratorCS

def _generate_class(self:BindingGeneratorCS, code:Code, class_:Class):
    # XMLコメントを出力
    if class_.brief[self.language] != None:
        code('/// <summary>\n/// {}\n/// </summary>'.format(class_.brief[self.language]))
    # クラス名を取得
    class_name = self._get_alias_or_name(class_)
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
            cache_code = 'private static {0} cacheRepo = new {0}();'.format(dictionary)
            code('[EditorBrowsable(EditorBrowsableState.Never)]\n' + cache_code + '\n')
            release_func_name = 'cbg_{}_Release'.format(class_.name)
            new_ = 'new ' if class_.base_class != None else ''
            remove_func = 'TryRemove' if class_.cache_mode == CacheMode.Cache_ThreadSafe else 'Remove'
            add_func = 'TryAdd' if class_.cache_mode == CacheMode.Cache_ThreadSafe else 'Add'
            body = '''[EditorBrowsable(EditorBrowsableState.Never)]
public static {2}{0} TryGetFromCache(IntPtr native)
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
'''.format(self._get_alias_or_name(class_), release_func_name, new_, add_func, remove_func)
            code(body)
        # Coreインスタンスに対するポインタ
        if class_.base_class == None:
            code('[EditorBrowsable(EditorBrowsableState.Never)]')
            code('internal IntPtr {} = IntPtr.Zero;'.format(self.self_ptr_name))
            code('')
        # Coreメソッド
        for func in [f for f in class_.functions if len(f.targets) == 0 or 'csharp' in f.targets]:
            self._generate_unmanaged_function(code, func, class_)
        for prop in class_.properties:
            self._generate_unmanaged_property(code, prop, class_)
        self._generate_unmanaged_function(code, Function('Release'), class_)
        code('#endregion\n')
        # コンストラクタの出力
        code('[EditorBrowsable(EditorBrowsableState.Never)]')
        title = 'internal {}(MemoryHandle handle)'
        if class_.base_class != None: title += ' : base(handle)'
        with CodeBlock(code, title.format(class_name), IndentStyle.BSDAllman):
            code('{} = handle.selfPtr;'.format(self.self_ptr_name))
        code('')
        # プロパティ呼び出し
        for prop in [p for p in class_.properties if p.is_only_extern]:
            self._generate_managed_property(code, prop, class_)
        # 関数呼び出し
        for func in [f for f in class_.functions if not f.is_only_extern and (len(f.targets) == 0 or 'csharp' in f.targets)]:
            self._generate_managed_function(code, func, class_)
        # ISerializableの実装部分
        if class_.serialize_type in [SerializeType.Interface, SerializeType.Interface_Usebase]:
            code('#region ISerialiable\n')
            # プロパティのシリアライズ名
            code('#region SerializeName\n')
            for prop in class_.properties:
                if prop.serialized:
                    code('[EditorBrowsable(EditorBrowsableState.Never)]')
                    code('private const string S_{0} = "S_{0}";'.format(prop.name))
            code('#endregion\n')
            if class_.call_back_type != CallBackType.Disable:
                    code('[EditorBrowsable(EditorBrowsableState.Never)]')
                    code('private SerializationInfo seInfo;\n')
            title_get_obj = ''
            title_const = class_name + '(SerializationInfo info, StreamingContext context)'
            title_const = ('private ' if class_.is_sealed else 'protected ') + title_const
            if class_.base_class != None and class_.base_class.serialize_type in [SerializeType.Interface, SerializeType.Interface_Usebase]:
                title_const += 'base(info, context)'
                title_get_obj = 'protected override void '
            else:
                title_get_obj = 'void ISerializable.' if class_.is_sealed else 'protected virtual void '
                if class_._constructor_count == 1: title_const += ' : this()'
                elif class_.base_class == None: title_const += ' : this(new MemoryHandle(IntPtr.Zero))'
            title_get_obj += 'GetObjectData(SerializationInfo info, StreamingContext context)'
            # デシリアライズ時に呼び出すコンストラクタ
            code('/// <summary>')
            code('/// シリアライズされたデータをもとに<see cref="{}"/>のインスタンスを生成します。'.format(class_name))
            code('/// </summary>')
            code('/// <param name="info">シリアライズされたデータを格納するオブジェクト</param>')
            code('/// <param name="context">送信元の情報</param>')
            code('[EditorBrowsable(EditorBrowsableState.Never)]')
            with CodeBlock(code, title_const, IndentStyle.BSDAllman):
                if class_.call_back_type != CallBackType.Disable: code('seInfo = info;\n')
                else: self._deserialize(code, class_, 'info')
                code('OnDeserialize_Constructor(info, context);')
            code('')
            # シリアライズするデータの設定
            code('/// <summary>')
            code('/// シリアライズするデータを設定します。')
            code('/// </summary>')
            code('/// <param name="info">シリアライズされるデータを格納するオブジェクト</param>')
            code('/// <param name="context">送信先の情報</param>')
            code('[EditorBrowsable(EditorBrowsableState.Never)]')
            with CodeBlock(code, title_get_obj, IndentStyle.BSDAllman):
                if class_.serialize_type in [SerializeType.Interface_Usebase] and class_.base_class != None and class_.base_class.serialize_type in [SerializeType.Interface, SerializeType.Interface_Usebase]:
                    code('base.GetObjectData(info, context);\n')
                else:
                    code('if (info == null) throw new ArgumentNullException(nameof(info), "引数がnullです");')
                for prop in class_.properties:
                    if prop.serialized:
                        code('info.AddValue(S_{0}, {0});'.format(prop.name))
                code('')
                code('OnGetObjectData(info, context);')
            code('')
            if (class_.base_class == None or class_.base_class.serialize_type in [SerializeType.Disable, SerializeType.AttributeOnly]) and not class_.is_sealed:
                code('[EditorBrowsable(EditorBrowsableState.Never)]')
                code('void ISerializable.GetObjectData(SerializationInfo info, StreamingContext context) => GetObjectData(info, context);')
            code('')
            # OnGetObjectData
            code('')
            code('/// <summary>')
            if class_.is_sealed and (class_.base_class == None or class_.base_class.serialize_type in [SerializeType.Disable, SerializeType.AttributeOnly]):
                code('/// <see cref="ISerializable.GetObjectData(SerializationInfo, StreamingContext)"/>内で実行されます。')
            else:
                code('/// <see cref="GetObjectData(SerializationInfo, StreamingContext)"/>内で実行されます。')
            code('/// </summary>')
            code('/// <param name="info">シリアライズされるデータを格納するオブジェクト</param>')
            code('/// <param name="context">送信先の情報</param>')
            code('[EditorBrowsable(EditorBrowsableState.Never)]')
            code('partial void OnGetObjectData(SerializationInfo info, StreamingContext context);')
            # OnDeserialization_Constructor
            code('')
            code('/// <summary>')
            code('/// <see cref="{}(SerializationInfo, StreamingContext)"/>内で実行します。'.format(class_name))
            code('/// </summary>')
            code('/// <param name="info">シリアライズされたデータを格納するオブジェクト</param>')
            code('/// <param name="context">送信元の情報</param>')
            code('[EditorBrowsable(EditorBrowsableState.Never)]')
            code('partial void OnDeserialize_Constructor(SerializationInfo info, StreamingContext context);')
            # Deserialize_GetPtr
            code('')
            code('/// <summary>')
            if class_.call_back_type != CallBackType.Disable:
                code('/// <see cref="IDeserializationCallback.OnDeserialization"/>内で呼び出されます。')
            else:
                code('/// <see cref="{}(SerializationInfo, StreamingContext)"/>内で呼び出される'.format(class_name))
            code('/// デシリアライズ時にselfPtrを取得する操作をここに必ず書くこと')
            code('/// </summary>')
            code('/// <param name="ptr">selfPtrとなる値 初期値である<see cref="IntPtr.Zero"/>のままだと<see cref="SerializationException"/>がスローされる</param>')
            code('/// <param name="info">シリアライズされたデータを格納するオブジェクト</param>')
            code('[EditorBrowsable(EditorBrowsableState.Never)]')
            code('partial void Deserialize_GetPtr(ref IntPtr ptr, SerializationInfo info);')
            title_get = ''
            if class_.base_class != None and class_.base_class.serialize_type in [SerializeType.Interface, SerializeType.Interface_Usebase] and class_.base_class.handle_cache:
                title_get = 'protected private override '
            else:
                title_get = 'private ' if class_.is_sealed else 'protected private virtual '
            title_get += 'IntPtr Call_GetPtr(SerializationInfo info)'
            code('')
            code('/// <summary>')
            code('/// 呼び出し禁止')
            code('/// </summary>')
            code('[EditorBrowsable(EditorBrowsableState.Never)]')
            with CodeBlock(code, title_get, IndentStyle.BSDAllman):
                code('var ptr = IntPtr.Zero;')
                code('Deserialize_GetPtr(ref ptr, info);')
                code('return ptr;')
            code('')
            # Unsetter_Deserialize
            title_des = 'private' if class_.is_sealed else 'protected private'
            title_des += ' void {}_Unsetter_Deserialize(SerializationInfo info'.format(class_name)
            title_des_args = ''
            for prop in class_.properties:
                if prop.is_serialized and not prop.has_setter:
                    title_des_args += ', out {} {}'.format(self._get_cs_type(prop.type_), prop.name)
            title_des_args += ')'
            if title_des_args != ')':
                code('/// <summary>')
                if class_.call_back_type != CallBackType.Disable:
                    code('/// <see cref="IDeserializationCallback.OnDeserialization"/>でデシリアライズされなかったオブジェクトを呼び出します。')
                else:
                    code('/// <see cref="{}(SerializationInfo, StreamingContext)"/>でデシリアライズされなかったオブジェクトを呼び出します。'.format(class_name))
                code('/// </summary>')
                code('/// <param name="info">シリアライズされたデータを格納するオブジェクト</param>')
                for prop in class_.properties:
                    if prop.is_serialized and not prop.has_setter:
                        code('/// <param name="{0}"><see cref="{1}.{0}"/></param>'.format(prop.name, class_name))
                code('[EditorBrowsable(EditorBrowsableState.Never)]')
                with CodeBlock(code, title_des + title_des_args, IndentStyle.BSDAllman):
                    self._deserialize_nosetter(code, class_)
            # ICacheKeeper
            if class_.handle_cache:
                code('#region ICacheKeeper')
                code('')
                code('[EditorBrowsable(EditorBrowsableState.Never)]')
                code('IDictionary<IntPtr, WeakReference<{0}>> ICacheKeeper<{0}>.CacheRepo => cacheRepo;'.format(class_name))
                code('')
                code('[EditorBrowsable(EditorBrowsableState.Never)]')
                with CodeBlock(code, 'IntPtr ICacheKeeper<{}>.Self'.format(class_name), IndentStyle.BSDAllman):
                    code('get => selfPtr;')
                    code('set => selfPtr = value;')
                code('')
                code('[EditorBrowsable(EditorBrowsableState.Never)]')
                code('void ICacheKeeper<{0}>.Release(IntPtr native) => cbg_{0}_Release(native);'.format(class_name))
                code('')
                code('#endregion')
            code('')
            code('#endregion')
            code('')
            # OnDeserializationCallback
            if class_.call_back_type != CallBackType.Disable:
                title = ''
                if class_.base_class != None and class_.base_class.call_back_type != CallBackType.Disable:
                    title = 'protected override void '
                elif class_.is_sealed:
                    title = 'void IDeserializationCallback.'
                else:
                    title = 'protected virtual void '
                title += 'OnDeserialization(object sender)'
                code('/// <summary>')
                code('/// デシリアライズ時に実行')
                code('/// </summary>')
                code('/// <param name="sender">現在はサポートされていない 常にnullを返します。</param>')
                code('[EditorBrowsable(EditorBrowsableState.Never)]')
                with CodeBlock(code, title):
                    if class_.serialize_type in [SerializeType.Interface, SerializeType.Interface_Usebase]:
                        code('if (seInfo == null) return;')
                        code('')
                        _deserialize(class_, code, 'seInfo')
                        if class_.base_class != None and class_.base_class.call_back_type != CallBackType.Disable:
                            code('base.OnDeserialization(sender);')
                        code('')
                    code('OnDeserialize_Method(sender);')
                    if class_.serialize_type in [SerializeType.Interface, SerializeType.Interface_Usebase]:
                        code('')
                        code('seInfo = null;')
                if class_.base_class == None and not class_.is_sealed:
                    code('[EditorBrowsable(EditorBrowsableState.Never)]')
                    code('void IDeserializationCallback.OnDeserialization(object sender) => OnDeserialization(sender);')
                # OnDeserialize_Method
                code('/// <summary>')
                code('/// <see cref="IDeserializationCallback.OnDeserialization"/>中で実行されます。')
                code('/// </summary>')
                code('/// <param name="sender">現在はサポートされていない 常にnullを返す</param>')
                code('[EditorBrowsable(EditorBrowsableState.Never)]')
                code('partial void OnDeserialize_Method(object sender);')
                code('')
            # デストラクタ
            code('/// <summary>')
            code('/// <see cref="{}"/>のインスタンスを削除します。'.format(class_name))
            code('/// </summary>')
            with CodeBlock(code, '~{}()'.format(class_name), IndentStyle.BSDAllman):
                with CodeBlock(code, 'lock (this) ', IndentStyle.BSDAllman):
                    with CodeBlock(code, 'if ({} != IntPtr.Zero)'.format(self.self_ptr_name), IndentStyle.BSDAllman):
                        code('{}({});'.format('cbg_{}_Release'.format(class_.name), self.self_ptr_name))
                        code('{} = IntPtr.Zero;'.format(self.self_ptr_name))

BindingGeneratorCS._generate_class = _generate_class

def _deserialize(self:BindingGeneratorCS, code:Code, class_:Class, info:str):
    if class_.handle_cache:
        if class_.base_class != None and class_.base_class.handle_cache:
            code('var ptr = (ptr == IntPtr.Zero) ? Call_GetPtr({}) : selfPtr;'.format(info))
        else:
            code('var ptr = Call_GetPtr({});'.format(info))
        code('')
        code('if (ptr == IntPtr.Zero) throw new SerializationException("インスタンス生成に失敗しました");')
        if class_.cache_mode == CacheMode.Cache_ThreadSafe:
            code('CacheHelper.CacheHandlingOnDeserializationConcurrent(this, ptr);')
        else:
            code('CacheHelper.CacheHandlingOnDeserialization(this, ptr);')
        code('')
    else:
        code('selfPtr = Call_GetPtr({});'.format(info))
        code('if (selfPtr == IntPtr.Zero) throw new SerializationException("インスタンス生成に失敗しました");')
        code('')
    for prop in class_.properties:
        if prop.serialized and prop.has_setter:
            c = '{} = {}.{}'.format(prop.name, info, _write_getvalue(prop))
            if isinstance(prop.type_, Class) and prop.type_.call_back_type != CallBackType.Disable:
                code('var ' + c)
                code('((IDeserializationCallback){})?.OnDeserialization(null);'.format(prop.name))
                code('this.{} = {};'.format(prop.name, prop.name))
            else:
                code(c)

BindingGeneratorCS._deserialize = _deserialize

def _deserialize_nosetter(self:BindingGeneratorCS, code:Code, class_:Class):
    for prop in class_.properties:
        if prop.is_serialized and not prop.has_setter:
            code('{} = info.{}'.format(prop.name, _write_getvalue(prop)))
            if isinstance(prop.type_, Class) and prop.type_.call_back_type != CallBackType.Disable:
                code('((IDeserializationCallback){}).OnDeserialization(null);'.format(prop.name))

BindingGeneratorCS._deserialize_nosetter = _deserialize_nosetter

def _write_getvalue(self:BindingGeneratorCS, prop:Property):
    if prop.type_ == ctypes.c_byte:
        return 'GetByte(S_{});'.format(prop.name)
    if prop.type_ == int:
        return 'GetInt32(S_{});'.format(prop.name)
    if prop.type_ == bool:
        return 'GetBoolean(S_{});'.format(prop.name)
    if prop.type_ == float:
        return 'GetSingle(S_{});'.format(prop.name)
    if prop.type_ == ctypes.c_wchar_p:
        return 'GetString(S_{}){};'.format(' ?? throw new SerializationException("デシリアライズに失敗しました")' if prop.is_null_deserialized else '', prop.name)
    if isinstance(prop.type_, Struct):
        return 'GetValue<{}>(S_{});'.format(prop.type_.alias, prop.name)
    if isinstance(prop.type_, Class) and not prop.is_null_deserialized:
        return 'GetValue<{}>(S_{}) ?? throw new SerializationException("デシリアライズに失敗しました");'.format(self.get_alias_or_name(prop.type_), prop.name)
    if isinstance(prop.type_, Enum):
        return 'GetValue<{}>(S_{});'.format(self.get_alias_or_name(prop.type_), prop.name)
    return 'GetValue<{}>(S_{});'.format(prop.type_.name, prop.name)

BindingGeneratorCS._write_getvalue = _write_getvalue