using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Test
{
    class Program
    {
        [STAThread]
        static void Main(string[] args)
        {
            var a = new HelloWorld.ClassA();
            a.FuncSimple();
            a.FuncArgInt(2);
            a.FuncArgFloatBoolStr(2.2f, true, "hello");

            // static test
            if (HelloWorld.ClassA.FuncReturnStatic() != 1) throw new Exception();

            a.EnumA = HelloWorld.EnumA.Tiger;
            if(a.EnumA != HelloWorld.EnumA.Tiger) throw new Exception();

            HelloWorld.StructA sa = new HelloWorld.StructA();
            sa.X = 1.0f;
            sa.Y = 2.0f;
            sa.Z = 3.0f;
            a.FuncArgStruct(ref sa);

            HelloWorld.ClassB cb = new HelloWorld.ClassB();
            cb.SetValue(100);
            a.FuncArgClass(cb);

            var retBool = a.FuncReturnBool();
            Console.WriteLine(retBool);

            var retStruct = a.FuncReturnStruct();
            Console.WriteLine(string.Format("{0},{1},{2}", retStruct.X, retStruct.Y, retStruct.Z));

            var retSrring = a.FuncReturnString();
            Console.WriteLine(retSrring);

            var retClass = a.FuncReturnClass();
            retClass.SetValue(101);
            a.FuncArgClass(retClass);


            Console.WriteLine("Inheritance Test:");
            var derived = new HelloWorld.DerivedClass();
            var asBase = derived as HelloWorld.BaseClass;
            asBase.SetBaseClassField(12345);
            Console.WriteLine($"As Base Value:{asBase.GetBaseClassField()}");
            Console.WriteLine($"Derived Value:{derived.GetBaseClassFieldFromDerivedClass()}");

        }
    }
}