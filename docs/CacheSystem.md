# キャッシュ

キャッシュするフラグが立っているクラスとその使用者に対しては、以下のコードを生成します：

```csharp
// キャッシュが必要なクラス
class Subject
{
    // キャッシュを保持するテーブル
    public static Dictionary<IntPtr, WeakReference<Subject>> cache = new Dictionary<IntPtr, WeakReference<Subject>>();

    // キャッシュから取得する
    public static Subject TryGetFromCache(IntPtr native)
    {
        if(cache.ContainsKey(native))
        {
            Subject cacheRet;
            cache[native].TryGetTarget(out cacheRet);
            if(cacheRet != null)
            {
                cbg_Subject_Release(native);
                return cacheRet;
            }
            else
            {
                cache.Remove(native);
            }
        }

        var newObject = new Subject(new MemoryHandle(native));
        cache[native] = new WeakReference<Subject>(newObject);
        return newObject;
    }
}

// Subjectクラスを使用するクラス
class Caller
{
    // キャッシュするクラスを取得するメソッドはこのように生成
    public Subject GetSubject()
    {
        var native = cbg_Caller_GetSubject();
        return Subject.TryGetFromCache(native);
    }

    // キャッシュするクラスを取得するプロパティはこのように生成
    public Subject ReadOnlySubject
    {
        get
        {
            return Subject.TryGetFromCache(cbg_Caller_GetReadOnlySubject());
        }
    }

    // キャッシュするクラスを取得・設定するプロパティはこのように生成
    // バッキング フィールドを伴う
    public Subject MySubject
    {
        get
        {
            return _MySubject ?? Subject.TryGetFromCache(cbg_Caller_GetMySubject());
        }
        set
        {
            _MySubject = value;
            cbg_Caller_SetMySubject(value);
        }
    }

    // これがバッキング フィールド
    private Subject _MySubject;

    // 設定しかできないプロパティはキャッシュ関係なし
    public Subject WriteOnlySubject
    {
        set => cbg_Caller_SetWriteOnlySubject(value);
    }
}
```

キャッシュするフラグが立っていないクラスに対しては、以下のコードを生成します：

```csharp
class Subject
{
}

public Subject GetSubject()
{
    var ret = Native_GetSubject();
    return ret != null ? new Subject(new MemoryHandle(ret)) : null;
}
```

## 関数の中身図鑑

`unmanaged_func_name` は、`__get_c_func_name__` から得ます。
`self_ptr_name` は、`self_ptr_name` から得ます。
`ClassName` は、`__get_cs_type__` から得ます。
`convert` は、`__convert_ret__` から得ます。

### コンストラクタ

```csharp
self_ptr_name = unmanaged_func_name(args);
```

### 戻り値がvoid

```csharp
unmanaged_func_name(args);
```

### 戻り値がキャッシュする型

```csharp
var native = unmanaged_func_name(args);
return ClassName.TryGetFromCache(native);
```

### 戻り値が通常の型

```csharp
var ret = unmanaged_func_name(args);
return convert(ret);
```
