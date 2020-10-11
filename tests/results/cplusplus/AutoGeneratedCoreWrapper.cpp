// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
//
//   このファイルは自動生成されました。
//   このファイルへの変更は消失することがあります。
//
//   THIS FILE IS AUTO GENERATED.
//   YOUR COMMITMENT ON THIS FILE WILL BE WIPED.
//
// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#include <stdint.h>
#include <stdio.h>

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


#include "HelloWorld.h"

extern "C" {

CBGEXPORT void* CBGSTDCALL cbg_ClassCppD_Constructor_0() {
    return new HelloWorldCpp::ClassCppD();
}

CBGEXPORT void* CBGSTDCALL cbg_ClassCppD_FuncReturnClass(void* cbg_self) {
    auto cbg_self_ = (HelloWorldCpp::ClassCppD*)(cbg_self);

    std::shared_ptr<HelloWorld::ClassB> cbg_ret = cbg_self_->FuncReturnClass();
    return (void*)AddAndGetSharedPtr_Dependence<HelloWorld::ClassB>(cbg_ret);
}

CBGEXPORT void CBGSTDCALL cbg_ClassCppD_AddRef(void* cbg_self) {
    auto cbg_self_ = (HelloWorldCpp::ClassCppD*)(cbg_self);

    cbg_self_->AddRef();
}

CBGEXPORT void CBGSTDCALL cbg_ClassCppD_Release(void* cbg_self) {
    auto cbg_self_ = (HelloWorldCpp::ClassCppD*)(cbg_self);

    cbg_self_->Release();
}


}

