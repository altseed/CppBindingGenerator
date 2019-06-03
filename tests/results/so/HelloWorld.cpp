#include "HelloWorld.h"

#include <codecvt>
#include <locale>
#include <iostream>

namespace HelloWorld
{

	inline int32_t ConvertUtf16ToUtf8(char* dst, int32_t dst_size, const char16_t* src)
	{
		int32_t cnt = 0;
		const char16_t* wp = src;
		char* cp = dst;

		if (dst_size == 0) return 0;

		dst_size -= 3;

		for (cnt = 0; cnt < dst_size; )
		{
			char16_t wc = *wp++;
			if (wc == 0)
			{
				break;
			}
			if ((wc & ~0x7f) == 0)
			{
				*cp++ = wc & 0x7f;
				cnt += 1;
			}
			else if ((wc & ~0x7ff) == 0)
			{
				*cp++ = ((wc >> 6) & 0x1f) | 0xc0;
				*cp++ = ((wc) & 0x3f) | 0x80;
				cnt += 2;
			}
			else {
				*cp++ = ((wc >> 12) & 0xf) | 0xe0;
				*cp++ = ((wc >> 6) & 0x3f) | 0x80;
				*cp++ = ((wc) & 0x3f) | 0x80;
				cnt += 3;
			}
		}
		*cp = '\0';
		return cnt;
	}

void ClassA::FuncSimple()
{
    printf("FuncSimple\n");
}

void ClassA::FuncArgInt(int value)
{
    printf("FuncArgInt %d\n", value);
}

void ClassA::FuncArgFloatBoolStr(float value1, bool value2, const char16_t* value3)
{
    printf("FuncArgFloatBoolStr %f %d\n", value1, (int)value2);

	char temp[200];
	ConvertUtf16ToUtf8(temp, 200, value3);
    std::cout << temp << std::endl;
}

void ClassA::FuncArgStruct(const StructA& value1)
{
	std::cout << value1.X << ", " << value1.Y << ", " << value1.Z << std::endl;
}

int ClassA::FuncReturnInt()
{
    return 100;
}

bool ClassA::FuncReturnBool()
{
    return true;
}

float ClassA::FuncReturnFloat()
{
    return 2.1f;
}

StructA ClassA::FuncReturnStruct()
{
	StructA ret;
	ret.X = 2.0f;
	ret.Y = 1.0f;
	ret.Z = 3.0f;
	return ret;
}
}