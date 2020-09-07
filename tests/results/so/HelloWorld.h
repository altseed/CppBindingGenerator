
#pragma once

#include <stdio.h>
#include <memory>
#include <string>

namespace HelloWorld
{

	class ReferenceObject
	{
		int ref = 1;

	public:
		ReferenceObject() = default;
		virtual ~ReferenceObject() = default;

		int AddRef()
		{
			ref++;
			return ref;
		}

		int Release()
		{
			ref--;
			auto ret = ref;
			if (ref == 0)
			{
				delete this;
			}
			return ret;
		}
	};

	template <typename T>
	struct ReferenceDeleter
	{
		void operator()(T *p)
		{
			if (p != nullptr)
			{
				p->Release();
				p = nullptr;
			}
		}
	};

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

	enum EnumA
	{
		Mouse,
		Cow,
		Tiger = 3,
	};

	template <class T>
	std::shared_ptr<T> CreateAndAddSharedPtr(T *p)
	{
		if (p == nullptr)
			return nullptr;

		p->AddRef();
		return std::shared_ptr<T>(p, ReferenceDeleter<T>());
	}

	template <class T>
	T *AddAndGetSharedPtr(std::shared_ptr<T> sp)
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
		EnumA enumA_;

	public:
		ClassA();
		virtual ~ClassA();
		void FuncSimple();
		void FuncArgInt(int value);
		void FuncArgFloatBoolStr(float value1, bool value2, const char16_t *value3);
		void FuncArgStruct(StructA *value1);
		void FuncArgClass(std::shared_ptr<ClassB> value1);
		int FuncReturnInt();
		bool FuncReturnBool();
		float FuncReturnFloat();
		StructA FuncReturnStruct();
		const char16_t *FuncReturnString();
		std::shared_ptr<ClassB> FuncReturnClass();

		std::shared_ptr<ClassB> GetBReference() { return nullptr; }

		EnumA GetEnumA() const;
		void SetEnumA(EnumA v);

		static int FuncReturnStatic();
	};

	class ClassB
		: public ReferenceObject
	{
		int value_ = 0;
		EnumA enumValue_ = EnumA::Mouse;

		std::shared_ptr<ClassA> classa_;

	public:
		ClassB();
		virtual ~ClassB();
		int GetValue() { return value_; }
		void SetValue(float value) { value_ = value; }
		EnumA GetEnum(int id) { return EnumA::Cow; }
		void SetEnum(EnumA value) { enumValue_ = value; }

		int GetMyProperty() { return 3; }
		void SetMyProperty(int value) {}
		void SetMyBool(bool value) {}

		std::shared_ptr<ClassA> GetClassProperty() { return classa_; }
		void SetClassProperty(std::shared_ptr<ClassA> value) { classa_ = value; }
	};

	class ClassC : public ReferenceObject
	{
	private:
		float value_;
		EnumA enum_;
		int myProperty_;
		std::u16string stringProperty_;
		bool myBool_;

	public:
		void SetValue(float value) { value_ = value; }

		void SetEnum(EnumA enumA) { enum_ = enumA; }
		EnumA GetEnum(int id) { return enum_; }

		void SetMyProperty(int value) { myProperty_ = value; }
		int GetMyProperty() { return myProperty_; }

		void SetStringProperty(const char16_t *value) { stringProperty_ = value; }
		const char16_t *GetStringProperty() { return stringProperty_.c_str(); }

		void FuncHasRefArg(int32_t *value) { *value = 2; }
		void SetMyBool(bool value) { myBool_ = value; }
	};

	class BaseClass : public ReferenceObject
	{
	protected:
		int baseClassField_;

	public:
		int GetBaseClassField()
		{
			return baseClassField_;
		}
		void SetBaseClassField(int value)
		{
			baseClassField_ = value;
		}
	};

	class DerivedClass : public BaseClass
	{
	public:
		int GetBaseClassFieldFromDerivedClass()
		{
			return baseClassField_;
		}
	};

	class ClassAlias_Cpp
		: public ReferenceObject
	{
	public:
		ClassAlias_Cpp() = default;
		~ClassAlias_Cpp() override = default;

		std::shared_ptr<ClassAlias_Cpp> FuncSimple() { return std::make_shared<ClassAlias_Cpp>(); }
	};

} // namespace HelloWorld