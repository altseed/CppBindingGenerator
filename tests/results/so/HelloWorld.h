
#pragma once

#include <stdio.h>

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

struct StructA
{
    float X;
    float Y;
    float Z;
};

//CreateAndAddSharedPtr

class ClassA
    : public ReferenceObject
{
public:
    void FuncSimple();
    void FuncArgInt(int value);
    void FuncArgFloatBoolStr(float value1, bool value2, const char16_t* value3);
    void FuncArgStruct(const StructA& value1);
    int FuncReturnInt();
    bool FuncReturnBool();
    float FuncReturnFloat();
    StructA FuncReturnStruct();
    const char16_t* FuncReturnString();
};

}