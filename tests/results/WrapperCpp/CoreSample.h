#pragma once

#include <codecvt>
#include <iostream>
#include <locale>
#include <memory>
#include <string>
#include <thread>

namespace CoreSample
{
    class ReferenceObject
    {
    private:
        int m_refCount = 1;

    public:
        ReferenceObject() = default;
        virtual ~ReferenceObject() = default;

        int AddRef()
        {
            return ++m_refCount;
        }

        int Release()
        {
            if(!(--m_refCount)) delete this;
            return m_refCount;
        }
    };

    template <typename T>
    struct ReferenceDeleter
    {
        void operator()(T* ptr)
        {
            if(ptr != nullptr)
            {
                ptr->Release();
                ptr = nullptr;
            }
        }
    };
    
    template <typename T>
    std::shared_ptr<T> CreateAndAddSharedPtr(T* ptr)
    {
		if (ptr == nullptr) return nullptr;
		ptr->AddRef();
		return std::shared_ptr<T>(ptr, ReferenceDeleter<T>());
    }

	template <class T>
	T* AddAndGetSharedPtr(std::shared_ptr<T> sharedPtr)
	{
		T* ptr = sharedPtr.get();
		if (ptr == nullptr) return nullptr;
		ptr->AddRef();
		return ptr;
	}

    class SimpleClass
    {
    public:
		SimpleClass();
		virtual ~SimpleClass();
    };
    
} // namespace CoreSample
