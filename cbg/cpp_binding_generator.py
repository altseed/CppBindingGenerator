from typing import List
import ctypes

class Description:
    '''
    a description for any objects    
    '''

    def __init__(self):
        self.descs = {}

    def add(self, lang: str, desc: str):
        '''
        add a description

        Parameters
        ----------
        lang : str
            language(ja,en)

        desc : str
            a description

        '''
        self.descs[lang] = desc


class Argument:
    '''
    an argument of function    
    '''

    def __init__(self, type_, name: str):
        '''
        add a description

        Parameters
        ----------
        type
            the type of argument

        name : str
            name

        '''

        self.type_ = type_
        self.name = name
        self.desc = Description()


Arguments = List[Argument]


class Function:
    '''
    an argument of function    
    '''

    def __init__(self, name: str):
        self.name = name
        self.brief = Description()
        self.desc = Description()
        self.args = []  # type: Arguments
        self.return_type = None
        self.is_static = False
        self.is_constructor = False

    def add_arg(self, type_, name: str) -> Argument:
        arg = Argument(type_, name)
        self.args.append(arg)
        return arg


Functions = List[Function]


class Property:
    def __init__(self):
        self.getter = None
        self.setter = None


class EnumValue:
    def __init__(self, name: str, value=None):
        self.name = name
        self.desc = Description()
        self.value = value


class Enum:
    def __init__(self):
        self.brief = Description()
        self.desc = Description()
        self.values = []  # type: List[EnumValue]

    def add(self, name: str, value=None):
        '''
        add an enum value
        '''
        v = EnumValue(name, value)
        self.values.append(v)
        return v


Enums = List[Enum]

class Field:
    def __init__(self, type_, name : str):
        self.name = name
        self.type_ = type_

Fields = List[Field]

class Struct:
    def __init__(self, namespace='', name=''):
        self.namespace = namespace
        self.name = name
        self.fields = [] # type: Fields

    def add_field(self, type_, name : str):
        field = Field(type_, name)
        self.fields.append(field)

    def cpp_fullname(self) -> str:
        if self.namespace == '':
            return self.name

        return self.namespace + '::' + self.name

Structs = List[Struct]


class Class:
    def __init__(self, namespace='', name=''):
        self.namespace = namespace  # type: str
        self.name = name  # type: str
        self.funcs = []  # type: Functions
        self.constructor_count = 0

    def add_constructor(self) -> Function:
        func = Function('Constructor_' + str(self.constructor_count))
        func.is_constructor = True
        func.return_type = self
        self.funcs.append(func)
        self.constructor_count += 1
        return func

    def add_func(self, name: str) -> Function:
        func = Function(name)
        self.funcs.append(func)
        return func


Classes = List[Class]


class Define:
    def __init__(self):
        self.enums = []  # type: Enums
        self.classes = []  # type: Classes
        self.structs = []  # type: Structs


def __get_c_func_name__(class_: Class, func_: Function) -> str:
    return 'cbg_' + class_.name + '_' + func_.name


def __get_c_release_func_name__(class_: Class) -> str:
    return 'cbg_' + class_.name + '_' + 'Release'


class Code:
    '''
    support to generate a code
    '''

    def __init__(self):
        self.lines = []
        self.indent = 0

    def inc_indent(self):
        self.indent += 1

    def dec_indent(self):
        self.indent -= 1

    def __call__(self, obj):
        self.lines.append((self.indent, obj))

    def __str__(self):
        code = ''
        for line in self.lines:
            indent = line[0]
            o = line[1]

            if isinstance(o, Code):
                ss = str(o).split('\n')

                for s in ss:
                    for i in range(indent):
                        code += '    '
                    code += s
                    code += '\n'

            else:
                for i in range(indent):
                    code += '    '

                code += str(o)
                code += '\n'

        return code


class SharedObjectGenerator:
    def __init__(self, define: Define):
        self.define = define
        self.output_path = ''

        self.header = ''  # header code inserted

    def __get_class_fullname__(self, type_: Class) -> str:
        if type_.namespace == '':
            return type_.name

        return type_.namespace + '::' + type_.name

    def __get_cpp_type__(self, type_) -> str:
        if type_ == int:
            return 'int32_t'

        if type_ == float:
            return 'float'

        if type_ == bool:
            return 'bool'

        if type_ == ctypes.c_wchar_p:
            return 'const char16_t*'

        if type_ in self.define.classes:
            return 'std::shared_ptr<{}>'.format(self.__get_class_fullname__(type_))

        if type_ in self.define.structs:
            return type_.cpp_fullname()

        if type_ in self.define.enums:
            return type_.name

        if type_ is None:
            return 'void'

        assert(False)

    def __get_c_type__(self, type_) -> str:
        if type_ == int:
            return 'int32_t'

        if type_ == float:
            return 'float'

        if type_ == bool:
            return 'bool'

        if type_ == ctypes.c_wchar_p:
            return 'const char16_t*'

        if type_ in self.define.classes:
            return 'void*'

        if type_ in self.define.structs:
            return 'void*'

        if type_ in self.define.enums:
            return 'int32_t'

        if type_ is None:
            return 'void'

        assert(False)

    def __convert_c_to_cpp__(self, type_, name: str) -> str:
        if type_ == int or type_ == float or type_ == bool or type_ == ctypes.c_wchar_p:
            return name

        if type_ in self.define.classes:
            return 'CreateAndAddSharedPtr<{}>(({}*){})'.format(self.__get_class_fullname__(type_), self.__get_class_fullname__(type_), name)

        if type_ in self.define.structs:
            return '(*({}*){})'.format(type_.cpp_fullname(), name)

        if type_ in self.define.enums:
            return '({}){}'.format(type_.name, name)

        assert(False)

    def __convert_ret__(self, type_, name: str) -> str:
        if type_ == int or type_ == float or type_ == bool or type_ == ctypes.c_wchar_p:
            return name

        if type_ in self.define.classes:
            return '(void*)GetAndAddSharedPtr<{}>({})'.format(self.__get_class_fullname__(type_), name)

        if type_ in self.define.structs:
            return '({})'.format(name)

        if type_ in self.define.enums:
            return '({}){}'.format(type_.name, name)

    def __generate_func__(self, class_: Class, func_: Function) -> str:
        code = Code()

        fname = __get_c_func_name__(class_, func_)

        args = [self.__get_c_type__(arg.type_) +
                ' ' + arg.name for arg in func_.args]

        # function name and args
        if not func_.is_static and not func_.is_constructor:
            args = ['void* cbg_self'] + args

        code('CBGEXPORT ' + self.__get_c_type__(func_.return_type) + ' CBGSTDCALL ' +
             fname + '(' + ','.join(args) + ') {')
        code.inc_indent()

        count = 0
        args = []

        if not func_.is_static and not func_.is_constructor:
            code(
                'auto cbg_self_ = ({}*)(cbg_self);\n'.format(self.__get_class_fullname__(class_)))

        # convert ctype into c++type
        for arg in func_.args:
            ex_name = 'cbg_arg' + str(count)
            code(self.__get_cpp_type__(arg.type_) + ' ' + ex_name +
                 ' = ' + self.__convert_c_to_cpp__(arg.type_, arg.name) + ';')
            args.append(ex_name)
            count += 1

        # call function and return
        if func_.is_constructor:
            code('return new ' + self.__get_class_fullname__(class_) +
                 '(' + ','.join(args) + ');')
        else:
            if func_.return_type is None:
                code('cbg_self_->' + func_.name + '(' + ','.join(args) + ');')
            else:
                code(self.__get_cpp_type__(func_.return_type) + ' cbg_ret = cbg_self_->' +
                     func_.name + '(' + ','.join(args) + ');')
                code('return ' +
                     self.__convert_ret__(func_.return_type, 'cbg_ret') + ';')

        code.dec_indent()
        code('}')
        code('')

        return str(code)

    def generate(self):

        code = ''

        header = '''\

#include <stdio.h>
#include <stdint.h>

#if defined(_WIN32) || defined(__WIN32__) || defined(__CYGWIN__)
  #include <Windows.h>
#endif

#ifndef CBGEXPORT
#if defined(_WIN32) || defined(__WIN32__) || defined(__CYGWIN__)
  #define CBGEXPORT __declspec(dllexport)
#else
  #define CBGEXPORT
#endif
#endif

#ifndef CBGSTDCALL
#if defined(_WIN32) || defined(__WIN32__) || defined(__CYGWIN__)
  #define CBGSTDCALL __stdcall
#else
  #define CBGSTDCALL
#endif
#endif

'''

        code += header

        code += self.header

        code += '''\

extern "C" {

'''

        for class_ in self.define.classes:
            for func in class_.funcs:
                code += self.__generate_func__(class_, func)

            # generate release
            release_func = Function('Release')
            code += self.__generate_func__(class_, release_func)

        footer = '''\

}

#if defined(_WIN32) || defined(__WIN32__) || defined(__CYGWIN__)

BOOL WINAPI DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpvReserved)
{
	bool res = true;
	switch (fdwReason) {
	case DLL_PROCESS_ATTACH:
		CoInitializeEx(NULL, COINIT_MULTITHREADED);
		break;
	case DLL_PROCESS_DETACH:
		CoUninitialize();
		break;
	case DLL_THREAD_ATTACH:
		CoInitializeEx(NULL, COINIT_MULTITHREADED);
		break;
	case DLL_THREAD_DETACH:
		CoUninitialize();
		break;
	default:
		break;
	}
	return res;
}

#endif

'''

        code += footer

        if self.output_path == '':
            print('please specify an output path')
        else:
            with open(self.output_path, mode='w') as f:
                f.write(code)


class BindingGenerator:
    def __init__(self, define: Define):
        self.define = define

    def generate(self):
        return