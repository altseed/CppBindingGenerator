// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
//
//   このファイルは自動生成されました。
//   このファイルへの変更は消失することがあります。
//
//   THIS FILE IS AUTO GENERATED.
//   YOUR COMMITMENT ON THIS FILE WILL BE WIPED. 
//
// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
using System;
using System.ComponentModel;
using System.Collections.Generic;
using System.Collections.Concurrent;
using System.Runtime.InteropServices;
using System.Runtime.Serialization;

namespace HelloWorld
{
    [EditorBrowsable(EditorBrowsableState.Never)]
    struct MemoryHandle
    {
        public IntPtr selfPtr;
        public MemoryHandle(IntPtr p)
        {
            this.selfPtr = p;
        }
    }
    
    /// <summary>
    /// 
    /// </summary>
    public partial class ClassCppD
    {
        #region unmanaged
        
        [EditorBrowsable(EditorBrowsableState.Never)]
        internal IntPtr selfPtr = IntPtr.Zero;
        [DllImport("cplusplus")]
        [EditorBrowsable(EditorBrowsableState.Never)]
        private static extern IntPtr cbg_ClassCppD_Constructor_0();
        
        [DllImport("cplusplus")]
        [EditorBrowsable(EditorBrowsableState.Never)]
        private static extern IntPtr cbg_ClassCppD_FuncReturnClass(IntPtr selfPtr);
        
        [DllImport("cplusplus")]
        [EditorBrowsable(EditorBrowsableState.Never)]
        private static extern void cbg_ClassCppD_Release(IntPtr selfPtr);
        
        #endregion
        
        [EditorBrowsable(EditorBrowsableState.Never)]
        internal ClassCppD(MemoryHandle handle)
        {
            selfPtr = handle.selfPtr;
        }
        
        public ClassCppD()
        {
            selfPtr = cbg_ClassCppD_Constructor_0();
        }
        
        protected ClassCppD(bool calledByDerived)
        {
            // Dummy function.
        }
        
        public HelloWorld.ClassB FuncReturnClass()
        {
            var ret = cbg_ClassCppD_FuncReturnClass(selfPtr);
            return HelloWorld.ClassB.TryGetFromCache(ret);
        }
        
        /// <summary>
        /// <see cref="ClassCppD"/>のインスタンスを削除します。
        /// </summary>
        ~ClassCppD()
        {
            lock (this) 
            {
                if (selfPtr != IntPtr.Zero)
                {
                    cbg_ClassCppD_Release(selfPtr);
                    selfPtr = IntPtr.Zero;
                }
            }
        }
    }
    
}
