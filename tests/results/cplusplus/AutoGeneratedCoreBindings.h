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

#pragma once

#include <memory>
#include <mutex>
#include <string>
#include <unordered_map>

#include "DynamicLinkLibrary.h"
#include "Additional.h"

namespace HelloWorldA
{
    static std::shared_ptr<DynamicLinkLibrary> dll = nullptr;
    
    bool LoadLibrary();
    
    enum class Animal : int
    {
        Mosue,
        Cow,
        Tiger = 3,
    };
    
    class ClassAlias_Cpp;
    class ClassA;
    class ClassB;
    class ClassC;
    class BaseClass;
    class DerivedClass;
    
    class ClassAlias_Cpp
    {
    private:
        static std::mutex mtx;
        static std::unordered_map<void*, std::weak_ptr<ClassAlias_Cpp> > cacheRepo;
        
    public:
        static std::shared_ptr<ClassAlias_Cpp> TryGetFromCache(void* native);
        
    public:
        void* selfPtr = nullptr;
        
    private:
        static void* cbg_ClassAlias_Cpp_Constructor_0();
    
        static void* cbg_ClassAlias_Cpp_FuncSimple(void* selfPtr);
    
        static void cbg_ClassAlias_Cpp_Release(void* selfPtr);
        
        
    public:
        ClassAlias_Cpp(void* handle);
        
    private:
        
    public:
        ClassAlias_Cpp(bool callCoreConstructor);
        
        std::shared_ptr<ClassAlias_Cpp> FuncSimple();
        
        /**
         @brief ClassAlias_Cppのインスタンスを削除します。
         */
        ~ClassAlias_Cpp();
    };
    
    class ClassA
    {
    private:
        static std::mutex mtx;
        static std::unordered_map<void*, std::weak_ptr<ClassA> > cacheRepo;
        
    public:
        static std::shared_ptr<ClassA> TryGetFromCache(void* native);
        
    public:
        void* selfPtr = nullptr;
        
    private:
        static void* cbg_ClassA_Constructor_0();
    
        static void cbg_ClassA_FuncSimple(void* selfPtr);
    
        static void cbg_ClassA_FuncArgInt(void* selfPtr, int value);
    
        static void cbg_ClassA_FuncArgFloatBoolStr(void* selfPtr, float value1, int value2, const char16_t* value3);
    
        static void cbg_ClassA_FuncArgStruct(void* selfPtr, void* value1);
    
        static void cbg_ClassA_FuncArgClass(void* selfPtr, void* value1);
    
        static int cbg_ClassA_FuncReturnInt(void* selfPtr);
    
        static int cbg_ClassA_FuncReturnBool(void* selfPtr);
    
        static float cbg_ClassA_FuncReturnFloat(void* selfPtr);
    
        static StructA_C cbg_ClassA_FuncReturnStruct(void* selfPtr);
    
        static void* cbg_ClassA_FuncReturnClass(void* selfPtr);
    
        static const char16_t* cbg_ClassA_FuncReturnString(void* selfPtr);
    
        static int cbg_ClassA_FuncReturnStatic();
    
        static void* cbg_ClassA_GetBReference(void* selfPtr);
    
        static int cbg_ClassA_GetEnumA(void* selfPtr);
    
        static void cbg_ClassA_SetEnumA(void* selfPtr, int value);
    
        static void cbg_ClassA_Release(void* selfPtr);
        
        
    public:
        ClassA(void* handle);
        
    private:
        Animal _EnumA;
        
    public:
        std::shared_ptr<ClassB> get_BReference();
        
        Animal get_EnumA();
        void set_EnumA(Animal value);
        
        ClassA(bool callCoreConstructor);
        
        void FuncSimple();
        
        void FuncArgInt(int value);
        
        void FuncArgFloatBoolStr(float value1, bool value2, std::basic_string<char16_t> value3);
        
        /**
         @brief Processes a structA.
         */
        void FuncArgStruct(std::shared_ptr<StructA_C> value1);
        
        void FuncArgClass(std::shared_ptr<ClassB> value1);
        
        /**
         @brief Returns some integer.
         */
        int FuncReturnInt();
        
        bool FuncReturnBool();
        
        float FuncReturnFloat();
        
        StructA_C FuncReturnStruct();
        
        std::shared_ptr<ClassB> FuncReturnClass();
        
        std::basic_string<char16_t> FuncReturnString();
        
        static int FuncReturnStatic();
        
        /**
         @brief ClassAのインスタンスを削除します。
         */
        ~ClassA();
    };
    
    class ClassB
    {
    private:
        static std::mutex mtx;
        static std::unordered_map<void*, std::weak_ptr<ClassB> > cacheRepo;
        
    public:
        static std::shared_ptr<ClassB> TryGetFromCache(void* native);
        
    public:
        void* selfPtr = nullptr;
        
    private:
        static void* cbg_ClassB_Constructor_0();
    
        static void cbg_ClassB_SetValue(void* selfPtr, float value);
    
        static void cbg_ClassB_SetEnum(void* selfPtr, int enumValue);
    
        static int cbg_ClassB_GetEnum(void* selfPtr, int id);
    
        static int cbg_ClassB_GetMyProperty(void* selfPtr);
    
        static void cbg_ClassB_SetMyProperty(void* selfPtr, int value);
    
        static void cbg_ClassB_Release(void* selfPtr);
        
        
    public:
        ClassB(void* handle);
        
    private:
        int _MyProperty;
        
    public:
        /**
         @brief 
         */
        int get_MyProperty();
        void set_MyProperty(int value);
        
        ClassB(bool callCoreConstructor);
        
        void SetValue(float value);
        
        void SetEnum(Animal enumValue);
        
        Animal GetEnum(int id);
        
        /**
         @brief ClassBのインスタンスを削除します。
         */
        ~ClassB();
    };
    
    class ClassC
    {
    private:
        static std::mutex mtx;
        static std::unordered_map<void*, std::weak_ptr<ClassC> > cacheRepo;
        
    public:
        static std::shared_ptr<ClassC> TryGetFromCache(void* native);
        
    public:
        void* selfPtr = nullptr;
        
    private:
        static void* cbg_ClassC_Constructor_0();
    
        static void cbg_ClassC_SetValue(void* selfPtr, float value);
    
        static void cbg_ClassC_SetEnum(void* selfPtr, int enumValue);
    
        static int cbg_ClassC_GetEnum(void* selfPtr, int id);
    
        static void cbg_ClassC_FuncHasRefArg(void* selfPtr, int* intRef);
    
        static int cbg_ClassC_GetMyProperty(void* selfPtr);
    
        static void cbg_ClassC_SetMyProperty(void* selfPtr, int value);
    
        static const char16_t* cbg_ClassC_GetStringProperty(void* selfPtr);
    
        static void cbg_ClassC_SetStringProperty(void* selfPtr, const char16_t* value);
    
        static void cbg_ClassC_SetMyBool(void* selfPtr, int value);
    
        static void cbg_ClassC_Release(void* selfPtr);
        
        
    public:
        ClassC(void* handle);
        
    private:
        int _MyProperty;
        std::basic_string<char16_t> _StringProperty;
        
    public:
        /**
         @brief 
         */
        int get_MyProperty();
        void set_MyProperty(int value);
        
        /**
         @brief 
         */
        std::basic_string<char16_t> get_StringProperty();
        void set_StringProperty(std::basic_string<char16_t> value);
        
        
        void set_MyBool(bool value);
        
        ClassC(bool callCoreConstructor);
        
        void SetValue(float value);
        
        void SetEnum(Animal enumValue);
        
        Animal GetEnum(int id);
        
        void FuncHasRefArg(std::shared_ptr<int> intRef);
        
        /**
         @brief ClassCのインスタンスを削除します。
         */
        ~ClassC();
    };
    
    class BaseClass
    {
    private:
        static std::mutex mtx;
        static std::unordered_map<void*, std::weak_ptr<BaseClass> > cacheRepo;
        
    public:
        static std::shared_ptr<BaseClass> TryGetFromCache(void* native);
        
    public:
        void* selfPtr = nullptr;
        
    private:
        static void* cbg_BaseClass_Constructor_0();
    
        static int cbg_BaseClass_GetBaseClassField(void* selfPtr);
    
        static void cbg_BaseClass_SetBaseClassField(void* selfPtr, int value);
    
        static void cbg_BaseClass_Release(void* selfPtr);
        
        
    public:
        BaseClass(void* handle);
        
    private:
        
    public:
        BaseClass(bool callCoreConstructor);
        
        int GetBaseClassField();
        
        void SetBaseClassField(int value);
        
        /**
         @brief BaseClassのインスタンスを削除します。
         */
        ~BaseClass();
    };
    
    class DerivedClass : public BaseClass
    {
    private:
        static std::mutex mtx;
        static std::unordered_map<void*, std::weak_ptr<DerivedClass> > cacheRepo;
        
    public:
        static std::shared_ptr<DerivedClass> TryGetFromCache(void* native);
        
    private:
        static void* cbg_DerivedClass_Constructor_0();
    
        static int cbg_DerivedClass_GetBaseClassFieldFromDerivedClass(void* selfPtr);
    
        static void cbg_DerivedClass_Release(void* selfPtr);
        
        
    public:
        DerivedClass(void* handle);
        
    private:
        
    public:
        DerivedClass(bool callCoreConstructor);
        
        int GetBaseClassFieldFromDerivedClass();
        
        /**
         @brief DerivedClassのインスタンスを削除します。
         */
        ~DerivedClass();
    };
    
}
