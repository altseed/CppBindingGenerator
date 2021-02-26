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

namespace CoreSample
{
    [EditorBrowsable(EditorBrowsableState.Never)]
    struct MemoryHandle
    {
        internal IntPtr selfPtr;
    
        internal MemoryHandle(IntPtr p)
        {
            this.selfPtr = p;
        }
    }
    
    /// <summary>
    /// 単純なクラス
    /// </summary>
    [Serializable]
    public partial class SimpleClass : ISerializable, ICacheKeeper<SimpleClass>
    {
        #region unmanaged
        
        [EditorBrowsable(EditorBrowsableState.Never)]
        private Dictionary<IntPtr, WeakReference<SimpleClass>> cacheRepo = new Dictionary<IntPtr, WeakReference<SimpleClass>>();
        
        [EditorBrowsable(EditorBrowsableState.Never)]
        public static  SimpleClass TryGetFromCache(IntPtr native)
        {
            if(native == IntPtr.Zero) return null;
        
            if(cacheRepo.ContainsKey(native))
            {
                SimpleClass cacheRet;
                cacheRepo[native].TryGetTarget(out cacheRet);
                if(cacheRet != null)
                {
                    cbg_SimpleClass_Release(native);
                    return cacheRet;
                }
                else
                {
                    cacheRepo.Remove(native, out _);
                }
            }
        
            var newObject = new SimpleClass(new MemoryHandle(native));
            cacheRepo.Add(native, new WeakReference<SimpleClass>(newObject));
            return newObject;
        }
        
        [EditorBrowsable(EditorBrowsableState.Never)]
        internal IntPtr selfPtr = IntPtr.Zero;
        
        [DllImport("CoreSample")]
        [EditorBrowsable(EditorBrowsableState.Never)]
        private static extern IntPtr cbg_SimpleClass_Constructor0();
        
        [DllImport("CoreSample")]
        [EditorBrowsable(EditorBrowsableState.Never)]
        private static extern void cbg_SimpleClass_Release(IntPtr selfPtr);
        
        #endregion
        
        [EditorBrowsable(EditorBrowsableState.Never)]
        internal SimpleClass(MemoryHandle handle)
        {
            selfPtr = handle.selfPtr;
        }
    }
}