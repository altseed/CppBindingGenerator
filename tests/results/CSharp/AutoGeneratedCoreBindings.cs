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
    [Serializable]
    public enum Animal : int
    {
        Mosue,
        Cow,
        Tiger = 3,
    }
    
    /// <summary>
    /// 
    /// </summary>
    public partial class ClassAlias_CS
    {
        #region unmanaged
        
        [EditorBrowsable(EditorBrowsableState.Never)]
        internal IntPtr selfPtr = IntPtr.Zero;
        [DllImport("CoreLib")]
        [EditorBrowsable(EditorBrowsableState.Never)]
        private static extern IntPtr cbg_ClassAlias_Cpp_Constructor_0();
        
        [DllImport("CoreLib")]
        [EditorBrowsable(EditorBrowsableState.Never)]
        private static extern IntPtr cbg_ClassAlias_Cpp_FuncSimple(IntPtr selfPtr);
        
        [DllImport("CoreLib")]
        [EditorBrowsable(EditorBrowsableState.Never)]
        private static extern void cbg_ClassAlias_Cpp_Release(IntPtr selfPtr);
        
        #endregion
        
        [EditorBrowsable(EditorBrowsableState.Never)]
        internal ClassAlias_CS(MemoryHandle handle)
        {
            selfPtr = handle.selfPtr;
        }
        
        public ClassAlias_CS()
        {
            selfPtr = cbg_ClassAlias_Cpp_Constructor_0();
        }
        
        protected ClassAlias_CS(bool calledByDerived)
        {
            // Dummy function.
        }
        
        public ClassAlias_CS FuncSimple()
        {
            var ret = cbg_ClassAlias_Cpp_FuncSimple(selfPtr);
            return ret != null ? new ClassAlias_CS(new MemoryHandle(ret)) : null;
        }
        
        /// <summary>
        /// <see cref="ClassAlias_CS"/>のインスタンスを削除します。
        /// </summary>
        ~ClassAlias_CS()
        {
            lock (this) 
            {
                if (selfPtr != IntPtr.Zero)
                {
                    cbg_ClassAlias_Cpp_Release(selfPtr);
                    selfPtr = IntPtr.Zero;
                }
            }
        }
    }
    
    /// <summary>
    /// ClassA-Desc
    /// </summary>
    public partial class ClassA
    {
        #region unmanaged
        
        [EditorBrowsable(EditorBrowsableState.Never)]
        internal IntPtr selfPtr = IntPtr.Zero;
        [DllImport("CoreLib")]
        [EditorBrowsable(EditorBrowsableState.Never)]
        private static extern IntPtr cbg_ClassA_Constructor_0();
        
        [DllImport("CoreLib")]
        [EditorBrowsable(EditorBrowsableState.Never)]
        private static extern void cbg_ClassA_FuncSimple(IntPtr selfPtr);
        
        [DllImport("CoreLib")]
        [EditorBrowsable(EditorBrowsableState.Never)]
        private static extern void cbg_ClassA_FuncArgInt(IntPtr selfPtr, int value);
        
        [DllImport("CoreLib")]
        [EditorBrowsable(EditorBrowsableState.Never)]
        private static extern void cbg_ClassA_FuncArgFloatBoolStr(IntPtr selfPtr, float value1, [MarshalAs(UnmanagedType.Bool)] bool value2, [MarshalAs(UnmanagedType.LPWStr)] string value3);
        
        [DllImport("CoreLib")]
        [EditorBrowsable(EditorBrowsableState.Never)]
        private static extern void cbg_ClassA_FuncArgStruct(IntPtr selfPtr, [In, Out] ref StructA value1);
        
        [DllImport("CoreLib")]
        [EditorBrowsable(EditorBrowsableState.Never)]
        private static extern void cbg_ClassA_FuncArgClass(IntPtr selfPtr, IntPtr value1);
        
        [DllImport("CoreLib")]
        [EditorBrowsable(EditorBrowsableState.Never)]
        private static extern int cbg_ClassA_FuncReturnInt(IntPtr selfPtr);
        
        [DllImport("CoreLib")]
        [EditorBrowsable(EditorBrowsableState.Never)]
        [return: MarshalAs(UnmanagedType.U1)]
        private static extern bool cbg_ClassA_FuncReturnBool(IntPtr selfPtr);
        
        [DllImport("CoreLib")]
        [EditorBrowsable(EditorBrowsableState.Never)]
        private static extern float cbg_ClassA_FuncReturnFloat(IntPtr selfPtr);
        
        [DllImport("CoreLib")]
        [EditorBrowsable(EditorBrowsableState.Never)]
        private static extern StructA cbg_ClassA_FuncReturnStruct(IntPtr selfPtr);
        
        [DllImport("CoreLib")]
        [EditorBrowsable(EditorBrowsableState.Never)]
        private static extern IntPtr cbg_ClassA_FuncReturnClass(IntPtr selfPtr);
        
        [DllImport("CoreLib")]
        [EditorBrowsable(EditorBrowsableState.Never)]
        private static extern IntPtr cbg_ClassA_FuncReturnString(IntPtr selfPtr);
        
        [DllImport("CoreLib")]
        [EditorBrowsable(EditorBrowsableState.Never)]
        private static extern int cbg_ClassA_FuncReturnStatic();
        
        [DllImport("CoreLib")]
        [EditorBrowsable(EditorBrowsableState.Never)]
        private static extern IntPtr cbg_ClassA_GetBReference(IntPtr selfPtr);
        
        
        [DllImport("CoreLib")]
        [EditorBrowsable(EditorBrowsableState.Never)]
        private static extern int cbg_ClassA_GetEnumA(IntPtr selfPtr);
        [DllImport("CoreLib")]
        [EditorBrowsable(EditorBrowsableState.Never)]
        private static extern void cbg_ClassA_SetEnumA(IntPtr selfPtr, int value);
        
        
        [DllImport("CoreLib")]
        [EditorBrowsable(EditorBrowsableState.Never)]
        private static extern void cbg_ClassA_Release(IntPtr selfPtr);
        
        #endregion
        
        [EditorBrowsable(EditorBrowsableState.Never)]
        internal ClassA(MemoryHandle handle)
        {
            selfPtr = handle.selfPtr;
        }
        
        public ClassB BReference
        {
            get
            {
                var ret = cbg_ClassA_GetBReference(selfPtr);
                return ClassB.TryGetFromCache(ret);
            }
        }
        
        public Animal EnumA
        {
            get
            {
                if (_EnumA != null)
                {
                    return _EnumA.Value;
                }
                var ret = cbg_ClassA_GetEnumA(selfPtr);
                return (Animal)ret;
            }
            set
            {
                _EnumA = value;
                cbg_ClassA_SetEnumA(selfPtr, (int)value);
            }
        }
        private Animal? _EnumA;
        
        public ClassA()
        {
            selfPtr = cbg_ClassA_Constructor_0();
        }
        
        protected ClassA(bool calledByDerived)
        {
            // Dummy function.
        }
        
        public void FuncSimple()
        {
            cbg_ClassA_FuncSimple(selfPtr);
        }
        
        public void FuncArgInt(int value)
        {
            cbg_ClassA_FuncArgInt(selfPtr, value);
        }
        
        public void FuncArgFloatBoolStr(float value1, bool value2, string value3)
        {
            cbg_ClassA_FuncArgFloatBoolStr(selfPtr, value1, value2, value3);
        }
        
        /// <summary>
        /// Processes a structA.
        /// </summary>
        public void FuncArgStruct(ref StructA value1)
        {
            cbg_ClassA_FuncArgStruct(selfPtr, ref value1);
        }
        
        public void FuncArgClass(ClassB value1)
        {
            cbg_ClassA_FuncArgClass(selfPtr, value1 != null ? value1.selfPtr : IntPtr.Zero);
        }
        
        /// <summary>
        /// Returns some integer.
        /// </summary>
        public int FuncReturnInt()
        {
            var ret = cbg_ClassA_FuncReturnInt(selfPtr);
            return ret;
        }
        
        public bool FuncReturnBool()
        {
            var ret = cbg_ClassA_FuncReturnBool(selfPtr);
            return ret;
        }
        
        public float FuncReturnFloat()
        {
            var ret = cbg_ClassA_FuncReturnFloat(selfPtr);
            return ret;
        }
        
        public StructA FuncReturnStruct()
        {
            var ret = cbg_ClassA_FuncReturnStruct(selfPtr);
            return ret;
        }
        
        public ClassB FuncReturnClass()
        {
            var ret = cbg_ClassA_FuncReturnClass(selfPtr);
            return ClassB.TryGetFromCache(ret);
        }
        
        public string FuncReturnString()
        {
            var ret = cbg_ClassA_FuncReturnString(selfPtr);
            return System.Runtime.InteropServices.Marshal.PtrToStringUni(ret);
        }
        
        public static int FuncReturnStatic()
        {
            var ret = cbg_ClassA_FuncReturnStatic();
            return ret;
        }
        
        /// <summary>
        /// <see cref="ClassA"/>のインスタンスを削除します。
        /// </summary>
        ~ClassA()
        {
            lock (this) 
            {
                if (selfPtr != IntPtr.Zero)
                {
                    cbg_ClassA_Release(selfPtr);
                    selfPtr = IntPtr.Zero;
                }
            }
        }
    }
    
    /// <summary>
    /// 
    /// </summary>
    public partial class ClassB
    {
        #region unmanaged
        
        [EditorBrowsable(EditorBrowsableState.Never)]
        private static Dictionary<IntPtr, WeakReference<ClassB>> cacheRepo = new Dictionary<IntPtr, WeakReference<ClassB>>();
        
        [EditorBrowsable(EditorBrowsableState.Never)]
        public static  ClassB TryGetFromCache(IntPtr native)
        {
            if(native == IntPtr.Zero) return null;
        
            if(cacheRepo.ContainsKey(native))
            {
                ClassB cacheRet;
                cacheRepo[native].TryGetTarget(out cacheRet);
                if(cacheRet != null)
                {
                    cbg_ClassB_Release(native);
                    return cacheRet;
                }
                else
                {
                    cacheRepo.Remove(native);
                }
            }
        
            var newObject = new ClassB(new MemoryHandle(native));
            cacheRepo[native] = new WeakReference<ClassB>(newObject);
            return newObject;
        }
        
        [EditorBrowsable(EditorBrowsableState.Never)]
        internal IntPtr selfPtr = IntPtr.Zero;
        [DllImport("CoreLib")]
        [EditorBrowsable(EditorBrowsableState.Never)]
        private static extern IntPtr cbg_ClassB_Constructor_0();
        
        [DllImport("CoreLib")]
        [EditorBrowsable(EditorBrowsableState.Never)]
        private static extern void cbg_ClassB_SetValue(IntPtr selfPtr, float value);
        
        [DllImport("CoreLib")]
        [EditorBrowsable(EditorBrowsableState.Never)]
        private static extern void cbg_ClassB_SetEnum(IntPtr selfPtr, int enumValue);
        
        [DllImport("CoreLib")]
        [EditorBrowsable(EditorBrowsableState.Never)]
        private static extern int cbg_ClassB_GetEnum(IntPtr selfPtr, int id);
        
        [DllImport("CoreLib")]
        [EditorBrowsable(EditorBrowsableState.Never)]
        private static extern int cbg_ClassB_GetMyProperty(IntPtr selfPtr);
        [DllImport("CoreLib")]
        [EditorBrowsable(EditorBrowsableState.Never)]
        private static extern void cbg_ClassB_SetMyProperty(IntPtr selfPtr, int value);
        
        
        [DllImport("CoreLib")]
        [EditorBrowsable(EditorBrowsableState.Never)]
        private static extern void cbg_ClassB_Release(IntPtr selfPtr);
        
        #endregion
        
        [EditorBrowsable(EditorBrowsableState.Never)]
        internal ClassB(MemoryHandle handle)
        {
            selfPtr = handle.selfPtr;
        }
        
        public int MyProperty
        {
            get
            {
                if (_MyProperty != null)
                {
                    return _MyProperty.Value;
                }
                var ret = cbg_ClassB_GetMyProperty(selfPtr);
                return ret;
            }
            set
            {
                _MyProperty = value;
                cbg_ClassB_SetMyProperty(selfPtr, value);
            }
        }
        private int? _MyProperty;
        
        public ClassB()
        {
            selfPtr = cbg_ClassB_Constructor_0();
        }
        
        protected ClassB(bool calledByDerived)
        {
            // Dummy function.
        }
        
        public void SetValue(float value)
        {
            cbg_ClassB_SetValue(selfPtr, value);
        }
        
        public void SetEnum(Animal enumValue)
        {
            cbg_ClassB_SetEnum(selfPtr, (int)enumValue);
        }
        
        public Animal GetEnum(int id)
        {
            var ret = cbg_ClassB_GetEnum(selfPtr, id);
            return (Animal)ret;
        }
        
        /// <summary>
        /// <see cref="ClassB"/>のインスタンスを削除します。
        /// </summary>
        ~ClassB()
        {
            lock (this) 
            {
                if (selfPtr != IntPtr.Zero)
                {
                    cbg_ClassB_Release(selfPtr);
                    selfPtr = IntPtr.Zero;
                }
            }
        }
    }
    
    /// <summary>
    /// 
    /// </summary>
    public partial class ClassC
    {
        #region unmanaged
        
        [EditorBrowsable(EditorBrowsableState.Never)]
        private static ConcurrentDictionary<IntPtr, WeakReference<ClassC>> cacheRepo = new ConcurrentDictionary<IntPtr, WeakReference<ClassC>>();
        
        [EditorBrowsable(EditorBrowsableState.Never)]
                internal static  ClassC TryGetFromCache(IntPtr native)
        {
            if(native == IntPtr.Zero) return null;
        
            if(cacheRepo.ContainsKey(native))
            {
                ClassC cacheRet;
                cacheRepo[native].TryGetTarget(out cacheRet);
                if(cacheRet != null)
                {
                    cbg_ClassC_Release(native);
                    return cacheRet;
                }
                else
                {
                    cacheRepo.TryRemove(native, out _);
                }
            }
        
            var newObject = new ClassC(new MemoryHandle(native));
            cacheRepo.TryAdd(native, new WeakReference<ClassC>(newObject));
            return newObject;
        }
        
        [EditorBrowsable(EditorBrowsableState.Never)]
        internal IntPtr selfPtr = IntPtr.Zero;
        [DllImport("CoreLib")]
        [EditorBrowsable(EditorBrowsableState.Never)]
        private static extern IntPtr cbg_ClassC_Constructor_0();
        
        [DllImport("CoreLib")]
        [EditorBrowsable(EditorBrowsableState.Never)]
        private static extern void cbg_ClassC_SetValue(IntPtr selfPtr, float value);
        
        [DllImport("CoreLib")]
        [EditorBrowsable(EditorBrowsableState.Never)]
        private static extern void cbg_ClassC_SetEnum(IntPtr selfPtr, int enumValue);
        
        [DllImport("CoreLib")]
        [EditorBrowsable(EditorBrowsableState.Never)]
        private static extern int cbg_ClassC_GetEnum(IntPtr selfPtr, int id);
        
        [DllImport("CoreLib")]
        [EditorBrowsable(EditorBrowsableState.Never)]
        private static extern void cbg_ClassC_FuncHasRefArg(IntPtr selfPtr, [In, Out] ref int intRef);
        
        [DllImport("CoreLib")]
        [EditorBrowsable(EditorBrowsableState.Never)]
        private static extern int cbg_ClassC_GetMyProperty(IntPtr selfPtr);
        [DllImport("CoreLib")]
        [EditorBrowsable(EditorBrowsableState.Never)]
        private static extern void cbg_ClassC_SetMyProperty(IntPtr selfPtr, int value);
        
        
        [DllImport("CoreLib")]
        [EditorBrowsable(EditorBrowsableState.Never)]
        private static extern IntPtr cbg_ClassC_GetStringProperty(IntPtr selfPtr);
        [DllImport("CoreLib")]
        [EditorBrowsable(EditorBrowsableState.Never)]
        private static extern void cbg_ClassC_SetStringProperty(IntPtr selfPtr, [MarshalAs(UnmanagedType.LPWStr)] string value);
        
        
        
        
        [DllImport("CoreLib")]
        [EditorBrowsable(EditorBrowsableState.Never)]
        private static extern void cbg_ClassC_SetMyBool(IntPtr selfPtr, [MarshalAs(UnmanagedType.Bool)] bool value);
        
        
        [DllImport("CoreLib")]
        [EditorBrowsable(EditorBrowsableState.Never)]
        private static extern void cbg_ClassC_Release(IntPtr selfPtr);
        
        #endregion
        
        [EditorBrowsable(EditorBrowsableState.Never)]
        internal ClassC(MemoryHandle handle)
        {
            selfPtr = handle.selfPtr;
        }
        
        public int MyProperty
        {
            get
            {
                if (_MyProperty != null)
                {
                    return _MyProperty.Value;
                }
                var ret = cbg_ClassC_GetMyProperty(selfPtr);
                return ret;
            }
            set
            {
                _MyProperty = value;
                cbg_ClassC_SetMyProperty(selfPtr, value);
            }
        }
        private int? _MyProperty;
        
        public string StringProperty
        {
            get
            {
                if (_StringProperty != null)
                {
                    return _StringProperty;
                }
                var ret = cbg_ClassC_GetStringProperty(selfPtr);
                return System.Runtime.InteropServices.Marshal.PtrToStringUni(ret);
            }
            set
            {
                _StringProperty = value;
                cbg_ClassC_SetStringProperty(selfPtr, value);
            }
        }
        private string _StringProperty;
        
        
        public bool MyBool
        {
            set
            {
                cbg_ClassC_SetMyBool(selfPtr, value);
            }
        }
        
        public ClassC()
        {
            selfPtr = cbg_ClassC_Constructor_0();
        }
        
        protected ClassC(bool calledByDerived)
        {
            // Dummy function.
        }
        
        public void SetValue(float value)
        {
            cbg_ClassC_SetValue(selfPtr, value);
        }
        
        public void SetEnum(Animal enumValue)
        {
            cbg_ClassC_SetEnum(selfPtr, (int)enumValue);
        }
        
        public Animal GetEnum(int id)
        {
            var ret = cbg_ClassC_GetEnum(selfPtr, id);
            return (Animal)ret;
        }
        
        public void FuncHasRefArg(ref int intRef)
        {
            cbg_ClassC_FuncHasRefArg(selfPtr, ref intRef);
        }
        
        /// <summary>
        /// <see cref="ClassC"/>のインスタンスを削除します。
        /// </summary>
        ~ClassC()
        {
            lock (this) 
            {
                if (selfPtr != IntPtr.Zero)
                {
                    cbg_ClassC_Release(selfPtr);
                    selfPtr = IntPtr.Zero;
                }
            }
        }
    }
    
    /// <summary>
    /// 
    /// </summary>
    public partial class BaseClass
    {
        #region unmanaged
        
        [EditorBrowsable(EditorBrowsableState.Never)]
        internal IntPtr selfPtr = IntPtr.Zero;
        [DllImport("CoreLib")]
        [EditorBrowsable(EditorBrowsableState.Never)]
        private static extern IntPtr cbg_BaseClass_Constructor_0();
        
        [DllImport("CoreLib")]
        [EditorBrowsable(EditorBrowsableState.Never)]
        private static extern int cbg_BaseClass_GetBaseClassField(IntPtr selfPtr);
        
        [DllImport("CoreLib")]
        [EditorBrowsable(EditorBrowsableState.Never)]
        private static extern void cbg_BaseClass_SetBaseClassField(IntPtr selfPtr, int value);
        
        [DllImport("CoreLib")]
        [EditorBrowsable(EditorBrowsableState.Never)]
        private static extern void cbg_BaseClass_Release(IntPtr selfPtr);
        
        #endregion
        
        [EditorBrowsable(EditorBrowsableState.Never)]
        internal BaseClass(MemoryHandle handle)
        {
            selfPtr = handle.selfPtr;
        }
        
        public BaseClass()
        {
            selfPtr = cbg_BaseClass_Constructor_0();
        }
        
        protected BaseClass(bool calledByDerived)
        {
            // Dummy function.
        }
        
        public int GetBaseClassField()
        {
            var ret = cbg_BaseClass_GetBaseClassField(selfPtr);
            return ret;
        }
        
        public void SetBaseClassField(int value)
        {
            cbg_BaseClass_SetBaseClassField(selfPtr, value);
        }
        
        /// <summary>
        /// <see cref="BaseClass"/>のインスタンスを削除します。
        /// </summary>
        ~BaseClass()
        {
            lock (this) 
            {
                if (selfPtr != IntPtr.Zero)
                {
                    cbg_BaseClass_Release(selfPtr);
                    selfPtr = IntPtr.Zero;
                }
            }
        }
    }
    
    /// <summary>
    /// 
    /// </summary>
    public partial class DerivedClass : BaseClass
    {
        #region unmanaged
        
        [DllImport("CoreLib")]
        [EditorBrowsable(EditorBrowsableState.Never)]
        private static extern IntPtr cbg_DerivedClass_Constructor_0();
        
        [DllImport("CoreLib")]
        [EditorBrowsable(EditorBrowsableState.Never)]
        private static extern int cbg_DerivedClass_GetBaseClassFieldFromDerivedClass(IntPtr selfPtr);
        
        [DllImport("CoreLib")]
        [EditorBrowsable(EditorBrowsableState.Never)]
        private static extern void cbg_DerivedClass_Release(IntPtr selfPtr);
        
        #endregion
        
        [EditorBrowsable(EditorBrowsableState.Never)]
        internal DerivedClass(MemoryHandle handle) : base(handle)
        {
            selfPtr = handle.selfPtr;
        }
        
        public DerivedClass() : base(true)
        {
            selfPtr = cbg_DerivedClass_Constructor_0();
        }
        
        protected DerivedClass(bool calledByDerived) : base(calledByDerived)
        {
            // Dummy function.
        }
        
        public int GetBaseClassFieldFromDerivedClass()
        {
            var ret = cbg_DerivedClass_GetBaseClassFieldFromDerivedClass(selfPtr);
            return ret;
        }
        
        /// <summary>
        /// <see cref="DerivedClass"/>のインスタンスを削除します。
        /// </summary>
        ~DerivedClass()
        {
            lock (this) 
            {
                if (selfPtr != IntPtr.Zero)
                {
                    cbg_DerivedClass_Release(selfPtr);
                    selfPtr = IntPtr.Zero;
                }
            }
        }
    }
    
}
