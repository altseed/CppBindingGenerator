using System;
using System.Runtime.InteropServices;

namespace HelloWorld {
    
    [StructLayout(LayoutKind.Sequential)]
    public struct StructA
    {
        public float X;
        public float Y;
        public float Z;
    }

	[StructLayout(LayoutKind.Sequential)]
	public struct ReplaceStructA
	{
		public float X;
		public float Y;
	}
}

