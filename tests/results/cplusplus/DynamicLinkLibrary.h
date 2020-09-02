#pragma once

#include <atomic>
#include <cassert>
#include <string>

#ifdef _WIN32
#include <Windows.h>
#else
#include <dlfcn.h>
#include <cstddef>
#endif

#ifdef _WIN32
#define	_STDCALL	__stdcall
#else
#define	_STDCALL
#endif

#ifdef _WIN32
#define _EXPORT __declspec(dllexport)
#else
#define _EXPORT
#endif

inline std::string ConvertSharedObjectPath(std::string path)
{
#ifndef _WIN32
	path = "lib" + path;
#endif

#ifdef _WIN32
	path += ".dll";
#elif defined(__APPLE__)
	path += ".dylib";
#else
	path += ".so";
#endif
	return path;
}

class DynamicLinkLibrary
{
private:
	mutable std::atomic<int32_t> reference_;

#if _WIN32
	HMODULE dll_;
#else
	void* dll_ = nullptr;
#endif

public:
	DynamicLinkLibrary() : reference_(1)
	{
		dll_ = nullptr;
	}

	~DynamicLinkLibrary()
	{
		Reset();
	}

	void Reset()
	{
		if (dll_ != nullptr)
		{
	#if _WIN32
			::FreeLibrary(dll_);
	#else
			dlclose(dll_);
	#endif
			dll_ = nullptr;
		}
	}
	
	bool Load(const char* path)
	{
		Reset();

	#if _WIN32
		dll_ = ::LoadLibraryA(path);
	#else
		dll_ = dlopen(path, RTLD_LAZY);
	#endif
		return dll_ != nullptr;
	}
	
	template <typename T> T GetProc(const char* name)
	{
	#if _WIN32
		void* pProc = ::GetProcAddress(dll_, name);
	#else
		void* pProc = dlsym(dll_, name);
	#endif
		if (pProc == NULL)
		{
			return nullptr;
		}
		return (T)(pProc);
	}

	int AddRef()
	{
		std::atomic_fetch_add_explicit(&reference_, 1, std::memory_order_consume);
		return reference_;
	}

	int GetRef()
	{
		return reference_;
	}

	int Release()
	{
		assert(reference_ > 0);
		bool destroy = std::atomic_fetch_sub_explicit(&reference_, 1, std::memory_order_consume) == 1;
		if (destroy)
		{
			delete this;
			return 0;
		}

		return reference_;
	}
};
