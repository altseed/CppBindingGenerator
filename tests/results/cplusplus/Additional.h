#pragma once

namespace HelloWorldA
{
	struct StructA_C;
	struct StructA
	{
	public:
		float X;
		float Y;
		float Z;

		StructA();
		StructA(float _x, float _y, float _z);

		operator StructA_C() const;
	};

	struct StructA_C
	{
	public:
		float X;
		float Y;
		float Z;

		operator StructA() const;
	};
}