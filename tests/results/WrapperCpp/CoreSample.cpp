#include "CoreSample.h"

namespace CoreSample
{
    SimpleClass::SimpleClass()
    {
        auto id = std::this_thread::get_id();
		std::cout << "Create ClassA(C++) in " << id << std::endl;
    }

    SimpleClass::~SimpleClass()
    {
		auto id = std::this_thread::get_id();
		std::cout << "Dispose ClassA(C++) in " << id << std::endl;
    }
    
} // namespace CoreSample
