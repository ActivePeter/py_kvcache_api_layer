# """
# Rust backend implementation for the KV Cache API layer.

# This module provides a wrapper around a Rust-based KV store implementation
# using a HashMap for storage, implemented with PyO3 bindings.
# """

# from typing import Union, Optional, Any
# from ..api import KVCacheStore
# from ..exceptions import StoreInitializationError, StorageError

# try:
#     import kvcache_rust
#     RustKVStore = kvcache_rust.KVStore
#     RustStoreConfig = kvcache_rust.StoreConfig
# except ImportError:
#     RustKVStore = None
#     RustStoreConfig = None


# class RustStore(KVCacheStore):
#     """Rust implementation of the KV Cache Store interface using HashMap."""
    
#     def __init__(self):
#         """Initialize the Rust store wrapper."""
#         if RustKVStore is None:
#             raise ImportError("Rust KV store is not available. Please install kvcache-rust module.")
        
#         self._store = RustKVStore()
#         self._initialized = False
    
#     def setup(self, 
#               local_hostname: str,
#               metadata_server: str, 
#               global_segment_size: int,
#               local_buffer_size: int,
#               protocol: str = "tcp",
#               device_name: str = "lo",
#               master_server_address: Optional[str] = None) -> int:
#         """
#         Initialize and setup the distributed store.
        
#         Args:
#             local_hostname: The local hostname
#             metadata_server: Address of the metadata server
#             global_segment_size: Size of global segments in bytes
#             local_buffer_size: Size of local buffer in bytes  
#             protocol: Network protocol to use (tcp, udp, etc.)
#             device_name: Network device name
#             master_server_address: Address of the master server
            
#         Returns:
#             0 on success, non-zero error code on failure
#         """
#         try:
#             config = RustStoreConfig(
#                 local_hostname=local_hostname,
#                 metadata_server=metadata_server,
#                 global_segment_size=global_segment_size,
#                 local_buffer_size=local_buffer_size,
#                 protocol=protocol,
#                 device_name=device_name,
#                 master_server_address=master_server_address
#             )
            
#             retcode = self._store.setup(config)
            
#             if retcode == 0:
#                 self._initialized = True
            
#             return retcode
            
#         except Exception as e:
#             raise StoreInitializationError(f"Failed to setup Rust store: {e}")
    
#     def put(self, key: str, *values: Union[bytes, bytearray]) -> int:
#         """
#         Store a key-value pair with single or multiple data parts.
        
#         Args:
#             key: The key to store
#             *values: One or more values to store as bytes
            
#         Returns:
#             0 on success, non-zero error code on failure
#         """
#         if not self._initialized:
#             raise StorageError("Store not initialized. Call setup() first.")
        
#         if not values:
#             raise ValueError("At least one value must be provided")
        
#         try:
#             if len(values) == 1:
#                 # Single value: use regular put
#                 return self._store.put(key, values[0])
#             else:
#                 # Multiple values: use put_parts
#                 return self._store.put_parts(key, list(values))
#         except Exception as e:
#             raise StorageError(f"Failed to put key '{key}': {e}")
    
#     def get(self, key: str) -> bytes:
#         """
#         Retrieve a value by key.
        
#         Args:
#             key: The key to retrieve
            
#         Returns:
#             The value as bytes, or empty bytes if key not found
#         """
#         if not self._initialized:
#             raise StorageError("Store not initialized. Call setup() first.")
        
#         try:
#             return self._store.get(key)
#         except Exception as e:
#             raise StorageError(f"Failed to get key '{key}': {e}")
    
#     def get_buffer(self, key: str) -> Optional[Any]:
#         """
#         Get a buffer object that supports the buffer protocol for efficient access to stored data.
        
#         Args:
#             key: The key to retrieve
            
#         Returns:
#             A buffer protocol compatible object or None if key not found
#         """
#         if not self._initialized:
#             raise StorageError("Store not initialized. Call setup() first.")
        
#         try:
#             return self._store.get_buffer(key)
#         except Exception as e:
#             raise StorageError(f"Failed to get buffer for key '{key}': {e}")
    
#     def get_size(self, key: str) -> int:
#         """
#         Get the size of a stored value.
        
#         Args:
#             key: The key to check
            
#         Returns:
#             Size in bytes, or negative value if key not found
#         """
#         if not self._initialized:
#             raise StorageError("Store not initialized. Call setup() first.")
        
#         try:
#             return self._store.get_size(key)
#         except Exception as e:
#             raise StorageError(f"Failed to get size for key '{key}': {e}")
    
#     def is_exist(self, key: str) -> int:
#         """
#         Check if a key exists in the store.
        
#         Args:
#             key: The key to check
            
#         Returns:
#             1 if key exists, 0 if not
#         """
#         if not self._initialized:
#             raise StorageError("Store not initialized. Call setup() first.")
        
#         try:
#             return self._store.is_exist(key)
#         except Exception as e:
#             raise StorageError(f"Failed to check existence of key '{key}': {e}")
    
#     def remove(self, key: str) -> int:
#         """
#         Remove a key from the store.
        
#         Args:
#             key: The key to remove
            
#         Returns:
#             0 on success, non-zero error code on failure
#         """
#         if not self._initialized:
#             raise StorageError("Store not initialized. Call setup() first.")
        
#         try:
#             return self._store.remove(key)
#         except Exception as e:
#             raise StorageError(f"Failed to remove key '{key}': {e}")
    
#     def close(self) -> int:
#         """
#         Close and tear down the store.
        
#         Returns:
#             0 on success, non-zero error code on failure
#         """
#         if not self._initialized:
#             return 0
        
#         try:
#             retcode = self._store.close()
            
#             if retcode == 0:
#                 self._initialized = False
#             return retcode
#         except Exception as e:
#             raise StorageError(f"Failed to close store: {e}")
    
#     @property
#     def native_store(self):
#         """Access to the underlying Rust store for advanced usage."""
#         return self._store
    
#     # Additional helper methods specific to Rust implementation
    
#     def len(self) -> int:
#         """Get the number of stored keys."""
#         if not self._initialized:
#             return 0
#         return self._store.len()
    
#     def is_empty(self) -> bool:
#         """Check if the store is empty."""
#         if not self._initialized:
#             return True
#         return self._store.is_empty()
    
#     def clear(self) -> int:
#         """Clear all stored data."""
#         if not self._initialized:
#             raise StorageError("Store not initialized. Call setup() first.")
        
#         try:
#             return self._store.clear()
#         except Exception as e:
#             raise StorageError(f"Failed to clear store: {e}")
    
#     def keys(self) -> list[str]:
#         """Get all keys in the store."""
#         if not self._initialized:
#             raise StorageError("Store not initialized. Call setup() first.")
        
#         try:
#             return self._store.keys()
#         except Exception as e:
#             raise StorageError(f"Failed to get keys: {e}")


# # Example of how to implement Rust bindings integration:
# """
# # If you're using PyO3 bindings, your Rust module might look like:

# import rust_kv_store  # Your compiled Rust module

# class RustStore(KVCacheStore):
#     def __init__(self):
#         self._store = rust_kv_store.KVStore()
#         self._initialized = False
    
#     def setup(self, ...):
#         config = rust_kv_store.Config(
#             local_hostname=local_hostname,
#             metadata_server=metadata_server,
#             # ... other parameters
#         )
#         retcode = self._store.setup(config)
#         if retcode == 0:
#             self._initialized = True
#         return retcode
    
#     def put(self, key: str, *values: Union[bytes, bytearray]) -> int:
#         if len(values) == 1:
#             return self._store.put(key, values[0])
#         else:
#             # Use Rust put_parts or fallback
#             if hasattr(self._store, 'put_parts'):
#                 return self._store.put_parts(key, *values)
#             else:
#                 combined = b''.join(values)
#                 return self._store.put(key, combined)
    
#     # ... implement other methods
    
#     def get_buffer(self, key: str) -> Optional[Any]:
#         # Return buffer protocol compatible object directly
#         return self._store.get_buffer(key)
# """ 