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

            HelloWorld.StructA sa = new HelloWorld.StructA();
            sa.X = 1.0f;
            sa.Y = 2.0f;
            sa.Z = 3.0f;
            a.FuncArgStruct(ref sa);

        }
    }
}