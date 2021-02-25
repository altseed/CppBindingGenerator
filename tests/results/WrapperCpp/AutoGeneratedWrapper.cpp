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

#include "CoreSample.h"

extern "C" {
    
    CBGEXPORT void* CBGSTDCALL cbg_SimpleClass_Constructor0() {
        return new CoreSample::SimpleClass();
    }
    
    CBGEXPORT void CBGSTDCALL cbg_SimpleClass_AddRef(void* cbg_self) {
        auto cbg_self_ = (CoreSample::SimpleClass*)(cbg_self);
        cbg_self_->AddRef();
    }
    
    CBGEXPORT void CBGSTDCALL cbg_SimpleClass_Release(void* cbg_self) {
        auto cbg_self_ = (CoreSample::SimpleClass*)(cbg_self);
        cbg_self_->Release();
    }
    
}
