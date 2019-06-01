
# 前提

全てが構造体でC99の範疇で記述するのなら、このようなバインディングのコードを生成する必要はありません。
classが他のクラスのインスタンスのスマートポインタをもったり、stlを使ったりするためにバインディングのコードを生成する必要があります。

全ての他の言語に出力されるクラスはshared_ptrで扱います。
加えて、参照カウンタを持ちます。

全ての列挙体はint型です。

全ての構造体は文字列を持ちません。

# クラスの出力

出力先の言語ではクラスは、ポインタ型で持ちます。
しかし、出力先の言語ではポインタから直接関数を呼び出すことはできないため、クラスのメンバ関数を呼び出す関数を用意します。
クラスAが関数1を持っているとします。

```cpp

void ClassA_Func1(void* self)
{
    auto classA = (ClassA*)self;
    classA->Func1();
}

```

```cs
class ClassA
{
    [Dllimport("DLL")]
    internal static extern void ClassA_Func1(IntPtr self);

    IntPtr self;

    public Func1()
    {
        ClassA_Func1(self);
    }
}

```

引数が増える場合は、引数を増やし、変換が必要な場合には変換を行います。
コンストラクタもデストラクタも関数を用意します。

```cpp

void* ClassA_Constructor()
{
    return new ClassA();
}

void* ClassA_Destructor(void* self)
{
    auto classA = (ClassA*)self;
    classA->Release();
}

```

## 引数にクラスのインスタンスが与えられる場合

前提として引数は必ずshared_ptrのため、一度ポインタからshared_ptrに変換します。
shared_ptrにするときは参照カウンタを考慮するために、カスタムデリーターを設定します。
バインディングの関数を抜けた時点で参照カウンタの数が減るので、参照カウンタを増やしてからshared_ptrを作成します。

もし、参照カウンタを増やさない場合、バインディングの関数を抜けた時点で引数に与えられたインスタンスの参照カウンタが1下がり、
場合によってはメモリを破壊します。

```cpp

class ClassB
{
public:
    int AddRef();
    int Release();
};

void ClassA_Func2(void* self /*中身はClassA*/, void* arg0 /*中身はClassB*/ )
{
    auto classA = (ClassA*)self;
    auto a0 = (ClassB*)arg0;
    a0->AddRef();
    auto a0_ = std::shared_ptr<ClassB>(a0, CustomDeleteter());
    classA->Func2(a0_);
}

```


## 戻り値にクラスのインスタンスが与えられる場合

関数を抜けると戻り値の参照カウンタが減るため、参照カウンタを1増やしてから返します。

```cpp
void* ClassA_Func3(void* self)
{
    auto classA = (ClassA*)self;
    auto ret = classA->Func1();
    ret->AddRef();
    return ret.get();
}
```

出力先の言語では、クラスのインスタンスを生成し、返された値を代入します。

```cs
[Dllimport("DLL")]
internal static extern IntPtr ClassA_Func3(IntPtr self);

public ClassB Func3()
{
    var ret_c = ClassA_Func3(self);
    var ret = new ClassB();
    ret.self = ret_c;
    return ret;
}

```

## 出力先の言語でインスタンスが同一であるようにする方法

上記の方法で戻り値としてクラスのインスタンスを扱うことはできました。
しかし、値を返すたびにC#のインスタンスを生成しているため、Func3() == Func3() は成り立ちません。
新規にインスタンスを作る関数なら問題ないですが、Getやキャッシュを返す関数だと問題になります。
その時は、C#側で弱参照を使用して、既にC#側にインスタンスが存在したらそれを使いまわすようにします。

```cs
[Dllimport("DLL")]
internal static extern IntPtr ClassA_Func3(IntPtr self);

[Dllimport("DLL")]
internal static extern void ClassB_Destructor(IntPtr self);

Dictionary<IntPtr, WeakReference<ClassB>> dicClassB = new Dictionary<IntPtr, WeakReference<ClassB>>();
public ClassB Func3()
{
    var ret_c = ClassA_Func3(self);
    if(dicClassB.ContainKey(ret_c))
    {
        ClassB ret;
        dicClassB[ret_c].TryGet(ref ret);
        if(ret != null)
        {
            ClassB_Destructor(ret_c);
            return ret;
        }
        else
        {
            dicClassB.Remove(ret_c);
        }
    }

    var ret = new ClassB();
    ret.self = ret_c;
    dicClassB.Add(ret_c, new WeakReference<ClassB>(ret));
    return ret;
}

```

ただ、この処理は重いのでGetの場合、一度取得したらC#側にキャッシュしておく。
一部の関数のみDictionaryから取得するようにする、といった対策が必要です。
また、Dictionaryの中身はインスタンスが解放されたとしても消えないため、
定期的に参照がなくなった要素から消す必要があります。