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

CBGEXPORT void* CBGSTDCALL cbg_ClassAlias_Cpp_Constructor_0() {
    return new HelloWorld::ClassAlias_Cpp();
}

CBGEXPORT void* CBGSTDCALL cbg_ClassAlias_Cpp_FuncSimple(void* cbg_self) {
    auto cbg_self_ = (HelloWorld::ClassAlias_Cpp*)(cbg_self);

    std::shared_ptr<HelloWorld::ClassAlias_Cpp> cbg_ret = cbg_self_->FuncSimple();
    return (void*)HelloWorld::AddAndGetSharedPtr<HelloWorld::ClassAlias_Cpp>(cbg_ret);
}

CBGEXPORT void CBGSTDCALL cbg_ClassAlias_Cpp_AddRef(void* cbg_self) {
    auto cbg_self_ = (HelloWorld::ClassAlias_Cpp*)(cbg_self);

    cbg_self_->AddRef();
}

CBGEXPORT void CBGSTDCALL cbg_ClassAlias_Cpp_Release(void* cbg_self) {
    auto cbg_self_ = (HelloWorld::ClassAlias_Cpp*)(cbg_self);

    cbg_self_->Release();
}

CBGEXPORT void* CBGSTDCALL cbg_ClassA_Constructor_0() {
    return new HelloWorld::ClassA();
}

CBGEXPORT void CBGSTDCALL cbg_ClassA_FuncSimple(void* cbg_self) {
    auto cbg_self_ = (HelloWorld::ClassA*)(cbg_self);

    cbg_self_->FuncSimple();
}

CBGEXPORT void CBGSTDCALL cbg_ClassA_FuncArgInt(void* cbg_self, int32_t value) {
    auto cbg_self_ = (HelloWorld::ClassA*)(cbg_self);

    int32_t cbg_arg0 = value;
    cbg_self_->FuncArgInt(cbg_arg0);
}

CBGEXPORT void CBGSTDCALL cbg_ClassA_FuncArgFloatBoolStr(void* cbg_self, float value1, bool value2, const char16_t* value3) {
    auto cbg_self_ = (HelloWorld::ClassA*)(cbg_self);

    float cbg_arg0 = value1;
    bool cbg_arg1 = value2;
    const char16_t* cbg_arg2 = value3;
    cbg_self_->FuncArgFloatBoolStr(cbg_arg0, cbg_arg1, cbg_arg2);
}

CBGEXPORT void CBGSTDCALL cbg_ClassA_FuncArgStruct(void* cbg_self, HelloWorld::StructA_C * value1) {
    auto cbg_self_ = (HelloWorld::ClassA*)(cbg_self);

    HelloWorld::StructA* cbg_arg0 = (HelloWorld::StructA*)value1;
    cbg_self_->FuncArgStruct(cbg_arg0);
}

CBGEXPORT void CBGSTDCALL cbg_ClassA_FuncArgClass(void* cbg_self, void* value1) {
    auto cbg_self_ = (HelloWorld::ClassA*)(cbg_self);

    std::shared_ptr<HelloWorld::ClassB> cbg_arg0 = HelloWorld::CreateAndAddSharedPtr<HelloWorld::ClassB>((HelloWorld::ClassB*)value1);
    cbg_self_->FuncArgClass(cbg_arg0);
}

CBGEXPORT int32_t CBGSTDCALL cbg_ClassA_FuncReturnInt(void* cbg_self) {
    auto cbg_self_ = (HelloWorld::ClassA*)(cbg_self);

    int32_t cbg_ret = cbg_self_->FuncReturnInt();
    return cbg_ret;
}

CBGEXPORT bool CBGSTDCALL cbg_ClassA_FuncReturnBool(void* cbg_self) {
    auto cbg_self_ = (HelloWorld::ClassA*)(cbg_self);

    bool cbg_ret = cbg_self_->FuncReturnBool();
    return cbg_ret;
}

CBGEXPORT float CBGSTDCALL cbg_ClassA_FuncReturnFloat(void* cbg_self) {
    auto cbg_self_ = (HelloWorld::ClassA*)(cbg_self);

    float cbg_ret = cbg_self_->FuncReturnFloat();
    return cbg_ret;
}

CBGEXPORT HelloWorld::StructA_C CBGSTDCALL cbg_ClassA_FuncReturnStruct(void* cbg_self) {
    auto cbg_self_ = (HelloWorld::ClassA*)(cbg_self);

    HelloWorld::StructA_C cbg_ret = cbg_self_->FuncReturnStruct();
    return (cbg_ret);
}

CBGEXPORT void* CBGSTDCALL cbg_ClassA_FuncReturnClass(void* cbg_self) {
    auto cbg_self_ = (HelloWorld::ClassA*)(cbg_self);

    std::shared_ptr<HelloWorld::ClassB> cbg_ret = cbg_self_->FuncReturnClass();
    return (void*)HelloWorld::AddAndGetSharedPtr<HelloWorld::ClassB>(cbg_ret);
}

CBGEXPORT const char16_t* CBGSTDCALL cbg_ClassA_FuncReturnString(void* cbg_self) {
    auto cbg_self_ = (HelloWorld::ClassA*)(cbg_self);

    const char16_t* cbg_ret = cbg_self_->FuncReturnString();
    return cbg_ret;
}

CBGEXPORT int32_t CBGSTDCALL cbg_ClassA_FuncReturnStatic() {
    int32_t cbg_ret = HelloWorld::ClassA::FuncReturnStatic();
    return cbg_ret;
}

CBGEXPORT void* CBGSTDCALL cbg_ClassA_GetBReference(void* cbg_self) {
    auto cbg_self_ = (HelloWorld::ClassA*)(cbg_self);

    std::shared_ptr<HelloWorld::ClassB> cbg_ret = cbg_self_->GetBReference();
    return (void*)HelloWorld::AddAndGetSharedPtr<HelloWorld::ClassB>(cbg_ret);
}

CBGEXPORT int32_t CBGSTDCALL cbg_ClassA_GetEnumA(void* cbg_self) {
    auto cbg_self_ = (HelloWorld::ClassA*)(cbg_self);

    HelloWorld::EnumA cbg_ret = cbg_self_->GetEnumA();
    return (int32_t)cbg_ret;
}

CBGEXPORT void CBGSTDCALL cbg_ClassA_SetEnumA(void* cbg_self, int32_t value) {
    auto cbg_self_ = (HelloWorld::ClassA*)(cbg_self);

    HelloWorld::EnumA cbg_arg0 = (HelloWorld::EnumA)value;
    cbg_self_->SetEnumA(cbg_arg0);
}

CBGEXPORT void CBGSTDCALL cbg_ClassA_AddRef(void* cbg_self) {
    auto cbg_self_ = (HelloWorld::ClassA*)(cbg_self);

    cbg_self_->AddRef();
}

CBGEXPORT void CBGSTDCALL cbg_ClassA_Release(void* cbg_self) {
    auto cbg_self_ = (HelloWorld::ClassA*)(cbg_self);

    cbg_self_->Release();
}

CBGEXPORT void* CBGSTDCALL cbg_ClassB_Constructor_0() {
    return new HelloWorld::ClassB();
}

CBGEXPORT void CBGSTDCALL cbg_ClassB_SetValue(void* cbg_self, float value) {
    auto cbg_self_ = (HelloWorld::ClassB*)(cbg_self);

    float cbg_arg0 = value;
    cbg_self_->SetValue(cbg_arg0);
}

CBGEXPORT void CBGSTDCALL cbg_ClassB_SetEnum(void* cbg_self, int32_t enumValue) {
    auto cbg_self_ = (HelloWorld::ClassB*)(cbg_self);

    HelloWorld::EnumA cbg_arg0 = (HelloWorld::EnumA)enumValue;
    cbg_self_->SetEnum(cbg_arg0);
}

CBGEXPORT int32_t CBGSTDCALL cbg_ClassB_GetEnum(void* cbg_self, int32_t id) {
    auto cbg_self_ = (HelloWorld::ClassB*)(cbg_self);

    int32_t cbg_arg0 = id;
    HelloWorld::EnumA cbg_ret = cbg_self_->GetEnum(cbg_arg0);
    return (int32_t)cbg_ret;
}

CBGEXPORT int32_t CBGSTDCALL cbg_ClassB_GetMyProperty(void* cbg_self) {
    auto cbg_self_ = (HelloWorld::ClassB*)(cbg_self);

    int32_t cbg_ret = cbg_self_->GetMyProperty();
    return cbg_ret;
}

CBGEXPORT void CBGSTDCALL cbg_ClassB_SetMyProperty(void* cbg_self, int32_t value) {
    auto cbg_self_ = (HelloWorld::ClassB*)(cbg_self);

    int32_t cbg_arg0 = value;
    cbg_self_->SetMyProperty(cbg_arg0);
}

CBGEXPORT void* CBGSTDCALL cbg_ClassB_GetClassProperty(void* cbg_self) {
    auto cbg_self_ = (HelloWorld::ClassB*)(cbg_self);

    std::shared_ptr<HelloWorld::ClassA> cbg_ret = cbg_self_->GetClassProperty();
    return (void*)HelloWorld::AddAndGetSharedPtr<HelloWorld::ClassA>(cbg_ret);
}

CBGEXPORT void CBGSTDCALL cbg_ClassB_SetClassProperty(void* cbg_self, void* value) {
    auto cbg_self_ = (HelloWorld::ClassB*)(cbg_self);

    std::shared_ptr<HelloWorld::ClassA> cbg_arg0 = HelloWorld::CreateAndAddSharedPtr<HelloWorld::ClassA>((HelloWorld::ClassA*)value);
    cbg_self_->SetClassProperty(cbg_arg0);
}

CBGEXPORT void CBGSTDCALL cbg_ClassB_SetMyBool(void* cbg_self, bool value) {
    auto cbg_self_ = (HelloWorld::ClassB*)(cbg_self);

    bool cbg_arg0 = value;
    cbg_self_->SetMyBool(cbg_arg0);
}

CBGEXPORT void CBGSTDCALL cbg_ClassB_AddRef(void* cbg_self) {
    auto cbg_self_ = (HelloWorld::ClassB*)(cbg_self);

    cbg_self_->AddRef();
}

CBGEXPORT void CBGSTDCALL cbg_ClassB_Release(void* cbg_self) {
    auto cbg_self_ = (HelloWorld::ClassB*)(cbg_self);

    cbg_self_->Release();
}

CBGEXPORT void* CBGSTDCALL cbg_ClassC_Constructor_0() {
    return new HelloWorld::ClassC();
}

CBGEXPORT void CBGSTDCALL cbg_ClassC_SetValue(void* cbg_self, float value) {
    auto cbg_self_ = (HelloWorld::ClassC*)(cbg_self);

    float cbg_arg0 = value;
    cbg_self_->SetValue(cbg_arg0);
}

CBGEXPORT void CBGSTDCALL cbg_ClassC_SetEnum(void* cbg_self, int32_t enumValue) {
    auto cbg_self_ = (HelloWorld::ClassC*)(cbg_self);

    HelloWorld::EnumA cbg_arg0 = (HelloWorld::EnumA)enumValue;
    cbg_self_->SetEnum(cbg_arg0);
}

CBGEXPORT int32_t CBGSTDCALL cbg_ClassC_GetEnum(void* cbg_self, int32_t id) {
    auto cbg_self_ = (HelloWorld::ClassC*)(cbg_self);

    int32_t cbg_arg0 = id;
    HelloWorld::EnumA cbg_ret = cbg_self_->GetEnum(cbg_arg0);
    return (int32_t)cbg_ret;
}

CBGEXPORT void CBGSTDCALL cbg_ClassC_FuncHasRefArg(void* cbg_self, int32_t * intRef) {
    auto cbg_self_ = (HelloWorld::ClassC*)(cbg_self);

    int32_t* cbg_arg0 = intRef;
    cbg_self_->FuncHasRefArg(cbg_arg0);
}

CBGEXPORT int32_t CBGSTDCALL cbg_ClassC_GetMyProperty(void* cbg_self) {
    auto cbg_self_ = (HelloWorld::ClassC*)(cbg_self);

    int32_t cbg_ret = cbg_self_->GetMyProperty();
    return cbg_ret;
}

CBGEXPORT void CBGSTDCALL cbg_ClassC_SetMyProperty(void* cbg_self, int32_t value) {
    auto cbg_self_ = (HelloWorld::ClassC*)(cbg_self);

    int32_t cbg_arg0 = value;
    cbg_self_->SetMyProperty(cbg_arg0);
}

CBGEXPORT const char16_t* CBGSTDCALL cbg_ClassC_GetStringProperty(void* cbg_self) {
    auto cbg_self_ = (HelloWorld::ClassC*)(cbg_self);

    const char16_t* cbg_ret = cbg_self_->GetStringProperty();
    return cbg_ret;
}

CBGEXPORT void CBGSTDCALL cbg_ClassC_SetStringProperty(void* cbg_self, const char16_t* value) {
    auto cbg_self_ = (HelloWorld::ClassC*)(cbg_self);

    const char16_t* cbg_arg0 = value;
    cbg_self_->SetStringProperty(cbg_arg0);
}

CBGEXPORT void CBGSTDCALL cbg_ClassC_SetMyBool(void* cbg_self, bool value) {
    auto cbg_self_ = (HelloWorld::ClassC*)(cbg_self);

    bool cbg_arg0 = value;
    cbg_self_->SetMyBool(cbg_arg0);
}

CBGEXPORT void CBGSTDCALL cbg_ClassC_AddRef(void* cbg_self) {
    auto cbg_self_ = (HelloWorld::ClassC*)(cbg_self);

    cbg_self_->AddRef();
}

CBGEXPORT void CBGSTDCALL cbg_ClassC_Release(void* cbg_self) {
    auto cbg_self_ = (HelloWorld::ClassC*)(cbg_self);

    cbg_self_->Release();
}

CBGEXPORT void* CBGSTDCALL cbg_BaseClass_Constructor_0() {
    return new HelloWorld::BaseClass();
}

CBGEXPORT int32_t CBGSTDCALL cbg_BaseClass_GetBaseClassField(void* cbg_self) {
    auto cbg_self_ = (HelloWorld::BaseClass*)(cbg_self);

    int32_t cbg_ret = cbg_self_->GetBaseClassField();
    return cbg_ret;
}

CBGEXPORT void CBGSTDCALL cbg_BaseClass_SetBaseClassField(void* cbg_self, int32_t value) {
    auto cbg_self_ = (HelloWorld::BaseClass*)(cbg_self);

    int32_t cbg_arg0 = value;
    cbg_self_->SetBaseClassField(cbg_arg0);
}

CBGEXPORT void CBGSTDCALL cbg_BaseClass_AddRef(void* cbg_self) {
    auto cbg_self_ = (HelloWorld::BaseClass*)(cbg_self);

    cbg_self_->AddRef();
}

CBGEXPORT void CBGSTDCALL cbg_BaseClass_Release(void* cbg_self) {
    auto cbg_self_ = (HelloWorld::BaseClass*)(cbg_self);

    cbg_self_->Release();
}

CBGEXPORT void* CBGSTDCALL cbg_DerivedClass_Constructor_0() {
    return new HelloWorld::DerivedClass();
}

CBGEXPORT int32_t CBGSTDCALL cbg_DerivedClass_GetBaseClassFieldFromDerivedClass(void* cbg_self) {
    auto cbg_self_ = (HelloWorld::DerivedClass*)(cbg_self);

    int32_t cbg_ret = cbg_self_->GetBaseClassFieldFromDerivedClass();
    return cbg_ret;
}

CBGEXPORT void CBGSTDCALL cbg_DerivedClass_AddRef(void* cbg_self) {
    auto cbg_self_ = (HelloWorld::DerivedClass*)(cbg_self);

    cbg_self_->AddRef();
}

CBGEXPORT void CBGSTDCALL cbg_DerivedClass_Release(void* cbg_self) {
    auto cbg_self_ = (HelloWorld::DerivedClass*)(cbg_self);

    cbg_self_->Release();
}


}

