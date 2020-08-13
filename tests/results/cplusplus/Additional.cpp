#include "Additional.h"

namespace HelloWorldA
{
    StructA::StructA() {
        X = 0;
        Y = 0;
        Z = 0;
    }

    StructA::StructA(float _x, float _y, float _z) {
        X = _x;
        Y = _y;
        Z = _z;
    }

    StructA::operator StructA_C() const { return StructA_C{ X, Y, Z }; }

    StructA_C::operator StructA() const { return StructA(X, Y, Z); } 
}
