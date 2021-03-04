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
        
        [EditorBrowsable(EditorBrowsableState.Never)]
        private Dictionary<IntPtr, WeakReference<SimpleClass>> cacheConstructor0 = new Dictionary<IntPtr, WeakReference<SimpleClass>>();
        public SimpleClass()
        {
        }
        
        protected SimpleClass(bool calledByDerived)
        {
        }
        
        #region ISerialiable
        
        #region SerializeName
        
        #endregion
        
        /// <summary>
        /// シリアライズされたデータをもとに<see cref="SimpleClass"/>のインスタンスを生成します。
        /// </summary>
        /// <param name="info">シリアライズされたデータを格納するオブジェクト</param>
        /// <param name="context">送信元の情報</param>
        [EditorBrowsable(EditorBrowsableState.Never)]
        protected SimpleClass(SerializationInfo info, StreamingContext context) : this(new MemoryHandle(IntPtr.Zero))
        {
            var ptr = Call_GetPtr(info);
            
            if (ptr == IntPtr.Zero) throw new SerializationException("インスタンス生成に失敗しました");
            CacheHelper.CacheHandlingOnDeserialization(this, ptr);
            
            OnDeserialize_Constructor(info, context);
        }
        /// <summary>
        /// シリアライズするデータを設定します。
        /// </summary>
        /// <param name="info">シリアライズされるデータを格納するオブジェクト</param>
        /// <param name="context">送信先の情報</param>
        [EditorBrowsable(EditorBrowsableState.Never)]
        protected override void GetObjectData(SerializationInfo info, StreamingContext context)
        {
            if (info == null) throw new ArgumentNullException(nameof(info), "引数がnullです");
            
            
            OnGetObjectData(info, context);
        }
        [EditorBrowsable(EditorBrowsableState.Never)]
        void ISerializable.GetObjectData(SerializationInfo info, StreamingContext context) => GetObjectData(info, context);
        
        /// <summary>
        /// <see cref="GetObjectData(SerializationInfo, StreamingContext)"/>内で実行されます。
        /// </summary>
        /// <param name="info">シリアライズされるデータを格納するオブジェクト</param>
        /// <param name="context">送信先の情報</param>
        [EditorBrowsable(EditorBrowsableState.Never)]
        partial void OnGetObjectData(SerializationInfo info, StreamingContext context);
        
        /// <summary>
        /// <see cref="SimpleClass(SerializationInfo, StreamingContext)"/>内で実行します。
        /// </summary>
        /// <param name="info">シリアライズされたデータを格納するオブジェクト</param>
        /// <param name="context">送信元の情報</param>
        [EditorBrowsable(EditorBrowsableState.Never)]
        partial void OnDeserialize_Constructor(SerializationInfo info, StreamingContext context);
        
        /// <summary>
        /// <see cref="SimpleClass(SerializationInfo, StreamingContext)"/>内で呼び出される
        /// デシリアライズ時にselfPtrを取得する操作をここに必ず書くこと
        /// </summary>
        /// <param name="ptr">selfPtrとなる値 初期値である<see cref="IntPtr.Zero"/>のままだと<see cref="SerializationException"/>がスローされる</param>
        /// <param name="info">シリアライズされたデータを格納するオブジェクト</param>
        [EditorBrowsable(EditorBrowsableState.Never)]
        partial void Deserialize_GetPtr(ref IntPtr ptr, SerializationInfo info);
        
        /// <summary>
        /// 呼び出し禁止
        /// </summary>
        [EditorBrowsable(EditorBrowsableState.Never)]
        protected private virtual IntPtr Call_GetPtr(SerializationInfo info)
        {
            var ptr = IntPtr.Zero;
            Deserialize_GetPtr(ref ptr, info);
            return ptr;
        }
        #region ICacheKeeper
        
        [EditorBrowsable(EditorBrowsableState.Never)]
        IDictionary<IntPtr, WeakReference<SimpleClass>> ICacheKeeper<SimpleClass>.CacheRepo => cacheRepo;
        
        [EditorBrowsable(EditorBrowsableState.Never)]
        IntPtr ICacheKeeper<SimpleClass>.Self
        {
            get => selfPtr;
            set
            {
                selfPtr = value;
            }
        }
        [EditorBrowsable(EditorBrowsableState.Never)]
        void ICacheKeeper<SimpleClass>.Release(IntPtr native) => cbg_SimpleClass_Release(native);
        
        #endregion
        
        #endregion
        
        /// <summary>
        /// <see cref="SimpleClass"/>のインスタンスを削除します。
        /// </summary>
        ~SimpleClass()
        {
            lock (this) 
            {
                if (selfPtr != IntPtr.Zero)
                {
                    cbg_SimpleClass_Release(selfPtr);
                    selfPtr = IntPtr.Zero;
                }
            }
        }
    }
}