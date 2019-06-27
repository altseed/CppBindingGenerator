
#pragma once

#include <stdio.h>
#include <memory>

namespace HelloWorld
{

class ReferenceObject
{
    int ref = 1;
public:
    ReferenceObject() = default;
    virtual ~ReferenceObject() = default;
    
    int AddRef() { 
        ref++;
        return ref;
     }
    
    int Release()
    {
        ref--;
        auto ret = ref;
        if(ref == 0)
        {
            delete this;
        }
        return ret;
    }
};

template <typename T> struct ReferenceDeleter
{
	void operator()(T* p)
	{
        if(p != nullptr)
        {
            p->Release();
            p = nullptr;
        }
	}
};


struct StructA
{
    float X;
    float Y;
    float Z;
};

enum EnumA
{
	Mouse,
	Cow,
	Tiger = 3,
};

template <class T> 
std::shared_ptr<T> CreateAndAddSharedPtr(T* p)
{
	if (p == nullptr)
		return nullptr;

    p->AddRef();
    return std::shared_ptr<T>(p, ReferenceDeleter<T>());
}

template <class T> 
T* AddAndGetSharedPtr(std::shared_ptr<T> sp)
{
    auto p = sp.get();
	if (p == nullptr)
		return nullptr;

    p->AddRef();
    return p;
}

class ClassA;
class ClassB;

class ClassA
    : public ReferenceObject
{
public:
	ClassA();
	virtual ~ClassA();
    void FuncSimple();
    void FuncArgInt(int value);
    void FuncArgFloatBoolStr(float value1, bool value2, const char16_t* value3);
    void FuncArgStruct(const StructA& value1);
    void FuncArgClass(std::shared_ptr<ClassB> value1);
    int FuncReturnInt();
    bool FuncReturnBool();
    float FuncReturnFloat();
    StructA FuncReturnStruct();
    const char16_t* FuncReturnString();
    std::shared_ptr<ClassB> FuncReturnClass();

	std::shared_ptr<ClassB> GetBReference() { return nullptr; }
};

class ClassB
    : public ReferenceObject
{
    int value_ = 0;
	EnumA enumValue_ = EnumA::Mouse;
public:
	ClassB();
	virtual ~ClassB();
    int GetValue() { return value_; }
    void SetValue(float value) { value_ = value; }
	EnumA GetEnum(int id) { return EnumA::Cow; }
	void SetEnum(EnumA value) { enumValue_ = value; }

	int GetMyProperty() { return 3; }
	void SetMyProperty(int value) { }
	void SetMyBool(bool value) { }
};

}