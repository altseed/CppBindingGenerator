
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
こうすることで、`tests/csharp.py`で決めた場所にラップ用コードが生成されます。つまり、`tests/results/csharp/csharp.cs`と、`tests/results/so/so.cpp`です。

