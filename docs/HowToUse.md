
# 使い方

CppBindingGeneratorは、設定ファイルで決めたクラス・構造体・列挙体の構造を元に、C++から様々な言語への橋渡しとなるコードを生成するソフトウェアです。

C++側に対してはDLLに関数を公開するためのコードを生成し、
連携先の言語に対してはDLLから関数を読み込んで実行できるクラスを生成します。

設定ファイルはpythonで書き、連携元・連携先の言語仕様とは比較的に独立した環境になっています。

## 準備

最初に、C++側でのラップされるためのソースコード(.h/.cpp) を用意します。
このソースコードの内容をDLL用にラップしたC++コードと、
C#用にDllImportを用いてラップするコードをこれから生成することになります。

また、cbgの機能を使うために、`PYTONPATH`環境変数を通しておきましょう。
このリポジトリのディレクトリを`PYTONPATH`に指定することで、
cbgフォルダがPythonから見つけられるようにしておきます。

## Pythonで定義ファイルを書く

Pythonを用いて、コードを生成するための定義ファイルを作成します。
Altseed2の開発中は、このリポジトリの`tests/csharp.py`ファイルを編集して、コード生成の設定をその都度追加していくことになるはずです。

### 基本

例えば、引数・戻り値なしの関数をひとつ持つクラスを生成するよう設定するためには、`tests/csharp.py`を以下のように書きます：

```python
# class
Class1 = cbg.Class('HelloWorld', 'ClassA', False)
Class1.add_func('FuncSimple')

# define
define = cbg.Define()
define.classes.append(Class1)

#generate
sharedObjectGenerator = cbg.SharedObjectGenerator(define)

sharedObjectGenerator.header = '''
#include "HelloWorld.h"
'''

sharedObjectGenerator.func_name_create_and_add_shared_ptr = 'HelloWorld::CreateAndAddSharedPtr'
sharedObjectGenerator.func_name_add_and_get_shared_ptr = 'HelloWorld::AddAndGetSharedPtr'

sharedObjectGenerator.output_path = 'tests/results/so/so.cpp'
sharedObjectGenerator.generate()

args = sys.argv
lang = 'en'
if len(args) >= 3 and args[1] == '-lang':
    if args[2] in ['ja', 'en']:
        lang = args[2]
    else:
        print('python csharp.py -lang [ja|en]')

bindingGenerator = cbg.BindingGeneratorCSharp(define, lang)
bindingGenerator.output_path = 'tests/results/csharp/csharp.cs'
bindingGenerator.dll_name = 'Common'
bindingGenerator.namespace = 'HelloWorld'
bindingGenerator.generate()
```

`# class`というコメントの下のところを見てください。
これは、`HelloWorld`名前空間に`ClassA`というクラスがあり、
`ClassA`は`FuncSimple`という関数を持っていることをCBGに伝える設定です。
このように定義した`FuncSimple`関数は、引数と戻り値を持ちません。

この名前空間名・クラス名・関数名は、ラップされるC++コードのものと一致させてください。
また、生成されるC#コードの名前空間名・クラス名・関数名も、この名前で生成されます。
ラップされるC++コードと、ラップするC#コードの間で名前を違うものにはできないので注意してください。

`# define`というコメントの下のところでは、作成したクラス定義を`Define`というPythonのクラスに登録しています。`Define`は、このコード生成の設定データのルートとなるPythonクラスです。生成されるクラス・列挙体・構造体などは全てこの`Define`Pythonクラスに登録される必要があります。

`# generate`というコメントの下の部分は、生成の設定などが書かれる部分です。Altseed2の開発中は、特に変更する必要のない部分です。

### 生成の手順

設定ファイルを書いたので、実際に生成してみましょう。
ターミナルでリポジトリのルートディレクトリへ行き、`python tests/csharp.py`を実行します。
こうすることで、`tests/csharp.py`で決めた場所にラップ用コードが生成されます。つまり、`tests/results/csharp/csharp.cs`と`tests/results/so/so.cpp`です。

こうして生成されたC++のコードはDLLの関数として公開されるもので、中身は生成元のC++コードを単にラップするものです。

生成されたC#のコードはDLLの関数を`DllImport`し、ラップしてC#側からC#らしく呼び出せるようにするものです。このコードは、そのままAltseed2のAPIとしてユーザーに公開してもよいですし、さらに使いやすいようにラップすることもできます。

## 定義ファイルの書き方詳細

定義ファイルでは、列挙体や構造体、引数のある関数などのコード生成を設定できます。その書き方を紹介します。

### クラス

まず、クラスの定義を作成するには以下のようにします。

```python
Class1 = cbg.Class('HelloWorld', 'ClassA', False)
```

このコードは、`HelloWorld`名前空間に`ClassA`クラスを生成するための設定です。
第三引数のBool値は、このクラスのインスタンスをC++側から取得した際にキャッシュを行うかどうかを表すフラグです。

クラスには関数やプロパティを追加することができます。フィールドを追加することはできません。

### 関数

クラスには関数を追加することができます。そのためには`add_func`関数を使います。

```python
Class1 = cbg.Class('HelloWorld', 'ClassA', False)
Class1.add_func("FuncA")
```

このように作成した関数定義には、引数や戻り値を設定することができます。

#### 引数の追加のしかた

引数を追加するには、`add_arg`関数を使います。第一引数に引数の型を、第二引数に引数の名前を指定します。

第一引数の型の設定には、`int`, `float`などというように型そのものを渡します。ここには以下のようなものを渡すことができます：

* プリミティブ型(int, float, bool)
* 文字列(ctypes.c_wchar_p)
* ユーザー定義の型(Classオブジェクト、Enumオブジェクト、Structオブジェクト)

```python
Class1 = cbg.Class('HelloWorld', 'ClassA', False)
func1 = Class1.add_func("FuncA")
func1.add_arg(int, "someArg")
func1.add_arg(Class1, "someArg2")
```

#### 戻り値の設定のしかた

戻り値を設定するには、`return_value`メンバー変数を利用します。

例えば、戻り値の型を設定するために、`function.return_value.type_`を利用することができます。このメンバー変数には型そのものを代入することができます。戻り値の型を明示的に`void`としたい場合は、`None`を渡してください。

```python
Class1 = cbg.Class('HelloWorld', 'ClassA', False)
func1 = Class1.add_func("FuncA")
func1.return_value.type_ = bool

# No return value
func2 = Class1.add_func("FuncB")
func2.return_value.type_ = None
```

### プロパティの設定のしかた

クラスにプロパティを追加するには、`add_property`関数を使用します。第一引数にはプロパティの型を、第二引数にはプロパティの名前を指定します。

第三引数はgetterを持つかどうかの設定です。第四引数はsetterを持つかどうかの設定です。デフォルト値はそれぞれFalseであり、両方にFalseが指定されたプロパティは結果的に生成されません。

```python
Class1 = cbg.Class('HelloWorld', 'ClassA', False)
Class1.add_property(float, 'SomeFloat', True, True)
```

### 構造体の設定のしかた

構造体を生成するように定義を追加することができます。そのためには以下のように書きます。

```python
Struct1 = cbg.Struct('HelloWorld', 'StructA')
```

第一引数は構造体の属する名前空間で、第二引数は構造体の名前です。

構造体にはフィールドを追加することができます。関数やプロパティを追加することはできません。

#### フィールドの設定のしかた

構造体にフィールドを設定するためには、`add_field`関数を用いて以下のように書きます。

```python
Struct1 = cbg.Struct('HelloWorld', 'StructA')
Struct1.add_field(float, 'MyField')
```

第一引数はフィールドの型であり、第二引数はフィールドの名前です。

### 列挙体の設定のしかた

列挙体を生成するように定義を追加することができます。そのためには以下のように書きます。

```python
Enum1 = cbg.Enum('HelloWorld', 'EnumA')
```

第一引数は列挙体の属する名前空間で、第二引数は列挙体の型の名前です。

こうして作成した列挙体には、列挙子を追加することができます。以下のように、`add`関数を使って追加することができます。第一引数は列挙子の名前です。そして、第二引数は列挙子の値を明示的に指定するための設定であり、省略されると実際に生成されたコードでも値の指定が省略されます。

```python
Enum1 = cbg.Enum('HelloWorld', 'EnumA')
Enum1.add('Mouse')
Enum1.add('Cow')
Enum1.add('Tiger', 3)
```

### ドキュメントの追加

定義された各要素には、説明の文章を付与することができます。

* 関数
* プロパティ
* 引数

```python
Class1 = cbg.Class('HelloWorld', 'ClassA', False)

# 関数の説明
func1 = Class1.add_func('Hoge')
func1.brief = cbg.Description()
func1.brief.add('en', 'Some comment.')

# プロパティの説明
prop1 = Class1.add_property(int, 'MyInt')
prop1.brief = cbg.Description()
prop1.brief.add('en', 'Some comment.')

# 引数の説明
arg1 = func1.add_arg(Class1, 'Fuga')
arg1.desc = cbg.Description()
arg1.desc.add('en', 'Some comment.')
```

### withステートメントを用いた記法

ひとつの関数に対して繰り返し操作をしたい場合、変数名がぶつかるなどの煩わしい問題が起きる場合があります。

```python
Class1 = cbg.Class('HelloWorld', 'ClassA', False)

func1 = Class1.add_func('GetApple')
func1.add_arg(int, 'id')
func1.return_value.type_ = int

func2 = Class1.add_func('GetOrange')
func2.add_arg(int, 'id')
func2.return_value.type_ = int

func3 = Class1.add_func('GetGrape')
func3.add_arg(int, 'id')
func3.return_value.type_ = int
```

これには（好みの問題ですが）いくつか気になる点があります：

* 関数定義を保持しておく変数の名前をその都度考える必要がある(func1, func2, ...など)
* どこからどこまでがひとつの関数定義なのかが見た目から分かりづらい

そのため、必要に応じて`with`ステートメントを用いた記法を使えるようにしてあります：

```python
Class1 = cbg.Class('HelloWorld', 'ClassA', False)

with Class1.add_func('GetApple') as func:
    func.add_arg(int, 'id')
    func.return_value.type_ = int

with Class1.add_func('GetOrange') as func:
    func.add_arg(int, 'id')
    func.return_value.type_ = int

with Class1.add_func('GetGrape') as func:
    func3.add_arg(int, 'id')
    func3.return_value.type_ = int
```

この記法は、クラス・関数・引数・プロパティ・構造体・列挙体で使うことができます。

```python
# クラス定義は後でDefineに渡すのでwithの外で生成しておく
Class1 = cbg.Class('HelloWorld', 'ClassA', False)
with Class1 as class_:
    with class_.add_func('GetPeach') as func:
        # 引数
        with func.add_arg(int, 'id') as arg:
            arg.desc = cbg.Description()
            arg.desc.add('en', 'Some description')
        func.return_value.type_ = int

    with class_.add_property(int, 'GetMelon', True, True) as prop:
        prop.brief = cbg.Description()
        prop.brief.add('ja', 'Some description')

# 列挙体
Enum1 = cbg.Enum('HelloWorld', 'EnumA')
with Enum1 as enum:
    enum.add('Mosue')
    enum.add('Cow')
    enum.add('Tiger')

# 構造体
StructA = cbg.Struct('HelloWorld', 'StructA')
with StructA as struct:
    struct.add_field(float, 'X')
    struct.add_field(float, 'Y')
    struct.add_field(float, 'Z')
```